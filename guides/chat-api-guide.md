# Chat API Practical Guide

[English](./chat-api-guide.en.md) | [中文](./chat-api-guide.md)

---

The Chat API is Surf's most flexible interface — OpenAI-compatible format that you can use directly to build Crypto AI applications.

## Architecture

```
Your App → POST /v1/chat/completions → Surf Model
                                         ↓
                                    Real-time on-chain data
                                    Market analysis engine
                                    Social sentiment analysis
                                    Prediction market data
                                         ↓
                                    Structured response
```

## How to Choose a Model?

| Scenario | Recommended Model | `reasoning_effort` | Why |
|----------|-------------------|-------------------|-----|
| Real-time prices / simple queries | `surf-1.5-instant` | `low` | Fast, 0.5-2 second response |
| Everyday analysis | `surf-1.5` | `medium` | Automatically selects instant or thinking |
| Deep research reports | `surf-1.5-thinking` | `high` | Multi-step reasoning, deeper results |
| Long-form due diligence | `surf-research` | N/A | Legacy but good for very long outputs (set 10-min timeout) |

## `ability` Parameter Explained

`ability` tells Surf which data capabilities to invoke for a query:

| ability | Meaning | Typical Use |
|---------|---------|-------------|
| `search` | Search engine | Project info, news, entity lookup |
| `evm_onchain` | EVM on-chain data | Transactions, contracts, wallets on ETH/Polygon/Arbitrum etc. |
| `solana_onchain` | Solana on-chain data | SPL tokens, DEX trades |
| `market_analysis` | Market analysis | Prices, candlesticks, technical indicators, funding rates |
| `calculate` | Calculation engine | Math calculations, portfolio valuation |

**Tip:** Explicitly specifying abilities speeds up response time. If omitted, Surf will auto-detect.

```python
# For on-chain data queries, specify evm_onchain
{"ability": ["evm_onchain"]}

# For market analysis, specify market_analysis
{"ability": ["market_analysis"]}

# When you need both on-chain and market data
{"ability": ["evm_onchain", "market_analysis"]}
```

## `citation` Parameter

Controls whether Surf includes citations in responses:

| Value | Effect |
|-------|--------|
| `source` | Includes data source links |
| `chart` | Generates visual charts |

## Practical Examples

### 1. Funding Rate Monitor Bot

```python
import requests
import json

def check_funding_rates():
    response = requests.post(
        "https://api.asksurf.ai/surf-ai/v1/chat/completions",
        headers={
            "Authorization": "Bearer <api-key>",
            "Content-Type": "application/json"
        },
        json={
            "model": "surf-1.5-instant",
            "messages": [{
                "role": "user",
                "content": "List the 5 tokens with the highest and lowest funding rates right now, including a comparison between Binance and OKX"
            }],
            "reasoning_effort": "low",
            "ability": ["market_analysis"]
        }
    )
    return response.json()["choices"][0]["message"]["content"]
```

### 2. Quick Project Due Diligence

```python
def quick_research(project_name):
    response = requests.post(
        "https://api.asksurf.ai/surf-ai/v1/chat/completions",
        headers={
            "Authorization": "Bearer <api-key>",
            "Content-Type": "application/json"
        },
        json={
            "model": "surf-1.5-thinking",
            "messages": [{
                "role": "system",
                "content": "You are a Crypto research analyst. Output a structured project due diligence report."
            }, {
                "role": "user",
                "content": f"Run a quick due diligence on {project_name}: fundamentals, on-chain data, social buzz, and risk factors"
            }],
            "reasoning_effort": "high",
            "ability": ["search", "evm_onchain", "market_analysis"],
            "citation": ["source"]
        },
        timeout=600  # Deep research may take longer
    )
    return response.json()["choices"][0]["message"]["content"]
```

### 3. Streaming Output (For UI Display)

```python
import requests
import json

response = requests.post(
    "https://api.asksurf.ai/surf-ai/v1/chat/completions",
    headers={
        "Authorization": "Bearer <api-key>",
        "Content-Type": "application/json"
    },
    json={
        "model": "surf-1.5",
        "messages": [{"role": "user", "content": "Analyze the on-chain activity trend of ETH"}],
        "stream": True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        line = line.decode("utf-8")
        if line.startswith("data: ") and line != "data: [DONE]":
            chunk = json.loads(line[6:])
            delta = chunk["choices"][0].get("delta", {})
            if "content" in delta:
                print(delta["content"], end="", flush=True)
```

## Error Handling

| HTTP Status | Meaning | What to Do |
|-------------|---------|------------|
| 400 | Bad request | Check request format |
| 401 | Invalid API Key | Check Authorization header |
| 402 | Insufficient Credits | Top up |
| 502 | Upstream data source temporarily unavailable | Wait and retry |

## Migrating from OpenAI SDK

If you're already using the OpenAI SDK, you only need to change two lines:

```python
from openai import OpenAI

client = OpenAI(
    api_key="<your-surf-api-key>",
    base_url="https://api.asksurf.ai/surf-ai/v1"  # Change this
)

response = client.chat.completions.create(
    model="surf-1.5",  # Change this
    messages=[{"role": "user", "content": "How's BTC doing today?"}]
)
```

> **Verified (2026-04-03):** Fully compatible with the OpenAI SDK. `extra_body` can pass Surf extension fields like `ability`, `reasoning_effort`, and `citation`. Streaming also works correctly.

---

**Next:** See the [Data API Practical Guide](./data-api-guide.md) to learn how to query structured data directly.
