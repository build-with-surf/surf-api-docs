# Surf CLI 速查表 & 常见踩坑

> 实测总结，帮你省掉 debug 时间。

## 每次开始前必做

```bash
surf install          # 升级到最新版
surf sync             # 刷新 API spec 缓存
surf <cmd> --help     # 看参数 enum、默认值、格式要求
```

**铁律：** 用新命令前先 `--help`，不要猜参数。

## 常用 Flag

| Flag | 作用 | 示例 |
|------|------|------|
| `-o json` | JSON 输出 | 几乎每次都加 |
| `-f body.data` | 跳过信封，直取数据 | `-f body.data[0]` 取第一条 |
| `-f body.meta` | 查 credits 消耗、分页信息 | 调试用 |
| `-r` | 配合 `-f`，输出 raw string 不转义 | 拿 URL 时有用 |

## 常见踩坑

### 1. Flag 命名用 kebab-case，不是 snake_case

`list-operations` 输出的参数名是 snake_case（`top_n`, `sort_by`），但 CLI 要 kebab-case：

```bash
# 错
surf prediction-market-dashboard --top_n 3
# 对
surf prediction-market-dashboard --top-n 3
```

同理：`--sort-by`、`--time-range`、`--reward-type`

### 2. Exchange 的 `--pair` 要带斜杠

```bash
# 错
surf exchange-funding-history --pair BTCUSDT
# 对
surf exchange-funding-history --pair BTC/USDT
```

### 3. 默认 filter 会悄悄藏数据

Airdrop 默认 `--phase active,claimable`，已结束的不显示：

```bash
surf search-airdrop --q hyperliquid                        # → []（已 completed，默认不显示）
surf search-airdrop --q hyperliquid --phase completed      # → 有数据
```

**拿到空结果，先查 `--help` 看默认过滤条件。**

### 4. Fund ranking 只支持两个 metric

```bash
# 错 — aum 不存在
surf fund-ranking --metric aum
# 对 — 只有 tier 和 portfolio_count
surf fund-ranking --metric tier --limit 10
```

### 5. 相同概念，不同端点参数名不同

| 端点 | 参数 | 格式 | 示例 |
|------|------|------|------|
| `market-price` | `--symbol` | 大写 ticker | `BTC` |
| `exchange-*` | `--pair` | 斜杠分隔交易对 | `BTC/USDT` |
| `social-user` | `--handle` | Twitter handle | `vitalikbuterin` |
| `wallet-detail` | `--address` | 链上地址或 ENS | `vitalik.eth` |
| `project-detail` | `--q` | 项目名搜索 | `hyperliquid` |

### 6. 不是所有端点都有 `--limit`

`social-mindshare` 用 `--from` / `--to` 控制时间范围，没有 limit：

```bash
surf social-mindshare --q ethereum --interval 1d --from 2026-04-01 --to 2026-04-07
```

## 全域速查

| 域 | 代表命令 | 关键参数 |
|---|---|---|
| Market | `market-price` | `--symbol`, `--time-range`, `--currency` |
| Market | `market-fear-greed` | `--from`, `--to` |
| Exchange | `exchange-funding-history` | `--pair`(带/), `--exchange`(默认 binance) |
| Social | `social-user` | `--handle` |
| Social | `social-mindshare` | `--q`, `--interval`(5m/1h/1d/7d) |
| Wallet | `wallet-detail` | `--address`(支持 ENS) |
| Project | `search-project` | `--q` |
| Project | `project-defi-ranking` | `--metric` |
| News | `news-feed` | `--source`, `--project`, `--limit` |
| On-chain | `onchain-gas-price` | `--chain` |
| On-chain | `onchain-sql` | POST，写 SQL 查询 |
| Prediction | `prediction-market-dashboard` | `--category`, `--top-n`(kebab!) |
| Fund | `fund-ranking` | `--metric`(仅 tier/portfolio_count) |
| Airdrop | `search-airdrop` | `--phase`(默认只显示 active) |
| Search | `search-*` | 通用 `--q`，跨域搜索 |

## 分页

所有列表端点支持 `--limit`（默认 20，最大 100）+ `--offset`。大量数据需循环翻页。

## Credits

每次调用消耗 credits，用 `-f body.meta` 查看消耗量。批量操作注意控制请求频率。

---

*发现新坑？欢迎提 PR 或 issue！*
