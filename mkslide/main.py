import streamlit as st
import io
from PIL import Image
from .mkcsv import mkcsv_gui

def mkslide_gui():

    # ファイルアップロード
    uploaded_file = st.file_uploader("Excel/CSVファイルをアップロード", type=["xlsx", "xls", "csv"])
    option_form = st.radio("MKSLIDEが作成したCSVファイルですか？", ["Yes", "No"], index = 1, horizontal = True)
    
    if uploaded_file and option_form == "No":
       mkcsv_gui(uploaded_file)

    uploaded_pict = st.file_uploader("画像ファイルを選択してください（複数可）",
                    type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if uploaded_pict:
       st.success(f"{len(uploaded_pict)} 件の画像をアップロードしました")
       cols = st.columns(3)
       for i, uploaded_pict in enumerate(uploaded_pict):
           #image = Image.open(uploaded_pict)
           image = Image.open(io.BytesIO(uploaded_pict.read()))
           col = cols[i % 3]
           #st.image(image, caption=f"画像 {i+1}: {uploaded_pict.name}", use_container_width=True) 
           col.image(image, caption=uploaded_pict.name, use_container_width=True)
