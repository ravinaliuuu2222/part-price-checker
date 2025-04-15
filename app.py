
import streamlit as st
import pandas as pd

st.set_page_config(page_title="料號單價核對工具", page_icon="🔍", layout="centered")

st.title("📊 料號單價核對工具（組合料號完全比對）")
st.write("請上傳 A 檔案（含 BH 欄與 AA 欄）與 B 檔案（含 P 欄與 F 欄）後，自動產生核對結果。")

file_a = st.file_uploader("上傳 A.xlsx（含 BH 欄與 AA 欄）", type="xlsx")
file_b = st.file_uploader("上傳 B.xlsx（含 P 欄與 F 欄）", type="xlsx")

if file_a and file_b:
    df_a = pd.read_excel(file_a, engine="openpyxl")
    df_b = pd.read_excel(file_b, engine="openpyxl", sheet_name=0)

    # 指定關鍵欄位
    col_key_a = "BH"
    col_price_a = "AA"
    col_key_b = "P"
    col_price_b = "F"

    # 篩選與轉型
    df_a = df_a[[col_key_a, col_price_a]].dropna()
    df_b = df_b[[col_key_b, col_price_b]].dropna()
    df_a.columns = ["料號", "單價_A"]
    df_b.columns = ["料號", "單價_B"]

    # 合併與比較
    merged = pd.merge(df_a, df_b, on="料號", how="inner")
    merged["單價是否一致"] = merged["單價_A"] == merged["單價_B"]

    st.success(f"比對完成，共比對 {len(merged)} 筆料號")
    st.dataframe(merged)

    # 提供下載
    @st.cache_data
    def convert_df(df):
        return df.to_excel(index=False, engine="openpyxl")

    st.download_button(
        label="📥 下載比對結果 Excel",
        data=convert_df(merged),
        file_name="比對結果.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
