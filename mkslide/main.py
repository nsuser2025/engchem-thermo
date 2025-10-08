import streamlit as st
import pandas as pd
import io
from PIL import Image
from .mkcsv import mkcsv_gui

def mkslide_gui():

    # ファイルアップロード
    uploaded_file = st.file_uploader("Excel/CSVファイルをアップロード", type=["xlsx", "xls", "csv"])
    option_form = st.radio("MKSLIDEが作成したCSVファイルですか？", ["Yes", "No"], index = 1, horizontal = True)
    
    if uploaded_file and option_form == "No":
       mkcsv_gui(uploaded_file)
    elif uploaded_file and option_form == "Yes":
       df = pd.read_csv(uploaded_file)
       st.dataframe(df)
    
    uploaded_pict = st.file_uploader("画像ファイルを選択してください（複数可）",
                    type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if uploaded_pict:
       st.success(f"{len(uploaded_pict)} 件の画像をアップロードしました")
       cols = st.columns(3)
       for i, uploaded_pict in enumerate(uploaded_pict):
           image = Image.open(io.BytesIO(uploaded_pict.read()))
           col = cols[i % 3]
           col.image(image, caption=uploaded_pict.name, use_container_width=True)
              
       selected_exam = st.selectbox("試験を選んでください", df["試験"].unique().tolist())
       selected_face = st.selectbox("測定面を選んでください", df["測定面"].unique().tolist())
       selected_cath = st.selectbox("正極を選んでください", df["正極"].unique().tolist()) 
       selected_mesu = st.selectbox("測定を選んでください", df["測定"].unique().tolist())
       selected_elec = st.selectbox("電解液を選んでください", df["電解液"].unique().tolist())
       selected_magn = st.selectbox("倍率を選んでください", df["倍率"].unique().tolist()) 

       result = df.loc[(df["試験"] == selected_exam) & 
                       (df["測定面"] == selected_face) & 
                       (df["正極"] == selected_cath) & 
                       (df["測定"] == selected_mesu) & 
                       (df["電解液"] == selected_elec) & 
                       (df["倍率"] == selected_magn), 
                       "ファイル名"].tolist()
       st.write(result)
       
