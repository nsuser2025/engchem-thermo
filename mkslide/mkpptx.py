import streamlit as st
import string
import pandas as pd
from pptx import Presentation
from openpyxl import load_workbook
import numpy as np

def mkpptx_gui(images, result):
    prs = Presentation()
    for name in result:
        if name in images:
           image = images[name]

           tmp_path = f"tmp_{name}"
           image.save(tmp_path)

           slide = prs.slides.add_slide(prs.slide_layouts[5]) 
           slide.shapes.add_picture(tmp_path, Inches(1), Inches(1), width=Inches(6))

    pptx_path = "output.pptx"
    prs.save(pptx_path)
    st.success(f"PPTXに画像を追加しました: {pptx_path}")

    with open(pptx_path, "rb") as f:
         st.download_button("PPTXをダウンロード", f, file_name="output.pptx")

# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
