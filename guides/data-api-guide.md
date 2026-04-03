# Data API 实战指南

[English](./data-api-guide.en.md) | 中文

---

Data API 提供 83 个 REST 端点，直接返回结构化 JSON — 适合构建看板、监控系统和数据管道。

## 基础信息

| 项目 | 值 |
|------|-----|
| Base URL | `https://api.ask.surf/gateway` |
| 认证 | `Authorization: Bearer <API_KEY>` |
| 分页 | `limit`（默认 20，最大 100）+ `offset` |
| 计费 | 每次调用消耗 Credits，响应里 `meta.credits_used` 显示消耗量 |

## 常用查询模式

### 1. 市场数据

```bash
# 查价格
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/market/price?symbol=BTC"

# 多币种价格
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/market/price?symbol=ETH,SOL,ARB"

# 恐贪指数
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/market/fear-greed"
```

### 2. 交易所数据

```bash
# 资金费率
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/exchange/funding-rate?symbol=BTC"

# K 线数据
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/exchange/candlestick?symbol=ETH&interval=1h"

# 多空比
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/exchange/long-short-ratio?symbol=BTC"
```

### 3. 钱包 & 链上

```bash
# 查钱包余额（支持 ENS）
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/wallet/balance?address=vitalik.eth&chain=ethereum"

# 钱包转账记录
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/wallet/transfers?address=0xdead...&chain=ethereum"
```

### 4. 社交数据

```bash
# Twitter 用户资料
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/social/twitter/profile?q=VitalikButerin"

# 项目 Mindshare
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/social/mindshare?symbol=ETH&time_range=7d"
```

### 5. 预测市场

```bash
# Polymarket 热门市场
curl -H "Authorization: Bearer <key>" \
  "https://api.ask.surf/gateway/v1/prediction/markets?sort_by=volume_24h&order=desc&limit=10"
```

## 参数规范

### 资产标识

| 参数 | 用法 | 示例 |
|------|------|------|
| `symbol` | 大写代号，多个用逗号分隔 | `BTC`, `ETH,SOL` |
| `q` | 自由文本搜索 | `bitcoin` |
| `address` | 链上地址或 ENS | `0xdead...`, `vitalik.eth` |

### 时间 & 聚合

| 参数 | 用法 | 示例 |
|------|------|------|
| `time_range` | 回看窗口 | `7d`, `30d`, `365d`, `max` |
| `interval` | K线/指标间隔 | `1h`, `1d`, `1w` |
| `granularity` | 数据粒度 | `day`, `block`, `hour` |

### 排序 & 过滤

| 参数 | 用法 | 示例 |
|------|------|------|
| `chain` | 链名称（必须用全称） | `ethereum`, `solana`, `base` |
| `sort_by` | 排序字段 | `volume_24h`, `market_cap` |
| `order` | 排序方向 | `asc`, `desc` |

### 支持的链

`ethereum` · `polygon` · `bsc` · `solana` · `avalanche` · `arbitrum` · `optimism` · `fantom` · `base` · `linea` · `cyber`

> **注意：** 不接受缩写（`eth`, `sol`, `matic` 等不行）。

## Python 封装示例

```python
import requests

class SurfDataAPI:
    def __init__(self, api_key):
        self.base_url = "https://api.ask.surf/gateway"
        self.headers = {"Authorization": f"Bearer {api_key}"}
    
    def get(self, path, params=None):
        resp = requests.get(
            f"{self.base_url}{path}",
            headers=self.headers,
            params=params
        )
        resp.raise_for_status()
        return resp.json()
    
    def price(self, symbols):
        return self.get("/v1/market/price", {"symbol": symbols})
    
    def funding_rate(self, symbol):
        return self.get("/v1/exchange/funding-rate", {"symbol": symbol})
    
    def wallet_balance(self, address, chain="ethereum"):
        return self.get("/v1/wallet/balance", {
            "address": address,
            "chain": chain
        })

# 使用
surf = SurfDataAPI("<your-api-key>")
btc_price = surf.price("BTC")
eth_funding = surf.funding_rate("ETH")
```

<!-- TODO(team): 验证以上端点路径是否准确，补充完整的端点列表 -->

## 错误处理

| 状态码 | 含义 | 处理 |
|--------|------|------|
| 400 | 参数错误 | 检查参数名和值 |
| 401 | 未认证 | 检查 API Key |
| 404 | 资源不存在 | 检查 symbol/address 是否正确 |
| 422 | 参数值无效 | 检查 chain 是否用了全称 |
| 429 | 限频 | 降低请求频率 |
| 502 | 上游不可用 | 重试 |

---

**下一步：** 查看 [使用场景](../use-cases/) 了解如何用这些 API 构建实际工具。
