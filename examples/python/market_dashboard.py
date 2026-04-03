"""
Surf API 示例：终端市场仪表盘
一个命令看全局 — 价格、恐贪指数、DeFi 排名、期货数据。

用法: python market_dashboard.py
"""

import subprocess
import json
from datetime import datetime


def surf_query(cmd: str) -> dict | None:
    result = subprocess.run(f"surf {cmd}", shell=True, capture_output=True, text=True, timeout=15)
    try:
        return json.loads(result.stdout)
    except (json.JSONDecodeError, Exception):
        return None


def print_section(title: str):
    print(f"\n{'─' * 50}")
    print(f"  {title}")
    print(f"{'─' * 50}")


if __name__ == "__main__":
    print(f"╔══════════════════════════════════════════════════╗")
    print(f"║           Surf 终端市场仪表盘                      ║")
    print(f"║           {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                     ║")
    print(f"╚══════════════════════════════════════════════════╝")

    # 1. 主流币价格
    print_section("💰 主流币价格")
    ranking = surf_query("market-ranking --limit 10")
    if ranking and ranking.get("data"):
        print(f"  {'#':<4} {'币种':<10} {'价格':<15} {'24h涨跌':<10} {'市值'}")
        for token in ranking["data"]:
            change = token.get("change_24h_pct", 0)
            arrow = "🟢" if change > 0 else "🔴" if change < 0 else "⚪"
            mcap = token.get("market_cap_usd", 0)
            mcap_str = f"${mcap/1e9:.1f}B" if mcap > 1e9 else f"${mcap/1e6:.0f}M"
            print(f"  {token.get('rank', '-'):<4} {token['symbol']:<10} ${token['price_usd']:>12,.2f} {arrow} {change:>+6.1f}%  {mcap_str}")

    # 2. 恐贪指数
    print_section("😱 恐贪指数")
    fg = surf_query("market-fear-greed")
    if fg and fg.get("data"):
        latest = fg["data"][-1]
        value = latest["value"]
        label = latest.get("classification", "")
        bar_len = int(value / 5)
        bar = "🟥" * min(bar_len, 4) + "🟧" * max(0, min(bar_len - 4, 4)) + "🟨" * max(0, min(bar_len - 8, 4)) + "🟩" * max(0, bar_len - 12)
        print(f"  {value:.0f} / 100  {label}")
        print(f"  {bar}")

    # 3. DeFi TVL 排名
    print_section("🏦 DeFi TVL Top 5")
    defi = surf_query("project-defi-ranking --metric tvl --limit 5")
    if defi and defi.get("data"):
        print(f"  {'协议':<15} {'TVL':<18} {'24h Fees'}")
        for p in defi["data"]:
            tvl = p.get("tvl", 0)
            fees = p.get("fees", 0)
            tvl_str = f"${tvl/1e9:.1f}B" if tvl > 1e9 else f"${tvl/1e6:.0f}M"
            fees_str = f"${fees/1e6:.1f}M" if fees > 1e6 else f"${fees/1e3:.0f}K"
            print(f"  {p['name']:<15} {tvl_str:<18} {fees_str}")

    # 4. 期货市场概览
    print_section("📊 期货市场 (Top 5 by OI)")
    futures = surf_query("market-futures")
    if futures and futures.get("data"):
        sorted_f = sorted(futures["data"], key=lambda x: x.get("open_interest", 0), reverse=True)[:5]
        print(f"  {'币种':<8} {'资金费率':<12} {'多空比':<10} {'未平仓 (OI)'}")
        for f in sorted_f:
            fr = f.get("funding_rate", 0)
            ls = f.get("long_short_ratio", 0)
            oi = f.get("open_interest", 0)
            oi_str = f"${oi/1e9:.2f}B" if oi > 1e9 else f"${oi/1e6:.0f}M"
            print(f"  {f['symbol']:<8} {fr*100:>+8.4f}%   {ls:>6.2f}     {oi_str}")

    print(f"\n{'─' * 50}")
    print(f"  数据来源: Surf API | Credits 消耗: ~6")
    print(f"{'─' * 50}")
