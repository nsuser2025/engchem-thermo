import streamlit as st

text = st.text_area("テキストを入力してください", height=200)
st.write("入力内容:")
st.text(text)
