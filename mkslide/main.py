import streamlit as st
import pandas as pd

def mkslide_gui():
    uploaded_file = st.file_uploader("Excelファイルを選択してください", type=["xlsx", "xls"])
