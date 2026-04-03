"""
Surf API 示例：项目 Mindshare 监控
追踪多个项目在 Crypto Twitter 上的注意力占比变化。

用法: python mindshare_monitor.py
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


def get_mindshare(project: str) -> list[dict]:
    """获取项目 mindshare 时间序列"""
    data = surf_query(f"social-mindshare --q {project} --interval 1d")
    if data and data.get("data"):
        return data["data"]
    return []


def analyze_trend(series: list[dict]) -> dict:
    """分析趋势：最近值、7日变化、峰值"""
    if len(series) < 2:
        return {"current": 0, "change_7d": 0, "peak": 0}

    current = series[-1]["value"]
    week_ago = series[-7]["value"] if len(series) >= 7 else series[0]["value"]
    peak = max(s["value"] for s in series)
    change = ((current - week_ago) / week_ago * 100) if week_ago > 0 else 0

    return {"current": current, "change_7d": change, "peak": peak}


if __name__ == "__main__":
    projects = ["ethereum", "solana", "bitcoin", "arbitrum", "base", "sui", "hyperliquid"]

    print(f"📡 Crypto Twitter Mindshare 监控")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    print(f"{'项目':<15} {'当前占比':<12} {'7日变化':<12} {'30日峰值':<12} {'趋势'}")
    print("-" * 65)

    results = []
    for project in projects:
        series = get_mindshare(project)
        if series:
            trend = analyze_trend(series)
            results.append((project, trend))

    # 按当前 mindshare 排序
    results.sort(key=lambda x: x[1]["current"], reverse=True)

    for project, t in results:
        change = t["change_7d"]
        arrow = "📈" if change > 10 else "📉" if change < -10 else "➡️"
        change_str = f"+{change:.1f}%" if change > 0 else f"{change:.1f}%"

        print(f"{project:<15} {t['current']*100:>8.2f}%   {change_str:>8}     {t['peak']*100:>8.2f}%   {arrow}")

    print(f"\n共追踪 {len(results)} 个项目")

    # 找异动
    rising = [(p, t) for p, t in results if t["change_7d"] > 20]
    falling = [(p, t) for p, t in results if t["change_7d"] < -20]

    if rising:
        print(f"\n🔥 异常上升: {', '.join(p for p, _ in rising)}")
    if falling:
        print(f"⚠️  异常下降: {', '.join(p for p, _ in falling)}")
