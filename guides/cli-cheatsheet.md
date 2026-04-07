# Surf CLI Cheatsheet & Common Pitfalls

> Battle-tested notes from real usage. Save yourself the debugging time.

## Before You Start

```bash
surf install          # Upgrade to latest version
surf sync             # Refresh API spec cache
surf <cmd> --help     # Check param enums, defaults, and formats
```

**Golden rule:** always run `--help` before calling a new command. Don't guess parameters.

## Essential Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `-o json` | JSON output | Almost always needed |
| `-f body.data` | Skip API envelope, extract data directly | `-f body.data[0]` for first item |
| `-f body.meta` | Check credits consumed, pagination info | Debugging |
| `-r` | Raw string output (no escaping) | Useful for URLs |

## Common Pitfalls

### 1. CLI flags use kebab-case, not snake_case

`list-operations` output shows snake_case param names (`top_n`, `sort_by`), but the CLI expects kebab-case:

```bash
# Wrong
surf prediction-market-dashboard --top_n 3
# Correct
surf prediction-market-dashboard --top-n 3
```

Same applies to: `--sort-by`, `--time-range`, `--reward-type`, etc.

### 2. Exchange `--pair` requires a slash

```bash
# Wrong
surf exchange-funding-history --pair BTCUSDT
# Correct
surf exchange-funding-history --pair BTC/USDT
```

### 3. Default filters hide data silently

Airdrop search defaults to `--phase active,claimable` — completed airdrops won't appear:

```bash
surf search-airdrop --q hyperliquid                        # → [] (completed, hidden by default)
surf search-airdrop --q hyperliquid --phase completed      # → results!
```

**When you get empty results, check `--help` for default filter values first.**

### 4. Fund ranking only supports two metrics

```bash
# Wrong — "aum" doesn't exist
surf fund-ranking --metric aum
# Correct — only "tier" and "portfolio_count"
surf fund-ranking --metric tier --limit 10
```

### 5. Same concept, different param names across endpoints

| Endpoint | Param | Format | Example |
|----------|-------|--------|---------|
| `market-price` | `--symbol` | Uppercase ticker | `BTC` |
| `exchange-*` | `--pair` | Slash-separated pair | `BTC/USDT` |
| `social-user` | `--handle` | Twitter handle | `vitalikbuterin` |
| `wallet-detail` | `--address` | On-chain address or ENS | `vitalik.eth` |
| `project-detail` | `--q` | Project name search | `hyperliquid` |

### 6. Not all endpoints support `--limit`

`social-mindshare` uses `--from` / `--to` for time range, not `--limit`:

```bash
surf social-mindshare --q ethereum --interval 1d --from 2026-04-01 --to 2026-04-07
```

## Quick Reference by Domain

| Domain | Key Command | Key Params |
|--------|------------|------------|
| Market | `market-price` | `--symbol`, `--time-range`, `--currency` |
| Market | `market-fear-greed` | `--from`, `--to` |
| Exchange | `exchange-funding-history` | `--pair` (with /), `--exchange` (default: binance) |
| Social | `social-user` | `--handle` |
| Social | `social-mindshare` | `--q`, `--interval` (5m/1h/1d/7d) |
| Wallet | `wallet-detail` | `--address` (supports ENS) |
| Project | `search-project` | `--q` |
| Project | `project-defi-ranking` | `--metric` |
| News | `news-feed` | `--source`, `--project`, `--limit` |
| On-chain | `onchain-gas-price` | `--chain` |
| On-chain | `onchain-sql` | POST — write SQL queries |
| Prediction | `prediction-market-dashboard` | `--category`, `--top-n` (kebab!) |
| Fund | `fund-ranking` | `--metric` (tier / portfolio_count only) |
| Airdrop | `search-airdrop` | `--phase` (default: active only) |
| Search | `search-*` | Universal `--q`, cross-domain |

## Pagination

All list endpoints support `--limit` (default 20, max 100) + `--offset`. For bulk data, loop with incrementing offset.

## Credits

Each API call consumes credits. Use `-f body.meta` to check usage. Be mindful of rate when running batch queries.

---

*Have a pitfall to add? Open a PR or issue!*
