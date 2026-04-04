# Use Case: Twitter Sentiment x On-Chain Data Dashboard

[English](./sentiment-dashboard.en.md) | [中文](./sentiment-dashboard.md)

---

## What It Does

Displays real-time Twitter sentiment on the left and corresponding on-chain data (TVL, trading volume, whale movements) on the right. When the two diverge, it automatically generates signals:

- **Hot sentiment + Cold on-chain = "False Hype Alert"** — Likely hype, be cautious about chasing
- **Hot on-chain + Cold sentiment = "Hidden Opportunity"** — Smart money is moving, market hasn't reacted yet

## Data Source Combinations

| Data | Surf Interface | Purpose |
|------|---------------|---------|
| Twitter Mindshare | Data API `/social/mindshare` | Sentiment trend |
| Twitter Sentiment | Chat API + `ability: ["search"]` | Positive/negative sentiment analysis |
| Project TVL | Data API `/project/tvl` | Real on-chain capital inflow |
| DEX Volume | Data Catalog `agent.ethereum_dex_trades` | On-chain trading activity |
| Whale Transfers | Data API `/wallet/transfers` | Large holder movements |

## Core Code

### 1. Fetch Sentiment + On-Chain Data

```python
import requests

class SentimentDashboard:
    def __init__(self, api_key):
        self.data_url = "https://api.ask.surf/gateway"
        self.chat_url = "https://api.asksurf.ai/surf-ai/v1/chat/completions"
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.chat_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_mindshare(self, symbol, time_range="7d"):
        """Get Twitter Mindshare trend"""
        resp = requests.get(
            f"{self.data_url}/v1/social/mindshare",
            headers=self.headers,
            params={"symbol": symbol, "time_range": time_range}
        )
        return resp.json() if resp.ok else None
    
    def get_sentiment(self, symbol):
        """Analyze current sentiment using Chat API"""
        resp = requests.post(
            self.chat_url,
            headers=self.chat_headers,
            json={
                "model": "surf-1.5-instant",
                "messages": [{
                    "role": "user",
                    "content": f"Analyze Twitter discussions about {symbol} over the past 24 hours. "
                               f"Provide: 1) Overall bullish/bearish/neutral 2) Main topics 3) Key KOL opinions"
                }],
                "ability": ["search"],
                "reasoning_effort": "low"
            }
        )
        return resp.json()["choices"][0]["message"]["content"]
```

### 2. Divergence Detection

```python
    def detect_divergence(self, symbol):
        """Detect sentiment vs on-chain divergence"""
        mindshare = self.get_mindshare(symbol)
        # Fetch DeFi TVL ranking data
        tvl_resp = requests.get(
            f"{self.data_url}/v1/project/defi-ranking",
            headers=self.headers,
            params={"metric": "tvl", "limit": 20}
        )
        tvl_data = tvl_resp.json().get("data", []) if tvl_resp.ok else []
        # Response format: [{"name": "Aave", "tvl": 40779865964, "fees": ..., "revenue": ...}, ...]
        
        # Divergence logic:
        # mindshare_change = (this_week_mindshare - last_week) / last_week
        # tvl_change = (this_week_tvl - last_week) / last_week
        # 
        # if mindshare_change > 30% and tvl_change < -5%:
        #     return "False Hype Alert"
        # if mindshare_change < -10% and tvl_change > 20%:
        #     return "Hidden Opportunity"
        # return "Normal"
        pass
```

### 3. Query Historical Divergence Events with SQL

```sql
-- Query a project's DEX trading volume trend (past 30 days, aggregated by day)
SELECT 
    block_date,
    sum(amount_usd) AS daily_volume,
    count(*) AS trade_count
FROM agent.ethereum_dex_trades
WHERE block_date >= today() - 30
  AND project = 'uniswap'  -- Filter by protocol name; options: uniswap, aave, curve, lido, etc.
GROUP BY block_date
ORDER BY block_date
```

## Frontend Layout Suggestion

Use the [dashboard-template](https://github.com/build-with-surf/dashboard-template) for quick setup:

```
┌─────────────────┬─────────────────┐
│ Twitter Sentiment │  On-Chain Data  │
│                 │                 │
│  📈 Mindshare    │  📊 TVL Trend   │
│  Line chart     │  Line chart     │
│                 │                 │
│  😊 Sentiment    │  🐋 Whale       │
│  Pie chart      │  Table          │
│                 │                 │
├─────────────────┴─────────────────┤
│       ⚠️ Divergence Signals       │
│  ETH: False Hype Alert —          │
│  Mindshare +45%, but TVL -8%,     │
│  whale net outflow $2.3M          │
└───────────────────────────────────┘
```

## Deployment

- **Refresh frequency:** Sentiment data every 1 hour, on-chain data every 6 hours (refer to Surf data latency table)
- **Storage:** Store historical divergence events in a database for backtesting signal accuracy
- **Alerts:** Push divergence signals via Telegram Bot

**Mindshare API Response Format (Verified):**

```json
{
  "data": [
    {"timestamp": 1774828800, "value": 0.0523},
    {"timestamp": 1774915200, "value": 0.0487},
    ...
  ],
  "meta": {"credits_used": 2, "limit": 30, "offset": 0, "total": 30}
}
```

> `value` is the project's mindshare ratio within Crypto Twitter (0-1), with `interval` defaulting to daily.

---

**Related use cases:** [Arbitrage Monitor](./arbitrage-monitor.md) · [Listing Tracker](./listing-tracker.md)
