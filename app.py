import streamlit as st
import pandas as pd
import re

st.title("🔍 料號單價核對工具（組合料號不拆分）")

uploaded_file_a = st.file_uploader("請上傳 A.xlsx（含 BH 欄與 AA 欄）", type=["xlsx"])
uploaded_file_b = st.file_uploader("請上傳 B.xlsx（含 P 欄與 F 欄）", type=["xlsx"])

if uploaded_file_a and uploaded_file_b:
    try:
        # A 檔案處理
        df_a = pd.read_excel(uploaded_file_a, header=8)  # 從第 9 列開始（index=8）

        df_a = df_a.rename(columns=lambda x: str(x).strip())
        col_price_a = "單價"
        col_mix = "BH"

        df_a = df_a[[col_price_a, col_mix]].dropna()

        # 用正則萃取料號與金額
        df_a["料號"] = df_a[col_mix].str.extract(r'([A-Z0-9]{10,})')
        df_a["金額"] = df_a[col_mix].str.extract(r'(\d+\.\d+)').astype(float)

        # B 檔案處理
        df_b = pd.read_excel(uploaded_file_b)
        df_b = df_b.rename(columns=lambda x: str(x).strip())

        col_key_b = "P"
        col_price_b = "F"
        df_b = df_b[[col_key_b, col_price_b]].dropna()
        df_b[col_price_b] = df_b[col_price_b].astype(float)

        # 合併比對
        df_merge = pd.merge(df_b, df_a, left_on=col_key_b, right_on="料號", how="left")
        df_merge["是否一致"] = df_merge[col_price_b] == df_merge["金額"]

        # 輸出結果
        st.success("✅ 比對完成，結果如下：")
        st.dataframe(df_merge[[col_key_b, col_price_b, "金額", "是否一致"]])

        # 提供下載
        @st.cache_data
        def convert_df(df):
            return df.to_excel(index=False, engine='openpyxl')

        result_bytes = convert_df(df_merge[[col_key_b, col_price_b, "金額", "是否一致"]])
        st.download_button(
            label="📥 下載結果 Excel",
            data=result_bytes,
            file_name="比對結果.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
