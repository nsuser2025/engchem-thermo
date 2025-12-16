import streamlit as st
import numpy as np
from scipy.signal import find_peaks

### MAXIMUM AND MINIMUM FINDER ###
def max_min_finder (wl, vals):
    peaks_pos, _ = find_peaks(vals)
    peaks_neg, _ = find_peaks(-vals)

    wl_pos = wl[peaks_pos]
    vals_pos = vals[peaks_pos]
    mask = wl_pos < 380
    if np.any(mask):
       min_pos_pre = peaks_pos[mask][np.argmax(wl_pos[mask])]
    else:
       min_pos_pre = None
    mask = wl_pos >= 380
    if np.any(mask):
       min_pos = peaks_pos[mask][np.argmin(wl_pos[mask] - 380)]
    else:
       min_pos = None 

    wl_neg = wl[peaks_neg]
    vals_neg = vals[peaks_neg]
    mask = wl_neg < 380
    if np.any(mask):
       min_neg_pre = peaks_neg[mask][np.argmax(wl_neg[mask])]
    else:
       min_neg_pre = None
    mask = wl_neg >= 380
    if np.any(mask):
       min_neg = peaks_neg[mask][np.argmin(wl_neg[mask] - 380)]
    else:
       min_neg = None 
    
    if wl[min_pos] > wl[min_neg] and min_pos_pre != None:
       idx_ini = min_pos_pre 
       wl_ini = wl[min_pos_pre]
       vl_ini = vals[min_pos_pre]
    elif wl[min_neg] > wl[min_pos] and min_neg_pre != None:
       idx_ini = min_neg_pre
       wl_ini = wl[min_neg_pre]
       vl_ini = vals[min_neg_pre] 

    mask = (wl_pos >= 380) & (wl_pos <= 780)
    wl_pos_range = wl_pos[mask]
    vals_pos_range = vals_pos[mask]
    peaks_pos_range = peaks_pos[mask]
    
    st.write('neko')
    st.write(peaks_pos)
    st.write(wl_pos)
    st.write(wl_pos_range)
    st.write(vals_pos_range)
    st.write(peaks_pos_range)
    
    
    #wl_sum = np.sort(np.concatenate([[wl_ini], wl_pos_range, wl_neg_range])) 
    #idx_sum = np.concatenate([[idx_ini], peaks_pos, peaks_neg])

    #order = np.argsort(wl_sum)
    #wl_sum = wl_sum[order]
    #idx_sum = idx_sum[order]
    #st.write(wl_sum)
    #st.write(idx_sum)
    
    return peaks_pos, peaks_neg

### POINTS OF MAX SLOPE ###
def remove_background (wl, vals):
    peaks_pos, peaks_neg = max_min_finder (wl, vals)
    peaks_all = np.sort(np.concatenate([peaks_pos, peaks_neg]))
    #for i in peaks_pos:
    return peaks_all

# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
