# Chat API 实战指南

[English](./chat-api-guide.en.md) | 中文

---

Chat API 是 Surf 最灵活的接口 — OpenAI 兼容格式，可以直接用来构建 Crypto AI 应用。

## 基础架构

```
你的应用 → POST /v1/chat/completions → Surf 模型
                                         ↓
                                    实时链上数据
                                    市场分析引擎
                                    社交情绪分析
                                    预测市场数据
                                         ↓
                                    结构化回答
```

## 模型怎么选？

| 场景 | 推荐模型 | `reasoning_effort` | 为什么 |
|------|---------|-------------------|--------|
| 实时价格/简单查询 | `surf-1.5-instant` | `low` | 快，0.5-2 秒返回 |
| 日常分析 | `surf-1.5` | `medium` | 自动选择 instant 或 thinking |
| 深度研究报告 | `surf-1.5-thinking` | `high` | 多步推理，结果更深入 |
| 长篇尽调 | `surf-research` | N/A | Legacy 但适合超长输出（超时设 10 分钟） |

## `ability` 参数详解

`ability` 告诉 Surf 这次查询需要调用哪些数据能力：

| ability | 含义 | 典型用途 |
|---------|------|---------|
| `search` | 搜索引擎 | 项目信息、新闻、实体查找 |
| `evm_onchain` | EVM 链上数据 | ETH/Polygon/Arbitrum 等链的交易、合约、钱包 |
| `solana_onchain` | Solana 链上数据 | SPL 代币、DEX 交易 |
| `market_analysis` | 市场分析 | 价格、K线、技术指标、资金费率 |
| `calculate` | 计算引擎 | 数学计算、投资组合估值 |

**建议：** 明确指定 ability 可以加快响应速度。不指定则 Surf 自动判断。

```python
# 查链上数据时，指定 evm_onchain
{"ability": ["evm_onchain"]}

# 做市场分析时，指定 market_analysis
{"ability": ["market_analysis"]}

# 需要同时看链上和市场数据
{"ability": ["evm_onchain", "market_analysis"]}
```

## `citation` 参数

控制 Surf 是否在回答中附带引用：

| 值 | 效果 |
|------|------|
| `source` | 附带数据来源链接 |
| `chart` | 生成可视化图表 |

## 实战示例

### 1. 资金费率监控 Bot

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
                "content": "列出当前资金费率最高和最低的 5 个币种，包括 Binance 和 OKX 的对比"
            }],
            "reasoning_effort": "low",
            "ability": ["market_analysis"]
        }
    )
    return response.json()["choices"][0]["message"]["content"]
```

### 2. 项目快速尽调

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
                "content": "你是一个 Crypto 研究分析师。输出结构化的项目尽调报告。"
            }, {
                "role": "user",
                "content": f"对 {project_name} 做一份快速尽调：基本面、链上数据、社交热度、风险点"
            }],
            "reasoning_effort": "high",
            "ability": ["search", "evm_onchain", "market_analysis"],
            "citation": ["source"]
        },
        timeout=600  # 深度研究可能需要更长时间
    )
    return response.json()["choices"][0]["message"]["content"]
```

### 3. 流式输出（适合 UI 展示）

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
        "messages": [{"role": "user", "content": "分析 ETH 的链上活跃度趋势"}],
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

## 错误处理

| HTTP 状态码 | 含义 | 怎么办 |
|------------|------|--------|
| 400 | 参数错误 | 检查请求格式 |
| 401 | API Key 无效 | 检查 Authorization header |
| 402 | Credits 不足 | 充值 |
| 502 | 上游数据源暂时不可用 | 等一会儿重试 |

## 从 OpenAI SDK 迁移

如果你已经在用 OpenAI SDK，只需要改两行：

```python
from openai import OpenAI

client = OpenAI(
    api_key="<your-surf-api-key>",
    base_url="https://api.asksurf.ai/surf-ai/v1"  # 改这里
)

response = client.chat.completions.create(
    model="surf-1.5",  # 改这里
    messages=[{"role": "user", "content": "BTC 今天怎么样？"}]
)
```

> **已验证（2026-04-03）：** OpenAI SDK 完全兼容。`extra_body` 可以传递 `ability`、`reasoning_effort`、`citation` 等 Surf 扩展字段。Streaming 也正常工作。

---

**下一步：** 查看 [Data API 实战指南](./data-api-guide.md) 学习如何直接查询结构化数据。
