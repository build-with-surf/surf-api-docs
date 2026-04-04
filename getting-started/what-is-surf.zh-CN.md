# Surf 是什么？

[English](./what-is-surf.en.md) | 中文

---

## 一句话

Surf 是一个 **Crypto 原生的 AI 平台**，给开发者和 AI Agent 提供统一的链上数据、市场分析、社交情绪和预测市场访问能力 — 覆盖 **40+ 条链**和 **200+ 数据源**。

## 四种使用方式

| 方式 | 适合谁 | 一句话描述 |
|------|--------|-----------|
| **Surf Skill** | AI Agent 用户 | 装进 Claude Code / Codex，问一句就拿到 Crypto 数据 |
| **Surf CLI** | 终端党 | 命令行工具，适合脚本和自动化 |
| **Chat API** | 开发者 | OpenAI 兼容格式，直接调 API 构建应用 |
| **Data API** | 数据分析师 | 83 个 REST 端点 + 58 张 ClickHouse 表，支持 SQL |

## 为什么不直接用 ChatGPT？

| 维度 | ChatGPT / Claude | Dune / Messari | TradingView | **Surf** |
|------|------------------|----------------|-------------|----------|
| 实时链上数据 | ❌ 无 | ✅ 有 | ❌ 仅价格 | ✅ 40+ 链 |
| 自然语言查询 | ✅ | ❌ 需要 SQL | ❌ | ✅ |
| Crypto 专业模型 | ❌ 通用模型 | N/A | N/A | ✅ surf-1.5 系列 |
| REST API | ❌ | ⚠️ 有限 | ❌ | ✅ 83 端点 |
| SQL 直查 | ❌ | ✅ | ❌ | ✅ ClickHouse |
| Agent 集成 | ❌ | ❌ | ❌ | ✅ Skill 插件 |

## 数据覆盖

Surf 的数据分为 9 大领域：

| 领域 | 包含什么 |
|------|---------|
| **Market** | 价格、排名、技术指标、恐贪指数、爆仓、期货、期权、ETF |
| **Exchange** | 订单簿、K线、资金费率、多空比 |
| **Wallet** | 余额、转账、DeFi 持仓、净值、地址标签 |
| **Social** | Twitter/X 个人资料、推文、粉丝、Mindshare、情绪分析 |
| **Token** | 持有者、DEX 交易、转账、解锁计划 |
| **Project** | 项目资料、DeFi TVL、协议指标 |
| **Prediction Markets** | Polymarket、Kalshi — 市场、交易、价格、持仓 |
| **On-chain** | 交易查询、SQL 查询、Gas、跨链桥、收益率排名 |
| **News & Search** | 跨域实体搜索、新闻、网页抓取 |

## 模型选择

Surf 提供多个模型，适合不同场景：

| 模型 | 特点 | 适合场景 |
|------|------|---------|
| `surf-1.5` | 自适应，自动选择 instant 或 thinking | **推荐默认使用** |
| `surf-1.5-instant` | 快速响应 | 简单查询、实时监控 |
| `surf-1.5-thinking` | 深度推理 | 复杂分析、多步研究 |
| `surf-ask` | Legacy 模型 | 向后兼容 |
| `surf-research` | Legacy 深度研究（超时建议 10 分钟） | 长篇报告 |

## 背景

- **投资方：** Pantera Capital、Coinbase Ventures、DCG
- **底层：** 基于 Cyber L2 构建
- **官网：** [asksurf.ai](https://asksurf.ai)
- **API 文档：** [docs.asksurf.ai](https://docs.asksurf.ai)
- **Twitter：** [@SurfAI](https://x.com/SurfAI)

---

**下一步：** 阅读 [快速开始](./quickstart.md)，5 分钟跑通你的第一个查询。
