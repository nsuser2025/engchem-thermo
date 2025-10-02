import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
from visco.kdvisco import kdvisco_gui
from odesolver.ode_gui2 import ode_gui2
from pic2xlsx.main import pic2xlsx_gui

st.image("zkanics_cute_logo.png", caption="Supported by Zkanics F. P. S. since 2024", width=250)
st.markdown("---")

page = st.selectbox("計算を選択してください", ["SAFT", "KD Viscosity", "ODE Solver", "PIC2XLSX"])
if page == "SAFT":
     st.header("SAFT Theory")
elif page == "KD Viscosity":
     kdvisco_gui ()
elif page == "ODE Solver":
     ode_gui2 ()
elif page == "PIC2XLSX":
     pic2xlsx_gui ()
