import streamlit as st

def cielab_overview():
    with st.expander("CIE Lab変換の概要"):
         st.markdown("""色の見え方を数値化する方法として色を座標点として表す方法が取られる。
         - **L\***：明度（0–100）
         - **a\***：赤（＋）↔ 緑（−）
         - **b\***：黄（＋）↔ 青（−）
         a\* や b\* が負になるのは正常です。""")
