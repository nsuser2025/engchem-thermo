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
    
# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
