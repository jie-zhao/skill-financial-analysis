# 中国宏观经济指标详解

## 一、增长指标

### 1. GDP（国内生产总值）

**AKShare函数**：
- `macro_china_gdp()` - 东方财富详细数据
- `macro_china_gdp_yearly()` - 金十数据年率

**判断要点**：
- 同比增速趋势方向
- 季度环比折年率（经济动能）
- 三次产业结构变化

**数据频率**：季度

### 2. PMI（采购经理指数）

**AKShare函数**：
- `macro_china_pmi_yearly()` - 官方制造业PMI
- `macro_china_non_man_pmi()` - 官方非制造业PMI
- `macro_china_cx_pmi_yearly()` - 财新制造业PMI
- `macro_china_cx_services_pmi_yearly()` - 财新服务业PMI

**判断要点**：
- **50为荣枯线**：>50扩张，<50收缩
- 官方PMI覆盖大中型企业，财新PMI偏向中小企业
- 制造业PMI分项：新订单、新出口订单、生产、从业人员、原材料库存

**数据频率**：月度（每月最后一天公布）

### 3. 工业增加值

**AKShare函数**：
- `macro_china_industrial_production_yoy()` - 金十年率数据
- `macro_china_gyzjz()` - 东方财富详细数据

**判断要点**：
- 同比增速反映工业生产活跃度
- 分行业看：高技术制造业vs传统制造业
- 累计增速vs当月增速

**数据频率**：月度（每月15日左右公布）

### 4. 社会消费品零售总额

**AKShare函数**：
- `macro_china_consumer_goods_retail()`

**判断要点**：
- 同比增速反映消费端强弱
- 线上vs线下消费结构
- 商品零售vs餐饮服务
- 汽车消费（消费大头）单独关注

**数据频率**：月度

### 5. 固定资产投资

**AKShare函数**：
- `macro_china_gdzctz()`

**判断要点**：
- 分项结构：制造业投资、基建投资、房地产开发投资
- 增速变化反映投资意愿
- 民间投资vs国有投资（信心差异）

**数据频率**：月度

### 6. 失业率

**AKShare函数**：
- `macro_china_urban_unemployment()`

**判断要点**：
- 城镇调查失业率（官方核心指标）
- 16-24岁青年失业率（敏感指标）
- 31个大城市城镇调查失业率

**数据频率**：月度

---

## 二、通胀指标

### 1. CPI（居民消费价格指数）

**AKShare函数**：
- `macro_china_cpi_yearly()` - 年率
- `macro_china_cpi_monthly()` - 月率
- `macro_china_cpi()` - 东方财富详细数据

**判断要点**：
- **同比**：反映物价总体水平变化
- **环比**：反映短期动态
- **核心CPI**（剔除食品能源）：更准确反映趋势
- 食品项（尤其猪肉）是中国CPI波动主因

**中国CPI权重（参考）**：
- 食品烟酒：~30%
- 居住：~20%
- 教育文化娱乐：~14%
- 交通通信：~13%

### 2. PPI（工业生产者出厂价格指数）

**AKShare函数**：
- `macro_china_ppi_yearly()` - 年率
- `macro_china_ppi()` - 东方财富详细数据

**判断要点**：
- 反映企业端成本和利润压力
- PPI上行→工业企业利润改善
- PPI下行→工业通缩压力
- 生产资料vs生活资料分项

**与CPI关系**：
- PPI领先CPI约3-6个月
- PPI向CPI传导效率反映需求强度

### 3. 企业商品价格指数

**AKShare函数**：
- `macro_china_qyspjg()`

**判断要点**：
- 央行编制，反映企业间商品交易价格
- 分项：农产品、矿产品、煤油电

---

## 三、金融指标

### 1. 货币供应量

**AKShare函数**：
- `macro_china_money_supply()` - M0/M1/M2
- `macro_china_m2_yearly()` - M2年率
- `macro_china_supply_of_money()` - 补充数据

**判断要点**：
- **M0**：流通中现金
- **M1** = M0 + 企业活期存款（交易活跃度）
- **M2** = M1 + 定期存款 + 居民储蓄（总购买力）

