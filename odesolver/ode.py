import streamlit as st

def ode_gui():
    st.markdown("---")
    st.markdown("#### 初期値問題とは？")
    #st.latex(r"\eta = \eta_{0}\biggl( 1 - \frac{\phi}{\phi_{\rm max}} \biggr)^{-[\eta]\phi_{\rm max}}")
    st.write("あなたが解きたい初期値問題を簡単にコーディングできます。")
    st.markdown("---")
    
    text = st.text_area("テキストを入力してください", height=200)
    st.write("入力内容:")
    st.text(text)
