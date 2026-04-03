"""
Surf API example: multi-wallet dashboard
Track several public wallets at once and print a compact asset overview.

Usage:
    python multi_wallet_dashboard.py
    python multi_wallet_dashboard.py vitalik.eth 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime


DEFAULT_ADDRESSES = ["vitalik.eth"]


def ensure_surf_cli() -> None:
    if shutil.which("surf"):
        return

    print("Error: Surf CLI was not found in PATH.", file=sys.stderr)
    print("Install it first: https://docs.asksurf.ai/cli/introduction", file=sys.stderr)
    raise SystemExit(1)


def surf_query(args: list[str]) -> dict | None:
    try:
        result = subprocess.run(
            ["surf", *args],
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return None

    if result.returncode != 0 or not result.stdout.strip():
        return None

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def short_usd(value: float) -> str:
    if value >= 1e9:
        return f"${value / 1e9:.2f}B"
    if value >= 1e6:
        return f"${value / 1e6:.2f}M"
    if value >= 1e3:
        return f"${value / 1e3:.1f}K"
    return f"${value:.2f}"


def get_wallet_detail(address: str) -> dict | None:
    data = surf_query(["wallet-detail", "--address", address, "--chain", "ethereum", "--fields", "balance"])
    if data and data.get("data"):
        return data["data"]
    return None


def get_wallet_labels(address: str) -> list[str]:
    data = surf_query(["wallet-labels-batch", "--addresses", address])
    if not data or not data.get("data"):
        return []

    labels = data["data"]
    if isinstance(labels, list):
        return [str(item) for item in labels]
    return [str(labels)]


def get_wallet_protocols(address: str, limit: int = 3) -> list[dict]:
    data = surf_query(["wallet-protocols", "--address", address, "--limit", str(limit)])
    if data and data.get("data"):
        return data["data"]
    return []


def build_wallet_summary(address: str) -> dict | None:
    detail = get_wallet_detail(address)
    if not detail:
        return None

    chains = sorted(
        detail.get("active_chains", []),
        key=lambda item: item.get("usd_value", 0),
        reverse=True,
    )
    total_usd = sum(item.get("usd_value", 0) for item in chains)

    return {
        "address": address,
        "total_usd": total_usd,
        "chains": chains[:3],
        "labels": get_wallet_labels(address)[:5],
        "protocols": get_wallet_protocols(address, limit=3),
    }


def print_header(addresses: list[str]) -> None:
    print("=" * 64)
    print("Surf Multi-Wallet Dashboard")
    print(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Wallets: {len(addresses)}")
    print("=" * 64)


def print_overview(summaries: list[dict]) -> None:
    total = sum(item["total_usd"] for item in summaries)

    print("\nOverview")
    print("-" * 64)
    print(f"Tracked wallets: {len(summaries)}")
    print(f"Combined net worth: {short_usd(total)}")
    print("\nRank by net worth")
    for index, item in enumerate(sorted(summaries, key=lambda x: x["total_usd"], reverse=True), start=1):
        print(f"{index:>2}. {item['address']:<44} {short_usd(item['total_usd'])}")


def print_wallet_breakdown(summary: dict) -> None:
    print("\n" + "-" * 64)
    print(summary["address"])
    print(f"Net worth: {short_usd(summary['total_usd'])}")

    if summary["labels"]:
        print(f"Labels: {', '.join(summary['labels'])}")

    if summary["chains"]:
        print("Top chains:")
        for item in summary["chains"]:
            chain = item.get("chain", "unknown")
            value = item.get("usd_value", 0)
            pct = (value / summary["total_usd"] * 100) if summary["total_usd"] else 0
            print(f"  - {chain:<12} {short_usd(value):>10}  {pct:>5.1f}%")

    if summary["protocols"]:
        print("Top protocols:")
        for protocol in summary["protocols"]:
            name = protocol.get("protocol", protocol.get("name", "Unknown"))
            value = protocol.get("usd_value", protocol.get("balance_usd", 0))
            value_str = short_usd(value) if isinstance(value, (int, float)) else "n/a"
            print(f"  - {name:<20} {value_str}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Track several wallets with Surf CLI.")
    parser.add_argument(
        "addresses",
        nargs="*",
        default=DEFAULT_ADDRESSES,
        help="Wallet addresses or ENS names to inspect.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ensure_surf_cli()
    print_header(args.addresses)

    summaries = []
    failed = []

    for address in args.addresses:
        summary = build_wallet_summary(address)
        if summary:
            summaries.append(summary)
        else:
            failed.append(address)

    if not summaries:
        print("No wallet data returned. Check the addresses and your Surf CLI setup.", file=sys.stderr)
        raise SystemExit(1)

    print_overview(summaries)
    for summary in summaries:
        print_wallet_breakdown(summary)

    if failed:
        print("\nSkipped")
        print("-" * 64)
        for address in failed:
            print(f"- {address}")


if __name__ == "__main__":
    main()
