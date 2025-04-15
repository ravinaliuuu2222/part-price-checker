import pandas as pd
import streamlit as st
import re

# 讀取 Excel 文件
def load_excel(file):
    df = pd.read_excel(file, usecols=[26, 59], skiprows=8)  # 讀取 A.xlsx 中的 AH 和 BH 欄位
    df.columns = ['Price', 'Material No.']  # 設定列名，Price 為 AH，Material No. 為 BH

    # 解析 BH 欄：提取料號
    df['料號'] = df['Material No.'].astype(str).str.extract(r'([A-Za-z0-9]+)', expand=False)

    # 解析 AH 欄：提取價格
    df['價格'] = df['Price'].astype(str).str.extract(r'([0-9.]+)USD')[0].astype(float)

    return df

# 主程式
def main():
    st.title('物料與價格比對工具')
    
    uploaded_a = st.file_uploader("請上傳 A.xlsx 檔案 (含 BH 和 AA 欄位)", type=["xlsx"])
    uploaded_b = st.file_uploader("請上傳 B.xlsx 檔案 (含 P 和 F 欄位)", type=["xlsx"])

    if uploaded_a and uploaded_b:
        # 讀取 A 檔案
        df_a = load_excel(uploaded_a)

        # 讀取 B 檔案，抓取 P 欄和 F 欄
        df_b = pd.read_excel(uploaded_b, usecols=['P', 'F'])
        df_b.columns = ['料號', '價格']

        # 比對資料：A 檔案的料號是否存在於 B 檔案的料號欄位，並且價格是否相符
        df_a['比對結果'] = df_a.apply(lambda row: 'Y' if row['料號'] in df_b['料號'].values and row['價格'] == df_b.loc[df_b['料號'] == row['料號'], '價格'].values[0] else 'N', axis=1)

        st.write(df_a)  # 顯示比對結果

if __name__ == "__main__":
    main()
