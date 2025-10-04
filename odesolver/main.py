import ast
import streamlit as st
import numpy as np
from scipy.integrate import solve_ivp
import numexpr as ne
import matplotlib.pyplot as plt
import pandas as pd

def ode_gui():
    
    st.markdown("---")
    st.markdown("#### ODE Solver")
    st.markdown("""例）化学反応の濃度変化(d[A]/dt)は常微分方程式（ODE）で表されます。例えば単純な一次反応なら次のODEに従います。""")
    st.latex(r"\frac{d [A]}{dt} = -k[A]")
    st.markdown("""時刻t=0の[A]の値（初期値）を用いてODEを解けば、任意の時刻における[A]を決めることができます。これを初期値問題といいます。
                 ODE Solverは、ユーザーが入力したODEの式（上式では右辺）、パラメータの値、初期値から初期値問題を解くツールです。""")
    st.markdown("---")

    option = st.radio("入力例：",("ローレンツアトラクター", "シュレーディンガー方程式"))
    st.write(f"あなたが選んだのは：{option} です 🌈")
    
    # INPUTS: ODE
    default_input = "-k1*x1 + k2*x2\n k1*x1 - k2*x2"
    st.write("変数を x1, x2, x3 ... のように表し、1行に1つのODE（dxi/dt）を入力してください")
    expr_text = st.text_area("常微分方程式を入力 (1行に1つの式)",
                             value = default_input)
    # INPUTS: PARAMETERS
    params_input = st.text_input("パラメータ（例: {'k1':1.0,'k2':0.5}）", value="{'k1':1.0,'k2':0.5}")
    params = ast.literal_eval(params_input)

    # INPUTS: INITIAL CONDITIONS
    initial_values_input = st.text_input("初期値（例: [1.0, 0.0]）", value="[1.0, 0.0]")
    Y0 = ast.literal_eval(initial_values_input)

    # INPUTS: TIME SPAN
    t0 = st.number_input("開始時刻 t0", value=0.0)
    t1 = st.number_input("終了時刻 t1", value=10.0)
    n_points = st.number_input("分割数", value=100, step=1)

    # INPUTS: TIME SPAN
    graph_title = st.text_input("グラフタイトル", value='ODE SOLUTION')
    graph_ylabel = st.text_input("Y軸ラベル", value='VARIABLES')
    
    # DEFINE THE FUNCTIONS
    def ode_system(t, Y):
        local_dict = {f"x{i+1}": Y[i] for i in range(len(Y))}
        local_dict.update(params)
        local_dict["t"] = t
        dYdt = []
        for expr in expr_lines:
            dYdt.append(ne.evaluate(expr, local_dict))
            return dYdt

    # RUN SOLVE_IVP
    if st.button("実行"):
       expr_lines = [line.strip() for line in expr_text.splitlines() if line.strip() != ""]
       t_eval = np.linspace(t0, t1, int(n_points))
       sol = solve_ivp(ode_system, (t0, t1), Y0, t_eval=t_eval)

       # --- プロット ---
       fig, ax = plt.subplots(figsize=(6,4))
       for i in range(len(Y0)):
           ax.plot(sol.t, sol.y[i], label=f"x{i+1}")
       ax.set_xlabel("t")
       ax.set_ylabel(graph_ylabel)
       ax.set_title(graph_title)
       ax.legend()
       ax.grid(True)
       st.pyplot(fig)
    
       # --- CSV ダウンロード ---
       data = {"t": sol.t}
       for i in range(len(Y0)):
           data[f"x{i+1}"] = sol.y[i]
       df = pd.DataFrame(data)
       csv = df.to_csv(index=False)
       st.download_button("CSVダウンロード", csv, file_name="ode_solution.csv", mime="text/csv")
