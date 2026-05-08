#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宏观经济深度分析报告生成器 - 专业版 (Macro Economic Report Generator - Professional Edition)
基于AKShare获取实时宏观数据，运用内置逻辑引擎生成机构级专业宏观经济分析报告。

包含：增长分析、通胀分析、金融条件、需求分解、政策研判、市场验证、风险清单、资产配置建议。

使用方法:
    python report_generator.py --country china
    python report_generator.py --country usa
"""

import akshare as ak
import pandas as pd
import numpy as np
import argparse
import sys
import io
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class DataFetcher:
    """宏观经济数据获取器"""
    
    def __init__(self):
        self.cache = {}
        self.errors = []
    
    def safe_fetch(self, func, name: str, *args, **kwargs) -> Optional[pd.DataFrame]:
        if name in self.cache:
            return self.cache[name]
        try:
            result = func(*args, **kwargs)
            self.cache[name] = result
            return result
        except Exception as e:
            self.errors.append(f"{name}: {str(e)[:50]}")
            return None
    
    @staticmethod
    def safe_float(val, default=0.0):
        try:
            v = float(val)
            return default if math.isnan(v) else v
        except:
            return default
    
    def get_latest(self, df: Optional[pd.DataFrame], val_col: str = '今值', date_col: str = '日期') -> Tuple[Any, Any, Any, Any]:
        if df is None or len(df) == 0:
            return None, None, None, None
        try:
            latest = df.iloc[-1]
            prev = df.iloc[-2] if len(df) > 1 else df.iloc[-1]
            prev3 = df.iloc[-4] if len(df) > 3 else df.iloc[0]
            prev12 = df.iloc[-13] if len(df) > 12 else df.iloc[0]
            return (
                self.safe_float(latest.get(val_col)),
                latest.get(date_col, ''),
                self.safe_float(prev.get(val_col)),
                self.safe_float(prev12.get(val_col))
            )
        except:
            return None, None, None, None

class MacroJudgmentEngine:
    """宏观逻辑判定引擎"""
    
    @staticmethod
    def judge_growth(pmi: float, pmi_prev: float, ind_yoy: float, gdp: float) -> Tuple[str, str, str]:
        if pmi >= 52 and ind_yoy >= 6.0:
            return "强劲复苏", "增长动能充沛，制造业景气度显著高于荣枯线，工业生产活跃度强劲。", "↗️ 上行"
        elif pmi >= 50 and ind_yoy >= 5.0:
            return "温和扩张", "经济处于扩张区间，但动能相对温和，需关注持续性。", "↗️ 温和上行"
        elif pmi >= 50 and ind_yoy < 5.0:
            return "弱复苏", "制造业重返扩张但工业生产跟进不足，存在'景气回升、实体偏冷'的分化。", "→ 震荡"
        elif pmi < 50 and pmi > pmi_prev:
            return "边际改善", "制造业仍处收缩区间但景气度环比回升，下行压力边际缓解，筑底信号初现。", "↘️ 下行趋缓"
        elif pmi < 48:
            return "深度收缩", "制造业景气度显著低于荣枯线，经济动能明显偏弱，内生需求亟待提振。", "↘️ 下行"
        else:
            return "弱势震荡", "经济在收缩区间徘徊，缺乏明确方向，等待政策或外需的催化。", "→ 震荡"
    
    @staticmethod
    def judge_inflation(cpi: float, ppi: float, cpi_prev: float, ppi_prev: float) -> Tuple[str, str, str]:
        trend = ""
        if cpi > cpi_prev + 0.5:
            trend += "CPI加速上行 "
        elif cpi < cpi_prev - 0.5:
            trend += "CPI持续回落 "
        else:
            trend += "CPI低位运行 "
        
        if cpi > 3.0 and ppi > 3.0:
            return "全面通胀", f"消费端与工业端价格同步快速上行，{trend}，全面通胀压力显著。", "↗️ 上行压力"
        elif cpi > 2.0:
            return "温和通胀", f"消费端通胀温和，{trend}，物价水平整体可控。", "→ 温和"
        elif cpi < 0 and ppi < 0:
            return "类通缩", f"消费端与工业端价格双降，{trend}，有效需求不足的矛盾突出，类通缩特征明显。", "↘️ 下行压力"
        elif cpi > 0 and cpi < 1.0 and ppi < 0:
            return "结构性分化", f"消费端价格平稳，但工业端持续通缩，{trend}，上游成本坍塌或需求疲软。", "→ 分化"
        elif cpi < 0 and ppi > 0:
            return "输入型压力", f"消费端通缩但工业端价格上涨，{trend}，可能受大宗商品或汇率因素影响。", "↗️ 结构性"
        else:
            return "价格平稳", f"通胀指标保持低位运行，{trend}，未对宏观政策形成掣肘。", "→ 平稳"
    
    @staticmethod
    def judge_credit(m2: float, m2_prev: float, m2_yoy: float) -> Tuple[str, str]:
        m2_trend = "上升" if m2 > m2_prev else "回落"
        if m2_yoy >= 10.0:
            return "宽货币", f"M2增速维持在{m2_yoy:.1f}%的高位，流动性充裕，广义货币投放积极。"
        elif m2_yoy >= 8.0:
            return "中性偏松", f"M2增速{m2_yoy:.1f}%，流动性水平适中，环比{m2_trend}。"
        else:
            return "偏紧", f"M2增速{m2_yoy:.1f}%，流动性投放相对克制，货币环境偏紧。"
    
    @staticmethod
    def judge_policy_space(cpi: float, ppi: float, unemployment: float, fx_stability: bool) -> Tuple[str, List[str]]:
        constraints = []
        space = "充足"
        
        if cpi > 3.0:
            constraints.append("通胀压力制约宽松空间")
            space = "受限"
        if unemployment > 6.0:
            constraints.append("就业压力要求政策加力")
        if not fx_stability:
            constraints.append("汇率波动制约外部空间")
        if ppi < -3.0:
            constraints.append("工业通缩需要政策对冲")
        
        if not constraints:
            constraints.append("无明显掣肘，政策空间充裕")
        
        return space, constraints
    
    @staticmethod
    def check_consistency(growth: str, inflation: str, credit: str) -> List[str]:
        warnings = []
        if "扩张" in growth or "复苏" in growth:
            if "通缩" in inflation or "下行" in inflation:
                warnings.append("⚠️ 【交叉预警】增长回升但价格走弱，需求修复的持续性存疑，可能存在'无通胀复苏'特征。")
        if "收缩" in growth or "弱势" in growth:
            if "宽货币" in credit:
                warnings.append("⚠️ 【交叉预警】经济动能偏弱但流动性充裕，资金可能淤积在金融体系，宽货币向宽信用传导不畅。")
        if "通胀" in inflation:
            if "宽货币" in credit:
                warnings.append("⚠️ 【交叉预警】通胀压力上升伴随宽货币环境，需警惕通胀预期自我强化。")
        return warnings

class ReportGenerator:
    """专业宏观报告生成器"""
    
    def __init__(self):
        self.fetcher = DataFetcher()
        self.engine = MacroJudgmentEngine()
        self.data = {}
    
    def fetch_china_data(self):
        """获取中国宏观经济数据"""
        print("正在获取宏观经济数据...")
        
        self.data['pmi_mfg'] = self.fetcher.safe_fetch(ak.macro_china_pmi_yearly, "制造业PMI")
        self.data['pmi_non_mfg'] = self.fetcher.safe_fetch(ak.macro_china_non_man_pmi, "非制造业PMI")
        self.data['gdp'] = self.fetcher.safe_fetch(ak.macro_china_gdp_yearly, "GDP年率")
        self.data['ind_prod'] = self.fetcher.safe_fetch(ak.macro_china_industrial_production_yoy, "工业增加值")
        self.data['retail'] = self.fetcher.safe_fetch(ak.macro_china_consumer_goods_retail, "社会消费品零售")
        self.data['fixed_inv'] = self.fetcher.safe_fetch(ak.macro_china_gdzctz, "固定资产投资")
        self.data['exports'] = self.fetcher.safe_fetch(ak.macro_china_exports_yoy, "出口年率")
        self.data['imports'] = self.fetcher.safe_fetch(ak.macro_china_imports_yoy, "进口年率")
        self.data['cpi'] = self.fetcher.safe_fetch(ak.macro_china_cpi_yearly, "CPI年率")
        self.data['ppi'] = self.fetcher.safe_fetch(ak.macro_china_ppi_yearly, "PPI年率")
        self.data['m2'] = self.fetcher.safe_fetch(ak.macro_china_m2_yearly, "M2年率")
        self.data['m2_supply'] = self.fetcher.safe_fetch(ak.macro_china_money_supply, "货币供应量")
        self.data['shrz'] = self.fetcher.safe_fetch(ak.macro_china_shrzgm, "社融增量")
        self.data['lpr'] = self.fetcher.safe_fetch(ak.macro_china_lpr, "LPR利率")
        self.data['unemployment'] = self.fetcher.safe_fetch(ak.macro_china_urban_unemployment, "城镇失业率")
        self.data['real_estate'] = self.fetcher.safe_fetch(ak.macro_china_real_estate, "房地产")
        self.data['house_price'] = self.fetcher.safe_fetch(ak.macro_china_new_house_price, "房价指数")
        self.data['fx_reserve'] = self.fetcher.safe_fetch(ak.macro_china_fx_reserves_yearly, "外汇储备")
        self.data['rmb'] = self.fetcher.safe_fetch(ak.macro_china_rmb, "人民币汇率")
        
        print(f"数据获取完成，成功{len(self.fetcher.cache)}项，失败{len(self.fetcher.errors)}项")
    
    def generate_china_report(self) -> str:
        """生成中国宏观经济深度分析报告"""
        self.fetch_china_data()
        
        pmi, pmi_date, pmi_prev, pmi_yoy = self.fetcher.get_latest(self.data.get('pmi_mfg'))
        pmi_non, _, pmi_non_prev, _ = self.fetcher.get_latest(self.data.get('pmi_non_mfg'))
        gdp, _, _, _ = self.fetcher.get_latest(self.data.get('gdp'))
        ind, ind_date, _, _ = self.fetcher.get_latest(self.data.get('ind_prod'))
        retail, retail_date, _, _ = self.fetcher.get_latest(self.data.get('retail'))
        exports, exports_date, _, _ = self.fetcher.get_latest(self.data.get('exports'))
        imports, imports_date, _, _ = self.fetcher.get_latest(self.data.get('imports'))
        cpi, cpi_date, cpi_prev, _ = self.fetcher.get_latest(self.data.get('cpi'))
        ppi, ppi_date, ppi_prev, _ = self.fetcher.get_latest(self.data.get('ppi'))
        m2, m2_date, m2_prev, _ = self.fetcher.get_latest(self.data.get('m2'))
        unemployment, _, _, _ = self.fetcher.get_latest(self.data.get('unemployment'))
        lpr_df = self.data.get('lpr')
        lpr_1y, lpr_5y = None, None
        if lpr_df is not None and len(lpr_df) > 0:
            lpr_latest = lpr_df.iloc[-1]
            lpr_1y = self.fetcher.safe_float(lpr_latest.get('LPR1Y'), 3.0)
            lpr_5y = self.fetcher.safe_float(lpr_latest.get('LPR5Y'), 3.5)
        
        pmi = pmi or 49.5
        pmi_prev = pmi_prev or 49.5
        pmi_non = pmi_non or 50.0
        gdp = gdp or 5.0
        ind = ind or 5.0
        cpi = cpi or 0.0
        cpi_prev = cpi_prev or 0.0
        ppi = ppi or 0.0
        ppi_prev = ppi_prev or 0.0
        m2 = m2 or 8.0
        m2_prev = m2_prev or 8.0
        unemployment = unemployment or 5.2
        lpr_1y = lpr_1y or 3.0
        lpr_5y = lpr_5y or 3.5
        
        growth_status, growth_narrative, growth_trend = self.engine.judge_growth(pmi, pmi_prev, ind, gdp)
        inf_status, inf_narrative, inf_trend = self.engine.judge_inflation(cpi, ppi, cpi_prev, ppi_prev)
        credit_status, credit_narrative = self.engine.judge_credit(m2, m2_prev, m2)
        policy_space, policy_constraints = self.engine.judge_policy_space(cpi, ppi, unemployment, True)
        consistency_warnings = self.engine.check_consistency(growth_status, inf_status, credit_status)
        
        quadrant = 4
        quad_name = "衰退/通缩"
        quad_policy = "全面宽松"
        quad_asset = "债券占优"
        if "强劲" in growth_status or "温和" in growth_status or "扩张" in growth_status:
            if "通胀" in inf_status:
                quadrant = 2
                quad_name = "过热"
                quad_policy = "收紧"
                quad_asset = "大宗商品占优"
            else:
                quadrant = 1
                quad_name = "复苏"
                quad_policy = "温和宽松"
                quad_asset = "股票占优"
        elif "改善" in growth_status or "震荡" in growth_status:
            if "通胀" in inf_status:
                quadrant = 3
                quad_name = "滞胀"
                quad_policy = "两难"
                quad_asset = "现金/黄金占优"
            else:
                quadrant = 4
                quad_name = "衰退/通缩"
                quad_policy = "全面宽松"
                quad_asset = "债券占优"
        
        year = datetime.now().year
        report = f"""
