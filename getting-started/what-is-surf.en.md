# What is Surf?

[English](./what-is-surf.en.md) | [中文](./what-is-surf.md)

---

## One Liner

Surf is a **Crypto-native AI platform** that provides developers and AI Agents with unified access to on-chain data, market analysis, social sentiment, and prediction markets — covering **40+ chains** and **200+ data sources**.

## Four Ways to Use Surf

| Method | Best For | Description |
|--------|----------|-------------|
| **Surf Skill** | AI Agent users | Install in Claude Code / Codex, get Crypto data with a single question |
| **Surf CLI** | Terminal users | Command-line tool for scripts and automation |
| **Chat API** | Developers | OpenAI-compatible format, build apps directly with the API |
| **Data API** | Data analysts | 83 REST endpoints + 58 ClickHouse tables with SQL support |

## Why Not Just Use ChatGPT?

| Dimension | ChatGPT / Claude | Dune / Messari | TradingView | **Surf** |
|-----------|------------------|----------------|-------------|----------|
| Real-time on-chain data | No | Yes | Prices only | Yes, 40+ chains |
| Natural language queries | Yes | No, requires SQL | No | Yes |
| Crypto-specialized model | No, general-purpose | N/A | N/A | Yes, surf-1.5 series |
| REST API | No | Limited | No | Yes, 83 endpoints |
| Direct SQL queries | No | Yes | No | Yes, ClickHouse |
| Agent integration | No | No | No | Yes, Skill plugin |

## Data Coverage

Surf's data spans 9 domains:

| Domain | What's Included |
|--------|----------------|
| **Market** | Prices, rankings, technical indicators, Fear & Greed Index, liquidations, futures, options, ETFs |
| **Exchange** | Order books, candlesticks, funding rates, long/short ratios |
| **Wallet** | Balances, transfers, DeFi positions, net worth, address labels |
| **Social** | Twitter/X profiles, tweets, followers, Mindshare, sentiment analysis |
| **Token** | Holders, DEX trades, transfers, unlock schedules |
| **Project** | Project profiles, DeFi TVL, protocol metrics |
| **Prediction Markets** | Polymarket, Kalshi — markets, trades, prices, positions |
| **On-chain** | Transaction queries, SQL queries, gas, bridges, yield rankings |
| **News & Search** | Cross-domain entity search, news, web scraping |

## Model Selection

Surf offers multiple models for different scenarios:

| Model | Characteristics | Best For |
|-------|----------------|----------|
| `surf-1.5` | Adaptive, automatically selects instant or thinking | **Recommended default** |
| `surf-1.5-instant` | Fast response | Simple queries, real-time monitoring |
| `surf-1.5-thinking` | Deep reasoning | Complex analysis, multi-step research |
| `surf-ask` | Legacy model | Backward compatibility |
| `surf-research` | Legacy deep research (recommend 10-min timeout) | Long-form reports |

## Background

- **Investors:** Pantera Capital, Coinbase Ventures, DCG
- **Built on:** Cyber L2
- **Website:** [asksurf.ai](https://asksurf.ai)
- **API Docs:** [docs.asksurf.ai](https://docs.asksurf.ai)
- **Twitter:** [@SurfAI](https://x.com/SurfAI)

---

**Next:** Read the [Quickstart](./quickstart.md) to run your first query in 5 minutes.
