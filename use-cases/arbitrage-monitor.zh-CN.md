# 场景：跨交易所套利监控

[English](./arbitrage-monitor.en.md) | 中文

---

## 做什么

实时监控多个交易所的资金费率和现货-合约价差，发现套利机会并计算扣除成本后的净收益。

## 架构

```
定时任务（每 5 分钟）
    │
    ├── Surf Data API: 资金费率 (/exchange/funding-rate)
    ├── Surf Data API: 现货价格 (/market/price)
    ├── Surf Chat API: 情绪分析（判断窗口持续时间）
    │
    ▼
  计算净套利空间
    │
    ▼
  Telegram/微信 推送（超过阈值时）
```

## 核心代码

### 1. 拉取资金费率

```python
import requests
from datetime import datetime

class ArbitrageMonitor:
    def __init__(self, api_key):
        self.base_url = "https://api.ask.surf/gateway"
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def get_funding_rates(self, symbols="BTC,ETH,SOL,ARB,DOGE"):
        """获取多币种资金费率"""
        rates = {}
        for symbol in symbols.split(","):
            resp = requests.get(
                f"{self.base_url}/v1/exchange/funding-rate",
                headers=self.headers,
                params={"symbol": symbol.strip()}
            )
            if resp.ok:
                rates[symbol.strip()] = resp.json()
        return rates
```

### 2. 计算套利空间

```python
    def calculate_spread(self, rates):
        """找出资金费率差异最大的机会"""
        opportunities = []
        for symbol, data in rates.items():
            for exchange in ["binance", "okx", "bybit"]:
            try:
                resp = requests.get(
                    f"{self.base_url}/v1/exchange/funding-history",
                    headers=self.headers,
                    params={"pair": f"{symbol}/USDT", "exchange": exchange, "limit": 1}
                )
                if resp.ok:
                    items = resp.json().get("data", [])
                    if items:
                        rates[f"{symbol}_{exchange}"] = {
                            "exchange": exchange,
                            "rate": items[0]["funding_rate"],
                            "timestamp": items[0]["timestamp"]
                        }
            except Exception:
                continue
        
        # 找最大和最小费率的交易所
        if len(rates) >= 2:
            sorted_rates = sorted(rates.values(), key=lambda x: x["rate"])
            spread = sorted_rates[-1]["rate"] - sorted_rates[0]["rate"]
            if spread > 0:
                opportunities.append({
                    "symbol": symbol,
                    "spread": round(spread * 100, 4),  # 转为百分比
                    "long_exchange": sorted_rates[0]["exchange"],
                    "long_rate": round(sorted_rates[0]["rate"] * 100, 4),
                    "short_exchange": sorted_rates[-1]["exchange"],
                    "short_rate": round(sorted_rates[-1]["rate"] * 100, 4),
                })
        return opportunities
```

### 3. 用 Chat API 判断窗口持续时间

```python
    def analyze_window(self, symbol, spread):
        """用 Surf AI 分析套利窗口可能持续多久"""
        resp = requests.post(
            "https://api.asksurf.ai/surf-ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "surf-1.5-instant",
                "messages": [{
                    "role": "user",
                    "content": f"{symbol} 当前资金费率异常（价差 {spread}%），"
                               f"结合当前市场情绪和持仓数据，这个套利窗口大概会持续多久？"
                }],
                "ability": ["market_analysis"],
                "reasoning_effort": "low"
            }
        )
        return resp.json()["choices"][0]["message"]["content"]
```

### 4. 告警推送

```python
    def check_and_alert(self, threshold=0.05):
        """主循环：检查并推送"""
        rates = self.get_funding_rates()
        opportunities = self.calculate_spread(rates)
        
        for opp in opportunities:
            if opp["spread"] > threshold:
                analysis = self.analyze_window(opp["symbol"], opp["spread"])
                # 推送到 Telegram / 微信
                message = (
                    f"🔔 套利机会: {opp['symbol']}\n"
                    f"价差: {opp['spread']}%\n"
                    f"做多: {opp['long_exchange']} ({opp['long_rate']}%)\n"
                    f"做空: {opp['short_exchange']} ({opp['short_rate']}%)\n"
                    f"AI 分析: {analysis[:200]}"
                )
                print(message)  # 替换为实际推送逻辑
```

**资金费率 API 返回格式（已验证）：**

```json
{
  "data": [
    {
      "exchange": "binance",
      "funding_rate": -0.00007398,
      "pair": "BTC/USDT",
      "timestamp": 1775145600
    }
  ],
  "meta": {"credits_used": 1}
}
```

> **注意：** `pair` 格式为 `BTC/USDT`（用 `/` 分隔）。`funding_rate` 是小数，`-0.00007398` = -0.007398%。
**Telegram Bot 推送：**

```python
import requests

def send_telegram(bot_token, chat_id, message):
    requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    )

# 在 check_and_alert 中调用：
# send_telegram(BOT_TOKEN, CHAT_ID, message)
```

## 进阶：用 SQL 做历史回测

```sql
-- 查历史资金费率异常事件
-- Hyperliquid 永续合约数据在 agent.hyperliquid_perp_* 表中
-- 其他交易所资金费率建议用 Data API (exchange-funding-history) 获取

SELECT 
    coin,
    funding_rate,
    block_date
FROM agent.hyperliquid_perp_funding
WHERE abs(funding_rate) > 0.01
  AND block_date >= today() - 30
ORDER BY abs(funding_rate) DESC
LIMIT 20
```

## 部署建议

- **频率：** 每 5 分钟跑一次（资金费率变化不快，不需要秒级）
- **部署：** 用 cron 或 Railway/Vercel 的定时任务
- **成本：** 每次大约消耗 5-10 Credits（取决于查询币种数量）

---

**相关场景：** [上币追踪器](./listing-tracker.md) · [舆情看板](./sentiment-dashboard.md)
