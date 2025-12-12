import streamlit as st
import os
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

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

def spectrum_to_lab(wl_vis, vals_vis, df_xyz, df_ill, assume_percent=True):
    
    ### convert percent -> 0..1 if needed ###
    spec = vals_vis.copy().astype(float)
    
    if assume_percent:
       spec = spec / 100.0

    st.write(df_xyz)
    
    # interpolate cmf and illuminant to measured wavelengths
    #fx = interp1d(cmf_df['wl'], cmf_df['xbar'], bounds_error=False, fill_value=0.0)
    #fy = interp1d(cmf_df['wl'], cmf_df['ybar'], bounds_error=False, fill_value=0.0)
    #fz = interp1d(cmf_df['wl'], cmf_df['zbar'], bounds_error=False, fill_value=0.0)
    #fS = interp1d(illum_df['wl'], illum_df['S'], bounds_error=False, fill_value=0.0)

    #xbar = fx(meas_wl)
    #ybar = fy(meas_wl)
    #zbar = fz(meas_wl)
    #S = fS(meas_wl)

    #deltas = compute_deltas(meas_wl)

    #denom = np.sum(S * ybar * deltas)
    #if denom == 0:
    #    raise RuntimeError("Denominator for k is zero; check illuminant and cmf coverage.")
    #k = 100.0 / denom

    #X = k * np.sum(spec * S * xbar * deltas)
    #Y = k * np.sum(spec * S * ybar * deltas)
    #Z = k * np.sum(spec * S * zbar * deltas)

    # whitepoint (R=1)
    #Xn = k * np.sum(1.0 * S * xbar * deltas)
    #Yn = k * np.sum(1.0 * S * ybar * deltas)
    #Zn = k * np.sum(1.0 * S * zbar * deltas)

    #fx_ = f_lab(X / Xn)
    #fy_ = f_lab(Y / Yn)
    #fz_ = f_lab(Z / Zn)
    #L = 116.0 * fy_ - 16.0
    #a = 500.0 * (fx_ - fy_)
    #b = 200.0 * (fy_ - fz_)

    #return {"X":X, "Y":Y, "Z":Z, "L":L, "a":a, "b":b, "k":k, "white":{"Xn":Xn,"Yn":Yn,"Zn":Zn}}

def cielab_core (df):

    base_dir = os.path.dirname(__file__)
    xyz_path = os.path.join(base_dir, "CIE_xyz_1931_2deg.csv")
    ill_path = os.path.join(base_dir, "CIE_std_illum_D65.csv")
    df_xyz = pd.read_csv(xyz_path)
    df_ill = pd.read_csv(ill_path)   
    
    wl, vals = load_measurements (df)

    ### restrict to 380-780 nm ###
    mask = (wl >= 380.0) & (wl <= 780.0)
    wl_vis = wl[mask]
    vals_vis = vals[mask]
    #if wl_vis.size == 0:
    #    print("No data in 380-780 nm range. Exiting.")
    #    sys.exit(1)

    res = spectrum_to_lab(wl_vis, vals_vis, df_xyz, df_ill, assume_percent=True)
    
    
