import streamlit as st
import numpy as np
from scipy.signal import find_peaks

### MAXIMUM AND MINIMUM FINDER ###
def max_min_finder (wl, vals):
    peaks_pos, _ = find_peaks(vals)
    peaks_neg, _ = find_peaks(-vals)

    wl_pos = wl[peaks_pos]
    wl_neg = wl[peaks_neg]
    vals_pos = vals[peaks_pos]
    vals_neg = vals[peaks_neg]
    
    mask = (wl_pos >= 380) & (wl_pos <= 780)
    wl_pos_range = wl_pos(mask)
    vals_pos_range = vals_pos(mask)
    peaks_pos_range = peaks_pos(mask)

    mask = (wl_neg >= 380) & (wl_neg <= 780)
    #wl_neg_range = wl_neg(mask)
    #vals_neg_range = vals_neg(mask)
    #peaks_neg_range = peaks_neg(mask)
    wl_cast = wl_neg(mask)
    vals_cast = vals_neg(mask)
    peaks_cast = peaks_neg(mask)
    
    #wl_cast = wl_pos[mask]
    #vals_cast = vals_pos[mask]
    #peaks_cast = peaks_pos[mask]

    return wl_cast, vals_cast, peaks_cast

### POINTS OF MAX SLOPE ###
def remove_background (wl, vals):
    peaks_pos, peaks_neg = max_min_finder (wl, vals)
    peaks_all = np.sort(np.concatenate([peaks_pos, peaks_neg]))
    #for i in peaks_pos:
    return peaks_all

# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
