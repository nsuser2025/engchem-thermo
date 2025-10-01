import streamlit as st

def ode_gui():
    st.write("あなたが解きたい初期値問題をコーディングできます。")
    text = st.text_area("テキストを入力してください", height=200)
    st.write("入力内容:")
    st.text(text)
