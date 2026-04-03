# 场景：多钱包资产监控看板

---

## 做什么

同时追踪多个钱包的资产净值、币种分布、最近转账和异常流出，适合以下场景：

- 个人多地址资产总览
- 小团队 treasury 监控
- 项目方/基金观察名单跟踪

核心目标不是只看余额，而是把多个地址的资产变化、资金流向和风险信号放到一个统一面板里。

## 数据源组合

| 数据 | Surf 能力/接口 | 用途 |
|------|----------------|------|
| 地址资产结构 | Chat API + `ability: ["evm_onchain", "calculate"]` | 总结地址当前持仓、净值和集中度 |
| 最近大额转账 | Data API `/wallet/transfers` | 检查是否有大额转出、跨地址搬仓、转入交易所 |
| 币价 | Data API `/market/price` | 把不同资产换算成统一 USD 口径 |
| 风险摘要 | Chat API + `citation: ["source"]` | 生成每天/每小时的自然语言总结 |

## 工作流程

```
定时任务（每 10 分钟）
    │
    ├── Chat API：总结每个地址的资产结构
    ├── Data API：拉取最近转账 (/wallet/transfers)
    ├── Data API：拉取价格 (/market/price)
    │
    ▼
  统一换算 USD 净值
    │
    ├── 计算总净值
    ├── 计算地址间资产占比
    ├── 检测大额流出 / 交易所流向
    │
    ▼
  生成看板 + Telegram/企业微信告警
```

## 核心代码

### 1. 获取地址资产摘要

```python
import json
import requests


class MultiWalletDashboard:
    def __init__(self, api_key):
        self.data_url = "https://api.ask.surf/gateway"
        self.chat_url = "https://api.asksurf.ai/surf-ai/v1/chat/completions"
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.chat_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def get_wallet_snapshot(self, address):
        """让 Surf 总结地址当前资产结构，输出统一 JSON。"""
        resp = requests.post(
            self.chat_url,
            headers=self.chat_headers,
            json={
                "model": "surf-1.5",
                "messages": [{
                    "role": "user",
                    "content": (
                        f"分析 EVM 地址 {address} 当前的资产结构，"
                        "返回 JSON，字段包括："
                        "address, net_worth_usd, top_holdings, stablecoin_ratio, "
                        "risk_flags。top_holdings 最多返回 5 个。"
                    )
                }],
                "ability": ["evm_onchain", "calculate"],
                "citation": ["source"],
                "reasoning_effort": "medium",
            }
        )
        content = resp.json()["choices"][0]["message"]["content"]
        return json.loads(content)
```

### 2. 拉取最近转账并识别异常流出

```python
    def get_recent_transfers(self, address, limit=20):
        resp = requests.get(
            f"{self.data_url}/v1/wallet/transfers",
            headers=self.headers,
            params={"address": address, "limit": limit}
        )
        return resp.json().get("data", []) if resp.ok else []

    def detect_large_outflows(self, address, threshold_usd=50000):
        alerts = []
        transfers = self.get_recent_transfers(address)

        for item in transfers:
            amount_usd = item.get("amount_usd", 0)
            direction = item.get("direction", "")
            if direction == "out" and amount_usd >= threshold_usd:
                alerts.append({
                    "address": address,
                    "token": item.get("symbol"),
                    "amount_usd": amount_usd,
                    "to": item.get("to_address"),
                    "timestamp": item.get("timestamp"),
                })

        return alerts
```

### 3. 汇总多个地址，生成统一面板数据

```python
    def build_dashboard(self, addresses):
        snapshots = []
        alerts = []
        total_net_worth = 0

        for address in addresses:
            snapshot = self.get_wallet_snapshot(address)
            snapshots.append(snapshot)
            total_net_worth += snapshot.get("net_worth_usd", 0)
            alerts.extend(self.detect_large_outflows(address))

        return {
            "total_net_worth_usd": round(total_net_worth, 2),
            "wallet_count": len(addresses),
            "snapshots": snapshots,
            "alerts": alerts,
        }
```

### 4. 用 Surf 自动写风险日报

```python
    def generate_daily_summary(self, dashboard_data):
        resp = requests.post(
            self.chat_url,
            headers=self.chat_headers,
            json={
                "model": "surf-1.5-instant",
                "messages": [{
                    "role": "user",
                    "content": (
                        "基于以下多钱包监控数据，生成一份 200 字以内的中文日报："
                        "1. 总资产变化 2. 集中度风险 3. 异常转账 4. 值得关注的钱包\n\n"
                        f"{json.dumps(dashboard_data, ensure_ascii=False)}"
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
📊 多钱包资产看板

监控地址数：6
总净值：$2.84M

Top 3 地址：
1. 0xA1...9F 净值 $1.12M，ETH 占比 46%
2. 0xC3...72 净值 $860K，稳定币占比 58%
3. 0xF8...11 净值 $420K，长尾资产较多

风险提示：
- 0xA1...9F 最近 30 分钟转出 $120K USDC
- 0xC3...72 对单一资产暴露过高（ETHFI 占比 31%）
- 2 个地址在同一小时内向新地址搬仓，建议人工复核
```

## 前端展示建议

用 [dashboard-template](https://github.com/build-with-surf/dashboard-template) 很适合直接搭：

```
┌─────────────────────────────────────────────┐
│  总资产净值  $2.84M   今日变化 +3.2%         │
├─────────────────┬───────────────────────────┤
│ 地址列表         │  资产构成 / 稳定币占比      │
│ 0xA1...9F       │  ETH 46% / USDC 22% ...   │
│ 0xC3...72       │  USDT 58% / ETH 18% ...   │
├─────────────────┴───────────────────────────┤
│ 最近异动：大额转出 / 跨地址搬仓 / 交易所流向    │
└─────────────────────────────────────────────┘
```

## 部署建议

- **刷新频率：** 10-15 分钟一次即可
- **告警阈值：** 按地址净值比例设置，比固定金额更实用
- **存储：** 每次快照落到数据库，方便做净值曲线和风险回放
- **通知：** 大额转出、转入交易所、短时连续搬仓建议即时推送

---

**相关场景：** [舆情看板](./sentiment-dashboard.md) · [新币上线追踪器](./listing-tracker.md)
