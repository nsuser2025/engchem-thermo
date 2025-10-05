import ast
import streamlit as st
import numpy as np
from scipy.integrate import solve_ivp
import numexpr as ne
import matplotlib.pyplot as plt
import pandas as pd

def ode_gui():
    # EXPLANATIONS
    st.markdown("---")
    st.markdown("#### ODE Solver（作成中）")
    st.markdown("""例）化学反応の濃度変化(d[A]/dt)は常微分方程式（ODE）で表されます。例えば単純な一次反応なら次のODEに従います。""")
    st.latex(r"\frac{d [A]}{dt} = -k[A]")
    st.markdown("""時刻t=0の[A]の値（初期値）を用いてODEを解けば、任意の時刻における[A]を決めることができます。これを初期値問題といいます。
                 ODE Solverは、ユーザーが入力したODEの式（上式では右辺）、パラメータの値、初期値から初期値問題を解くツールです。""")    
    option = st.radio("入力例：",("ローレンツアトラクター", "シュレディンガー方程式", "拡散方程式", "反応速度式（1次）", "テスト"), horizontal=True)
    st.markdown("---")
    # EXAMPLES
    if option == "テスト":
       default_input = "-k1*x1 + k2*x2\n k1*x1 - k2*x2"
       default_param = "{'k1':1.0,'k2':0.5}"
       default_initi = "[1.0, 0.0]"
    elif option == "ローレンツアトラクター":
       default_input = "-p * x + p * y\n -x * z + r * x - y\n x * y - b * z"
       default_param = "{'p':10.0,'r':28.0,'b':8.0/3.0}"
       default_initi = "[1.0, 0.0, 0.0]"
    
    # INPUTS: ODE
    st.write("変数を x1, x2, x3 ... のように表し、1行に1つのODE（dxi/dt）を入力してください")
    expr_text = st.text_area("常微分方程式を入力 (1行に1つの式)",
                             value = default_input)
    # INPUTS: PARAMETERS
    params_input = st.text_input("パラメータ（例: {'k1':1.0,'k2':0.5}）", 
                                 value = default_param)
    try:
        parsed_params = ast.literal_eval(params_input)
        if not isinstance(parsed_params, dict):
           st.error("パラメータは辞書形式（例: {'k1':1.0,'k2':0.5}）で入力してください。")
           st.stop()
        for key, val in parsed_params.items():
            if not isinstance(val, (int, float)):
               st.error(f"パラメータ {key} の値が数値ではありません")
               st.stop()
    except Exception as e:
        st.error(f"パラメータの読み込みに失敗しました: {e}")
        st.stop()
    params = parsed_params
    
    # INPUTS: INITIAL CONDITIONS
    initial_values_input = st.text_input("初期値（例: [1.0, 0.0]）", 
                                         value = default_initi)
    try:
        parsed_Y0 = ast.literal_eval(initial_values_input)
        if not isinstance(parsed_Y0, list):
           st.error("初期値はリスト形式で入力してください。")
           st.stop()
        if not all(isinstance(x, (int, float)) for x in parsed_Y0):
           st.error("リストの中身はすべて数値にしてください。")
           st.stop()
        if len(parsed_Y0) == 0:
           st.error("初期値リストは空にできません。")
           st.stop()
    except Exception as e:
        st.error(f"初期値の読み込みに失敗しました: {e}")
        st.stop()
    Y0 = parsed_Y0

    # INPUTS: TIME SPAN
    t0 = st.number_input("開始時刻 t0", value=0.0, min_value=0.0, max_value=1e5)
    t1 = st.number_input("終了時刻 t1", value=10.0, min_value=0.0, max_value=1e5)
    n_points = st.number_input("分割数", value=100, min_value=1, max_value=10000, step=1)

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

       # FIGURE PLOT
       fig, ax = plt.subplots(figsize=(6,4))
       for i in range(len(Y0)):
           ax.plot(sol.t, sol.y[i], label=f"x{i+1}")
       ax.set_xlabel("t")
       ax.set_ylabel(graph_ylabel)
       ax.set_title(graph_title)
       ax.legend()
       ax.grid(True)
       st.pyplot(fig)
    
       # CSV DOWNLOAD
       data = {"t": sol.t}
       for i in range(len(Y0)):
           data[f"x{i+1}"] = sol.y[i]
       df = pd.DataFrame(data)
       csv = df.to_csv(index=False)
       st.download_button("CSVダウンロード", csv, file_name="ode_solution.csv", mime="text/csv")
