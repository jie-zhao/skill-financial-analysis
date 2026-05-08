# 美国宏观经济指标详解

## 一、增长指标

### 1. GDP（国内生产总值）

**AKShare函数**：
- `macro_usa_gdp_monthly()` - GDP月度数据

**判断要点**：
- 同比增速趋势
- 环比折年率（经济动能）
- 分项贡献：消费、投资、净出口、政府

**美国GDP结构**（2024年参考）：
- 个人消费支出(PCE)：~68%
- 私人投资：~18%
- 政府支出：~17%
- 净出口：-3%（逆差）

### 2. PMI（采购经理指数）

**AKShare函数**：
- `macro_usa_ism_pmi()` - ISM制造业PMI
- `macro_usa_ism_non_pmi()` - ISM非制造业PMI
- `macro_usa_pmi()` - Markit PMI
- `macro_usa_services_pmi()` - 服务业PMI

**判断要点**：
- ISM PMI官方权威
- 50为荣枯线
- 制造业PMI分项：新订单、生产、就业、供应商交货、库存

**关键分项**：
- 新订单：未来需求
- 就业：招聘意愿
- 供应商交货：供应链压力

### 3. 就业指标

**AKShare函数**：
- `macro_usa_non_farm()` - 非农就业（核心！）
- `macro_usa_unemployment_rate()` - 失业率
- `macro_usa_adp_employment()` - ADP就业（非农前瞻）
- `macro_usa_initial_jobless()` - 初请失业金人数
- `macro_usa_lmci()` - 劳动力市场状况指数
- `macro_usa_job_cuts()` - 裁员人数

**判断要点**：

**非农就业**（每月第一周五发布）：
- 新增就业人数（20万+为强劲）
- 私人部门vs政府部门
- 分行业就业结构

**失业率**：
- 自然失业率~4%
- 低于自然率→劳动力市场紧张

**初请失业金**：
- 高频指标（每周）
- <20万=强劲，>25万=走弱

### 4. 零售销售

**AKShare函数**：
- `macro_usa_retail_sales()` - 零售销售
- `macro_usa_personal_spending()` - 个人支出
- `macro_usa_real_consumer_spending()` - 实际消费支出

**判断要点**：
- 消费是美国经济核心引擎
- 同比/环比增速
- 汽车销售（剔除汽车的零售销售更稳定）

### 5. 工业生产

**AKShare函数**：
- `macro_usa_industrial_production()` - 工业生产指数
- `macro_usa_factory_orders()` - 工厂订单
- `macro_usa_durable_goods_orders()` - 耐用品订单

**判断要点**：
- 制造业、矿业、公用事业分项
- 产能利用率（>80%=紧张）

---

## 二、通胀指标

### 1. CPI（消费者价格指数）

**AKShare函数**：
- `macro_usa_cpi_yoy()` - CPI年率
- `macro_usa_cpi_monthly()` - CPI月率
- `macro_usa_core_cpi_monthly()` - 核心CPI

**判断要点**：
- **核心CPI**（剔除食品能源）是关键指标
- 服务通胀vs商品通胀
- 住房通胀（权重最大~33%）

### 2. PCE（个人消费支出物价指数）

**AKShare函数**：
- `macro_usa_core_pce_price()` - 核心PCE（美联储最关注！）

**判断要点**：
- **PCE是美联储官方通胀目标**
- 目标：核心PCE=2%
- PCE比CPI更全面（包含替代效应）

### 3. PPI（生产者价格指数）

**AKShare函数**：
- `macro_usa_ppi()` - PPI
- `macro_usa_core_ppi()` - 核心PPI

**判断要点**：
- PPI向CPI传导
- 生产端成本压力

---

## 三、房地产指标

### 1. 房屋销售

**AKShare函数**：
- `macro_usa_new_home_sales()` - 新屋销售
- `macro_usa_exist_home_sales()` - 成屋销售
- `macro_usa_pending_home_sales()` - 成屋签约销售

**判断要点**：
- 成屋销售占市场~90%
- 新屋销售反映开发商信心
- 利率敏感指标

### 2. 房屋建设

**AKShare函数**：
- `macro_usa_house_starts()` - 新屋开工
- `macro_usa_building_permits()` - 营建许可
- `macro_usa_nahb_house_market_index()` - NAHB房产市场指数

**判断要点**：
- 新屋开工领先指标
- 营建许可反映未来建设意愿

### 3. 房价

**AKShare函数**：
- `macro_usa_house_price_index()` - 房价指数
- `macro_usa_spcs20()` - S&P/Case-Shiller房价指数

---

## 四、货币政策相关指标

### 1. 美联储政策

**判断要点**：
- 联邦基金利率目标区间
- 美联储点阵图（利率预期）
- 缩表规模（量化紧缩）

### 2. 国债收益率

**AKShare函数**：
- `bond_gb_us_sina()` - 美国国债
- `bond_zh_us_rate()` - 中美国债利差

**判断要点**：
- 2年期国债：短期利率预期
- 10年期国债：长期增长和通胀预期
- **收益率曲线倒挂**：衰退信号

---

## 五、消费者与商业信心

**AKShare函数**：
- `macro_usa_cb_consumer_confidence()` - 谘商会消费者信心
- `macro_usa_michigan_consumer_sentiment()` - 密歇根消费者信心
- `macro_usa_nfib_small_business()` - NFIB小企业信心

**判断要点**：
- 消费者信心→消费支出
- 小企业信心→就业（小企业贡献大部分就业）

---

## 六、贸易与财政

### 1. 贸易

**AKShare函数**：
- `macro_usa_trade_balance()` - 贸易差额
- `macro_usa_export_price()` - 出口价格
- `macro_usa_import_price()` - 进口价格

### 2. 财政

**AKShare函数**：
- `macro_usa_current_account()` - 经常账户

---

## 七、数据发布时间表

| 数据类型 | 发布时间 | 发布机构 |
|---------|---------|---------|
| 非农就业 | 每月第一周五 | BLS |
| CPI | 每月13日左右 | BLS |
| PCE | 每月底 | BEA |
| 零售销售 | 每月15日左右 | 商务部 |
| ISM制造业PMI | 每月1日 | ISM |
| ISM非制造业PMI | 每月3日 | ISM |
| FOMC会议 | 每年8次 | 美联储 |
| GDP | 季末月月底 | BEA |

---

## 八、美联储决策框架（双目标制）

```
┌─────────────────────────────────────────┐
│            美联储双目标                   │
├───────────────────┬─────────────────────┤
│   通胀目标         │    就业目标          │
│   核心PCE = 2%     │   最大就业          │
├───────────────────┴─────────────────────┤
│                                         │
│   ┌─────────────────────────────────┐   │
│   │     利率决策矩阵                 │   │
│   │                                 │   │
│   │   通胀↑ + 就业↑ → 加息          │   │
│   │   通胀↓ + 就业↓ → 降息          │   │
│   │   通胀↑ + 就业↓ → 两难          │   │
│   │   通胀↓ + 就业↑ → 维持/观望     │   │
│   │                                 │   │
│   └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```