**M1-M2剪刀差**：
- M1增速 > M2增速：经济活跃，企业投资意愿强
- M1增速 < M2增速：经济保守，资金沉淀

### 2. 社会融资规模

**AKShare函数**：
- `macro_china_shrzgm()` - 社融增量统计

**判断要点**：
- **核心信用指标**（中国特色！）
- 社融增量反映信用扩张力度
- 分项结构：人民币贷款、信托贷款、债券融资、股票融资
- **关注**：中长期贷款占比（实体需求）

**传导链条**：
```
政策 → 银行信用扩张 → 社融增加 → 投资开工 → 就业消费 → 经济增长
```

### 3. 利率指标

**AKShare函数**：
- `macro_china_lpr()` - LPR利率
- `macro_china_shibor_all()` - Shibor利率
- `rate_interbank()` - 银行间利率
- `repo_rate_hist()` - 回购利率

**判断要点**：
- **LPR**：贷款市场报价利率，政策传导
- **Shibor**：上海银行间同业拆放利率
- **DR007**：7天银行间质押式回购利率（流动性水温计）
  - DR007↑ = 钱紧
  - DR007↓ = 钱松

### 4. 存款准备金率

**AKShare函数**：
- `macro_china_reserve_requirement_ratio()`

**判断要点**：
- 降准→释放流动性→信用扩张
- 大型金融机构vs中小金融机构差异

### 5. 汇率与外储

**AKShare函数**：
- `macro_china_rmb()` - 人民币汇率
- `macro_china_fx_reserves_yearly()` - 外汇储备
- `macro_china_fx_gold()` - 外汇和黄金储备
- `currency_boc_sina()` - 中行汇率

**判断要点**：
- 汇率稳定是外部约束
- 外储规模反映国际支付能力
- 中美利差影响资金流向

---

## 四、地产指标

### 1. 房地产开发投资

**AKShare函数**：
- `macro_china_real_estate()`

**判断要点**：
- 开发投资增速
- 新开工面积增速
- 销售面积/销售额增速
- 到位资金结构

### 2. 房价

**AKShare函数**：
- `macro_china_new_house_price()`

**判断要点**：
- 70城房价指数
- 一线vs二三线分化
- 同比vs环比

**地产链条**：
```
销售回暖 → 开发投资 → 新开工 → 施工 → 地方财政 → 银行信用
```

---

## 五、贸易指标

### 1. 进出口

**AKShare函数**：
- `macro_china_exports_yoy()` - 出口年率
- `macro_china_imports_yoy()` - 进口年率
- `macro_china_trade_balance()` - 贸易差额
- `macro_china_hgjck()` - 海关进出口详细数据

**判断要点**：
- 出口反映外需
- 进口反映内需
- 贸易顺差影响外汇储备

### 2. 外商直接投资

**AKShare函数**：
- `macro_china_fdi()`

---

## 六、其他重要指标

### 1. 宏观杠杆率

**AKShare函数**：
- `macro_cnbs()` - 国家金融与发展实验室数据

**判断要点**：
- 居民部门杠杆率
- 非金融企业部门杠杆率
- 政府部门杠杆率（中央+地方）

### 2. 财政收支

**AKShare函数**：
- `macro_china_czsr()` - 财政收支
- `macro_china_national_tax_receipts()` - 国税收入

### 3. 用电量

**AKShare函数**：
- `macro_china_society_electricity()`

**判断要点**：
- 高频指标，验证工业生产
- 分产业用电结构

---

## 七、数据发布时间表

| 数据类型 | 发布时间 | 发布机构 |
|---------|---------|---------|
| PMI | 每月最后一天/次月1日 | 国家统计局 |
| CPI/PPI | 次月9-10日 | 国家统计局 |
| 工业增加值 | 次月15日左右 | 国家统计局 |
| 社融/M2 | 次月10-15日 | 央行 |
| GDP | 季后15日左右 | 国家统计局 |
| 进出口 | 次月7-8日 | 海关总署 |
| 外储 | 欏月7日左右 | 央行 |