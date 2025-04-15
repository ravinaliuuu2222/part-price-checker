import pandas as pd
import streamlit as st

# 讀取 Excel 文件
def load_excel(file):
    # 讀取 A 檔案中的 AA（價格欄位）和 BH（料號欄位），以及 B 檔案中的 P（料號欄位）和 F（價格欄位）
    df = pd.read_excel(file, usecols=[26, 59])  # 26 是 A.xlsx 中的 AA（價格），59 是 A.xlsx 中的 BH（料號）
    return df

# 比對料號和價格
def compare_prices(df_a, df_b):
    # 根據 A 檔案的 BH 欄位與 B 檔案的 P 欄位比對料號，並比對價格
    matched = pd.merge(df_a, df_b, left_on='Unnamed: 59', right_on='MAT_NO', how='inner')
    return matched

# Streamlit 介面設置
def main():
    st.title("料號價格核對工具")
    
    # 上傳 A 檔案（包含 BH 和 AA 欄位）
    uploaded_a = st.file_uploader("請上傳 A 檔案 (含 BH 和 AA 欄位)", type="xlsx")
    if uploaded_a is not None:
        df_a = load_excel(uploaded_a)
        st.write("A 檔案資料：")
        st.dataframe(df_a)
    
    # 上傳 B 檔案（包含 P 和 F 欄位）
    uploaded_b = st.file_uploader("請上傳 B 檔案 (含 P 和 F 欄位)", type="xlsx")
    if uploaded_b is not None:
        df_b = load_excel(uploaded_b)
        st.write("B 檔案資料：")
        st.dataframe(df_b)
    
    if uploaded_a is not None and uploaded_b is not None:
        # 比對價格
        matched = compare_prices(df_a, df_b)
        st.write("比對結果：")
        st.dataframe(matched)

if __name__ == "__main__":
    main()
