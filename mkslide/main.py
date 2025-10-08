import streamlit as st
import pandas as pd

def mkslide_gui():
    uploaded_file = st.file_uploader("Excelファイルを選択してください", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
       df = pd.read_excel(uploaded_file)
       #st.dataframe(df)
       st.data_editor(df, use_container_width=True)
       selected_rows = edited_df[edited_df["選択"] == True]
       st.dataframe(selected_rows)
    else:
       pass

# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
