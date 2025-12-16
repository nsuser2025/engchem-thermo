import streamlit as st
import numpy as np
from scipy.signal import find_peaks

### MAXIMUM AND MINIMUM FINDER ###
def max_min_finder (wl, vals):
    peaks_pos, _ = find_peaks(vals)
    peaks_neg, _ = find_peaks(-vals)

    wl_pos = wl[peaks_pos]
    mask = wl_pos < 380
    if np.any(mask):
       min_pos_pre = peaks_pos[mask][np.argmax(wl_pos[mask])]
    else:
       min_pos_pre = None
    
    #mask = wl_pos < 380
    #min_pos_pre = peaks_pos[mask][np.argmax(wl_pos[mask])]
    #mask = wl_pos >= 380
    #min_pos = peaks_pos[mask][np.argmin(wl_pos[mask] - 380)]
    #mask = wl_pos <= 780
    #max_pos = peaks_pos[mask][np.argmax(wl_pos[mask])]
    
    st.write(wl_pos)
    st.write(wl[min_pos_pre])
    
    #st.write(wl[min_pos])
    #st.write(wl[max_pos])

    #wl_neg = wl[peaks_neg]
    #mask = wl_neg >= 380
    #min_neg = peaks_neg[mask][np.argmin(wl_neg[mask] - 380)]
    #mask = wl_neg <= 780
    #max_neg = peaks_neg[mask][np.argmax(wl_neg[mask])]
    
    #if wl[min_pos] > wl[min_neg]:
    #   wl_ini = wl_pos[min_pos-1]
    #elif wl[min_neg] > wl[min_pos]:
    #   wl_ini = wl_neg[min_neg-1]
    #st.write(wl_ini)    
    
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
