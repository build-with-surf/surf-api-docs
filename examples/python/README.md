<p align="right">
  <a href="./README.md">English</a> | <a href="./README.zh-CN.md">中文</a>
</p>

# Example Scripts

Ready-to-run Python scripts demonstrating practical usage of the Surf API.

## Prerequisites

- Python 3.10+
- [Surf CLI](https://docs.asksurf.ai/cli/introduction) installed (`curl -fsSL https://agent.asksurf.ai/cli/releases/install.sh | sh`)
- No API Key required — scripts call data through the Surf CLI

## Script List

| Script | Function | Data Source |
|--------|----------|------------|
| [market_dashboard.py](market_dashboard.py) | Terminal market dashboard — prices, Fear & Greed Index, DeFi TVL, futures | Market + DeFi + Futures |
| [funding_rate_scanner.py](funding_rate_scanner.py) | Cross-exchange funding rate scanner, finds arbitrage opportunities | Exchange Funding |
| [whale_tracker.py](whale_tracker.py) | Whale wallet cross-chain asset tracking | Wallet |
| [mindshare_monitor.py](mindshare_monitor.py) | Project Twitter Mindshare monitoring with anomaly detection | Social |
| [kol_analyzer.py](kol_analyzer.py) | Batch KOL influence analysis and ranking | Social |

## Running

```bash
# Clone the repo
git clone https://github.com/build-with-surf/surf-api-docs.git
cd surf-api-docs/examples/python

# Run directly (no dependencies to install)
python market_dashboard.py
python funding_rate_scanner.py
python whale_tracker.py
python mindshare_monitor.py
python kol_analyzer.py

# whale_tracker supports custom addresses
python whale_tracker.py vitalik.eth
python whale_tracker.py 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
```

## Sample Output

### market_dashboard.py

```
╔══════════════════════════════════════════════════╗
║         Surf Terminal Market Dashboard           ║
╚══════════════════════════════════════════════════╝
──────────────────────────────────────────────────
  💰 Major Token Prices
──────────────────────────────────────────────────
  #    Token      Price            24h Change  Market Cap
  1    BTC        $83,466.00    🟢  +1.2%   $1,652.3B
  2    ETH        $1,827.00     🔴  -0.5%   $220.4B
  ...
```

## Customization

Each script has configurable parameters at the top (token lists, KOL lists, wallet addresses, etc.) — just edit them directly.

---

<p align="center">
  <sub><a href="https://github.com/build-with-surf">Build with Surf</a> community project</sub>
</p>
