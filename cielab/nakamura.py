import streamlit as st
import numpy as np
from scipy.signal import find_peaks

### MAXIMUM AND MINIMUM FINDER ###
def max_min_finder (wl, vals):
    peaks_pos, _ = find_peaks(vals)
    peaks_neg, _ = find_peaks(-vals)

    wl_pos = wl[peaks_pos]
    #st.write(wl_pos)
    mask = wl_pos < 380
    if np.any(mask):
       min_pos_pre = peaks_pos[mask][np.argmax(wl_pos[mask])]
       #st.write(wl[min_pos_pre])
    else:
       min_pos_pre = None
    mask = wl_pos >= 380
    if np.any(mask):
       min_pos = peaks_pos[mask][np.argmin(wl_pos[mask] - 380)]
       #st.write(wl[min_pos])
    else:
       min_pos = None 
    mask = wl_pos <= 780
    if np.any(mask):
       max_pos = peaks_pos[mask][np.argmax(wl_pos[mask])]
       #st.write(wl[max_pos])
    else:
       max_pos = None

    wl_neg = wl[peaks_neg]
    #st.write(wl_neg)
    mask = wl_neg < 380
    if np.any(mask):
       min_neg_pre = peaks_neg[mask][np.argmax(wl_neg[mask])]
       #st.write(wl[min_neg_pre])
    else:
       min_neg_pre = None
    mask = wl_neg >= 380
    if np.any(mask):
       min_neg = peaks_neg[mask][np.argmin(wl_neg[mask] - 380)]
       #st.write(wl[min_neg])
    else:
       min_neg = None 
    mask = wl_neg <= 780
    if np.any(mask):
       max_neg = peaks_neg[mask][np.argmax(wl_neg[mask])]
       #st.write(wl[max_neg])
    else:
       max_neg = None

    
    if wl[min_pos] > wl[min_neg] and min_pos_pre != None:
       wl_ini = wl[min_pos_pre]
       vl_ini = vals[min_pos_pre]
    elif wl[min_neg] > wl[min_pos] and min_neg_pre != None:
       wl_ini = wl[min_neg_pre]
       vl_ini = vals[min_neg_pre] 
    #st.write(wl_ini)
    #st.write(vl_ini)
    wl_sum = np.sort(np.concatenate([wl_ini, wl_pos, wl_neg])) 
    st.write(wl_sum)
    
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
