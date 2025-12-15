import streamlit as st
import numpy as np
from scipy.signal import find_peaks

### MAXIMUM AND MINIMUM FINDER ###
def max_min_finder (wl, vals):
    peaks_pos, _ = find_peaks(vals)
    peaks_neg, _ = find_peaks(-vals)

    wl_pos = wl[peaks_pos]
    st.write(wl_pos)
    mask = wl_pos >= 380
    min_pos = peaks_pos[mask][np.argmin(wl_pos[mask] - 380)]
    st.write(min_pos)
    st.write(wl[min_pos])
    mask = wl_pos <= 780
    max_pos = peaks_pos[mask][np.argmax(wl_peaks[mask])]
    st.write(wl[max_pos])
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
