import streamlit as st

def ode_gui():
    st.markdown("---")
    st.markdown("#### 初期値問題とは？")
    line = "例）化学反応の濃度変化(d[A]/dt)は常微分方程式（ODE）で表されます。"\\
         + "例えば単純な一次反応なら次のODEに従います。"
    #st.write("例）化学反応の濃度変化(d[A]/dt)は常微分方程式（ODE）で表されます。例えば単純な一次反応なら次のODEに従います。")
    st.write(line)
    st.latex(r"\frac{d [A]}{dt} = -k[A]")
    st.write("時刻t=0の[A]の値（初期値）を用いてODEを解けば、任意の時刻における[A]を決めることができます。これを初期値問題といいます。")
    st.write("ODE SolverはODEの式と初期値をユーザーが与えることで初期値問題を解くツールです。")
    st.markdown("---")
    
    text = st.text_area("テキストを入力してください", height=200)
    st.write("入力内容:")
    st.text(text)
