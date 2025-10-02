import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io

# KRIEGER-DOUGHERTY VISCOSITY MODEL
def kd_viscosity(phi, eta0, eta_intrinsic, phi_max):
    return eta0 * (1 - phi/phi_max)**(-eta_intrinsic * phi_max)

def kdvisco_gui():
    st.markdown("---")
    st.markdown("#### Krieger-Dougherty 粘性推算")
    st.markdown("""固体粒子が高濃度に分散している懸濁液の粘性を簡単に推算するための経験式です。""")
    st.latex(r"\eta = \eta_{0}\biggl( 1 - \frac{\phi}{\phi_{\rm max}} \biggr)^{-[\eta]\phi_{\rm max}}")
    st.markdown("""$$\eta_{0}$$: 基材粘度""")
    st.markdown("""[η]: 固有粘度（粉体が球体であれば2.5のままでOKです）""")
    st.markdown("""Φmax: 最大充填体積分率（粘度を決める最も重要な因子です。離散要素法や実験で決められることが多いです。）""")
    st.markdown("---")
        
    eta0 = st.number_input("基材粘度 [mPa・s]（def. エポキシ樹脂単体の粘度 1000）", value=1000)
    eta_intrinsic = st.number_input("固有粘度（形状依存性, def. 球体2.5）", value=2.5)
    phi_max_1 = st.number_input("最大充填体積分率（粒子1を隙間なく詰めたときの上限, def. 0.58）", value=0.58)
    phi_max_2 = st.number_input("最大充填体積分率（粒子2を隙間なく詰めたときの上限, def. 0.58）", value=0.58)
    bool_comp = st.checkbox("粒子1と2を比較しますか?")
    
    # CALCULATE KRIEGER-DOUGHERTY VISCOSITY MODEL 
    phi = np.linspace(0, 0.55, 100)
    eta_1 = kd_viscosity(phi, eta0, eta_intrinsic, phi_max_1)
    if bool_comp:
       eta_2 = kd_viscosity(phi, eta0, eta_intrinsic, phi_max_2)

    # SESSION BUTTON
    bool_execute = st.button("実行")

    # INITIALIZE SESSION_STATE
    if "fig" not in st.session_state:
        st.session_state["fig"] = None
    if "df" not in st.session_state:
        st.session_state["df"] = None

    # SESSION START
    if bool_execute:
       # SESSION_STATE SAVE: FIGURE
       fig, ax = plt.subplots(figsize=(6,4))
       ax.plot(phi, eta_1, label='φmax: '+str(phi_max_1))
       if bool_comp:
          ax.plot(phi, eta_2, label='φmax: '+str(phi_max_2))
       ax.set_xlabel('φ')
       ax.set_ylabel('η [mPa·s]')
       ax.set_yscale('log')
       ax.set_title('Krieger–Dougherty Viscosity')
       ax.legend()
       ax.grid(True)
       st.session_state["fig"] = fig
       # SESSION_STATE SAVE: DF
       data = {"phi": phi, "eta_1": eta_1}
       if bool_comp:
          data["eta_2"] = eta_2
       df = pd.DataFrame(data)
       st.session_state["df"] = df

    # DISPLAY SAVED FIGURE AND DATA
    if st.session_state["fig"] is not None:
       st.pyplot(st.session_state["fig"])
       buf = io.BytesIO()
       st.session_state["fig"].savefig(buf, format="png")
       buf.seek(0)
       st.download_button("📥 PNG ダウンロード", data=buf, file_name="plot.png", mime="image/png")
    if st.session_state["df"] is not None:
        st.dataframe(st.session_state["df"])
        csv = st.session_state["df"].to_csv(index=False)
        st.download_button("📥 CSV ダウンロード", data=csv, file_name="viscosity.csv", mime="text/csv")

# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
