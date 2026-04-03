"""
Surf API 示例：跨交易所资金费率扫描器
扫描多个币种在 Binance/OKX/Bybit 的资金费率，找出套利机会。

用法: python funding_rate_scanner.py
无需 API Key（使用 Surf CLI 内置认证）
"""

import subprocess
import json
from datetime import datetime


def surf_query(cmd: str) -> dict | None:
    """调用 Surf CLI 并返回 JSON"""
    result = subprocess.run(f"surf {cmd}", shell=True, capture_output=True, text=True, timeout=15)
    try:
        return json.loads(result.stdout)
    except (json.JSONDecodeError, Exception):
        return None


def scan_funding_rates(symbols: list[str], exchanges: list[str]) -> list[dict]:
    """扫描多币种多交易所的资金费率"""
    opportunities = []

    for symbol in symbols:
        rates = {}
        for exchange in exchanges:
            data = surf_query(f"exchange-funding-history --pair {symbol}/USDT --exchange {exchange} --limit 1")
            if data and data.get("data"):
                item = data["data"][0]
                rates[exchange] = item["funding_rate"]

        if len(rates) >= 2:
            sorted_ex = sorted(rates.items(), key=lambda x: x[1])
            low_ex, low_rate = sorted_ex[0]
            high_ex, high_rate = sorted_ex[-1]
            spread = high_rate - low_rate

            opportunities.append({
                "symbol": symbol,
                "spread_pct": round(spread * 100, 4),
                "long": f"{low_ex} ({low_rate*100:.4f}%)",
                "short": f"{high_ex} ({high_rate*100:.4f}%)",
                "all_rates": {ex: f"{r*100:.4f}%" for ex, r in rates.items()}
            })

    return sorted(opportunities, key=lambda x: x["spread_pct"], reverse=True)


if __name__ == "__main__":
    symbols = ["BTC", "ETH", "SOL", "ARB", "DOGE", "AVAX", "LINK", "SUI"]
    exchanges = ["binance", "okx", "bybit"]

    print(f"🔍 扫描资金费率... ({len(symbols)} 币种 × {len(exchanges)} 交易所)")
    print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    results = scan_funding_rates(symbols, exchanges)

    print(f"{'币种':<8} {'价差%':<10} {'做多(低费率)':<25} {'做空(高费率)':<25}")
    print("-" * 70)

    for r in results:
        flag = "🔥" if r["spread_pct"] > 0.01 else "  "
        print(f"{flag}{r['symbol']:<6} {r['spread_pct']:<10} {r['long']:<25} {r['short']:<25}")

    print(f"\n共 {len(results)} 个币种有数据")
    hot = [r for r in results if r["spread_pct"] > 0.01]
    if hot:
        print(f"🔥 {len(hot)} 个套利机会（价差 > 0.01%）")