# {year-1}年中国宏观经济分析及{year}年经济预测报告

<br>

<div style="text-align: center;">

**报告类型：宏观经济年度分析报告**

**发布日期：{datetime.now().strftime('%Y年%m月%d日')}**

**研究机构：宏观经济研究部**

</div>

<br>
<br>
<br>

---

## 目录

**一、执行摘要** .................................................. 1

**二、宏观经济运行分析** ........................................ 2

> 2.1 经济增长分析 ................................................ 2
> 
> 2.2 通货膨胀分析 ................................................ 3
> 
> 2.3 金融条件分析 ................................................ 4
> 
> 2.4 需求结构分析 ................................................ 5

**三、宏观经济周期定位** ........................................ 6

**四、政策研判** .................................................... 7

**五、风险评估** .................................................... 8

**六、资产配置建议** .............................................. 9

**附录：主要数据附表** .......................................... 10

---

<br>
<br>

## 一、执行摘要

### 研究背景

{year-1}年是中国经济发展的重要一年，面对复杂多变的国内外经济环境，本报告旨在系统分析{year-1}年宏观经济运行态势，并对{year}年经济走势进行预测，为政策制定和投资决策提供参考依据。

### 核心结论

**（一）经济增长方面**：{year-1}年国内生产总值同比增长{gdp:.1f}%，经济呈现{growth_status}态势。

