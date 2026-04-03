# 常见问题 FAQ

[English](./faq.en.md) | 中文

---

### Chat API 和 Data API 有什么区别？

- **Chat API** — 自然语言输入，Surf AI 理解你的问题并返回分析结果。适合研究、报告生成、复杂分析
- **Data API** — 结构化 REST 请求，返回 JSON 数据。适合构建看板、监控系统、数据管道

简单说：Chat API 是让 AI 帮你分析，Data API 是你自己拿数据来分析。

### 模型怎么选？

| 你要做什么 | 用哪个模型 |
|-----------|-----------|
| 快速查价格、简单问答 | `surf-1.5-instant` |
| 日常分析（不知道选哪个就用这个） | `surf-1.5` |
| 深度研究、多步推理 | `surf-1.5-thinking` |
| 超长尽调报告 | `surf-research`（超时设 10 分钟） |

### 支持哪些链？

`ethereum` · `polygon` · `bsc` · `solana` · `avalanche` · `arbitrum` · `optimism` · `fantom` · `base` · `linea` · `cyber`

Data API 的 `chain` 参数必须用全称，不接受缩写（`eth`, `sol` 等不行）。

### Credits 怎么计费？

每次 API 调用消耗 Credits，具体消耗量在响应的 `meta.credits_used` 字段中返回。可以通过 `GET /v1/me/credit-balance` 查询余额。

<!-- TODO(team): 补充 Credit 价格表和充值方式 -->

### 能用 OpenAI SDK 调 Surf 吗？

可以。Chat API 兼容 OpenAI 格式，只需要改 `base_url` 和 `model`：

```python
from openai import OpenAI
client = OpenAI(
    api_key="<surf-api-key>",
    base_url="https://api.asksurf.ai/surf-ai/v1"
)
```

Surf 的扩展字段（`ability`, `citation`）可能需要通过 `extra_body` 传递。

> **已验证：** `extra_body` 可传递 `ability`、`reasoning_effort`、`citation`。Streaming 正常。

### 数据延迟是多少？

取决于数据源：

| 数据类型 | 延迟 |
|---------|------|
| CoinGecko 价格 | ~1 小时 |
| Polygon 链上 | ~1 小时 |
| Base 链上 | ~6 小时 |
| Ethereum/Arbitrum 链上 | ~1 天 |
| Polymarket | ~1 天 |
| Kalshi | ~6 小时 |

### Data Catalog 怎么连接？

通过 ClickHouse HTTP 接口（端口 8443，TLS），用户名 `agent`（只读）。

<!-- TODO(team): 补充连接地址和密码获取方式 -->

### 请求报错了怎么办？

| 错误码 | 含义 | 解决 |
|--------|------|------|
| 400 | 参数错误 | 检查请求格式和参数值 |
| 401 | 认证失败 | 检查 API Key |
| 402 | Credits 不足 | 充值 |
| 422 | 参数值无效 | 检查 chain 是否用了全称等 |
| 429 | 限频 | 降低频率，等一会儿重试 |
| 502 | 上游不可用 | 等一会儿重试 |

### 这个知识库是官方的吗？

不是。这是社区维护的非官方知识库。官方文档在 [docs.asksurf.ai](https://docs.asksurf.ai)。

我们的目的是提供更多实战教程、使用场景和代码示例，补充官方文档没覆盖的内容。

---

**还有问题？** 在 [GitHub Issues](https://github.com/build-with-surf/surf-api-docs/issues) 提问。
