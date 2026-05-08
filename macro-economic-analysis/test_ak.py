import akshare as ak
import pandas as pd

try:
    df_retail = ak.macro_china_consumer_goods_retail()
    print("Retail cols:", df_retail.columns.tolist() if df_retail is not None else "None")
except Exception as e:
    print("Retail error:", e)

try:
    df_invest = ak.macro_china_gdzctz()
    print("Invest cols:", df_invest.columns.tolist() if df_invest is not None else "None")
except Exception as e:
    print("Invest error:", e)

try:
    df_unemp = ak.macro_china_urban_unemployment()
    print("Unemp cols:", df_unemp.columns.tolist() if df_unemp is not None else "None")
except Exception as e:
    print("Unemp error:", e)

try:
    df_export = ak.macro_china_exports_yoy()
    print("Export cols:", df_export.columns.tolist() if df_export is not None else "None")
except Exception as e:
    print("Export error:", e)