**（二）通胀形势方面**：CPI同比{cpi:.1f}%，PPI同比{ppi:.1f}%，价格体系呈现{inf_status}特征。

**（三）需求结构方面**：经济增长呈现{"出口强、内需弱" if exports and exports > 5 else "内需温和复苏"}特征。

**（四）金融条件方面**：M2增速{m2:.1f}%，信用环境为{credit_status}。

**（五）周期定位方面**：当前经济处于第{quadrant}象限（{quad_name}期），政策空间{policy_space}。

### 主要风险提示

本报告识别出三类主要风险：一是外部贸易摩擦升级风险；二是房地产调整深化风险；三是通缩预期固化风险。

---

<br>

## 二、宏观经济运行分析

### 2.1 经济增长分析

#### 2.1.1 总体态势

根据国家统计局公布数据，{year-1}年全年国内生产总值保持稳定增长，经济运行总体平稳。

**表2-1 {year-1}年GDP增长情况**

| 指标 | 数值 | 判断 |
|:---:|:---:|:---:|
| GDP增速 | {gdp:.1f}% | {'强劲' if gdp >= 5.5 else '稳健' if gdp >= 4.5 else '承压'} |
| 制造业PMI | {pmi:.1f} | {'扩张' if pmi >= 50 else '收缩'} |
| 非制造业PMI | {pmi_non:.1f} | {'扩张' if pmi_non >= 50 else '收缩'} |
| 工业增加值 | {ind:.1f}% | {'强劲' if ind >= 6 else '温和'} |

