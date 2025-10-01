import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
from visco.kdvisco import kdvisco_gui
from odesolver.ode import ode_gui

st.image("zkanics_full.png", caption="Supported by Zkanics F. P. S. since 2024", width=250)
st.markdown("---")

page = st.selectbox("計算を選択してください", ["SAFT EoS", "KD Viscosity", "ODE Solver"])
if page == "SAFT EoS":
    st.header("SAFT型状態方程式")
elif page == "KD Viscosity":
     kdvisco_gui()
elif page == "ODE Solver":
     ode_gui()
