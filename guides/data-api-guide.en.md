# Data API Practical Guide

[English](./data-api-guide.en.md) | [中文](./data-api-guide.md)

---

The Data API provides 83 REST endpoints that return structured JSON — ideal for building dashboards, monitoring systems, and data pipelines.

## Basic Information

| Item | Value |
|------|-------|
| Base URL | `https://api.ask.surf/gateway` |
| Authentication | `Authorization: Bearer <API_KEY>` |
| Pagination | `limit` (default 20, max 100) + `offset` |
| Billing | Each call consumes Credits; `meta.credits_used` in the response shows the amount |

## Common Query Patterns

### 1. Market Data

```bash
# Get price
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/market/price?symbol=BTC"

# Multiple token prices
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/market/price?symbol=ETH,SOL,ARB"

# Fear & Greed Index
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/market/fear-greed"
```

### 2. Exchange Data

```bash
# Funding rates
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/exchange/funding-rate?symbol=BTC"

# Candlestick data
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/exchange/candlestick?symbol=ETH&interval=1h"

# Long/short ratio
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/exchange/long-short-ratio?symbol=BTC"
```

### 3. Wallet & On-chain

```bash
# Check wallet balance (supports ENS)
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/wallet/balance?address=vitalik.eth&chain=ethereum"

# Wallet transfer history
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/wallet/transfers?address=0xdead...&chain=ethereum"
```

### 4. Social Data

```bash
# Twitter user profile
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/social/twitter/profile?q=VitalikButerin"

# Project Mindshare
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/social/mindshare?symbol=ETH&time_range=7d"
```

### 5. Prediction Markets

```bash
# Polymarket trending markets
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/prediction/markets?sort_by=volume_24h&order=desc&limit=10"
```

## Parameter Reference

### Asset Identifiers

| Parameter | Usage | Examples |
|-----------|-------|----------|
| `symbol` | Uppercase ticker, comma-separated for multiple | `BTC`, `ETH,SOL` |
| `q` | Free text search | `bitcoin` |
| `address` | On-chain address or ENS | `0xdead...`, `vitalik.eth` |

### Time & Aggregation

| Parameter | Usage | Examples |
|-----------|-------|----------|
| `time_range` | Lookback window | `7d`, `30d`, `365d`, `max` |
| `interval` | Candlestick/indicator interval | `1h`, `1d`, `1w` |
| `granularity` | Data granularity | `day`, `block`, `hour` |

### Sorting & Filtering

| Parameter | Usage | Examples |
|-----------|-------|----------|
| `chain` | Chain name (must use full name) | `ethereum`, `solana`, `base` |
| `sort_by` | Sort field | `volume_24h`, `market_cap` |
| `order` | Sort direction | `asc`, `desc` |

### Supported Chains

`ethereum` · `polygon` · `bsc` · `solana` · `avalanche` · `arbitrum` · `optimism` · `fantom` · `base` · `linea` · `cyber`

> **Note:** Abbreviations are not accepted (`eth`, `sol`, `matic`, etc. won't work).

## Python Wrapper Example

```python
import requests

class SurfDataAPI:
    def __init__(self, api_key):
        self.base_url = "https://api.ask.surf/gateway"
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def get(self, path, params=None):
        resp = requests.get(
            f"{self.base_url}{path}",
            headers=self.headers,
            params=params
        )
        resp.raise_for_status()
        return resp.json()
    
    def price(self, symbols):
        return self.get("/v1/market/price", {"symbol": symbols})
    
    def funding_rate(self, symbol):
        return self.get("/v1/exchange/funding-rate", {"symbol": symbol})
    
    def wallet_balance(self, address, chain="ethereum"):
        return self.get("/v1/wallet/balance", {
            "address": address,
            "chain": chain
        })

# Usage
surf = SurfDataAPI("<your-api-key>")
btc_price = surf.price("BTC")
eth_funding = surf.funding_rate("ETH")
```

> **Verified (2026-04-03):** The following endpoints have been tested and confirmed working. Pair format is `BTC/USDT` (separated by `/`, not `-`):
>
> | Endpoint | Response Fields | Credits |
> |----------|----------------|---------|
> | `market-price` | metric, symbol, timestamp, value | 1 |
> | `market-ranking` | name, symbol, price_usd, market_cap_usd, volume_24h_usd, change_24h_pct... | 1 |
> | `market-futures` | symbol, funding_rate, long_short_ratio, open_interest, volume_24h | 1 |
> | `market-fear-greed` | classification, price, timestamp, value | 1 |
> | `exchange-price` | pair, last, bid, ask, high_24h, low_24h, volume_24h_base, change_24h_pct | 1 |
> | `exchange-funding-history` | exchange, pair, funding_rate, timestamp | 1 |
> | `exchange-long-short-ratio` | exchange, pair, long_short_ratio, timestamp | 1 |
> | `exchange-markets` | pair, exchange, base, quote, type, active, maker_fee, taker_fee | 1 |
> | `social-user` | handle, name, bio, avatar, followers_count, following_count, user_id | 2 |
> | `social-mindshare` | timestamp, value | 2 |
> | `token-holders` | address, balance, entity_name, entity_type, percentage | 1 |
> | `wallet-detail` | active_chains (chain, chain_id, usd_value) | - |
> | `project-defi-ranking` | name, symbol, tvl, fees, revenue, users | 2 |
>
> **Note:** The `chain` parameter must use full names (`ethereum` not `eth`), and `pair` uses `/` as separator (`BTC/USDT` not `BTC-USDT`).

## Error Handling

| Status Code | Meaning | Action |
|-------------|---------|--------|
| 400 | Bad request | Check parameter names and values |
| 401 | Unauthenticated | Check API Key |
| 404 | Resource not found | Check if symbol/address is correct |
| 422 | Invalid parameter value | Check if chain uses full name |
| 429 | Rate limited | Reduce request frequency |
| 502 | Upstream unavailable | Retry |

---

**Next:** Check out [Use Cases](../use-cases/) to see how to build real tools with these APIs.
