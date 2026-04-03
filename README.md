<p align="right">
  <a href="./README.en.md">English</a> | <a href="./README.md">中文</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/build-with-surf/.github/main/assets/surf-logo.jpg" width="60" alt="Surf" />
</p>

<h1 align="center">Surf API 知识库</h1>

<p align="center">
  社区维护的 <a href="https://asksurf.ai">Surf</a> 教程、指南和最佳实践<br/>
  官方文档：<a href="https://docs.asksurf.ai">docs.asksurf.ai</a>
</p>

---

## 目录

### 入门

| 文档 | 说明 |
|------|------|
| [Surf 是什么？](getting-started/what-is-surf.md) | 产品介绍、能力对比、数据覆盖 |
| [快速开始](getting-started/quickstart.md) | 5 分钟跑通：Skill / CLI / Chat API / Data API / SQL |

### 实战指南

| 文档 | 说明 |
|------|------|
| [Chat API 实战](guides/chat-api-guide.md) | 模型选择、ability 参数、流式输出、从 OpenAI 迁移 |
| [Data API 实战](guides/data-api-guide.md) | 83 个端点速查、参数规范、Python 封装 |

### 使用场景

| 文档 | 说明 |
|------|------|
| [跨交易所套利监控](use-cases/arbitrage-monitor.md) | 资金费率追踪 + AI 窗口分析 + 告警推送 |
| [舆情 × 链上联动看板](use-cases/sentiment-dashboard.md) | Twitter 情绪 vs 链上数据背离检测 |
| [新币上线追踪器](use-cases/listing-tracker.md) | 上线表现追踪 + KOL 站队分析 |

### 参考

| 文档 | 说明 |
|------|------|
| [FAQ](faq.md) | 常见问题：模型选择、计费、数据延迟、错误处理 |

## 仓库结构

```
surf-api-docs/
├── getting-started/
│   ├── what-is-surf.md          # Surf 是什么
│   └── quickstart.md            # 快速开始
├── guides/
│   ├── chat-api-guide.md        # Chat API 实战
│   └── data-api-guide.md        # Data API 实战
├── use-cases/
│   ├── arbitrage-monitor.md     # 套利监控
│   ├── sentiment-dashboard.md   # 舆情看板
│   └── listing-tracker.md       # 上币追踪
└── faq.md                       # 常见问题
```

## 标记说明

文档中的 `<!-- TODO(team) -->` 标记表示需要团队补充的内容，通常是：
- 实际 API 返回格式的截图或示例
- 具体的 Credit 消耗数值
- 产品操作流程截图
- 需要实际测试验证的代码

## 贡献

1. Fork 这个仓库
2. 写教程或修正错误
3. 提交 Pull Request

**写作规范：**
- 中文为主，技术术语保留英文
- 包含可运行的代码示例
- 标注难度等级
- 需要团队补充的地方用 `<!-- TODO(team) -->` 标记

---

<p align="center">
  <sub><a href="https://github.com/build-with-surf">Build with Surf</a> 社区项目</sub>
</p>
