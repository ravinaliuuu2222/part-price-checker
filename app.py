import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="料號單價核對工具", layout="centered")
st.title("🔍 料號單價核對工具")
st.caption("請上傳 A 檔（含 BH 欄與 AH 欄）與 B 檔（含 P 欄與 F 欄）")

file_a = st.file_uploader("請上傳 A.xlsx（含 BH 與 AH 欄）", type="xlsx", key="a")
file_b = st.file_uploader("請上傳 B.xlsx（含 P 與 F 欄）", type="xlsx", key="b")

if file_a and file_b:
    try:
        # 讀取 A.xlsx，從第 9 列開始（header=8）
        df_a = pd.read_excel(file_a, header=8)
        df_a.columns = df_a.columns.astype(str).str.strip()

        # 指定欄位名稱
        col_bh = "BH"
        col_price = "AH"

        df_a = df_a[[col_bh, col_price]].dropna()
        df_a["料號"] = df_a[col_bh].astype(str).str.extract(r'([A-Z0-9]{10,})')
        df_a["A_金額"] = df_a[col_price].astype(float)

        # 讀取 B 檔案
        df_b = pd.read_excel(file_b)
        df_b.columns = df_b.columns.astype(str).str.strip()
        df_b = df_b[["P", "F"]].dropna()
        df_b["F"] = df_b["F"].astype(float)

        # 比對
        df_merge = pd.merge(df_b, df_a, left_on="P", right_on="料號", how="left")
        df_merge["是否一致"] = df_merge["F"].round(5) == df_merge["A_金額"].round(5)

        # 顯示結果
        st.success(f"✅ 共比對到 {len(df_merge)} 筆資料")
        st.dataframe(df_merge[["P", "F", "A_金額", "是否一致"]])

        # 下載功能
        @st.cache_data
        def convert_df(df):
            return df.to_excel(index=False, engine='openpyxl')

        xlsx = convert_df(df_merge[["P", "F", "A_金額", "是否一致"]])
        st.download_button("📥 下載結果", xlsx, file_name="核對結果.xlsx")

    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
