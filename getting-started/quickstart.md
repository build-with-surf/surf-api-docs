# 快速开始

[English](./quickstart.en.md) | 中文

---

5 分钟内跑通 Surf。选择你的使用方式：

## 方式一：Surf Skill（推荐 — 给 AI Agent）

如果你用 Claude Code、Codex 或其他 AI 编程工具，一行命令装好 Surf Skill：

```bash
npx skills add asksurf-ai/surf-skills --skill surf
```

装完后直接对 Agent 说话就行：

```
"ETH 现在多少钱？"
"Polymarket 上最热门的市场是哪些？"
"显示持有 AAVE 最多的钱包"
```

Skill 会自动处理认证、数据发现和请求。

## 方式二：Surf CLI

终端安装：

```bash
curl -fsSL https://agent.asksurf.ai/cli/releases/install.sh | sh
```

登录并发出第一个请求：

```bash
surf login
surf market-price --symbol BTC
```

## 方式三：Chat API（构建应用）

Chat API 兼容 OpenAI 格式，切换成本为零：

```bash
curl --request POST \
  --url https://api.asksurf.ai/surf-ai/v1/chat/completions \
  --header 'Authorization: Bearer <your-api-key>' \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "surf-1.5",
    "messages": [
      {"role": "user", "content": "分析 BTC 过去 7 天的市场走势，给出关键支撑位和阻力位"}
    ],
    "reasoning_effort": "medium"
  }'
```

### 用 Python 调用

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
            {"role": "user", "content": "对比 Aave 和 Compound 的 TVL 趋势"}
        ],
        "reasoning_effort": "medium",
        "ability": ["evm_onchain", "market_analysis"],
        "citation": ["source", "chart"]
    }
)

result = response.json()
print(result["choices"][0]["message"]["content"])
```

### 关键参数

| 参数 | 作用 | 选项 |
|------|------|------|
| `model` | 选择模型 | `surf-1.5`（推荐）/ `surf-1.5-instant` / `surf-1.5-thinking` |
| `reasoning_effort` | 推理深度 | `low` / `medium` / `high` |
| `ability` | 指定数据能力 | `search` / `evm_onchain` / `solana_onchain` / `market_analysis` / `calculate` |
| `citation` | 引用格式 | `source` / `chart` |
| `stream` | 流式输出 | `true` / `false` |

## 方式四：Data API（直接查数据）

83 个 REST 端点，直接拿结构化数据：

```bash
# 查 BTC 价格
curl -H "Authorization: Bearer <your-api-key>" \
  "https://api.ask.surf/gateway/v1/market/price?symbol=BTC"

# 查资金费率
curl -H "Authorization: Bearer <your-api-key>" \
  "https://api.ask.surf/gateway/v1/exchange/funding-rate?symbol=BTC"
```

## 方式五：SQL 直查（Data Catalog）

58 张 ClickHouse 表，直接写 SQL：

```sql
-- 昨天 DEX 交易量 Top 10 协议
SELECT project, sum(amount_usd) AS volume_usd
FROM agent.ethereum_dex_trades
WHERE block_date = today() - 1
GROUP BY project
ORDER BY volume_usd DESC
LIMIT 10
```

> **性能提示：** 永远先按 `block_date` 过滤 — 这是分区键，能让 ClickHouse 跳过无关分区。

<!-- TODO(team): 补充 ClickHouse 连接地址和端口（文档说 port 8443 TLS, user: agent） -->

## Credits 计费

每次 API 调用消耗一定 Credits，响应里的 `meta.credits_used` 会告诉你这次花了多少。

```bash
# 查剩余额度
curl -H "Authorization: Bearer <your-api-key>" \
  "https://api.ask.surf/gateway/v1/me/credit-balance"
```

<!-- TODO(team): 补充获取 API Key 的步骤和 Credit 充值方式 -->

---

**下一步：** 看 [Chat API 实战指南](../guides/chat-api-guide.md) 学习如何构建实际应用，或者查看 [使用场景](../use-cases/) 获取灵感。
