import streamlit as st
import io
import pandas as pd
from typing import List
from PIL import Image
from .mkcsv import mkcsv_gui
from .cielab import cielab_core

def cielab_gui():

    # EXPLANATIONS
    st.markdown("#### CIE Lab変換")
    st.markdown("""
    透過率/反射率スペクトルのCIE Lab変換アプリです. 
    標準光源D65およびCIE1931等色関数に基づき, 透過光/反射光の知覚色を近似的に表示します. 
    表示色は実際の観察条件下で見える色を正確に再現するものではありません.
    このアプリにアップロードした情報は全てメモリ上に保存されます.
    セッションの終了と同時にサーバー上のスペクトル情報は完全に消去されます.
    また, 出力されるCSVにはコードインジェクションの無効化処理が施されています.
    安心してダウンロードしてください.""") 
    #st.latex(r"\eta = \eta_{0}\biggl( 1 - \frac{\phi}{\phi_{\rm max}} \biggr)^{-[\eta]\phi_{\rm max}}")
    #st.markdown(r"""$$\eta_{0}$$: 基材粘度（粉体を一切含まない基材の粘度）""")
    #st.markdown(r"$\left[ \eta \right]$: 固有粘度（粉体が球体であれば2.5のままでOK）")
    #st.markdown(r"""$$\phi_{\mathrm{max}}$$: 最大充填体積分率（粘度を決める最も重要なパラメータ。離散要素法や実験から決める。）""")
    st.markdown("---")
    
    # INITIALIZE SESSIONS
    if 'data_df' not in st.session_state:
        st.session_state.data_df = None
    if 'condition_count' not in st.session_state:
        st.session_state.condition_count = 1
        
    # CSV FILE READER
    uploaded_file = st.file_uploader("透過率スペクトルのExcel/CSVファイルをアップロード", 
                    type=["xlsx", "xls", "xlsm", "csv"])
    
    st.markdown("---")
    mode_spec = st.radio("スペクトル種別", ["透過率", "反射率"], horizontal=True)
    mode_intp = st.radio("補間方法", ["なし", "線形", "3次スプライン"], horizontal=True)
    st.markdown("---")

    if uploaded_file:
       df = mkcsv_gui(uploaded_file)
       ### ERROR MESSAGES ###
       if df.shape[1] < 2:
          st.error("波長・スペクトルのペアになっていません")
          st.stop()
       if df.shape[1] % 2 != 0:
          st.error("列数が奇数です（波長・スペクトルのペアになっていません）")
          st.stop()
       ### CIELAB ### 
       st.session_state.data_df = df
       st.markdown("---")
       for i in range(0, df.shape[1], 2):
           wl = df.iloc[:, i]
           spec = df.iloc[:, i+1]
           df_pair = pd.DataFrame({"wl": wl,"spec": spec})
           cielab_core (mode_spec, mode_intp, df_pair)
       st.markdown("---") 
    
    df = st.session_state.data_df
    if df is None:
       st.info("データファイル（CSV）をアップロードしてください。")
       return
    
    st.markdown("---")

# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
