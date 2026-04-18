# 场景：KOL 观点聚合 × 链上验证器

---

## 做什么

每天自动汇总重点 KOL 对某个叙事或代币的观点，再用链上数据和交易活跃度去验证这些观点有没有被真钱支持。

适合做两类事情：

- 跟踪一个叙事到底是“嘴上热”还是“链上热”
- 过滤掉纯喊单内容，只保留有链上配合的高质量信号

最终输出不是“谁说了什么”，而是一个更可执行的结论：

- 哪些观点正在被市场兑现
- 哪些观点只有舆论，没有资金
- 哪些 KOL 的历史判断更值得跟踪

## 数据源组合

| 数据 | Surf 能力/接口 | 用途 |
|------|----------------|------|
| KOL 观点提取 | Chat API + `ability: ["search"]` | 抓取最近观点、总结论点、提取代币和方向 |
| 讨论热度 | Data API `/social/mindshare` | 判断观点发布后热度有没有同步放大 |
| 链上大额动向 | Data API `/wallet/transfers` | 判断是否有巨鲸/项目相关地址同步行动 |
| DEX 活跃度 | Data Catalog `agent.ethereum_dex_trades` | 看交易量和参与人数是否跟上 |
| 最终结论 | Chat API + `citation: ["source"]` | 生成带依据的 conviction summary |

## 工作流程

```
每天 / 每 4 小时
    │
    ├── 抓取 KOL 最新观点（看多 / 看空 / 中性）
    ├── 提取涉及代币、叙事、时间点
    ├── 拉取 mindshare 和链上转账
    ├── 查询 DEX 活跃度变化
    │
    ▼
  计算 conviction score
    │
    ├── 观点强度
    ├── 社交扩散强度
    ├── 链上资金确认
    ├── 交易活跃度确认
    │
    ▼
  输出排行榜 / 告警 / 每日摘要
```

## 核心代码

### 1. 提取 KOL 观点

```python
import json
import requests


class KOLOnchainValidator:
    def __init__(self, api_key):
        self.data_url = "https://api.ask.surf/gateway"
        self.chat_url = "https://api.asksurf.ai/surf-ai/v1/chat/completions"
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.chat_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def extract_kol_views(self, handles, narrative):
        prompt = (
            f"分析以下 KOL 过去 72 小时关于 {narrative} 的公开观点：{', '.join(handles)}。"
            "返回 JSON 数组，每项包含：handle, symbol, stance, confidence, "
            "thesis, posted_at。stance 只允许 bullish / bearish / neutral。"
        )
        resp = requests.post(
            self.chat_url,
            headers=self.chat_headers,
            json={
                "model": "surf-1.5",
                "messages": [{"role": "user", "content": prompt}],
                "ability": ["search"],
                "citation": ["source"],
                "reasoning_effort": "medium",
            }
        )
        content = resp.json()["choices"][0]["message"]["content"]
        return json.loads(content)
```

### 2. 用社交热度和链上动向做二次验证

```python
    def get_mindshare(self, symbol, time_range="7d"):
        resp = requests.get(
            f"{self.data_url}/v1/social/mindshare",
            headers=self.headers,
            params={"symbol": symbol, "time_range": time_range}
        )
        return resp.json().get("data", []) if resp.ok else []

    def get_wallet_flow(self, address, limit=20):
        resp = requests.get(
            f"{self.data_url}/v1/wallet/transfers",
            headers=self.headers,
            params={"address": address, "limit": limit}
        )
        return resp.json().get("data", []) if resp.ok else []

    def validate_signal(self, symbol, watched_wallets):
        mindshare = self.get_mindshare(symbol)
        wallet_flows = []

        for wallet in watched_wallets:
            wallet_flows.extend(self.get_wallet_flow(wallet))

        return {
            "symbol": symbol,
            "mindshare_points": len(mindshare),
            "large_wallet_events": len([
                item for item in wallet_flows
                if item.get("amount_usd", 0) >= 100000
            ]),
        }
```

### 3. 查询 DEX 活跃度是否同步放大

```sql
-- 如果跟踪的是协议类叙事，可以直接看项目 DEX 活跃度变化
SELECT
    block_date,
    count(*) AS trade_count,
    sum(amount_usd) AS volume_usd
FROM agent.ethereum_dex_trades
WHERE block_date >= today() - 7
  AND project = 'uniswap'
GROUP BY block_date
ORDER BY block_date
```

> 如果某个观点发布后，`volume_usd` 和 `trade_count` 同时放大，通常比只看 KOL 文本更有参考价值。

### 4. 汇总 conviction score

```python
    def build_conviction_score(self, view, validation):
        score = 0

        if view["stance"] == "bullish":
            score += 20
        if view["confidence"] >= 0.7:
            score += 20
        if validation["mindshare_points"] >= 5:
            score += 20
        if validation["large_wallet_events"] >= 2:
            score += 40

        return {
            "handle": view["handle"],
            "symbol": view["symbol"],
            "stance": view["stance"],
            "conviction_score": min(score, 100),
        }
```

### 5. 生成最终日报

```python
    def summarize_rankings(self, rankings):
        resp = requests.post(
            self.chat_url,
            headers=self.chat_headers,
            json={
                "model": "surf-1.5-instant",
                "messages": [{
                    "role": "user",
                    "content": (
                        "把下面这份 KOL 观点验证结果整理成中文日报，"
                        "突出：最值得跟踪的 3 个观点、没有链上确认的噪音观点、"
                        "以及需要人工复核的信号。\n\n"
                        f"{json.dumps(rankings, ensure_ascii=False)}"
                    )
                }],
                "ability": ["calculate"],
                "reasoning_effort": "low",
            }
        )
        return resp.json()["choices"][0]["message"]["content"]
```

## 输出示例

```
📌 KOL 观点验证日报

1. @kol_a → ETHFI → bullish → conviction 82
   原因：观点发布后 24h mindshare 放大，链上出现 3 笔 >$100K 的相关资金流入

2. @kol_b → ENA → bullish → conviction 61
   原因：社交热度明显提升，但链上确认一般，适合继续观察

3. @kol_c → XYZ → bullish → conviction 28
   原因：只有讨论，没有明显成交量和链上确认，噪音概率较高
```

## 告警规则建议

- **高 conviction 告警：** 分数 >= 75 时推送
- **背离告警：** KOL 集体偏多，但链上净流出持续增加
- **抢跑告警：** 社交热度还没起来，但链上大额买入已出现

## 部署建议

- **KOL 观点提取：** 每 4 小时跑一次
- **链上验证：** 每 1 小时更新一次
- **日报：** 每天固定时间输出一次
- **看板：** 左边放观点列表，右边放链上验证和 conviction 排名

---

**相关场景：** [舆情看板](./sentiment-dashboard.md) · [新币上线追踪器](./listing-tracker.md)