数据来源：国家统计局

#### 2.1.2 季度走势

经济增速呈现{'逐季回升' if pmi > pmi_prev else '前高后低'}态势，制造业PMI较前值{'上升' if pmi > pmi_prev else '下降'}{abs(pmi-pmi_prev):.1f}个百分点。

#### 2.1.3 生产端分析

**制造业景气度**：PMI录得{pmi:.1f}，{'处于扩张区间，显示制造业景气度较好' if pmi >= 50 else '处于收缩区间，制造业景气度偏弱'}。

**工业生产**：工业增加值同比增长{ind:.1f}%，{'显示工业生产活跃' if ind >= 5 else '工业生产相对温和'}。

#### 2.1.4 就业形势

城镇调查失业率为{unemployment:.1f}%，{'处于正常区间' if unemployment < 5.5 else '就业压力值得关注'}。

### 2.2 通货膨胀分析

#### 2.2.1 物价总体水平

**表2-2 {year-1}年主要物价指标**

| 指标 | 数值 | 判断 |
|:---:|:---:|:---:|
| CPI同比 | {cpi:.1f}% | {'通胀压力' if cpi > 2 else '温和' if cpi > 0 else '通缩压力'} |
| PPI同比 | {ppi:.1f}% | {'工业通胀' if ppi > 0 else '工业通缩'} |

数据来源：国家统计局

#### 2.2.2 通胀结构分析

{inf_narrative}

### 2.3 金融条件分析

#### 2.3.1 货币供应

**表2-3 {year-1}年主要金融指标**

| 指标 | 数值 | 判断 |
|:---:|:---:|:---:|
| M2增速 | {m2:.1f}% | {'宽货币' if m2 >= 10 else '中性'} |
| LPR(1年) | {lpr_1y:.2f}% | 利率水平 |
| LPR(5年) | {lpr_5y:.2f}% | 房贷参考利率 |

数据来源：中国人民银行

{credit_narrative}

### 2.4 需求结构分析

#### 2.4.1 三驾马车仪表盘

**表2-4 {year-1}年需求结构分析**

| 分项 | 指标 | 数值 | 判断 |
|:---:|:---:|:---:|:---:|
| 消费 | 社零增速 | {retail:.1f}% if retail else 'N/A' | {'强劲' if retail and retail >= 6 else '温和'} |
| 出口 | 出口增速 | {exports:.1f}% if exports else 'N/A' | {'强劲' if exports and exports >= 10 else '稳健'} |
| 进口 | 进口增速 | {imports:.1f}% if imports else 'N/A' | {'内需旺盛' if imports and imports >= 5 else '内需偏弱'} |

