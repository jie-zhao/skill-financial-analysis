# skill-financial-analysis
基于 AKShare 的完整金融数据分析解决方案，包含数据获取和宏观经济分析两个协同工作的技能。

## 📦 包含技能

### 1. akshare-finance - 数据获取层
**功能定位**: 提供全面的金融数据获取能力

- 📈 股票数据：实时行情、历史数据、基本面
- 💰 基金数据：净值、持仓、业绩
- 🏛️ 宏观数据：GDP、PMI、CPI、利率
- 💱 外汇数据：汇率、外汇储备
- 📊 指数数据：股指、行业指数
- 🔗 债券数据：国债、企业债
- ₿ 加密货币：比特币、以太坊等

### 2. macro-economic-analysis - 数据分析层
**功能定位**: 基于数据进行宏观经济分析和决策支持

- 📉 经济周期判断
- 📊 四象限资产配置模型
- 🏦 货币政策分析
- 📈 通胀趋势预测
- 🌍 国际比较分析
- 📋 自动生成分析报告

## 🔄 协同工作流程

```
┌─────────────────────┐
│  akshare-finance    │
│  (数据获取层)       │
│  - 获取GDP数据      │
│  - 获取PMI数据      │
│  - 获取通胀数据     │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ macro-economic-     │
│ analysis            │
│ (数据分析层)        │
│  - 趋势分析         │
│  - 周期判断         │
│  - 生成报告         │
└─────────────────────┘
```

## 🚀 安装使用

### 方式一：直接复制

```powershell
# Windows - 复制到 OpenCode skills 目录
$skillsDir = "$env:USERPROFILE\.config\opencode\skills"

xcopy /E /I "akshare-finance" "$skillsDir\akshare-finance"
xcopy /E /I "macro-economic-analysis" "$skillsDir\macro-economic-analysis"
```

### 方式二：符号链接（推荐）

```powershell
# Windows PowerShell (管理员)
$repoDir = "C:\path\to\opencode-financial-analysis"
$skillsDir = "$env:USERPROFILE\.config\opencode\skills"

New-Item -ItemType SymbolicLink -Path "$skillsDir\akshare-finance" -Target "$repoDir\akshare-finance"
New-Item -ItemType SymbolicLink -Path "$skillsDir\macro-economic-analysis" -Target "$repoDir\macro-economic-analysis"
```

## 📋 使用示例

### 示例 1：获取并分析中国宏观经济数据

**步骤1**: 使用 akshare-finance 获取数据
```
请使用 akshare-finance 获取中国近5年的 GDP 和 PMI 数据
```

**步骤2**: 使用 macro-economic-analysis 进行分析
```
请分析当前的宏观经济周期阶段，并给出资产配置建议
```

### 示例 2：生成经济分析报告

```
请基于最新的经济数据，生成一份完整的宏观经济分析报告，包含：
1. 当前经济周期判断
2. 通胀趋势分析
3. 货币政策展望
4. 资产配置建议
```

## 📁 目录结构

```
opencode-financial-analysis/
├── akshare-finance/
│   ├── SKILL.md              # 技能定义文件
│   ├── OPTIMIZATION.md       # 优化说明
│   ├── scripts/              # Python 脚本
│   │   ├── akshare_optimizer.py
│   │   ├── stock_price.py
│   │   ├── macro_data.py
│   │   └── crypto_price.py
│   ├── examples/             # 使用示例
│   └── references/           # 参考资料
│       └── README.md
│
├── macro-economic-analysis/
│   ├── SKILL.md              # 技能定义文件
│   ├── scripts/              # Python 脚本
│   │   ├── quadrant_analyzer.py
│   │   ├── report_generator.py
│   │   └── dashboard_generator.py
│   └── references/           # 参考资料
│       ├── analysis-templates.md
│       ├── china-indicators.md
│       └── usa-indicators.md
│
└── README.md                 # 本文件
```

## ⚙️ 系统要求

- Python >= 3.8
- OpenCode 最新版本
- 依赖包：
  - akshare >= 1.12
  - pandas >= 1.5
  - numpy
  - matplotlib
  - requests

## 🔄 更新日志

### v1.0.0 (2024-01-XX)
- ✨ 初始版本发布
- 📈 集成 akshare-finance 技能
- 📊 集成 macro-economic-analysis 技能
- 🔄 建立技能协同机制

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🔗 相关链接

- [AKShare 官方文档](https://www.akshare.xyz/)
