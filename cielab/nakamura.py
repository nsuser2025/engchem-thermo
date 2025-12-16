import streamlit as st
import numpy as np
from scipy.signal import find_peaks

### INITIAL POINT ###
def ini_finder (wl_pos, wl_neg, vals_pos, vals_neg, wl_pos_range, wl_neg_range):

    if wl_pos_range[0] > wl_neg_range[0]:
       mask = wl_pos < 380
       if np.any(mask):
          nearest_idx_in_mask = np.argmax(wl_pos[mask])
          nearest_idx = np.where(mask)[0][nearest_idx_in_mask]
          wl_ini  = wl_pos[nearest_idx]
          vals_ini = vals_pos[nearest_idx]
       else:
          wl_ini = None
          vals_ini = None
    elif wl_neg_range[0] > wl_pos_range[0]:
       mask = wl_neg < 380
       if np.any(mask):
          nearest_idx_in_mask = np.argmax(wl_neg[mask])
          nearest_idx = np.where(mask)[0][nearest_idx_in_mask]
          wl_ini  = wl_neg[nearest_idx]
          vals_ini = vals_neg[nearest_idx]
       else:
          wl_ini = None
          vals_ini = None
         
    return wl_ini, vals_ini    
        
### MAXIMUM AND MINIMUM FINDER ###
def max_min_finder (wl, vals):
    peaks_pos, _ = find_peaks(vals)
    peaks_neg, _ = find_peaks(-vals)

    wl_pos = wl[peaks_pos]
    wl_neg = wl[peaks_neg]
    vals_pos = vals[peaks_pos]
    vals_neg = vals[peaks_neg]
    
    mask = (wl_pos >= 380) & (wl_pos <= 780)
    wl_pos_range = wl_pos[mask]
    vals_pos_range = vals_pos[mask]
    peaks_pos_range = peaks_pos[mask]

    mask = (wl_neg >= 380) & (wl_neg <= 780)
    wl_neg_range = wl_neg[mask]
    vals_neg_range = vals_neg[mask]
    peaks_neg_range = peaks_neg[mask]

    wl_ini, vals_ini = ini_finder (wl_pos, wl_neg, vals_pos, vals_neg, wl_pos_range, wl_neg_range)
    
    wl_all = np.concatenate([[wl_ini], wl_pos_range, wl_neg_range])
    vals_all = np.concatenate([[vals_ini], vals_pos_range, vals_neg_range])

    order = np.argsort(wl_all)
    wl_cast = wl_all[order]
    vals_cast = vals_all[order]

    return wl_cast, vals_cast

### LINEAR SPECTRUM GENERATOR ###
def linear_spectrum (wl_grid, vals_i, wl_maxmin, vals_maxmin):
    wl_mid = []
    vals_mid = []
    for i in range(len(wl_maxmin)-1):
        wl_mid_value = 0.50 * (wl_maxmin[i] + wl_maxmin[i+1])
        mask = wl_grid <= wl_mid_value
        idx_in_mask = np.argmax(wl_grid[mask])
        idx = np.where(mask)[0][idx_in_mask]
        wl_mid += [wl_grid[idx]]
        vals_mid += [vals_i[idx]]
    wl_mid = np.array(wl_mid)
    vals_mid = np.array(vals_mid)
    st.write(wl_mid)
    st.write(vals_mid)
    vals_cast = vals_mid
    return vals_cast
    
# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
