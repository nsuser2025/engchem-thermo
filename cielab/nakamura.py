import streamlit as st
import numpy as np
from scipy.signal import find_peaks

### MAXIMUM AND MINIMUM FINDER ###
def max_min_finder (wl, vals):
    peaks_pos, _ = find_peaks(vals)
    peaks_neg, _ = find_peaks(-vals)

    wl_pos = wl[peaks_pos]
    mask = wl_pos >= 380
    min_pos = peaks_pos[mask][np.argmin(wl_pos[mask] - 380)]
    mask = wl_pos <= 780
    max_pos = peaks_pos[mask][np.argmax(wl_pos[mask])]

    wl_neg = wl[peaks_neg]
    st.write(wl_neg)
    mask = wl_neg >= 380
    min_neg = peaks_neg[mask][np.argmin(wl_neg[mask] - 380)]
    st.write(wl[min_neg])
    mask = wl_neg <= 780
    max_neg = peaks_neg[mask][np.argmax(wl_neg[mask])]
    st.write(wl[max_neg])
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
