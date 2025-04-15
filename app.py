import pandas as pd
import streamlit as st
import re

# 讀取 Excel 文件
def load_excel(file):
    df = pd.read_excel(file, usecols=[26, 59], skiprows=8)
    df.columns = ['Price', 'Material No.']
    
    # 解析 BH 欄資料，提取料號與價格
    df['料號'] = df['Material No.'].astype(str).str.extract(r'([A-Za-z0-9]+)', expand=False)
    df['金額'] = df['Price'].astype(str).str.extract(r'([0-9.]+)USD')[0].astype(float)
    
    return df

# 比對資料並顯示結果
def compare_prices(df_a, df_b):
    df_merge = pd.merge(df_a, df_b, left_on='料號', right_on='料號', how='left')
    df_merge['是否一致'] = df_merge['金額'].round(2) == df_merge['Price'].round(2)
    
    # 若找不到對應資料，顯示 'N'
    df_merge['料號'] = df_merge['料號'].fillna('N')
    
    return df_merge

# Streamlit 介面設置
def main():
    st.title('料號價格核對工具')
    
    # 上傳 A 檔案（含 BH 和 AA 欄位）
    uploaded_file_a = st.file_uploader('請上傳 A.xlsx（含 BH 和 AA 欄位）', type='xlsx')
    # 上傳 B 檔案（含 P 和 F 欄位）
    uploaded_file_b = st.file_uploader('請上傳 B.xlsx（含 P 和 F 欄位）', type='xlsx')
    
    if uploaded_file_a and uploaded_file_b:
        # 讀取資料
        df_a = load_excel(uploaded_file_a)
        df_b = pd.read_excel(uploaded_file_b, usecols=['料號', '價格'])  # 只讀取 P 欄和 F 欄
        
        # 顯示資料
        st.write('A 檔資料：')
        st.dataframe(df_a)
        st.write('B 檔資料：')
        st.dataframe(df_b)
        
        # 比對價格
        df_result = compare_prices(df_a, df_b)
        st.write('比對結果：')
        st.dataframe(df_result)

        # 提供下載功能
        @st.cache_data
        def convert_df(df):
            return df.to_excel(index=False, engine='openpyxl')
        
        xlsx = convert_df(df_result)
        st.download_button('📥 下載比對結果', xlsx, file_name='比對結果.xlsx')

if __name__ == '__main__':
    main()
