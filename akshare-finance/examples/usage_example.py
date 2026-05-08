#!/usr/bin/env python3
"""
AKShare优化工具使用示例
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from akshare_optimizer import AKShareOptimizer

def main():
    # 创建优化器实例
    optimizer = AKShareOptimizer()
    
    print("=== AKShare优化工具使用示例 ===\n")
    
    # 示例1：获取并分析PMI数据
    print("1. PMI数据分析示例")
    print("-" * 30)
    
    pmi_data = optimizer.get_safe_macro_data('pmi')
    if not pmi_data.empty:
        print(f"成功获取PMI数据，共{len(pmi_data)}条记录")
        print(f"数据列: {list(pmi_data.columns)}")
        
        analysis = optimizer.analyze_pmi_data(pmi_data)
        report = optimizer.format_pmi_report(analysis)
        print(report)
    else:
        print("获取PMI数据失败")
    
    print("\n" + "="*50 + "\n")
    
    # 示例2：获取GDP数据
    print("2. GDP数据获取示例")
    print("-" * 30)
    
    gdp_data = optimizer.get_safe_macro_data('gdp')
    if not gdp_data.empty:
        print(f"成功获取GDP数据，共{len(gdp_data)}条记录")
        print("前5条数据:")
        print(gdp_data.head())
        
        # 保存数据
        gdp_data.to_csv('china_gdp_data.csv', index=False)
        print("GDP数据已保存到 china_gdp_data.csv")
    else:
        print("获取GDP数据失败")
    
    print("\n" + "="*50 + "\n")
    
    # 示例3：获取CPI数据
    print("3. CPI数据获取示例")
    print("-" * 30)
    
    cpi_data = optimizer.get_safe_macro_data('cpi')
    if not cpi_data.empty:
        print(f"成功获取CPI数据，共{len(cpi_data)}条记录")
        print("数据形状:", cpi_data.shape)
        print("数据类型:")
        print(cpi_data.dtypes)
    else:
        print("获取CPI数据失败")

if __name__ == "__main__":
    main()