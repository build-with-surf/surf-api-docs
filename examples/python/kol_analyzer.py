"""
Surf API 示例：KOL 影响力分析器
批量查询 Crypto KOL 的 Twitter 数据，对比粉丝数和影响力。

用法: python kol_analyzer.py
"""

import subprocess
import json


def surf_query(cmd: str) -> dict | None:
    result = subprocess.run(f"surf {cmd}", shell=True, capture_output=True, text=True, timeout=15)
    try:
        return json.loads(result.stdout)
    except (json.JSONDecodeError, Exception):
        return None


def analyze_kol(handle: str) -> dict | None:
    """获取 KOL 的 Twitter 数据"""
    data = surf_query(f"social-user --handle {handle}")
    if not data or "data" not in data:
        return None

    user = data["data"]
    return {
        "handle": user.get("handle", handle),
        "name": user.get("name", ""),
        "followers": user.get("followers_count", 0),
        "following": user.get("following_count", 0),
        "bio": user.get("bio", "")[:60],
    }


if __name__ == "__main__":
    # Crypto KOL 列表 — 自行修改
    kol_handles = [
        "VitalikButerin",
        "caborofficial",
        "CryptoHayes",
        "Ashcryptoreal",
        "inversebrah",
        "SurfAI",
        "KaitoAI",
        "0xSisyphus",
        "DegenSpartan",
        "coaborofficial",
    ]

    print(f"🔍 分析 {len(kol_handles)} 个 Crypto KOL...\n")
    print(f"{'Handle':<20} {'名称':<18} {'粉丝数':<15} {'关注数':<10} {'简介'}")
    print("-" * 90)

    results = []
    for handle in kol_handles:
        info = analyze_kol(handle)
        if info:
            results.append(info)
            followers = info["followers"]
            f_str = f"{followers/1e6:.1f}M" if followers > 1e6 else f"{followers/1e3:.0f}K"
            print(f"@{info['handle']:<19} {info['name']:<18} {f_str:<15} {info['following']:<10} {info['bio']}")
        else:
            print(f"@{handle:<19} ❌ 未找到")

    if results:
        results.sort(key=lambda x: x["followers"], reverse=True)
        print(f"\n📊 排名:")
        for i, r in enumerate(results, 1):
            f = r["followers"]
            f_str = f"{f/1e6:.1f}M" if f > 1e6 else f"{f/1e3:.0f}K"
            bar = "█" * min(int(f / max(results[0]["followers"], 1) * 30), 30)
            print(f"  {i}. @{r['handle']:<18} {f_str:<8} {bar}")
