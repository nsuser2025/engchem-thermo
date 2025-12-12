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
    
    # sort ascending by wavelength
    order = np.argsort(wl)
    return wl[order], vals[order]
    
def cielab_core (df):

    base_dir = os.path.dirname(__file__)
    cie_path = os.path.join(base_dir, "CIE_xyz_1931_2deg.csv")
    ill_path = os.path.join(base_dir, "CIE_std_illum_D65.csv")
    df_cie = pd.read_csv(cie_path)
    df_ill = pd.read_csv(ill_path)   
    
    wl, vals = load_measurements (df)

    st.write(wl)
    st.write(vals)
    
