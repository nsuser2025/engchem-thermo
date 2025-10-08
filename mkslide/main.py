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

    uploaded_pict = st.file_uploader("画像ファイルを選択してください（複数可）",
                    type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if uploaded_pict:
       st.success(f"{len(uploaded_pict)} 件の画像をアップロードしました")
       cols = st.columns(3)
       for i, uploaded_pict in enumerate(uploaded_pict):
           image = Image.open(io.BytesIO(uploaded_pict.read()))
           col = cols[i % 3]
           col.image(image, caption=uploaded_pict.name, use_container_width=True)
           
       df = pd.DataFrame({"試験": ["Alice", "Bob", "Alice", "David"],"点数": [90, 85, 95, 92]})
       selected_exam = st.selectbox("試験を選んでください", df["試験"].tolist())
       #exam = st.text_input("試験", value="B1:B10", key="k_exam")
       #face = st.text_input("測定面", value="C1:C10", key="k_face")
       #cath = st.text_input("正極", value="D1:D10", key="k_cath")
       #mesu = st.text_input("測定", value="E1:E10", key="k_mesu")
       #elec = st.text_input("電解液", value="F1:F10", key="k_elec")
       #magn = st.text_input("倍率", value="G1:G10", key="k_magn")
