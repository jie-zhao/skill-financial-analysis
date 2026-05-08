# AKShare财经数据技能优化

## 优化概述

基于实际使用中遇到的问题，对akshare-finance技能进行了全面优化，主要解决了以下关键问题：

## 解决的问题

### 1. 中文编码问题
- **问题**: AKShare返回的数据中，中文列名出现乱码（如"��"）
- **解决方案**: 
  - 实现智能编码检测和修复
  - 自动尝试多种编码方式（GBK, UTF-8等）
  - 提供备用的通用列名方案

### 2. 数据结构问题
- **问题**: 数据格式不一致，时间排序混乱，难以直接分析
- **解决方案**:
  - 统一数据格式标准化处理
  - 自动时间排序（最新数据在前）
  - 智能数据类型转换

### 3. 分析功能缺失
- **问题**: 原版只提供数据获取，缺少分析功能
- **解决方案**:
  - 完整的PMI数据分析框架
  - 自动生成分析报告
  - 包含趋势分析、统计特征等

## 优化后的工具

### 核心组件

#### AKShareOptimizer类
主要的优化器类，提供以下功能：

```python
from scripts.akshare_optimizer import AKShareOptimizer

optimizer = AKShareOptimizer()

# 安全获取宏观数据
pmi_data = optimizer.get_safe_macro_data('pmi')
gdp_data = optimizer.get_safe_macro_data('gdp')
cpi_data = optimizer.get_safe_macro_data('cpi')

# 分析PMI数据
analysis = optimizer.analyze_pmi_data(pmi_data)

# 生成格式化报告
report = optimizer.format_pmi_report(analysis)
```

#### 便捷函数
提供一键式分析功能：

```python
from scripts.akshare_optimizer import get_pmi_analysis

# 直接获取PMI分析报告
print(get_pmi_analysis())
```

### 主要功能

#### 数据获取和修复
- 自动修复中文编码问题
- 标准化数据结构
- 错误处理和容错机制

#### PMI分析功能
- 当前制造业和服务业PMI值
- 经济状态判断（扩张/收缩）
- 历史统计特征（均值、最大值、最小值、标准差）
- 月度变化分析
- 近一年数据分析

#### 报告生成
- 格式化中文报告
- 综合经济判断
- 趋势分析

## 使用示例

### 基本使用
```bash
# 直接运行PMI分析
python scripts/akshare_optimizer.py
```

### 编程使用
```python
from scripts.akshare_optimizer import AKShareOptimizer

optimizer = AKShareOptimizer()

# 获取和分析PMI数据
pmi_data = optimizer.get_safe_macro_data('pmi')
analysis = optimizer.analyze_pmi_data(pmi_data)
report = optimizer.format_pmi_report(analysis)

print(report)
```

### 示例脚本
运行完整示例：
```bash
python examples/usage_example.py
```

## 输出示例

```
=== PMI数据分析报告 ===
数据时间: 2026-02-01

【制造业PMI分析】
当前值: 49.0 (收缩)
历史均值: 50.64
历史最高: 59.20
历史最低: 35.70
历史波动: 2.32
月度变化: 上升 0.30
近一年均值: 49.48
近一年波动: 0.47

【服务业PMI分析】
当前值: 49.5 (收缩)
历史均值: 53.95
历史最高: 60.20
历史最低: 29.60
历史波动: 3.25
月度变化: 下降 0.10
近一年均值: 50.09
近一年波动: 0.43

【综合判断】经济全面收缩
```

## 技术特性

### 错误处理
- 全面的异常捕获机制
- 友好的错误提示
- 优雅降级处理

### 性能优化
- 高效的数据处理
- 内存优化
- 快速分析算法

### 扩展性
- 模块化设计
- 易于扩展新的分析功能
- 支持多种数据源

## 文件结构

```
akshare-finance/
├── SKILL.md                    # 技能文档
├── scripts/
│   ├── akshare_optimizer.py   # 核心优化器
│   └── __init__.py            # 包初始化
├── examples/
│   └── usage_example.py       # 使用示例
├── _meta.json                  # 技能元数据
└── references/                # 参考资料
```

## 兼容性

- Python 3.7+
- pandas >= 1.3.0
- akshare >= 1.12.0
- Windows/Linux/macOS

## 更新日志

### v1.1 (优化版)
- 修复中文编码问题
- 添加数据标准化处理
- 实现PMI完整分析功能
- 提供便捷函数和示例脚本
- 增强错误处理机制

### v1.0 (原版)
- 基础AKShare接口封装
- 简单的数据获取功能