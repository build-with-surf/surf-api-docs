# 场景：Twitter 舆情 × 链上数据联动看板

[English](./sentiment-dashboard.en.md) | 中文

---

## 做什么

左边显示 Twitter 实时舆情热度，右边显示对应项目的链上数据（TVL、交易量、巨鲸动向）。当两边走势背离时，自动发出信号：

- **舆情热 + 链上冷 = "虚火警报"** — 可能是炒作，谨慎追高
- **链上热 + 舆情冷 = "埋伏机会"** — 聪明钱在行动，市场还没反应

## 数据源组合

| 数据 | Surf 接口 | 用途 |
|------|----------|------|
| Twitter Mindshare | Data API `/social/mindshare` | 舆情热度趋势 |
| Twitter 情绪 | Chat API + `ability: ["search"]` | 正面/负面情绪判断 |
| 项目 TVL | Data API `/project/tvl` | 链上真实资金流入 |
| DEX 交易量 | Data Catalog `agent.ethereum_dex_trades` | 链上交易活跃度 |
| 巨鲸转账 | Data API `/wallet/transfers` | 大户动向 |

## 核心代码

### 1. 获取舆情 + 链上数据

```python
import requests

class SentimentDashboard:
    def __init__(self, api_key):
        self.data_url = "https://api.ask.surf/gateway"
        self.chat_url = "https://api.asksurf.ai/surf-ai/v1/chat/completions"
        self.headers = {"Authorization": f"Bearer {api_key}"}
        self.chat_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_mindshare(self, symbol, time_range="7d"):
        """获取 Twitter Mindshare 趋势"""
        resp = requests.get(
            f"{self.data_url}/v1/social/mindshare",
            headers=self.headers,
            params={"symbol": symbol, "time_range": time_range}
        )
        return resp.json() if resp.ok else None
    
    def get_sentiment(self, symbol):
        """用 Chat API 分析当前情绪"""
        resp = requests.post(
            self.chat_url,
            headers=self.chat_headers,
            json={
                "model": "surf-1.5-instant",
                "messages": [{
                    "role": "user",
                    "content": f"分析 Twitter 上过去 24 小时关于 {symbol} 的讨论情绪。"
                               f"给出：1) 整体偏多/偏空/中性 2) 主要话题 3) 影响力最大的 KOL 观点"
                }],
                "ability": ["search"],
                "reasoning_effort": "low"
            }
        )
        return resp.json()["choices"][0]["message"]["content"]
```

### 2. 背离检测

```python
    def detect_divergence(self, symbol):
        """检测舆情-链上背离"""
        mindshare = self.get_mindshare(symbol)
        # TODO(team): 补充 TVL 数据获取
        # tvl = requests.get(f"{self.data_url}/v1/project/tvl", ...)
        
        # 背离逻辑：
        # mindshare_change = (本周 mindshare - 上周) / 上周
        # tvl_change = (本周 TVL - 上周) / 上周
        # 
        # if mindshare_change > 30% and tvl_change < -5%:
        #     return "虚火警报"
        # if mindshare_change < -10% and tvl_change > 20%:
        #     return "埋伏机会"
        # return "正常"
        pass
```

### 3. 用 SQL 查历史背离事件

```sql
-- 查某个项目的 DEX 交易量趋势（过去 30 天，按天聚合）
SELECT 
    block_date,
    sum(amount_usd) AS daily_volume,
    count(*) AS trade_count
FROM agent.ethereum_dex_trades
WHERE block_date >= today() - 30
  -- TODO(team): 添加项目过滤条件（project = 'uniswap' 等）
GROUP BY block_date
ORDER BY block_date
```

## 前端展示建议

用 [dashboard-template](https://github.com/build-with-surf/dashboard-template) 快速搭建：

```
┌─────────────────┬─────────────────┐
│  Twitter 舆情     │   链上数据       │
│                 │                 │
│  📈 Mindshare    │  📊 TVL 趋势     │
│  曲线图          │  曲线图          │
│                 │                 │
│  😊 情绪分布      │  🐋 巨鲸动向     │
│  饼图            │  表格            │
│                 │                 │
├─────────────────┴─────────────────┤
│          ⚠️ 背离信号               │
│  ETH: 虚火警报 — Mindshare +45%,   │
│  但 TVL -8%, 巨鲸净流出 $2.3M      │
└───────────────────────────────────┘
```

## 部署

- **刷新频率：** 舆情数据 1 小时，链上数据 6 小时（参考 Surf 数据延迟表）
- **存储：** 历史背离事件存数据库，用于回测信号准确率
- **告警：** 背离信号通过 Telegram Bot 推送

<!-- TODO(team): 补充实际 mindshare API 返回格式 -->

---

**相关场景：** [套利监控](./arbitrage-monitor.md) · [上币追踪器](./listing-tracker.md)
