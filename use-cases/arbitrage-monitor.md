# Use Case: Cross-Exchange Arbitrage Monitor

[English](./arbitrage-monitor.en.md) | [中文](./arbitrage-monitor.md)

---

## What It Does

Monitors funding rates and spot-futures price spreads across multiple exchanges in real time, identifies arbitrage opportunities, and calculates net profit after costs.

## Architecture

```
Cron Job (every 5 minutes)
    │
    ├── Surf Data API: Funding rates (/exchange/funding-rate)
    ├── Surf Data API: Spot prices (/market/price)
    ├── Surf Chat API: Sentiment analysis (estimate window duration)
    │
    ▼
  Calculate net arbitrage spread
    │
    ▼
  Telegram/WeChat alert (when threshold exceeded)
```

## Core Code

### 1. Fetch Funding Rates

```python
import requests
from datetime import datetime

class ArbitrageMonitor:
    def __init__(self, api_key):
        self.base_url = "https://api.ask.surf/gateway"
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def get_funding_rates(self, symbols="BTC,ETH,SOL,ARB,DOGE"):
        """Get funding rates for multiple tokens"""
        rates = {}
        for symbol in symbols.split(","):
            resp = requests.get(
                f"{self.base_url}/v1/exchange/funding-rate",
                headers=self.headers,
                params={"symbol": symbol.strip()}
            )
            if resp.ok:
                rates[symbol.strip()] = resp.json()
        return rates
```

### 2. Calculate Arbitrage Spread

```python
    def calculate_spread(self, rates):
        """Find opportunities with the largest funding rate discrepancies"""
        opportunities = []
        for symbol, data in rates.items():
            for exchange in ["binance", "okx", "bybit"]:
            try:
                resp = requests.get(
                    f"{self.base_url}/v1/exchange/funding-history",
                    headers=self.headers,
                    params={"pair": f"{symbol}/USDT", "exchange": exchange, "limit": 1}
                )
                if resp.ok:
                    items = resp.json().get("data", [])
                    if items:
                        rates[f"{symbol}_{exchange}"] = {
                            "exchange": exchange,
                            "rate": items[0]["funding_rate"],
                            "timestamp": items[0]["timestamp"]
                        }
            except Exception:
                continue
        
        # Find exchanges with highest and lowest rates
        if len(rates) >= 2:
            sorted_rates = sorted(rates.values(), key=lambda x: x["rate"])
            spread = sorted_rates[-1]["rate"] - sorted_rates[0]["rate"]
            if spread > 0:
                opportunities.append({
                    "symbol": symbol,
                    "spread": round(spread * 100, 4),  # Convert to percentage
                    "long_exchange": sorted_rates[0]["exchange"],
                    "long_rate": round(sorted_rates[0]["rate"] * 100, 4),
                    "short_exchange": sorted_rates[-1]["exchange"],
                    "short_rate": round(sorted_rates[-1]["rate"] * 100, 4),
                })
        return opportunities
```

### 3. Use Chat API to Estimate Window Duration

```python
    def analyze_window(self, symbol, spread):
        """Use Surf AI to analyze how long the arbitrage window might last"""
        resp = requests.post(
            "https://api.asksurf.ai/surf-ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "surf-1.5-instant",
                "messages": [{
                    "role": "user",
                    "content": f"{symbol} has an abnormal funding rate (spread {spread}%). "
                               f"Based on current market sentiment and position data, how long is this arbitrage window likely to last?"
                }],
                "ability": ["market_analysis"],
                "reasoning_effort": "low"
            }
        )
        return resp.json()["choices"][0]["message"]["content"]
```

### 4. Alert Notification

```python
    def check_and_alert(self, threshold=0.05):
        """Main loop: check and notify"""
        rates = self.get_funding_rates()
        opportunities = self.calculate_spread(rates)
        
        for opp in opportunities:
            if opp["spread"] > threshold:
                analysis = self.analyze_window(opp["symbol"], opp["spread"])
                # Push to Telegram / WeChat
                message = (
                    f"🔔 Arbitrage Opportunity: {opp['symbol']}\n"
                    f"Spread: {opp['spread']}%\n"
                    f"Long: {opp['long_exchange']} ({opp['long_rate']}%)\n"
                    f"Short: {opp['short_exchange']} ({opp['short_rate']}%)\n"
                    f"AI Analysis: {analysis[:200]}"
                )
                print(message)  # Replace with actual push logic
```

**Funding Rate API Response Format (Verified):**

```json
{
  "data": [
    {
      "exchange": "binance",
      "funding_rate": -0.00007398,
      "pair": "BTC/USDT",
      "timestamp": 1775145600
    }
  ],
  "meta": {"credits_used": 1}
}
```

> **Note:** `pair` format is `BTC/USDT` (separated by `/`). `funding_rate` is a decimal — `-0.00007398` = -0.007398%.

**Telegram Bot Push:**

```python
import requests

def send_telegram(bot_token, chat_id, message):
    requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    )

# Call in check_and_alert:
# send_telegram(BOT_TOKEN, CHAT_ID, message)
```

## Advanced: Historical Backtesting with SQL

```sql
-- Query historical abnormal funding rate events
-- Hyperliquid perpetual data is in agent.hyperliquid_perp_* tables
-- For other exchange funding rates, use the Data API (exchange-funding-history)

SELECT 
    coin,
    funding_rate,
    block_date
FROM agent.hyperliquid_perp_funding
WHERE abs(funding_rate) > 0.01
  AND block_date >= today() - 30
ORDER BY abs(funding_rate) DESC
LIMIT 20
```

## Deployment Tips

- **Frequency:** Run every 5 minutes (funding rates don't change fast enough to need sub-second polling)
- **Hosting:** Use cron or Railway/Vercel scheduled tasks
- **Cost:** Approximately 5-10 Credits per run (depends on number of tokens queried)

---

**Related use cases:** [Listing Tracker](./listing-tracker.md) · [Sentiment Dashboard](./sentiment-dashboard.md)
