import streamlit as st
import numpy as np
from scipy.integrate import solve_ivp
import numexpr as ne
import matplotlib.pyplot as plt
import pandas as pd

def ode_gui2():
    # --- ユーザー入力 ---
    st.write("変数を x1, x2, x3 ... のように表し、1行に1つの dXi/dt を入力してください")
    st.write("例: '-k1*x1 + k2*x2'")

    expr_text = st.text_area("反応速度式を入力 (1行に1つの式)",
                             value = "-k1*x1 + k2*x2\n k1*x1 - k2*x2")

    # パラメータ入力
    params_input = st.text_input("パラメータを辞書形式で入力 (例: {'k1':1.0,'k2':0.5})", value="{'k1':1.0,'k2':0.5}")
    params = eval(params_input)  # 注意: ユーザー入力で eval は安全性に注意

    # 初期値
    initial_values_input = st.text_input("初期値をリスト形式で入力 (例: [1.0, 0.0])", value="[1.0, 0.0]")
    Y0 = eval(initial_values_input)

    # 時間範囲
    t0 = st.number_input("開始時刻 t0", value=0.0)
    t1 = st.number_input("終了時刻 t1", value=10.0)
    n_points = st.number_input("分割数", value=100, step=1)

    # --- solve_ivp 関数定義 ---
    def ode_system(t, Y):
        local_dict = {f"x{i+1}": Y[i] for i in range(len(Y))}
        local_dict.update(params)
        local_dict["t"] = t
        dYdt = []
        for expr in expr_lines:
            dYdt.append(ne.evaluate(expr, local_dict))
            return dYdt

    # --- 実行 ---
    if st.button("シミュレーション実行"):
       expr_lines = [line.strip() for line in expr_text.splitlines() if line.strip() != ""]
       t_eval = np.linspace(t0, t1, int(n_points))
    
       sol = solve_ivp(ode_system, (t0, t1), Y0, t_eval=t_eval)

       # --- プロット ---
       fig, ax = plt.subplots(figsize=(6,4))
       for i in range(len(Y0)):
           ax.plot(sol.t, sol.y[i], label=f"x{i+1}")
       ax.set_xlabel("t")
       ax.set_ylabel("濃度 / 値")
       ax.set_title("連立反応速度式シミュレーション")
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
