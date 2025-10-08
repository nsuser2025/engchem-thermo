import streamlit as st
import pandas as pd

def mkslide_gui():
    uploaded_file = st.file_uploader("Excelファイルを選択してください", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
       df = pd.read_excel(uploaded_file)
       st.dataframe(df) 
       test_col = st.selectbox("試験（列）を選択してください", df.columns)
       st.write(f"選択された項目: **{test_col}**")
       st.dataframe(df[[test_col]])
    else:
       pass

# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
