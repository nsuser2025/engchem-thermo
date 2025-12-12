import streamlit as st
import os
import pandas as pd
import numpy as np

def load_measurements (df):
    #try:
    #    df = pd.read_csv(path)
    #except Exception:
    #    df = pd.read_csv(path, header=None)
    
    wl = df.iloc[:,0].to_numpy(dtype=float)
    vals = df.iloc[:,1].to_numpy(dtype=float)
    
    ### sort ascending by wavelength ###
    order = np.argsort(wl)
    return wl[order], vals[order]

def f_lab(t):
    delta = 6.0 / 29.0
    delta2 = delta * delta
    delta3 = delta2 * delta
    if t > delta3:
        return t**(1/3)
    else:
        return (t / (3 * delta2)) + (4.0 / 29.0)

def cielab_core (df):

    base_dir = os.path.dirname(__file__)
    cie_path = os.path.join(base_dir, "CIE_xyz_1931_2deg.csv")
    ill_path = os.path.join(base_dir, "CIE_std_illum_D65.csv")
    df_cie = pd.read_csv(cie_path)
    df_ill = pd.read_csv(ill_path)   
    
    wl, vals = load_measurements (df)

    ### restrict to 380-780 nm ###
    mask = (wl >= 380.0) & (wl <= 780.0)
    wl_vis = wl[mask]
    vals_vis = vals[mask]
    #if wl_vis.size == 0:
    #    print("No data in 380-780 nm range. Exiting.")
    #    sys.exit(1)

    st.write(wl_vis)
    #st.write(vals)
    
