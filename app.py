import streamlit as st
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Krieger–Dougherty式
def kd_viscosity(phi, eta0, eta_intrinsic, phi_max):
    return eta0 * (1 - phi/phi_max)**(-eta_intrinsic * phi_max)

page = st.selectbox("計算を選択してください", ["SAFT EoS", "KD Viscosity", "ODE Solver"])

if page == "SAFT EoS":
    st.header("SAFT型状態方程式")
    st.write("建設中！注意！")

elif page == "KD Viscosity":
    st.header("Krieger-Dougherty粘性推算")
    eta0 = st.number_input("基材粘度 [mPa・s]（def. エポキシ樹脂単体の粘度 1000）", value=1000)
    eta_intrinsic = st.number_input("固有粘度（形状依存性, def. 球体2.5）", value=2.5)
    phi_max_1 = st.number_input("最大充填体積分率（粒子1を隙間なく詰めたときの上限, def. 0.58）", value=0.58)
    phi_max_2 = st.number_input("最大充填体積分率（粒子2を隙間なく詰めたときの上限, def. 0.58）", value=0.58)
    bool_comp = st.checkbox("粒子1と2を比較しますか?")
    
    eta0 = float(eta0)
    eta_intrinsic = float(eta_intrinsic)
    phi_max_1 = float(phi_max_1)
    
    # 体積分率 φ の範囲
    phi = np.linspace(0, 0.55, 100)
    
    # 粒径による差を考慮（ここは概念的に分散性の違いを反映）
    # 119.3 nm: φ_max = 0.58
    # 295.4 nm: φ_max や [η] がわずかに変化した場合（分散性低下を仮定）
    eta_1 = kd_viscosity(phi, eta0, eta_intrinsic, phi_max_1)
    if bool_comp:
       eta_2 = kd_viscosity(phi, eta0, eta_intrinsic, phi_max_2)

    plot_placeholder = st.empty()
    
    if st.button("実行"):
       # プロット
       fig, ax = plt.subplots(figsize=(6,4))
       ax.plot(phi, eta_1, label='φmax: '+str(phi_max_1))
       if bool_comp:
          ax.plot(phi, eta_2, label='φmax: '+str(phi_max_2))
          st.write("粒子2のグラフも表示しています")
       ax.set_xlabel('φ')
       ax.set_ylabel('η [mPa·s]')
       ax.set_yscale('log')
       ax.set_title('Krieger–Dougherty Viscosity')
       ax.legend()
       ax.grid(True)
       plot_placeholder.pyplot(fig)
    
elif page == "ODE Solvedr":
    st.header("常微分方程式（ODE）ソルバー")
    st.write("SCIPY")
