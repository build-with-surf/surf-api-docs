<p align="right">
  <a href="./README.en.md">English</a> | <a href="./README.md">中文</a>
</p>

# 示例脚本

可直接运行的 Python 脚本，展示 Surf API 的实际用法。

## 前提条件

- Python 3.10+
- [Surf CLI](https://docs.asksurf.ai/cli/introduction) 已安装（`curl -fsSL https://agent.asksurf.ai/cli/releases/install.sh | sh`）
- 无需 API Key — 脚本通过 Surf CLI 调用数据

## 脚本列表

| 脚本 | 功能 | 数据源 |
|------|------|--------|
| [market_dashboard.py](market_dashboard.py) | 终端市场仪表盘 — 价格、恐贪指数、DeFi TVL、期货 | Market + DeFi + Futures |
| [multi_wallet_dashboard.py](multi_wallet_dashboard.py) | 多钱包资产总览 — 净值、链分布、标签、DeFi 持仓 | Wallet |
| [funding_rate_scanner.py](funding_rate_scanner.py) | 跨交易所资金费率扫描，发现套利机会 | Exchange Funding |
| [whale_tracker.py](whale_tracker.py) | 巨鲸钱包跨链资产追踪 | Wallet |
| [mindshare_monitor.py](mindshare_monitor.py) | 项目 Twitter Mindshare 监控与异动检测 | Social |
| [kol_analyzer.py](kol_analyzer.py) | KOL 影响力批量分析与排名 | Social |

## 运行

```bash
# 克隆仓库
git clone https://github.com/build-with-surf/surf-api-docs.git
cd surf-api-docs/examples/python

# 直接运行（无需安装依赖）
python market_dashboard.py
python multi_wallet_dashboard.py
python funding_rate_scanner.py
python whale_tracker.py
python mindshare_monitor.py
python kol_analyzer.py

# multi_wallet_dashboard 支持一次传多个地址
python multi_wallet_dashboard.py vitalik.eth 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045

# whale_tracker 支持自定义地址
python whale_tracker.py vitalik.eth
python whale_tracker.py 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
```

## 输出示例

### market_dashboard.py

```
╔══════════════════════════════════════════════════╗
║           Surf 终端市场仪表盘                      ║
╚══════════════════════════════════════════════════╝
──────────────────────────────────────────────────
  💰 主流币价格
──────────────────────────────────────────────────
  #    币种       价格             24h涨跌    市值
  1    BTC        $83,466.00    🟢  +1.2%   $1,652.3B
  2    ETH        $1,827.00     🔴  -0.5%   $220.4B
  ...
```

## 自定义

每个脚本顶部都有可配置的参数（币种列表、KOL 列表、钱包地址等），直接修改即可。

---

<p align="center">
  <sub><a href="https://github.com/build-with-surf">Build with Surf</a> 社区项目</sub>
</p>
