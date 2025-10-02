import streamlit as st
import os
import pandas as pd
from PIL import Image
import pytesseract

def pic2xlsx_gui():
    st.markdown("---")
    st.markdown("#### Picuture to Excel（PIC2XLSX）")
    st.markdown("---")
    uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
       filename = uploaded_file.name
       image = Image.open(uploaded_file)
    else:
       filename = "sample.png"
       st.info("サンプル画像の変換結果を表示しています")
       image = Image.open("pic2xlsx/" + filename)
       
    col1, col2 = st.columns([1, 1])
    with col1:
         st.image(image, caption="変換前の画像", width=100)
    
    # INITIALIZE SESSION_STATE 
    if "df" not in st.session_state:
       st.session_state["df"] = None
        
    all_rows = []
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
       text = pytesseract.image_to_string(image, lang="jpn+eng")
          
       # 改行で分割して行ごとに格納
       lines = text.splitlines()
       for line in lines:
           if line.strip():  # 空行は無視
              all_rows.append({"text": line.strip()})

       # --> DataFrame
       df = pd.DataFrame(all_rows)
       st.session_state["df"] = df
       
       # DISPLAY DATAFRAME
       if st.session_state["df"] is not None:
          with col2:
               st.dataframe(st.session_state["df"])
               csv = st.session_state["df"].to_csv(index=False)

# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
