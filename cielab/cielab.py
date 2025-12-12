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

### XYZ --> linear RGB ###
def xyz_to_linear_rgb(X, Y, Z):
    ### sRGB D65 ###
    M = np.array([[ 3.2406, -1.5372, -0.4986],
                  [-0.9689,  1.8758,  0.0415],
                  [ 0.0557, -0.2040,  1.0570]])
    XYZ = np.array([X, Y, Z]) / 100
    RGB = M.dot(XYZ) 
    return RGB

### linear RGB --> sRGB ###
def linear_to_srgb(RGB):
    def compand(c):
        c = np.clip(c, 0, 1)
        return np.where(c <= 0.0031308,
                        12.92 * c,
                        1.055 * c**(1/2.4) - 0.055)
    return compand(RGB)


def compute_deltas(wl):
    dw = np.diff(wl)
    if dw.size == 0:
        return np.array([1.0])
    if np.allclose(dw, dw[0]):
        return np.full_like(wl, dw[0], dtype=float)
    deltas = np.empty_like(wl, dtype=float)
    deltas[0] = wl[1] - wl[0]
    deltas[-1] = wl[-1] - wl[-2]
    deltas[1:-1] = 0.5 * (wl[2:] - wl[:-2])
    return deltas
    
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
    
    # interpolate cmf and illuminant to measured wavelengths
    fx_bar = interp1d(df_xyz['wl'], df_xyz['xbar'], bounds_error=False, fill_value=0.0)
    fy_bar = interp1d(df_xyz['wl'], df_xyz['ybar'], bounds_error=False, fill_value=0.0)
    fz_bar = interp1d(df_xyz['wl'], df_xyz['zbar'], bounds_error=False, fill_value=0.0)
    fs = interp1d(df_ill['wl'], df_ill['S'], bounds_error=False, fill_value=0.0)

    xbar = fx_bar(wl_vis)
    ybar = fy_bar(wl_vis)
    zbar = fz_bar(wl_vis)
    s = fs(wl_vis)

    deltas = compute_deltas(wl_vis)

    denom = np.sum(s * ybar * deltas)
    if denom == 0:
       st.error("❌ k の分母が 0 です。照明光（illuminant）と色度関数（CMF）の波長範囲を確認してください。")
       st.stop()

    k = 100.0 / denom

    X = k * np.sum(spec * s * xbar * deltas)
    Y = k * np.sum(spec * s * ybar * deltas)
    Z = k * np.sum(spec * s * zbar * deltas)

    ### whitepoint (R=1) ###
    Xn = k * np.sum(1.0 * s * xbar * deltas)
    Yn = k * np.sum(1.0 * s * ybar * deltas)
    Zn = k * np.sum(1.0 * s * zbar * deltas)

    fx = f_lab (X / Xn)
    fy = f_lab (Y / Yn)
    fz = f_lab (Z / Zn)
    L = (116.0 * fy) - 16.0
    a = 500.0 * (fx - fy)
    b = 200.0 * (fy - fz)

    return {"X":X, "Y":Y, "Z":Z, "L":L, "a":a, "b":b, "k":k, "white":{"Xn":Xn,"Yn":Yn,"Zn":Zn}}

def cielab_core (df):

    base_dir = os.path.dirname(__file__)
    xyz_path = os.path.join(base_dir, "CIE_xyz_1931_2deg.csv")
    ill_path = os.path.join(base_dir, "CIE_std_illum_D65.csv")
    df_xyz = pd.read_csv(xyz_path, header=None, names=["wl", "xbar", "ybar", "zbar"])
    df_ill = pd.read_csv(ill_path, header=None, names=["wl", "S"])   
    
    wl, vals = load_measurements (df)

    ### restrict to 380-780 nm ###
    mask = (wl >= 380.0) & (wl <= 780.0)
    wl_vis = wl[mask]
    vals_vis = vals[mask]
    #if wl_vis.size == 0:
    #    print("No data in 380-780 nm range. Exiting.")
    #    sys.exit(1)

    res = spectrum_to_lab(wl_vis, vals_vis, df_xyz, df_ill, assume_percent=True)
    
    st.write("Using illuminant:", "D65")
    st.write("k =", res["k"])
    st.write("XYZ = {:.6f}, {:.6f}, {:.6f}".format(res["X"], res["Y"], res["Z"]))
    st.write("Lab L*, a*, b* = {:.4f}, {:.4f}, {:.4f}".format(res["L"], res["a"], res["b"]))
    
    X, Y, Z = res["X"], res["Y"], res["Z"]
    linear_rgb = xyz_to_linear_rgb(X, Y, Z)
    srgb = linear_to_srgb(linear_rgb)

    ### 色の矩形表示 ###
    r, g, b_ = (srgb * 255).astype(int)
    #st.markdown(f"<div style='width:100px;height:50px;background-color:rgb({r},{g},{b_});'></div>", unsafe_allow_html=True)
    st.markdown(f"""<div style="width:300px;height:150px;background-color: rgb({r},{g},{b_});border: 3px solid gray;"></div>""",unsafe_allow_html=True)
