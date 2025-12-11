import streamlit as st
import io
import pandas as pd
from typing import List
from PIL import Image

def cielab_gui():

    # EXPLANATIONS
    st.markdown("---")
    st.markdown("#### CIE Lab変換")
    st.markdown("""透過率データをCIE Lab変換するアプリです。
    このアプリにアップロードした透過率データは全てメモリ上に保存されます。
    セッションの終了と同時にサーバー上のデータは完全に消去されます。
    また、出力されるCSVにはコードインジェクションの無効化処理が施されています。
    安心してダウンロードしてください。""") 
    st.markdown("---")
    
# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
