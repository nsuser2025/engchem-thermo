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
       image = Image.open(uploaded_file)
       st.image(image, caption="アップロード画像", use_column_width=True)
       #text = pytesseract.image_to_string(image, lang="eng")  # lang="jpn" も可
       #st.text_area("OCR 結果", text, height=200)
        
       all_rows = []
       if uploaded_file.lower().endswith((".png", ".jpg", ".jpeg")):
          text = pytesseract.image_to_string(image, lang="eng")
          # 改行で分割して行ごとに格納
          lines = text.splitlines()
          for line in lines:
              if line.strip():  # 空行は無視
                 all_rows.append({"text": line.strip()})

          # DataFrame に変換して Excel 出力
          df = pd.DataFrame(all_rows)

# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
