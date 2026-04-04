# Quickstart

[English](./quickstart.en.md) | [中文](./quickstart.md)

---

Get up and running with Surf in 5 minutes. Choose your preferred method:

## Option 1: Surf Skill (Recommended — for AI Agents)

If you use Claude Code, Codex, or other AI coding tools, install the Surf Skill with one command:

```bash
npx skills add asksurf-ai/surf-skills --skill surf
```

Then just talk to your Agent:

```
"What's the current price of ETH?"
"What are the hottest markets on Polymarket?"
"Show me the wallets holding the most AAVE"
```

The Skill automatically handles authentication, data discovery, and requests.

## Option 2: Surf CLI

Install from your terminal:

```bash
curl -fsSL https://agent.asksurf.ai/cli/releases/install.sh | sh
```

Log in and make your first request:

```bash
surf login
surf market-price --symbol BTC
```

## Option 3: Chat API (Build Applications)

The Chat API is OpenAI-compatible, so switching over is seamless:

```bash
curl --request POST \
  --url https://api.asksurf.ai/surf-ai/v1/chat/completions \
  --header 'Authorization: Bearer <your-api-key>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "surf-1.5",
    "messages": [
      {"role": "user", "content": "Analyze BTC market trends over the past 7 days, including key support and resistance levels"}
    ],
    "reasoning_effort": "medium"
  }'
```

### Python Example

```python
import requests

response = requests.post(
    "https://api.asksurf.ai/surf-ai/v1/chat/completions",
    headers={
        "Authorization": "Bearer <your-api-key>",
        "Content-Type": "application/json"
    },
    json={
        "model": "surf-1.5",
        "messages": [
            {"role": "user", "content": "Compare TVL trends between Aave and Compound"}
        ],
        "reasoning_effort": "medium",
        "ability": ["evm_onchain", "market_analysis"],
        "citation": ["source", "chart"]
    }
)

result = response.json()
print(result["choices"][0]["message"]["content"])
```

### Key Parameters

| Parameter | Purpose | Options |
|-----------|---------|---------|
| `model` | Select model | `surf-1.5` (recommended) / `surf-1.5-instant` / `surf-1.5-thinking` |
| `reasoning_effort` | Reasoning depth | `low` / `medium` / `high` |
| `ability` | Specify data capabilities | `search` / `evm_onchain` / `solana_onchain` / `market_analysis` / `calculate` |
| `citation` | Citation format | `source` / `chart` |
| `stream` | Streaming output | `true` / `false` |

## Option 4: Data API (Query Data Directly)

83 REST endpoints returning structured data:

```bash
# Get BTC price
curl -H "Authorization: Bearer <your-api-key>" \
  "https://api.ask.surf/gateway/v1/market/price?symbol=BTC"

# Get funding rates
curl -H "Authorization: Bearer <your-api-key>" \
  "https://api.ask.surf/gateway/v1/exchange/funding-rate?symbol=BTC"
```

## Option 5: SQL Queries (Data Catalog)

58 ClickHouse tables with direct SQL access:

```sql
-- Top 10 DEX protocols by volume yesterday
SELECT project, sum(amount_usd) AS volume_usd
FROM agent.ethereum_dex_trades
WHERE block_date = today() - 1
GROUP BY project
ORDER BY volume_usd DESC
LIMIT 10
```

> **Performance tip:** Always filter by `block_date` first — it's the partition key, allowing ClickHouse to skip irrelevant partitions.

**Connection details:**

| Setting | Value |
|---------|-------|
| Protocol | ClickHouse HTTP (port 8443, TLS) |
| User | `agent` (read-only) |
| Database | `agent` (raw tables), `curated` (analytical views) |
| Max execution time | 120 seconds |
| Max memory | 16 GB |
| Max rows returned | 1,000,000 |

## Credits Billing

Each API call consumes Credits. The `meta.credits_used` field in the response tells you how much was consumed.

```bash
# Check remaining balance
curl -H "Authorization: Bearer <your-api-key>" \
  "https://api.ask.surf/gateway/v1/me/credit-balance"
```

> **Get API Key & Credits:** Contact [@siriusxyzzz](https://x.com/siriusxyzzz) to join the developer WeChat group for API keys and Credits.

---

**Next:** See the [Chat API Guide](../guides/chat-api-guide.md) to learn how to build real applications, or check out [Use Cases](../use-cases/) for inspiration.
