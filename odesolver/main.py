import ast
import streamlit as st
import numpy as np
from scipy.integrate import solve_ivp
import numexpr as ne
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d.art3d import Line3DCollection
import pandas as pd

# DEFINE THE FUNCTIONS
def ode_system(t, Y):
    local_dict = {f"x{i+1}": Y[i] for i in range(len(Y))}
    local_dict.update(params)
    local_dict["t"] = t
    dYdt = []
    for expr in expr_lines:
        dYdt.append(ne.evaluate(expr, local_dict))
    return dYdt

# MAIN PART OF ODE SOLVER GUI
def ode_gui():
    
    # EXPLANATIONS
    st.markdown("---")
    st.markdown("#### ODE Solver（作成中）")
    st.markdown("""例）化学反応の濃度変化(d[A]/dt)は常微分方程式（ODE）で表されます。例えば単純な一次反応なら次のODEに従います。""")
    st.latex(r"\frac{d [A]}{dt} = -k[A]")
    st.markdown("""時刻t=0の[A]の値（初期値）を用いてODEを解けば、任意の時刻における[A]を決めることができます。これを初期値問題といいます。
                 ODE Solverは、ユーザーが入力したODEの式（上式では右辺）、パラメータの値、初期値から初期値問題を解くツールです。""") 
    examples = ["ローレンツアトラクター", "シュレディンガー方程式（未）", "拡散方程式（未）", "反応速度式（未）", "テスト"]
    option_examples = st.radio("入力例：", examples, index = 0, horizontal = True)
    st.markdown("---")
    
    # EXAMPLES
    if option_examples == "テスト":
       default_input = "-k1*x1 + k2*x2\n k1*x1 - k2*x2"
       default_param = "{'k1':1.0,'k2':0.5}"
       default_initi = "[1.0, 0.0]"
    elif option_examples == "ローレンツアトラクター":
       default_input = "-p * x1 + p * x2\n -x1 * x3 + r * x1 - x2\n x1 * x2 - (b/c) * x3"
       default_param = "{'p':10.0,'r':28.0,'b':8.0,'c':3.0}"
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
        expr_lines = [line.strip() for line in expr_text.splitlines() if line.strip() != ""]
        if len(parsed_Y0) != len(expr_lines):
           st.error("初期値の数とODE式の数が一致しません")
           st.stop()
    except Exception as e:
        st.error(f"初期値の読み込みに失敗しました: {e}")
        st.stop()
    Y0 = parsed_Y0

    # INPUTS: TIME SPAN
    t0 = st.number_input("開始時刻 t0", value=0.0, min_value=0.0, max_value=1e5)
    t1 = st.number_input("終了時刻 t1", value=10.0, min_value=0.0, max_value=1e5)
    n_points = st.number_input("分割数", value=100, min_value=1, max_value=10000, step=1)

    # INPUTS: GRAPH INFORMATION (2D PLOT)
    graph_title = st.text_input("グラフタイトル（2次元プロット）", value='ODE SOLUTION')
    graph_xlabel = st.text_input("X軸ラベル（2次元プロット）", value='TIME')
    graph_ylabel = st.text_input("Y軸ラベル（2次元プロット）", value='VARIABLES')

    # INPUTS: GRAPH INFORMATION (3D PLOT)
    option_3dplot = st.radio("3次元プロット:", ["OFF", "ON"], index = 0, horizontal = True)
    if option_3dplot == "ON":
       graph_title3d = st.text_input("グラフタイトル（3次元プロット）", value='ODE SOLUTION 3D PLOT')
       graph_xlabel3d = st.text_input("X軸ラベル（3次元プロット）", value='x1')
       graph_ylabel3d = st.text_input("Y軸ラベル（3次元プロット）", value='x2')
       graph_zlabel3d = st.text_input("Z軸ラベル（3次元プロット）", value='x3')
       x_var = st.text_input("X軸の変数（3次元プロット）", value="x1")
       y_var = st.text_input("Y軸の変数（3次元プロット）", value="x2")
       z_var = st.text_input("Z軸の変数（3次元プロット）", value="x3")
    
    # SESSION BUTTON
    bool_execute = st.button("実行")

    # INITIALIZE SESSION_STATE
    if "fig2d" not in st.session_state:
        st.session_state["fig2d"] = None
    if "df" not in st.session_state:
        st.session_state["df"] = None

    # SESSION START
    if bool_execute:

       # SOLVE INITIAL PROBLEMS
       expr_lines = [line.strip() for line in expr_text.splitlines() if line.strip() != ""]
       t_eval = np.linspace(t0, t1, int(n_points))
       sol = solve_ivp(ode_system, (t0, t1), Y0, t_eval=t_eval)

       # SESSION_STATE SAVE: FIGURE2D
       fig2d, ax = plt.subplots(figsize=(6,4))
       for i in range(len(Y0)):
           ax.plot(sol.t, sol.y[i], label=f"x{i+1}")
       ax.set_xlabel(graph_xlabel)
       ax.set_ylabel(graph_ylabel)
       ax.set_title(graph_title)
       ax.legend()
       ax.grid(True)
       st.session_state["fig2d"] = fig2d
       #st.pyplot(fig2d)
    
       # CSV DOWNLOAD
       data = {"t": sol.t}
       for i in range(len(Y0)):
           data[f"x{i+1}"] = sol.y[i]
       df = pd.DataFrame(data)
       st.session_state["df"] = df
       #csv = df.to_csv(index=False)
       #st.download_button("CSVダウンロード", csv, file_name="ode_solution.csv", mime="text/csv")

       # DISPLAY SAVED FIGURE AND DATA
       if st.session_state["fig2d"] is not None:
          st.pyplot(st.session_state["fig2d"])
          buf = io.BytesIO()
          st.session_state["fig"].savefig(buf, format="png")
          buf.seek(0)
          st.download_button("📥 PNG ダウンロード", data=buf, file_name="plot2d.png", mime="image/png")
       if st.session_state["df"] is not None:
          st.dataframe(st.session_state["df"])
          csv = st.session_state["df"].to_csv(index=False)
        
       # 3D PLOT
       if option_3dplot == "ON":
          
          # ERROR MESSAGE
          if sol.y.shape[0] < 3:
             st.error("3Dプロットには変数が3つ以上必要です")
             st.stop()

          num_vars = sol.y.shape[0]
          var_options = [f"x{i+1}" for i in range(num_vars)]
          try:
              x_idx = var_options.index(x_var)
              y_idx = var_options.index(y_var)
              z_idx = var_options.index(z_var)
          except ValueError:
              st.error("3Dプロットに用いる変数が存在ていないようです。x1, x2, x3 のように入力してください。")
              st.stop()
           
          x_data, y_data, z_data = sol.y[x_idx], sol.y[y_idx], sol.y[z_idx]
           
          fig = plt.figure(figsize=(8, 6))
          ax = fig.add_subplot(111, projection="3d")

          points = np.array([x_data, y_data, z_data]).T.reshape(-1, 1, 3)
          segments = np.concatenate([points[:-1], points[1:]], axis=1)

          norm = Normalize(t_eval.min(), t_eval.max())
          lc = Line3DCollection(segments, cmap='plasma', norm=norm)
          lc.set_array(t_eval[:-1])
          lc.set_linewidth(0.5)

          ax.add_collection(lc)
          fig.colorbar(lc, ax=ax, label="Time", pad=0.1, fraction=0.02)
          ax.set_xlabel(graph_xlabel3d)
          ax.set_ylabel(graph_ylabel3d)
          ax.set_zlabel(graph_zlabel3d)
          ax.set_title(graph_title3d)
          ax.set_xlim(x_data.min(), x_data.max())
          ax.set_ylim(y_data.min(), y_data.max())
          ax.set_zlim(z_data.min(), z_data.max())
          plt.tight_layout()
          st.pyplot(fig)