数据来源：国家统计局、海关总署

---

<br>

## 三、宏观经济周期定位

### 3.1 增长-通胀四象限分析

**图3-1 增长-通胀四象限模型**

```
                           通胀上行
                             ↑
         ② 过热                  ③ 滞胀
         政策：收紧                政策：两难
         配置：大宗商品             配置：现金/黄金
                                  
增长放缓 ←──────────────────────────────────→ 增长强劲
                                  
         ④ 衰退/通缩               ① 复苏
         政策：全面宽松             政策：温和宽松
         配置：债券                 配置：股票
                             ↓
                           通胀下行
```

### 3.2 周期定位结论

**当前位置：第{quadrant}象限（{quad_name}期）**

**判断依据：**

（1）增长维度：GDP增速{gdp:.1f}%，{growth_status}；
（2）通胀维度：CPI为{cpi:.1f}%，{inf_status}；
（3）政策空间：{policy_space}。

---

<br>

## 四、政策研判

### 4.1 货币政策研判

**当前立场**：{'宽松' if m2 >= 10 and lpr_1y < 3.5 else '中性偏松' if m2 >= 8 else '中性'}

**政策空间**：{policy_space}

**下一步预判**：
"""
        
        for i, constraint in enumerate(policy_constraints, 1):
            report += f"\n{i}. {constraint}"
        
        report += f"""

### 1.3 核心结论

> 当前中国经济处于**{quad_name}**象限。制造业PMI为{pmi:.1f}，{'处于扩张区间' if pmi >= 50 else '处于收缩区间'}；
> CPI同比{cpi:.1f}%，PPI同比{ppi:.1f}%，价格体系呈现**{inf_status}**特征；
> M2增速{m2:.1f}%，信用环境为**{credit_status}**。
> 
> **政策预判**：在{quad_policy}基调下，重点关注财政发力节奏与货币政策传导效率。
> **资产配置**：{quad_asset}。

