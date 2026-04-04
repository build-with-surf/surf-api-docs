# Use Case: New Listing Tracker

[English](./listing-tracker.en.md) | [中文](./listing-tracker.md)

---

## What It Does

Monitors exchange new listing announcements, automatically tracks performance for 30 days after listing (price, volume, holder count), and uses Surf AI to analyze pre-listing Twitter buzz and KOL sentiment.

## Workflow

```
1. Discover new listing → Chat API fetches listing announcements
2. Daily tracking post-listing → Data API pulls price/volume
3. Social analysis → Chat API analyzes Twitter discussions
4. 30-day summary → Chat API generates performance report
```

## Core Code

### 1. Discover New Listings

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
        """Discover recent new listings using Chat API"""
        resp = requests.post(
            self.chat_url,
            headers=self.headers,
            json={
                "model": "surf-1.5-instant",
                "messages": [{
                    "role": "user",
                    "content": "List the tokens newly listed on Binance and OKX in the past 7 days, "
                               "including: token name, listing date, exchange, and listing price"
                }],
                "ability": ["search", "market_analysis"],
                "reasoning_effort": "low"
            }
        )
        return resp.json()["choices"][0]["message"]["content"]
```

### 2. Track Performance

```python
    def track_performance(self, symbol, days_since_listing):
        """Track a newly listed token's performance"""
        resp = requests.post(
            self.chat_url,
            headers=self.headers,
            json={
                "model": "surf-1.5",
                "messages": [{
                    "role": "user",
                    "content": f"Performance of {symbol} since listing ({days_since_listing} days ago):\n"
                               f"1. Price change (listing price vs current price)\n"
                               f"2. Average daily volume trend\n"
                               f"3. Holder address count change\n"
                               f"4. Comparison with other tokens listed in the same period"
                }],
                "ability": ["market_analysis", "evm_onchain"],
                "reasoning_effort": "medium",
                "citation": ["source", "chart"]
            }
        )
        return resp.json()["choices"][0]["message"]["content"]
```

### 3. Pre-Listing Social Buzz Analysis

```python
    def pre_listing_buzz(self, symbol):
        """Analyze Twitter discussions before listing"""
        resp = requests.post(
            self.chat_url,
            headers=self.headers,
            json={
                "model": "surf-1.5",
                "messages": [{
                    "role": "user",
                    "content": f"Analyze Twitter discussions about {symbol} in the 7 days before listing:\n"
                               f"1. Discussion volume trend\n"
                               f"2. Key KOL stances (bullish/bearish/neutral)\n"
                               f"3. Community sentiment distribution\n"
                               f"4. Any signs of abnormal early leaks or insider information"
                }],
                "ability": ["search"],
                "reasoning_effort": "medium"
            }
        )
        return resp.json()["choices"][0]["message"]["content"]
```

### 4. Historical Statistics with SQL

```sql
-- Count DEX trading activity for recently listed tokens
-- Applicable to tokens with on-chain liquidity

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
HAVING first_trade_date >= today() - 30  -- Only tokens first seen in the past 30 days
ORDER BY total_volume DESC
LIMIT 20
```

## Output Format

Daily tracking report example:

```
📊 New Listing Tracker — 2026-04-03

🔵 TOKEN_A (Binance, Day 5 since listing)
   Price: $0.52 → $0.78 (+50%)
   24h Volume: $12.3M
   Holders: 8,234 (+15% vs yesterday)
   KOL Sentiment: Bullish (7/10 KOLs bullish)
   ⚡ Signal: Volume surge + address growth, strong short-term momentum

🟡 TOKEN_B (OKX, Day 12 since listing)
   Price: $1.20 → $0.85 (-29%)
   24h Volume: $3.1M (↓40%)
   Holders: 2,100 (-5% vs yesterday)
   KOL Sentiment: Neutral turning bearish
   ⚠️ Signal: Volume and price both declining, watch support levels
```

## Deployment Tips

- **New listing discovery:** Run once daily
- **Performance tracking:** Update every 6 hours (matching Surf data latency)
- **Report push:** Send previous day's tracking summary every morning

---

**Related use cases:** [Arbitrage Monitor](./arbitrage-monitor.md) · [Sentiment Dashboard](./sentiment-dashboard.md)
