"""
Surf API 示例：巨鲸钱包追踪器
查询知名钱包的持仓分布和跨链资产。

用法: python whale_tracker.py [address]
默认追踪 vitalik.eth
"""

import subprocess
import json
import sys


def surf_query(cmd: str) -> dict | None:
    result = subprocess.run(f"surf {cmd}", shell=True, capture_output=True, text=True, timeout=15)
    try:
        return json.loads(result.stdout)
    except (json.JSONDecodeError, Exception):
        return None


def track_wallet(address: str):
    """查询钱包跨链资产分布"""
    print(f"🐋 追踪钱包: {address}\n")

    # 1. 钱包概览
    data = surf_query(f"wallet-detail --address {address} --chain ethereum --fields balance")
    if not data or "data" not in data:
        print("❌ 查询失败，请检查地址")
        return

    wallet = data["data"]

    # 跨链资产
    chains = wallet.get("active_chains", [])
    total_usd = sum(c.get("usd_value", 0) for c in chains)

    print(f"💰 总资产: ${total_usd:,.2f}\n")
    print(f"{'链':<15} {'价值 (USD)':<20} {'占比':<10}")
    print("-" * 45)

    for chain in sorted(chains, key=lambda x: x.get("usd_value", 0), reverse=True):
        value = chain.get("usd_value", 0)
        pct = (value / total_usd * 100) if total_usd > 0 else 0
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        print(f"{chain['chain']:<15} ${value:>14,.2f}   {pct:>5.1f}%  {bar}")

    # 2. 地址标签
    labels = surf_query(f"wallet-labels-batch --addresses {address}")
    if labels and labels.get("data"):
        print(f"\n🏷️  标签: {labels['data']}")

    # 3. DeFi 持仓
    protocols = surf_query(f"wallet-protocols --address {address} --limit 5")
    if protocols and protocols.get("data"):
        print(f"\n📊 DeFi 持仓 (Top 5):")
        for p in protocols["data"]:
            name = p.get("protocol", p.get("name", "Unknown"))
            value = p.get("usd_value", p.get("balance_usd", 0))
            print(f"   • {name}: ${value:,.2f}" if isinstance(value, (int, float)) else f"   • {name}")


if __name__ == "__main__":
    address = sys.argv[1] if len(sys.argv) > 1 else "vitalik.eth"
    track_wallet(address)