"""
        
        if consistency_warnings:
            report += "### 1.4 交叉验证预警\n\n"
            for warning in consistency_warnings:
                report += f"{warning}\n\n"
        
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 二、增长端分析 (Growth Analysis)

### 2.1 增长仪表盘

| 指标 | 当前值 | 前值 | 变化 | 判断 |
|------|--------|------|------|------|
| **GDP年率** | {gdp:.1f}% | — | — | {'强劲' if gdp >= 5.5 else '稳健' if gdp >= 4.5 else '承压'} |
| **制造业PMI** | {pmi:.1f} | {pmi_prev:.1f} | {'+' if pmi > pmi_prev else ''}{pmi-pmi_prev:.1f} | {'扩张' if pmi >= 50 else '收缩'} |
| **非制造业PMI** | {pmi_non:.1f} | {pmi_non_prev:.1f} | {'+' if pmi_non > pmi_non_prev else ''}{pmi_non-pmi_non_prev:.1f} | {'扩张' if pmi_non >= 50 else '收缩'} |
| **工业增加值** | {ind:.1f}% | — | — | {'强劲' if ind >= 6 else '温和' if ind >= 4 else '偏弱'} |
| **失业率** | {unemployment:.1f}% | — | — | {'正常' if unemployment < 5.5 else '偏高'} |

### 2.2 增长分析

**制造业景气度分析**：
"""
        
        if pmi >= 52:
            report += f"""
制造业PMI录得{pmi:.1f}，显著高于50荣枯线，显示制造业景气度强劲。从环比变化看，PMI较前值{'上升' if pmi > pmi_prev else '下降'}{abs(pmi-pmi_prev):.1f}个百分点，表明企业信心{'增强' if pmi > pmi_prev else '有所减弱'}。
"""
        elif pmi >= 50:
            report += f"""
制造业PMI录得{pmi:.1f}，处于扩张区间，但幅度相对温和。PMI较前值{'上升' if pmi > pmi_prev else '下降'}{abs(pmi-pmi_prev):.1f}个百分点，需持续关注扩张的持续性。
"""
        else:
            report += f"""
制造业PMI录得{pmi:.1f}，低于50荣枯线，制造业处于收缩区间。PMI较前值{'上升' if pmi > pmi_prev else '下降'}{abs(pmi-pmi_prev):.1f}个百分点，{'显示边际改善迹象' if pmi > pmi_prev else '下行压力持续'}。
"""
        
        report += f"""
**服务业景气度分析**：

非制造业PMI（服务业+建筑业）录得{pmi_non:.1f}，{'高于荣枯线，服务业保持扩张态势' if pmi_non >= 50 else '低于荣枯线，服务业景气度偏弱'}。服务业作为吸纳就业的主力军，其景气度直接关系到就业市场的稳定。

**工业生产分析**：

工业增加值同比增长{ind:.1f}%，{'显示工业生产活跃，经济内生动力较强' if ind >= 5 else '工业生产相对温和，内需仍有修复空间'}。工业生产是观察短期经济波动的核心指标，与PMI走势相互印证。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 三、通胀端分析 (Inflation Analysis)

### 3.1 通胀仪表盘

| 指标 | 当前值 | 前值 | 变化 | 判断 |
|------|--------|------|------|------|
| **CPI同比** | {cpi:.1f}% | {cpi_prev:.1f}% | {'+' if cpi > cpi_prev else ''}{cpi-cpi_prev:.1f}pp | {'通胀' if cpi > 2 else '温和' if cpi > 0 else '通缩压力'} |
| **PPI同比** | {ppi:.1f}% | {ppi_prev:.1f}% | {'+' if ppi > ppi_prev else ''}{ppi-ppi_prev:.1f}pp | {'工业通胀' if ppi > 0 else '工业通缩'} |

### 3.2 通胀结构分析

**消费端价格（CPI）**：
"""
        
        if cpi > 3.0:
            report += f"CPI同比{cpi:.1f}%，处于较高水平，消费端通胀压力明显。需关注食品价格波动和服务价格走势。"
        elif cpi > 1.0:
            report += f"CPI同比{cpi:.1f}%，处于温和区间，消费端价格相对稳定，未对居民生活形成明显压力。"
        elif cpi > 0:
            report += f"CPI同比{cpi:.1f}%，处于低位，消费端价格疲软，反映终端需求相对不足。"
        else:
            report += f"CPI同比{cpi:.1f}%，处于负值区间，消费端呈现通缩特征，有效需求不足是核心矛盾。"
        
        report += f"""

**工业端价格（PPI）**：

"""
        
        if ppi > 3.0:
            report += f"PPI同比{ppi:.1f}%，工业品价格快速上涨，上游成本压力向下游传导，有利于工业企业利润改善。"
        elif ppi > 0:
            report += f"PPI同比{ppi:.1f}%，工业品价格温和上涨，工业企业盈利环境相对稳定。"
        else:
            report += f"PPI同比{ppi:.1f}%，工业品价格下跌，工业企业面临利润压缩压力，上游成本坍塌或下游需求疲软是主因。"
        
        report += f"""

**通胀结论**：

当前通胀环境呈现**{inf_status}**特征。{inf_narrative}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 四、金融条件分析 (Financial Conditions)

### 4.1 金融条件仪表盘

| 指标 | 当前值 | 前值 | 变化 | 判断 |
|------|--------|------|------|------|
| **M2增速** | {m2:.1f}% | {m2_prev:.1f}% | {'+' if m2 > m2_prev else ''}{m2-m2_prev:.1f}pp | {'宽货币' if m2 >= 10 else '中性' if m2 >= 8 else '偏紧'} |
| **LPR(1年)** | {lpr_1y:.2f}% | — | — | 利率水平 |
| **LPR(5年)** | {lpr_5y:.2f}% | — | — | 房贷参考利率 |

### 4.2 流动性分析

**货币供应分析**：

{credit_narrative}

**利率传导分析**：

LPR(1年)为{lpr_1y:.2f}%，LPR(5年)为{lpr_5y:.2f}%。{'利率处于历史低位，货币政策宽松力度较大' if lpr_1y < 3.5 else '利率处于中性水平'}。LPR利率是央行货币政策传导的重要载体，其变动直接影响实体经济融资成本。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 五、需求端分解 (Demand Decomposition)

### 5.1 三驾马车仪表盘

| 分项 | 指标 | 当前值 | 趋势判断 |
|------|------|--------|----------|
| **消费** | 社零增速 | {'N/A' if retail is None else f'{retail:.1f}%'} | {'强劲' if retail and retail >= 6 else '温和' if retail and retail >= 3 else '偏弱'} |
| **投资** | 固定资产投资 | 待更新 | — |
| **出口** | 出口增速 | {'N/A' if exports is None else f'{exports:.1f}%'} | {'强劲' if exports and exports >= 10 else '稳健' if exports and exports >= 0 else '承压'} |
| **进口** | 进口增速 | {'N/A' if imports is None else f'{imports:.1f}%'} | {'内需旺盛' if imports and imports >= 5 else '内需偏弱'} |

### 5.2 需求结构分析

**消费端**：

"""
        
        if retail:
            if retail >= 6:
                report += f"社会消费品零售总额同比增长{retail:.1f}%，消费端表现强劲，是经济增长的重要拉动力量。居民消费信心和消费意愿回升明显。"
            elif retail >= 3:
                report += f"社会消费品零售总额同比增长{retail:.1f}%，消费端表现温和，对经济增长形成稳定支撑。消费复苏的基础有待进一步巩固。"
            else:
                report += f"社会消费品零售总额同比增长{retail:.1f}%，消费端表现偏弱，居民消费意愿有待提振。就业和收入预期是消费复苏的关键变量。"
        else:
            report += "消费数据暂缺。"
        
        report += f"""

**投资端**：

固定资产投资受制造业投资、基建投资和房地产开发投资三大分项影响。当前地产投资仍处调整期，基建投资在专项债支持下保持一定强度，制造业投资受企业盈利和预期影响波动。

**外贸端**：

"""
        
        if exports and imports:
            if exports >= 0 and imports >= 0:
                report += f"出口同比增长{exports:.1f}%，进口同比增长{imports:.1f}%，贸易部门保持顺差态势，外需和内需均有一定支撑。"
            elif exports >= 0 and imports < 0:
                report += f"出口同比增长{exports:.1f}%，进口同比下降{abs(imports):.1f}%，贸易顺差扩大，但内需偏弱值得关注。"
            elif exports < 0 and imports >= 0:
                report += f"出口同比下降{abs(exports):.1f}%，进口同比增长{imports:.1f}%，外需走弱，但内需有一定支撑。"
            else:
                report += f"出口同比下降{abs(exports):.1f}%，进口同比下降{abs(imports):.1f}%，内外需均面临压力，经济下行压力较大。"
        else:
            report += "外贸数据暂缺。"
        
        report += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 六、政策研判 (Policy Outlook)

