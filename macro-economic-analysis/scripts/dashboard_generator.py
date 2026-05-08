#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宏观经济数据仪表盘生成器
基于AKShare获取实时宏观数据，生成分析报告

使用方法:
    python dashboard_generator.py --country china
    python dashboard_generator.py --country usa
    python dashboard_generator.py --country all
"""

import akshare as ak
import pandas as pd
import argparse
import sys
import io
from datetime import datetime
from typing import Dict, List, Any, Optional

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class MacroDashboard:
    """宏观经济数据仪表盘"""
    
    def __init__(self):
        self.data = {}
        self.errors = []
    
    def safe_fetch(self, func, name: str, *args, **kwargs) -> Optional[pd.DataFrame]:
        """安全获取数据"""
        try:
            result = func(*args, **kwargs)
            print(f"✓ {name} 获取成功")
            return result
        except Exception as e:
            self.errors.append(f"{name}: {str(e)}")
            print(f"✗ {name} 获取失败: {e}")
            return None
    
    def fetch_china_growth(self) -> Dict[str, Any]:
        """获取中国增长指标"""
        indicators = {}
        
        # PMI
        df = self.safe_fetch(ak.macro_china_pmi_yearly, "官方制造业PMI")
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            indicators['制造业PMI'] = {
                'value': latest.get('今值', None),
                'date': latest.get('日期', None),
                'status': '扩张' if latest.get('今值', 0) > 50 else '收缩'
            }
        
        # 非制造业PMI
        df = self.safe_fetch(ak.macro_china_non_man_pmi, "非制造业PMI")
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            indicators['非制造业PMI'] = {
                'value': latest.get('今值', None),
                'date': latest.get('日期', None),
                'status': '扩张' if latest.get('今值', 0) > 50 else '收缩'
            }
        
        # 工业增加值
        df = self.safe_fetch(ak.macro_china_industrial_production_yoy, "工业增加值")
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            indicators['工业增加值'] = {
                'value': latest.get('今值', None),
                'date': latest.get('日期', None),
                'unit': '%'
            }
        
        # GDP
        df = self.safe_fetch(ak.macro_china_gdp_yearly, "GDP年率")
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            indicators['GDP年率'] = {
                'value': latest.get('今值', None),
                'date': latest.get('日期', None),
                'unit': '%'
            }
        
        return indicators
    
    def fetch_china_inflation(self) -> Dict[str, Any]:
        """获取中国通胀指标"""
        indicators = {}
        
        # CPI
        df = self.safe_fetch(ak.macro_china_cpi_yearly, "CPI年率")
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            indicators['CPI年率'] = {
                'value': latest.get('今值', None),
                'date': latest.get('日期', None),
                'unit': '%',
                'status': '通胀' if latest.get('今值', 0) > 2 else ('通缩' if latest.get('今值', 0) < 0 else '温和')
            }
        
        # PPI
        df = self.safe_fetch(ak.macro_china_ppi_yearly, "PPI年率")
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            indicators['PPI年率'] = {
                'value': latest.get('今值', None),
                'date': latest.get('日期', None),
                'unit': '%',
                'status': '工业通胀' if latest.get('今值', 0) > 0 else '工业通缩'
            }
        
        return indicators
    
    def fetch_china_financial(self) -> Dict[str, Any]:
        """获取中国金融指标"""
        indicators = {}
        
        # M2
        df = self.safe_fetch(ak.macro_china_m2_yearly, "M2年率")
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            indicators['M2年率'] = {
                'value': latest.get('今值', None),
                'date': latest.get('日期', None),
                'unit': '%'
            }
        
        # 社融
        df = self.safe_fetch(ak.macro_china_shrzgm, "社融增量")
        if df is not None and len(df) > 0:
            latest = df.iloc[0]  # 通常按时间倒序
            indicators['社融增量'] = {
                'value': latest.iloc[1] if len(latest) > 1 else None,
                'date': latest.iloc[0] if len(latest) > 0 else None,
                'unit': '亿元'
            }
        
        # LPR
        df = self.safe_fetch(ak.macro_china_lpr, "LPR利率")
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            indicators['LPR(1Y)'] = {
                'value': latest.get('LPR1Y', None),
                'date': latest.get('TRADE_DATE', None),
                'unit': '%'
            }
            indicators['LPR(5Y)'] = {
                'value': latest.get('LPR5Y', None),
                'date': latest.get('TRADE_DATE', None),
                'unit': '%'
            }
        
        return indicators
    
    def fetch_usa_growth(self) -> Dict[str, Any]:
        """获取美国增长指标"""
        indicators = {}
        
        # GDP
        df = self.safe_fetch(ak.macro_usa_gdp_monthly, "美国GDP")
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            indicators['美国GDP'] = {
                'value': latest.get('今值', None),
                'date': latest.get('日期', None),
                'unit': '%'
            }
        
        # ISM PMI
        df = self.safe_fetch(ak.macro_usa_ism_pmi, "美国ISM制造业PMI")
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            indicators['ISM制造业PMI'] = {
                'value': latest.get('今值', None),
                'date': latest.get('日期', None),
                'status': '扩张' if latest.get('今值', 0) > 50 else '收缩'
            }
        
        # 非农
        df = self.safe_fetch(ak.macro_usa_non_farm, "美国非农就业")
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            indicators['非农就业'] = {
                'value': latest.get('今值', None),
                'date': latest.get('日期', None),
                'unit': '万人'
            }
        
        # 失业率
        df = self.safe_fetch(ak.macro_usa_unemployment_rate, "美国失业率")
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            indicators['失业率'] = {
                'value': latest.get('今值', None),
                'date': latest.get('日期', None),
                'unit': '%'
            }
        
        return indicators
    
    def fetch_usa_inflation(self) -> Dict[str, Any]:
        """获取美国通胀指标"""
        indicators = {}
        
        # CPI
        df = self.safe_fetch(ak.macro_usa_cpi_yoy, "美国CPI年率")
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            indicators['CPI年率'] = {
                'value': latest.get('今值', None),
                'date': latest.get('日期', None),
                'unit': '%'
            }
        
        # 核心CPI
        df = self.safe_fetch(ak.macro_usa_core_cpi_monthly, "美国核心CPI")
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            indicators['核心CPI'] = {
                'value': latest.get('今值', None),
                'date': latest.get('日期', None),
                'unit': '%'
            }
        
        # 核心PCE
        df = self.safe_fetch(ak.macro_usa_core_pce_price, "美国核心PCE")
        if df is not None and len(df) > 0:
            latest = df.iloc[-1]
            indicators['核心PCE'] = {
                'value': latest.get('今值', None),
                'date': latest.get('日期', None),
                'unit': '%',
                'note': '美联储最关注的通胀指标'
            }
        
        return indicators
    
    def generate_china_report(self) -> str:
        """生成中国宏观报告"""
        print("\n" + "="*60)
        print("        中国宏观经济数据仪表盘")
        print("        生成时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("="*60 + "\n")
        
        growth = self.fetch_china_growth()
        inflation = self.fetch_china_inflation()
        financial = self.fetch_china_financial()
        
        report = []
        report.append("\n【增长指标】")
        for name, data in growth.items():
            value = data.get('value', 'N/A')
            date = data.get('date', '')
            status = data.get('status', '')
            unit = data.get('unit', '')
            report.append(f"  • {name}: {value}{unit} ({date}) {status}")
        
        report.append("\n【通胀指标】")
        for name, data in inflation.items():
            value = data.get('value', 'N/A')
            date = data.get('date', '')
            status = data.get('status', '')
            unit = data.get('unit', '')
            report.append(f"  • {name}: {value}{unit} ({date}) {status}")
        
        report.append("\n【金融指标】")
        for name, data in financial.items():
            value = data.get('value', 'N/A')
            date = data.get('date', '')
            unit = data.get('unit', '')
            report.append(f"  • {name}: {value}{unit} ({date})")
        
        # 简单判断
        report.append("\n【快速判断】")
        if growth.get('制造业PMI', {}).get('value', 0) > 50:
            report.append("  • 制造业处于扩张区间")
        else:
            report.append("  • 制造业处于收缩区间")
        
        if inflation.get('CPI年率', {}).get('value', 0) < 0:
            report.append("  • 消费端存在通缩压力")
        elif inflation.get('CPI年率', {}).get('value', 0) > 3:
            report.append("  • 消费端存在通胀压力")
        else:
            report.append("  • 消费端通胀温和")
        
        if inflation.get('PPI年率', {}).get('value', 0) < 0:
            report.append("  • 工业端存在通缩压力")
        else:
            report.append("  • 工业端价格平稳")
        
        return "\n".join(report)
    
    def generate_usa_report(self) -> str:
        """生成美国宏观报告"""
        print("\n" + "="*60)
        print("        美国宏观经济数据仪表盘")
        print("        生成时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("="*60 + "\n")
        
        growth = self.fetch_usa_growth()
        inflation = self.fetch_usa_inflation()
        
        report = []
        report.append("\n【增长指标】")
        for name, data in growth.items():
            value = data.get('value', 'N/A')
            date = data.get('date', '')
            status = data.get('status', '')
            unit = data.get('unit', '')
            report.append(f"  • {name}: {value}{unit} ({date}) {status}")
        
        report.append("\n【通胀指标】")
        for name, data in inflation.items():
            value = data.get('value', 'N/A')
            date = data.get('date', '')
            unit = data.get('unit', '')
            note = data.get('note', '')
            report.append(f"  • {name}: {value}{unit} ({date}) {note}")
        
        # 简单判断
        report.append("\n【快速判断】")
        pce_val = inflation.get('核心PCE', {}).get('value', 0)
        if pce_val and pce_val > 2:
            report.append(f"  • 核心PCE({pce_val}%)高于2%目标，通胀压力仍存")
        elif pce_val:
            report.append(f"  • 核心PCE({pce_val}%)接近或低于2%目标，通胀可控")
        
        unemployment = growth.get('失业率', {}).get('value', 0)
        if unemployment:
            if unemployment < 4:
                report.append(f"  • 失业率({unemployment}%)低于自然率，劳动力市场紧张")
            else:
                report.append(f"  • 失业率({unemployment}%)处于正常区间")
        
        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description='宏观经济数据仪表盘')
    parser.add_argument('--country', type=str, default='china', 
                        choices=['china', 'usa', 'all'],
                        help='选择国家 (china/usa/all)')
    args = parser.parse_args()
    
    dashboard = MacroDashboard()
    
    if args.country in ['china', 'all']:
        print(dashboard.generate_china_report())
    
    if args.country in ['usa', 'all']:
        print(dashboard.generate_usa_report())
    
    if dashboard.errors:
        print("\n【获取失败的数据】")
        for error in dashboard.errors:
            print(f"  ✗ {error}")


if __name__ == "__main__":
    main()