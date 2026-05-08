#!/usr/bin/env python3
"""
宏观经济四象限分析工具
基于增长×通胀矩阵进行经济周期定位

使用方法:
    python quadrant_analyzer.py --pmi 49.5 --cpi 0.5 --ppi -2.5
    python quadrant_analyzer.py --interactive
"""

import argparse
from typing import Tuple, Dict, Any, Optional


class QuadrantAnalyzer:
    """四象限分析器"""
    
    # 四象限定义
    QUADRANTS = {
        1: {
            'name': '复苏期',
            'growth': '强',
            'inflation': '低',
            'description': '经济复苏，通胀可控',
            'policy': '温和宽松',
            'asset': '股票占优',
            'color': '🟢'
        },
        2: {
            'name': '过热期',
            'growth': '强',
            'inflation': '高',
            'description': '经济增长强劲，通胀上行',
            'policy': '收紧',
            'asset': '大宗商品占优',
            'color': '🔴'
        },
        3: {
            'name': '滞胀期',
            'growth': '弱',
            'inflation': '高',
            'description': '经济增长乏力，通胀高企',
            'policy': '两难',
            'asset': '现金/黄金占优',
            'color': '🟡'
        },
        4: {
            'name': '衰退/通缩期',
            'growth': '弱',
            'inflation': '低',
            'description': '经济下行，通胀回落',
            'policy': '全面宽松',
            'asset': '债券占优',
            'color': '🔵'
        }
    }
    
    def __init__(self):
        self.pmi = None
        self.cpi = None
        self.ppi = None
        self.core_cpi = None
    
    def set_indicators(self, pmi: float, cpi: float, ppi: Optional[float] = None, core_cpi: Optional[float] = None):
        """设置指标值"""
        self.pmi = pmi
        self.cpi = cpi
        self.ppi = ppi
        self.core_cpi = core_cpi
    
    def analyze_growth(self) -> Tuple[str, str]:
        """分析增长状态"""
        if self.pmi is None:
            return '未知', 'PMI数据缺失'
        
        if self.pmi >= 52:
            return '强', f'PMI={self.pmi}，明显高于50荣枯线'
        elif self.pmi >= 50:
            return '中性偏强', f'PMI={self.pmi}，略高于50荣枯线'
        elif self.pmi >= 48:
            return '中性偏弱', f'PMI={self.pmi}，略低于50荣枯线'
        else:
            return '弱', f'PMI={self.pmi}，明显低于50荣枯线'
    
    def analyze_inflation(self) -> Tuple[str, str]:
        """分析通胀状态"""
        if self.cpi is None:
            return '未知', 'CPI数据缺失'
        
        # 中国：结合CPI和PPI
        reasons = []
        
        if self.cpi > 3:
            cpi_status = '高'
            reasons.append(f'CPI={self.cpi}%，消费端通胀压力')
        elif self.cpi > 1:
            cpi_status = '温和'
            reasons.append(f'CPI={self.cpi}%，消费端通胀温和')
        elif self.cpi > 0:
            cpi_status = '低'
            reasons.append(f'CPI={self.cpi}%，消费端通胀偏低')
        else:
            cpi_status = '低/通缩'
            reasons.append(f'CPI={self.cpi}%，消费端通缩压力')
        
        # PPI补充判断
        if self.ppi is not None:
            if self.ppi < 0:
                reasons.append(f'PPI={self.ppi}%，工业端通缩')
            elif self.ppi > 3:
                reasons.append(f'PPI={self.ppi}%，工业端通胀')
        
        return cpi_status, '；'.join(reasons)
    
    def determine_quadrant(self) -> int:
        """确定象限"""
        growth_status, _ = self.analyze_growth()
        inflation_status, _ = self.analyze_inflation()
        
        growth_strong = growth_status in ['强', '中性偏强']
        inflation_high = inflation_status in ['高']
        
        if growth_strong and not inflation_high:
            return 1  # 复苏
        elif growth_strong and inflation_high:
            return 2  # 过热
        elif not growth_strong and inflation_high:
            return 3  # 滞胀
        else:
            return 4  # 衰退/通缩
    
    def generate_report(self) -> str:
        """生成分析报告"""
        growth_status, growth_reason = self.analyze_growth()
        inflation_status, inflation_reason = self.analyze_inflation()
        quadrant = self.determine_quadrant()
        quad_info = self.QUADRANTS[quadrant]
        
        report = []
        report.append("\n" + "="*60)
        report.append("        宏观经济四象限分析报告")
        report.append("="*60)
        
        report.append("\n【指标输入】")
        report.append(f"  • PMI: {self.pmi if self.pmi is not None else '未设置'}")
        report.append(f"  • CPI: {str(self.cpi) + '%' if self.cpi is not None else '未设置'}")
        if self.ppi is not None:
            report.append(f"  • PPI: {self.ppi}%")
        if self.core_cpi is not None:
            report.append(f"  • 核心CPI: {self.core_cpi}%")
        
        report.append("\n【增长分析】")
        report.append(f"  • 判断: {growth_status}")
        report.append(f"  • 依据: {growth_reason}")
        
        report.append("\n【通胀分析】")
        report.append(f"  • 判断: {inflation_status}")
        report.append(f"  • 依据: {inflation_reason}")
        
        report.append("\n【象限定位】")
        report.append(f"  {quad_info['color']} 第{quadrant}象限: {quad_info['name']}")
        report.append(f"  • 特征: {quad_info['description']}")
        report.append(f"  • 政策倾向: {quad_info['policy']}")
        report.append(f"  • 资产配置: {quad_info['asset']}")
        
        # 绘制象限图
        report.append("\n【象限示意图】")
        report.append("              通胀高")
        report.append("                ↑")
        report.append(f"    ② 过热         ③ 滞胀")
        report.append("    大宗商品       现金/黄金")
        report.append("←增长弱 ─────────────── 增长强→")
        report.append("    ④ 衰退         ① 复苏")
        report.append("    债券          股票")
        report.append("                ↓")
        report.append("              通胀低")
        
        # 标记当前位置
        if quadrant == 1:
            marker = "                              ★ 当前"
        elif quadrant == 2:
            marker = "    ★ 当前"
        elif quadrant == 3:
            marker = "                 ★ 当前"
        else:
            marker = "                 ★ 当前"
        report.append(f"\n{marker}")
        
        report.append("\n【投资建议】")
        if quadrant == 1:
            report.append("  • 股票: 增配，经济复苏利好企业盈利")
            report.append("  • 债券: 中性，利率可能上行")
            report.append("  • 商品: 谨慎，需求尚未过热")
        elif quadrant == 2:
            report.append("  • 股票: 谨慎，估值可能承压")
            report.append("  • 债券: 减配，利率上行风险")
            report.append("  • 商品: 增配，通胀利好")
        elif quadrant == 3:
            report.append("  • 股票: 减配，企业盈利承压")
            report.append("  • 债券: 谨慎，通胀制约利率下行")
            report.append("  • 现金/黄金: 增配，避险为主")
        else:
            report.append("  • 股票: 谨慎，等待复苏信号")
            report.append("  • 债券: 增配，利率下行")
            report.append("  • 现金: 保留，等待机会")
        
        report.append("\n" + "="*60)
        
        return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description='宏观经济四象限分析')
    parser.add_argument('--pmi', type=float, help='PMI值')
    parser.add_argument('--cpi', type=float, help='CPI同比(%)')
    parser.add_argument('--ppi', type=float, help='PPI同比(%)')
    parser.add_argument('--core-cpi', type=float, help='核心CPI同比(%)')
    parser.add_argument('--interactive', action='store_true', help='交互模式')
    args = parser.parse_args()
    
    analyzer = QuadrantAnalyzer()
    
    if args.interactive:
        print("\n宏观经济四象限分析 - 交互模式")
        print("-" * 40)
        pmi = float(input("请输入PMI值: "))
        cpi = float(input("请输入CPI同比(%): "))
        ppi_input = input("请输入PPI同比(%), 可选: ")
        ppi = float(ppi_input) if ppi_input else None
        core_cpi_input = input("请输入核心CPI同比(%), 可选: ")
        core_cpi = float(core_cpi_input) if core_cpi_input else None
        
        analyzer.set_indicators(pmi, cpi, ppi, core_cpi)
    elif args.pmi is not None and args.cpi is not None:
        analyzer.set_indicators(args.pmi, args.cpi, args.ppi, args.core_cpi)
    else:
        # 使用默认示例数据
        print("\n使用示例数据进行分析...")
        analyzer.set_indicators(
            pmi=49.5,   # 收缩区间
            cpi=0.3,    # 低通胀
            ppi=-2.5,   # 工业通缩
        )
    
    print(analyzer.generate_report())


if __name__ == "__main__":
    main()