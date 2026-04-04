# Frequently Asked Questions

[English](./faq.en.md) | [中文](./faq.md)

---

### What's the difference between Chat API and Data API?

- **Chat API** — Natural language input; Surf AI understands your question and returns analysis results. Best for research, report generation, and complex analysis.
- **Data API** — Structured REST requests returning JSON data. Best for building dashboards, monitoring systems, and data pipelines.

In short: Chat API lets AI analyze for you; Data API gives you the data to analyze yourself.

### How do I choose a model?

| What you need | Which model |
|---------------|-------------|
| Quick price checks, simple Q&A | `surf-1.5-instant` |
| Everyday analysis (use this if unsure) | `surf-1.5` |
| Deep research, multi-step reasoning | `surf-1.5-thinking` |
| Long-form due diligence reports | `surf-research` (set 10-min timeout) |

### Which chains are supported?

`ethereum` · `polygon` · `bsc` · `solana` · `avalanche` · `arbitrum` · `optimism` · `fantom` · `base` · `linea` · `cyber`

The Data API `chain` parameter requires full names — abbreviations like `eth`, `sol`, etc. are not accepted.

### How does Credits billing work?

Each API call consumes Credits. The exact amount is returned in the `meta.credits_used` field of the response. You can check your balance via `GET /v1/me/credit-balance`.

> **Get Credits:** Contact [@siriusxyzzz](https://x.com/siriusxyzzz) to join the developer WeChat group for Credits and technical support.

### Can I use the OpenAI SDK with Surf?

Yes. The Chat API is OpenAI-compatible — just change `base_url` and `model`:

```python
from openai import OpenAI
client = OpenAI(
    api_key="<surf-api-key>",
    base_url="https://api.asksurf.ai/surf-ai/v1"
)
```

Surf extension fields (`ability`, `citation`) can be passed via `extra_body`.

> **Verified:** `extra_body` supports `ability`, `reasoning_effort`, and `citation`. Streaming works correctly.

### What's the data latency?

Depends on the data source:

| Data Type | Latency |
|-----------|---------|
| CoinGecko prices | ~1 hour |
| Polygon on-chain | ~1 hour |
| Base on-chain | ~6 hours |
| Ethereum/Arbitrum on-chain | ~1 day |
| Polymarket | ~1 day |
| Kalshi | ~6 hours |

### How do I connect to the Data Catalog?

Via ClickHouse HTTP interface (port 8443, TLS), username `agent` (read-only).

> Contact [@siriusxyzzz](https://x.com/siriusxyzzz) to join the developer WeChat group for connection details.

### What should I do when I get an error?

| Error Code | Meaning | Solution |
|------------|---------|----------|
| 400 | Bad request | Check request format and parameter values |
| 401 | Authentication failed | Check API Key |
| 402 | Insufficient Credits | Top up |
| 422 | Invalid parameter value | Check if chain uses full name, etc. |
| 429 | Rate limited | Reduce frequency, wait and retry |
| 502 | Upstream unavailable | Wait and retry |

### Is this an official knowledge base?

No. This is a community-maintained unofficial knowledge base. Official documentation is at [docs.asksurf.ai](https://docs.asksurf.ai).

Our goal is to provide more hands-on tutorials, use cases, and code examples that supplement what the official docs don't cover.

---

**Still have questions?** Ask on [GitHub Issues](https://github.com/build-with-surf/surf-api-docs/issues).
