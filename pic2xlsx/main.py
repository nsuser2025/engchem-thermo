import streamlit as st
import os
import pandas as pd
from PIL import Image
import pytesseract

def pic2xlsx_gui():
    st.markdown("---")
    st.markdown("#### Picuture to Excel（PIC2XLSX）")
    st.markdown("---")
    uploaded_file = st.file_uploader("画像をアップロードしてください", type=["png", "jpg", "jpeg"])
    
    # SESSION BUTTON
    #bool_execute = st.button("実行")

    if "df" not in st.session_state:
        st.session_state["df"] = None

    # SESSION START
    #if bool_execute:
    #   # SESSION_STATE SAVE: FIGURE
    #   fig, ax = plt.subplots(figsize=(6,4))
    #   ax.plot(phi, eta_1, label='φmax: '+str(phi_max_1))
    #   if bool_comp:
    #      ax.plot(phi, eta_2, label='φmax: '+str(phi_max_2))
    #   ax.set_xlabel('φ')
    #   ax.set_ylabel('η [mPa·s]')
    #   ax.set_yscale('log')
    #   ax.set_title('Krieger–Dougherty Viscosity')
    #   ax.legend()
    #   ax.grid(True)
    #   st.session_state["fig"] = fig
    #   # SESSION_STATE SAVE: DF
    #   data = {"phi": phi, "eta_1": eta_1}
    #   if bool_comp:
    #      data["eta_2"] = eta_2
    #   df = pd.DataFrame(data)
    #   st.session_state["df"] = df

    ## DISPLAY SAVED FIGURE AND DATA
    #if st.session_state["fig"] is not None:
    #   st.pyplot(st.session_state["fig"])
    #   buf = io.BytesIO()
    #   st.session_state["fig"].savefig(buf, format="png")
    #   buf.seek(0)
    #   st.download_button("📥 PNG ダウンロード", data=buf, file_name="plot.png", mime="image/png")
    #if st.session_state["df"] is not None:
    #    st.dataframe(st.session_state["df"])
    #    csv = st.session_state["df"].to_csv(index=False)
    #    st.download_button("📥 CSV ダウンロード", data=csv, file_name="viscosity.csv", mime="text/csv")

# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
