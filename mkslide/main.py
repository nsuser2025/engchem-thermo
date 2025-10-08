import streamlit as st
import pandas as pd
from openpyxl import load_workbook

def mkslide_gui():
    uploaded_file = st.file_uploader("Excelファイルを選択してください", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
       df = pd.read_excel(uploaded_file)
       st.dataframe(df) 
       exam_input = st.text_input("試験を選んでください（例: A1:A10）", value="A1:A10")

       wb = load_workbook(uploaded_file, data_only=True)
       ws = wb.active
       try:
           # セル範囲を取得
           cells = ws[exam_input]
           # 値をリスト化
           data = [[c.value for c in row] for row in cells]
           # DataFrameに変換
           df_range = pd.DataFrame(data)
           st.success(f"抽出範囲: {exam_input}")
           st.dataframe(df_range)
       except Exception as e:
           st.error(f"範囲の読み込みに失敗しました: {e}")
       #test_col = st.selectbox("試験（列）を選択してください", df.columns)
       #st.write(f"選択された項目: **{test_col}**")
       #st.dataframe(df[[test_col]])
    else:
       pass

# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
