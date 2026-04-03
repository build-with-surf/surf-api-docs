# 场景：链上异动告警机器人

---

## 做什么

实时监控指定地址、指定代币或指定叙事的链上异动，在“真正值得打断你”的时候才推送告警。

这类机器人最常见的问题不是抓不到数据，而是噪音太多。所以重点不只是“发现事件”，而是做三层过滤：

1. 事件本身是否够大
2. 和历史基线相比是否异常
3. 是否值得立刻人工介入

## 适合监控的异动

- 巨鲸地址突然大额转出
- 项目相关钱包向交易所转账
- 某代币交易活跃度短时放大
- 某叙事在社交热度上升前，链上先开始异动

## 数据源组合

| 数据 | Surf 能力/接口 | 用途 |
|------|----------------|------|
| 钱包转账 | Data API `/wallet/transfers` | 检测大额转账、交易所流向、连续异动 |
| 币价 | Data API `/market/price` | 把转账金额统一换算成 USD |
| 交易活跃度 | Data Catalog `agent.ethereum_dex_trades` | 判断成交量/交易次数是否偏离基线 |
| 事件解读 | Chat API + `ability: ["market_analysis", "search"]` | 给出事件可能含义和优先级 |

## 工作流程

```
定时任务（每 5 分钟）
    │
    ├── 监控钱包转账 (/wallet/transfers)
    ├── 拉取价格 (/market/price)
    ├── 查询 DEX 交易基线
    │
    ▼
  事件标准化
    │
    ├── 计算 USD 金额
    ├── 判断是否超阈值
    ├── 判断是否偏离历史基线
    │
    ▼
  用 Surf AI 生成事件解释
    │
    ▼
  Telegram / 飞书 / 企业微信告警
```

## 核心代码

### 1. 拉取最近链上转账

```python
import requests


class OnchainAlertBot:
    def __init__(self, api_key):
        self.data_url = "https://api.ask.surf/gateway"
        self.chat_url = "https://api.asksurf.ai/surf-ai/v1/chat/completions"
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.chat_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def get_transfers(self, address, limit=20):
        resp = requests.get(
            f"{self.data_url}/v1/wallet/transfers",
            headers=self.headers,
            params={"address": address, "limit": limit}
        )
        return resp.json().get("data", []) if resp.ok else []
```

### 2. 把事件标准化为统一告警格式

```python
    def normalize_events(self, address, threshold_usd=100000):
        transfers = self.get_transfers(address)
        events = []

        for item in transfers:
            amount_usd = item.get("amount_usd", 0)
            if amount_usd < threshold_usd:
                continue

            events.append({
                "address": address,
                "symbol": item.get("symbol"),
                "amount_usd": amount_usd,
                "direction": item.get("direction"),
                "from_address": item.get("from_address"),
                "to_address": item.get("to_address"),
                "timestamp": item.get("timestamp"),
            })

        return events
```

### 3. 用历史基线过滤噪音

```sql
-- 看某个协议最近 14 天的交易基线
SELECT
    block_date,
    count(*) AS trade_count,
    sum(amount_usd) AS volume_usd
FROM agent.ethereum_dex_trades
WHERE block_date >= today() - 14
  AND project = 'uniswap'
GROUP BY block_date
ORDER BY block_date
```

> 如果今天的 `trade_count` 或 `volume_usd` 明显高于最近 14 天均值，可以把告警优先级抬高。

### 4. 让 Surf 给出事件解读

```python
    def explain_event(self, event):
        resp = requests.post(
            self.chat_url,
            headers=self.chat_headers,
            json={
                "model": "surf-1.5-instant",
                "messages": [{
                    "role": "user",
                    "content": (
                        "请分析下面这条链上异动，返回 3 个字段："
                        "summary, priority, hypothesis。"
                        "priority 只允许 low / medium / high。\n\n"
                        f"{event}"
                    )
                }],
                "ability": ["market_analysis", "search"],
                "citation": ["source"],
                "reasoning_effort": "low",
            }
        )
        return resp.json()["choices"][0]["message"]["content"]
```

### 5. 告警主循环

```python
    def run_once(self, addresses):
        alerts = []

        for address in addresses:
            events = self.normalize_events(address)
            for event in events:
                explanation = self.explain_event(event)
                alerts.append({
                    "event": event,
                    "explanation": explanation,
                })

        return alerts
```

## 输出示例

```
🚨 链上异动告警

地址：0xA1...9F
事件：转出 420,000 USDC
方向：out
时间：2026-04-03 13:25 UTC

Surf 解读：
- summary: 该地址出现明显高于平时水平的大额转出
- priority: high
- hypothesis: 若目标地址为交易所或做市相关地址，可能意味着短期卖压上升
```

## 告警策略建议

- **金额阈值：** 绝对金额 + 地址净值占比双阈值一起用
- **冷却时间：** 同一地址 30 分钟内合并告警，避免刷屏
- **优先级：**
  - `high`：大额转出 + 交易所流向 + 活跃度同步放大
  - `medium`：大额转账，但没有更多确认
  - `low`：金额不大，或更像日常调仓

## 部署建议

- **频率：** 5 分钟一次够用，大多数场景不需要秒级
- **通知渠道：** Telegram、飞书、企业微信 Webhook 都适合
- **存档：** 每次告警入库，后面可以回测哪些信号最有效
- **扩展：** 后续可以加白名单、黑名单、交易所地址标签

---

**相关场景：** [套利监控](./arbitrage-monitor.md) · [舆情看板](./sentiment-dashboard.md)
