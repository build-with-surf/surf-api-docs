# 场景：新币上线追踪器

[English](./listing-tracker.en.md) | 中文

---

## 做什么

监控交易所新币上线公告，自动追踪上线后 30 天的表现（价格、成交量、持币地址数），结合 Surf AI 分析上线前的 Twitter 热度和 KOL 站队。

## 工作流程

```
1. 发现新上线 → Chat API 抓取上线公告
2. 上线后每天记录 → Data API 拉取价格/成交量
3. 社交分析 → Chat API 分析 Twitter 讨论
4. 30 天总结 → Chat API 生成表现报告
```

## 核心代码

### 1. 发现新上线

```python
import requests
from datetime import datetime, timedelta

class ListingTracker:
    def __init__(self, api_key):
        self.chat_url = "https://api.asksurf.ai/surf-ai/v1/chat/completions"
        self.data_url = "https://api.ask.surf/gateway"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def discover_new_listings(self):
        """用 Chat API 发现最近的新币上线"""
        resp = requests.post(
            self.chat_url,
            headers=self.headers,
            json={
                "model": "surf-1.5-instant",
                "messages": [{
                    "role": "user",
                    "content": "列出过去 7 天 Binance 和 OKX 新上线的代币，"
                               "包括：代币名称、上线日期、上线交易所、上线价格"
                }],
                "ability": ["search", "market_analysis"],
                "reasoning_effort": "low"
            }
        )
        return resp.json()["choices"][0]["message"]["content"]
```

### 2. 追踪表现

```python
    def track_performance(self, symbol, days_since_listing):
        """追踪新币上线后的表现"""
        resp = requests.post(
            self.chat_url,
            headers=self.headers,
            json={
                "model": "surf-1.5",
                "messages": [{
                    "role": "user",
                    "content": f"{symbol} 上线 {days_since_listing} 天以来的表现：\n"
                               f"1. 价格变化（上线价 vs 当前价）\n"
                               f"2. 日均成交量趋势\n"
                               f"3. 持币地址数变化\n"
                               f"4. 与同期上线的其他币相比如何"
                }],
                "ability": ["market_analysis", "evm_onchain"],
                "reasoning_effort": "medium",
                "citation": ["source", "chart"]
            }
        )
        return resp.json()["choices"][0]["message"]["content"]
```

### 3. 上线前社交热度分析

```python
    def pre_listing_buzz(self, symbol):
        """分析上线前的 Twitter 讨论"""
        resp = requests.post(
            self.chat_url,
            headers=self.headers,
            json={
                "model": "surf-1.5",
                "messages": [{
                    "role": "user",
                    "content": f"分析 {symbol} 上线前 7 天 Twitter 上的讨论：\n"
                               f"1. 讨论热度曲线\n"
                               f"2. 主要 KOL 的态度（看多/看空/中性）\n"
                               f"3. 社区情绪分布\n"
                               f"4. 是否有异常的提前泄露或内部消息信号"
                }],
                "ability": ["search"],
                "reasoning_effort": "medium"
            }
        )
        return resp.json()["choices"][0]["message"]["content"]
```

### 4. 用 SQL 做历史统计

```sql
-- 统计最近上线代币的 DEX 交易活跃度
-- 适用于有链上流动性的代币

SELECT 
    t.token_symbol,
    min(t.block_date) AS first_trade_date,
    count(*) AS total_trades,
    sum(t.amount_usd) AS total_volume,
    count(DISTINCT t.block_date) AS active_days
FROM agent.ethereum_dex_trades t
WHERE t.block_date >= today() - 30
  AND t.amount_usd > 0
GROUP BY t.token_symbol
HAVING first_trade_date >= today() - 30  -- 只看最近 30 天首次出现的代币
ORDER BY total_volume DESC
LIMIT 20
```

## 输出格式

每日跟踪报告示例：

```
📊 新币上线追踪 — 2026-04-03

🔵 TOKEN_A (Binance, 上线第 5 天)
   价格: $0.52 → $0.78 (+50%)
   24h 成交量: $12.3M
   持币地址: 8,234 (+15% vs 昨天)
   KOL 情绪: 偏多 (7/10 KOL 看多)
   ⚡ 信号: 成交量放大 + 地址增长，短期动能强

🟡 TOKEN_B (OKX, 上线第 12 天)
   价格: $1.20 → $0.85 (-29%)
   24h 成交量: $3.1M (↓40%)
   持币地址: 2,100 (-5% vs 昨天)
   KOL 情绪: 中性转空
   ⚠️ 信号: 量价齐跌，关注支撑位
```

## 部署建议

- **新币发现：** 每天跑一次
- **表现追踪：** 每 6 小时更新（跟 Surf 数据延迟匹配）
- **报告推送：** 每天早上推送前一天的追踪汇总

---

**相关场景：** [套利监控](./arbitrage-monitor.md) · [舆情看板](./sentiment-dashboard.md)
