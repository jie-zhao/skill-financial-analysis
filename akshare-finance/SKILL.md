---
name: akshare-finance
description: AKShare财经数据接口库封装，提供股票、期货、期权、基金、外汇、债券、指数、加密货币等金融产品的基本面数据、实时和历史行情数据、衍生数据。
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "pip": ["akshare>=1.12", "pandas>=1.5"] },
        "install":
          [
            {
              "id": "pip-install",
              "kind": "pip",
              "packages": ["akshare>=1.12", "pandas>=1.5"],
              "label": "安装AKShare依赖"
            }
          ]
      }
  }
keywords:
  - 股票
  - 财经
  - 行情
  - 加密货币
  - 宏观经济
  - AKShare
---

# AKShare财经数据技能

## 快速开始

```bash
# 安装依赖
pip install akshare pandas

# 测试安装
python -c "import akshare; print(akshare.__version__)"
```

## 优化版工具

为了解决编码问题和数据结构问题，提供了优化版的分析工具：

```bash
# 使用优化版工具
python scripts/akshare_optimizer.py
```

## 核心功能

### 1. 股票行情

```python
import akshare as ak

# A股实时行情
stock_zh_a_spot_em()  # 东方财富A股

# 股票K线数据
stock_zh_kline(symbol="000001", period="daily", adjust="qfq")

# 港股行情
stock_hk_spot_em()  # 港股实时

# 美股
stock_us_spot()  # 美股实时
```

### 2. 宏观经济

```python
# GDP数据
macro_china_gdp()  # 中国GDP

# CPI通胀
macro_china_cpi()  # 中国CPI

# PMI采购经理指数
macro_china_pmi()  # 中国PMI
```

**优化版宏观经济分析：**

```python
from scripts.akshare_optimizer import AKShareOptimizer

# 创建优化器实例
optimizer = AKShareOptimizer()

# 获取PMI数据（自动处理编码问题）
pmi_data = optimizer.get_safe_macro_data('pmi')

# 分析PMI数据
analysis = optimizer.analyze_pmi_data(pmi_data)

# 生成格式化报告
report = optimizer.format_pmi_report(analysis)
print(report)
```

**便捷函数：**

```python
from scripts.akshare_optimizer import get_pmi_analysis

# 直接获取PMI分析报告
print(get_pmi_analysis())
```

### 3. 加密货币

```python
# 币种列表
crypto_binance_symbols()  # 币安交易对

# 实时价格
crypto_binance_btc_usdt_spot()  # BTC/USDT

# K线数据
crypto_binance_btc_usdt_kline(period="daily")
```

### 4. 外汇贵金属

```python
# 外汇汇率
forex_usd_cny()  # 美元兑人民币

# 贵金属
metals_shibor()  # 上海银行间拆借利率

# 金银价格
metals_gold()  # 国际金价
```

### 5. 财务数据

```python
# 股票基本面
stock_fundamental(symbol="000001")  # 基本面数据

# 估值指标
stock_valuation(symbol="000001")  # PE、PB等

# 盈利能力
stock_profit_em(symbol="000001")
```

## 常用组合

### 投资组合监控

```python
import akshare as ak
import pandas as pd

# 监控自选股
tickers = ["000001", "000002", "600519"]
for ticker in tickers:
    df = ak.stock_zh_kline(symbol=ticker, period="daily", adjust="qfq", start_date="20240101")
    latest = df.iloc[-1]
    print(f"{ticker}: 收盘价={latest['close']}, 涨跌幅={latest['pct_chg']}%")
```

### 市场概览

```python
# A股大盘
index_zh_a_spot()  # 大盘指数

# 涨跌幅排行
stock_zh_a_spot_em()[['代码', '名称', '涨跌幅']].sort_values('涨跌幅', ascending=False)
```

## 注意事项

1. **数据来源**: 公开财经网站，仅用于学术研究
2. **商业风险**: 投资有风险，决策需谨慎
3. **更新频率**: 实时数据可能有延迟
4. **数据验证**: 建议多数据源交叉验证

## 优化特性

### 解决的问题
- **中文编码问题**: 自动检测和修复中文列名编码错误
- **数据结构问题**: 标准化数据格式，确保数据按时间倒序排列
- **健壮性**: 增加错误处理，避免程序因数据问题中断
- **分析功能**: 提供完整的PMI数据分析和报告生成

### 主要功能
- 自动修复中文编码问题
- 标准化宏观数据结构
- 智能数据分析和统计
- 格式化报告生成
- 错误处理和数据验证

### 使用建议
- 优先使用优化版工具 `scripts/akshare_optimizer.py`
- 对于简单的数据获取，可以直接使用原版AKShare函数
- 对于复杂分析，建议使用优化器提供的分析功能

## 输出格式

默认返回Pandas DataFrame，可直接处理：

```python
df = ak.stock_zh_a_spot_em()
print(df.head())  # 查看前5行
print(df.columns)  # 查看列名
df.to_csv("data.csv")  # 保存CSV
```

## 参考文档

- AKShare文档: https://akshare.akfamily.xyz/
- GitHub: https://github.com/akfamily/akshare
