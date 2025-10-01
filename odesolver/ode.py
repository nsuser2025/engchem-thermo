import streamlit as st
import numpy as np
from scipy.integrate import solve_ivp
import numexpr as ne
import matplotlib.pyplot as plt

def ode_gui():
    st.markdown("---")
    st.markdown("#### ODE Solver")
    st.markdown("""例）化学反応の濃度変化(d[A]/dt)は常微分方程式（ODE）で表されます。例えば単純な一次反応なら次のODEに従います。""")
    st.latex(r"\frac{d [A]}{dt} = -k[A]")
    st.markdown("""時刻t=0の[A]の値（初期値）を用いてODEを解けば、任意の時刻における[A]を決めることができます。これを初期値問題といいます。
                 ODE Solverは、ユーザーが入力したODEの式（上式では右辺）、パラメータの値、初期値から初期値問題を解くツールです。""")
    st.markdown("---")
    
    # ユーザー入力（安全な式のみ）
    st.markdown("dx/dt = f(x,t) の f(x,t) を入力")
    expr = st.text_area("右辺の式 (例: -0.5*x + np.sin(t))", "-0.5*x")

    x0 = st.number_input("初期値 x(0)", value=1.0)
    t_start = st.number_input("開始時刻", value=0.0)
    t_end = st.number_input("終了時刻", value=10.0)
    n_points = st.number_input("分割点数", value=1000)

    if st.button("計算"):

       # solve_ivp に渡す関数を作成
       def f(t, x):
           try:
               # numexprで安全に評価
               return ne.evaluate(expr, local_dict={"x": x, "t": t, "np": np})
           except Exception as e:
               st.error(f"計算エラー: {e}")
               return 0.0

       t_eval = np.linspace(t_start, t_end, n_points)
       sol = solve_ivp(f, [t_start, t_end], [x0], t_eval=t_eval)

       # 結果表示
       fig, ax = plt.subplots()
       ax.plot(sol.t, sol.y[0], label="x(t)")
       ax.set_xlabel("t")
       ax.set_ylabel("x")
       ax.grid(True)
       ax.legend()
       st.pyplot(fig)



    
    text = st.text_area("テキストを入力してください", height=200)
    st.write("入力内容:")
    st.text(text)