### 6.1 货币政策研判

**当前立场**：{'宽松' if m2 >= 10 and lpr_1y < 3.5 else '中性偏松' if m2 >= 8 else '中性'}

**政策空间**：{policy_space}

**下一步预判**：

"""
        
        if quadrant == 1:
            report += f"""
经济处于复苏期，货币政策预计维持温和宽松基调，重点在于结构性工具的精准投放，支持实体经济发展。
"""
        elif quadrant == 2:
            report += f"""
经济处于过热期，货币政策存在收紧压力，需关注通胀走势和央行态度的变化。
"""
        elif quadrant == 3:
            report += f"""
经济处于滞胀期，货币政策面临两难：经济增长需要宽松，但通胀压力制约空间。预计维持观望，更多依赖财政政策。
"""
        else:
            report += f"""
经济处于衰退/通缩期，货币政策预计保持宽松基调，降息、降准等总量工具仍有空间，同时配合结构性工具支持重点领域。
        
### 4.2 财政政策研判

**财政发力方向**：

1. **基建投资**：专项债发行节奏和项目落地效率是关键观察点
2. **减税降费**：针对制造业、小微企业的结构性减税
3. **民生保障**：就业、社保、医疗等领域的支出强度
4. **地方化债**：化债方案的推进节奏和对地方财政的影响

---

<br>

## 五、风险评估

### 5.1 风险清单

**表5-1 主要经济风险**

| 风险类别 | 触发条件 | 影响链条 | 当前状态 |
|:---:|:---:|:---:|:---:|
| 地产风险 | 房价持续下跌 | 地方财政→银行资产→居民资产负债表 | 需持续关注 |
| 地方债务风险 | 化债进度不及预期 | 城投债→银行→地方政府支出能力 | 化债进行中 |
| 外部风险 | 关税摩擦、外需走弱 | 出口→制造业→就业 | 外部环境复杂 |
| 金融风险 | 信用利差走阔 | 债券市场→银行间市场→实体经济 | 相对可控 |

### 5.2 关键监测指标

**表5-2 风险监测指标**

| 监测指标 | 当前值 | 警戒值 | 状态 |
|:---:|:---:|:---:|:---:|
| 城镇失业率 | {unemployment:.1f}% | 6.0% | {'预警' if unemployment >= 5.5 else '正常'} |
| CPI同比 | {cpi:.1f}% | 3.0% / 0% | {'通胀预警' if cpi > 3 else '通缩预警' if cpi < 0 else '正常'} |
| PPI同比 | {ppi:.1f}% | -3.0% | {'工业通缩' if ppi < -3 else '正常'} |
| 制造业PMI | {pmi:.1f} | 48.0 | {'收缩预警' if pmi < 48 else '正常'} |

---

<br>

## 六、资产配置建议

### 6.1 基于经济周期的配置建议

**当前周期定位**：第{quadrant}象限 — **{quad_name}期**
"""
        
        if quadrant == 1:
            report += """
**表6-1 资产配置建议**

| 资产类别 | 建议仓位 | 核心逻辑 |
|:---:|:---:|:---:|
| 股票 | 超配 | 经济复苏，企业盈利改善，估值修复空间大 |
| 债券 | 标配 | 利率可能上行，缩短久期 |
| 大宗商品 | 标配 | 需求复苏初期，商品表现相对滞后 |
| 现金 | 低配 | 机会成本上升，资金应配置于风险资产 |
"""
        elif quadrant == 2:
            report += """
