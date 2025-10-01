import streamlit as st

def ode_gui():
    st.markdown("---")
    st.markdown("#### 初期値問題とは？")
    st.write("例）化学反応の濃度変化は常微分方程式（ODE）で表されます。\n 例えば単純な一次反応なら")
    st.latex(r"\frac{d [A]}{dt} = -k[A}")
    st.markdown("---")
    
    text = st.text_area("テキストを入力してください", height=200)
    st.write("入力内容:")
    st.text(text)
