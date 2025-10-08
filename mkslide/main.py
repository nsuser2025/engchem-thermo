import streamlit as st
import string
import pandas as pd
from openpyxl import load_workbook

def mkslide_gui():
    uploaded_file = st.file_uploader("Excelファイルを選択してください", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
       df = pd.read_excel(uploaded_file, header=None)
       df.columns = list(string.ascii_uppercase[:len(df.columns)])
       df.index = range(1, len(df) + 1)
       st.dataframe(df) 
       file_input = st.text_input("ファイル名を選んでください（例: A1:A10）", value="A1:A10")
       exam_input = st.text_input("試験を選んでください（例: B1:B10）", value="B1:B10")
       face_input = st.text_input("測定面を選んでください（例: C1:C10）", value="C1:C10")
       cath_input = st.text_input("正極を選んでください（例: D1:D10）", value="D1:D10")
       mesu_input = st.text_input("測定を選んでください（例: E1:E10）", value="E1:E10")
       elec_input = st.text_input("電解液を選んでください（例: F1:F10）", value="F1:F10")
       magn_input = st.text_input("倍率を選んでください（例: G1:G10）", value="G1:G10")

       def extract_range(range_str):
           try:
               cells = ws[range_str]
               return [c[0].value for c in cells]
           except:
               return []
       
       data = {
            "ファイル名": extract_range(file_input),
            "試験": extract_range(exam_input),
            "測定面": extract_range(face_input),
            "正極": extract_range(cath_input),
            "測定": extract_range(mesu_input),
            "電解液": extract_range(elec_input),
            "倍率": extract_range(magn_input),
       }
        
       df_new = pd.DataFrame(data)
       st.success("データ選択に誤りがないか確認してください")
       st.dataframe(df_new)
        
       #wb = load_workbook(uploaded_file, data_only=True)
       #ws = wb.active
       #try:
       #    # セル範囲を取得
       #    cells = ws[exam_input]
       #    # 値をリスト化
       #    data = [[c.value for c in row] for row in cells]
       #    # DataFrameに変換
       #    df_range = pd.DataFrame(data)
       #    st.success(f"試験: {exam_input}")
       #    st.dataframe(df_range)
       #except Exception as e:
       #    st.error(f"範囲の読み込みに失敗しました: {e}")
    else:
       pass

# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