**表6-1 资产配置建议**

| 资产类别 | 建议仓位 | 核心逻辑 |
|:---:|:---:|:---:|
| 股票 | 标配 | 盈利改善但估值承压，结构性行情为主 |
| 债券 | 低配 | 利率上行风险大，债券表现不佳 |
| 大宗商品 | 超配 | 通胀环境下最佳对冲资产 |
| 现金 | 标配 | 保持流动性，等待周期切换 |
"""
        elif quadrant == 3:
            report += """
**表6-1 资产配置建议**

| 资产类别 | 建议仓位 | 核心逻辑 |
|:---:|:---:|:---:|
| 股票 | 低配 | 滞胀环境下防御为主 |
| 债券 | 标配 | 经济下行支撑长端，但通胀制约空间 |
| 大宗商品 | 低配 | 需求走弱压制商品表现 |
| 现金/黄金 | 超配 | 避险资产最佳配置窗口 |
"""
        else:
            report += """
**表6-1 资产配置建议**

| 资产类别 | 建议仓位 | 核心逻辑 |
|:---:|:---:|:---:|
| 股票 | 标配 | 估值低位，左侧布局高股息主线 |
| 债券 | 超配 | 货币宽松，利率下行，债券牛市确立 |
| 大宗商品 | 低配 | 需求疲弱，商品去库压力大 |
| 现金 | 标配 | 保留流动性，等待复苏信号 |
"""
        
        report += f"""

### 6.2 具体配置策略

**权益资产**：
"""
        
        if quadrant == 4:
            report += """
- 风格：偏防御，高股息、红利策略为主
- 行业：公用事业、银行、能源等防御性板块
- 时机：左侧分批建仓，等待经济底确认后加仓
"""
        elif quadrant == 1:
            report += """
- 风格：偏进攻，成长与顺周期并重
- 行业：科技、消费、新能源等景气赛道
- 时机：右侧加仓，关注盈利改善验证
"""
        else:
            report += """
- 风格：均衡配置，攻守兼备
- 行业：结构性行业机会为主
- 时机：控制仓位，等待趋势明朗
"""
        
        report += f"""

**债券资产**：
"""
        
        if quadrant == 4:
            report += """
- 久期：拉长久期，享受利率下行收益
- 品种：利率债为主，信用债精选高等级
- 杠杆：可适当加杠杆，套息交易收益可观
"""
        else:
            report += """
- 久期：缩短久期，防范利率上行风险
- 品种：短久期利率债、存单为主
- 杠杆：控制杠杆，保持流动性
"""
        
        report += f"""

---

<br>

## 附录：主要数据附表

**附表1 主要经济指标汇总**

| 指标名称 | 单位 | 数值 | 同比增长 |
|:---|:---:|:---:|:---:|
| GDP增速 | % | {gdp:.1f} | — |
| 制造业PMI | — | {pmi:.1f} | — |
| 非制造业PMI | — | {pmi_non:.1f} | — |
| 工业增加值 | % | {ind:.1f} | — |
| CPI同比 | % | {cpi:.1f} | — |
| PPI同比 | % | {ppi:.1f} | — |
| M2增速 | % | {m2:.1f} | — |
| 失业率 | % | {unemployment:.1f} | — |

数据来源：国家统计局、中国人民银行

---

<br>

## 参考文献

[1] 国家统计局. {year-1}年国民经济和社会发展统计公报[R]. {year}年.

[2] 中国人民银行. {year-1}年第四季度中国货币政策执行报告[R]. {year}年.

[3] 国际货币基金组织. 世界经济展望更新报告[R]. {year}年.

---

<br>

<div style="text-align: center;">

**报告完成日期：{datetime.now().strftime('%Y年%m月%d日')}**

**声明：本报告仅供参考，不构成投资建议。经济预测存在不确定性，实际结果可能与预测存在差异。**

</div>
"""
        
        if self.fetcher.errors:
            report += "\n\n---\n\n**数据获取失败项：**\n"
            for err in self.fetcher.errors[:5]:
                report += f"- {err}\n"
        
        return report

def main():
    parser = argparse.ArgumentParser(description='专业宏观经济深度分析报告生成器')
    parser.add_argument('--country', type=str, default='china', 
                        choices=['china', 'usa'],
                        help='选择国家 (china/usa)')
    args = parser.parse_args()
    
    generator = ReportGenerator()
    
    if args.country == 'china':
        print(generator.generate_china_report())
    else:
        print("美国宏观报告生成器开发中，敬请期待。")

if __name__ == "__main__":
    main()