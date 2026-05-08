#!/usr/bin/env python3
"""
优化版AKShare财经数据工具
解决编码问题、数据结构问题，提供健壮的分析功能
"""

import akshare as ak
import pandas as pd
import numpy as np
import warnings
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

class AKShareOptimizer:
    """AKShare财经数据优化器"""
    
    def __init__(self):
        self.encoding_map = {
            'utf-8': 'utf-8',
            'gbk': 'gbk',
            'gb2312': 'gb2312',
            'gb18030': 'gb18030'
        }
    
    def fix_chinese_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """修复中文列名编码问题"""
        if df.empty:
            return df
            
        new_columns = {}
        for i, col in enumerate(df.columns):
            if isinstance(col, str) and any(c in col for c in ['��', '��', '��', '��']):
                try:
                    decoded_col = col.encode('latin1').decode('gbk')
                    new_columns[col] = decoded_col
                except:
                    new_columns[col] = f"列_{i}"
            else:
                new_columns[col] = col
        
        return df.rename(columns=new_columns)
    
    def standardize_macro_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """标准化宏观数据结构"""
        if df.empty:
            return df
            
        df = self.fix_chinese_columns(df)
        
        if len(df.columns) > 0:
            date_col = df.columns[0]
            
            try:
                if df[date_col].dtype == 'object':
                    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            except:
                pass
            
            try:
                if pd.api.types.is_datetime64_any_dtype(df[date_col]):
                    col_name = str(date_col)
                    df = df.sort_values(by=col_name, ascending=False).reset_index(drop=True)
            except:
                pass
        
        return df
    
    def get_safe_macro_data(self, data_type: str) -> pd.DataFrame:
        """安全获取宏观数据"""
        try:
            data_map = {
                'pmi': ak.macro_china_pmi,
                'gdp': ak.macro_china_gdp,
                'cpi': ak.macro_china_cpi
            }
            
            if data_type not in data_map:
                raise ValueError(f"不支持的数据类型: {data_type}")
            
            df = data_map[data_type]()
            df = self.standardize_macro_data(df)
            
            return df
            
        except Exception as e:
            print(f"获取{data_type}数据失败: {e}")
            return pd.DataFrame()
    
    def analyze_pmi_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """分析PMI数据"""
        if df.empty:
            return {"error": "数据为空"}
        
        try:
            df = self.standardize_macro_data(df)
            
            date_col = df.columns[0]
            mfg_col_idx = 1
            svc_col_idx = 3
            
            mfg_pmi = df.iloc[:, mfg_col_idx]
            svc_pmi = df.iloc[:, svc_col_idx]
            
            latest_data = df.iloc[0]
            latest_date = latest_data[date_col]
            
            result = {
                "latest_date": str(latest_date),
                "manufacturing": {
                    "current": float(latest_data.iloc[mfg_col_idx]),
                    "status": "扩张" if latest_data.iloc[mfg_col_idx] > 50 else "收缩",
                    "mean": float(mfg_pmi.mean()),
                    "max": float(mfg_pmi.max()),
                    "min": float(mfg_pmi.min()),
                    "std": float(mfg_pmi.std())
                },
                "services": {
                    "current": float(latest_data.iloc[svc_col_idx]),
                    "status": "扩张" if latest_data.iloc[svc_col_idx] > 50 else "收缩",
                    "mean": float(svc_pmi.mean()),
                    "max": float(svc_pmi.max()),
                    "min": float(svc_pmi.min()),
                    "std": float(svc_pmi.std())
                }
            }
            
            if len(df) > 1:
                mfg_change = mfg_pmi.diff().dropna()
                svc_change = svc_pmi.diff().dropna()
                
                result["manufacturing"]["monthly_change"] = float(mfg_change.iloc[0]) if len(mfg_change) > 0 else 0
                result["services"]["monthly_change"] = float(svc_change.iloc[0]) if len(svc_change) > 0 else 0
                
                if len(df) >= 12:
                    recent_year_mfg = mfg_pmi.head(12)
                    recent_year_svc = svc_pmi.head(12)
                    
                    result["manufacturing"]["yearly_mean"] = float(recent_year_mfg.mean())
                    result["manufacturing"]["yearly_std"] = float(recent_year_mfg.std())
                    result["services"]["yearly_mean"] = float(recent_year_svc.mean())
                    result["services"]["yearly_std"] = float(recent_year_svc.std())
            
            return result
            
        except Exception as e:
            return {"error": f"分析失败: {e}"}
    
    def format_pmi_report(self, analysis: Dict[str, Any]) -> str:
        """格式化PMI分析报告"""
        if "error" in analysis:
            return f"分析错误: {analysis['error']}"
        
        report = []
        report.append(f"=== PMI数据分析报告 ===")
        report.append(f"数据时间: {analysis['latest_date']}")
        report.append("")
        
        mfg = analysis["manufacturing"]
        report.append(f"【制造业PMI分析】")
        report.append(f"当前值: {mfg['current']:.1f} ({mfg['status']})")
        report.append(f"历史均值: {mfg['mean']:.2f}")
        report.append(f"历史最高: {mfg['max']:.2f}")
        report.append(f"历史最低: {mfg['min']:.2f}")
        report.append(f"历史波动: {mfg['std']:.2f}")
        
        if "monthly_change" in mfg:
            trend = "上升" if mfg["monthly_change"] > 0 else "下降"
            report.append(f"月度变化: {trend} {abs(mfg['monthly_change']):.2f}")
        
        if "yearly_mean" in mfg:
            report.append(f"近一年均值: {mfg['yearly_mean']:.2f}")
            report.append(f"近一年波动: {mfg['yearly_std']:.2f}")
        
        report.append("")
        
        svc = analysis["services"]
        report.append(f"【服务业PMI分析】")
        report.append(f"当前值: {svc['current']:.1f} ({svc['status']})")
        report.append(f"历史均值: {svc['mean']:.2f}")
        report.append(f"历史最高: {svc['max']:.2f}")
        report.append(f"历史最低: {svc['min']:.2f}")
        report.append(f"历史波动: {svc['std']:.2f}")
        
        if "monthly_change" in svc:
            trend = "上升" if svc["monthly_change"] > 0 else "下降"
            report.append(f"月度变化: {trend} {abs(svc['monthly_change']):.2f}")
        
        if "yearly_mean" in svc:
            report.append(f"近一年均值: {svc['yearly_mean']:.2f}")
            report.append(f"近一年波动: {svc['yearly_std']:.2f}")
        
        report.append("")
        
        both_expanding = mfg['status'] == "扩张" and svc['status'] == "扩张"
        both_contracting = mfg['status'] == "收缩" and svc['status'] == "收缩"
        
        if both_expanding:
            report.append("【综合判断】经济全面扩张")
        elif both_contracting:
            report.append("【综合判断】经济全面收缩")
        elif mfg['status'] == "扩张":
            report.append("【综合判断】制造业扩张，服务业收缩")
        else:
            report.append("【综合判断】制造业收缩，服务业扩张")
        
        return "\n".join(report)

def get_pmi_analysis():
    """获取PMI数据分析的便捷函数"""
    optimizer = AKShareOptimizer()
    
    print("正在获取中国PMI数据...")
    pmi_data = optimizer.get_safe_macro_data('pmi')
    
    if pmi_data.empty:
        return "获取PMI数据失败"
    
    pmi_data.to_csv('china_pmi_data.csv', index=False)
    print("数据已保存到 china_pmi_data.csv")
    
    analysis = optimizer.analyze_pmi_data(pmi_data)
    report = optimizer.format_pmi_report(analysis)
    
    return report

if __name__ == "__main__":
    print(get_pmi_analysis())