import streamlit as st

def cielab_overview():
    with st.expander("CIE L$^{*}$a$^{*}$b$^{*}$変換の概要"):
         st.markdown(r"""色の見え方を定量的に扱うために, 色を色空間上の座標として表す方法が用いられます.  
                         CIE L$^{*}$a$^{*}$b$^{*}$空間では「座標間距離 $\approx$ 人間が感じる色差」
                         が成り立つように設計されています.""")
         st.markdown(r"""L$^{*}$（明度）: 0–100  
                         a$^{*}$：赤（＋）$\leftrightarrow$ 緑（−）  
                         b$^{*}$：黄（＋）$\leftrightarrow$ 青（−）""")
        
         st.markdown(r"""本アプリでは透過/吸収スペクトルの波長領域を380–780 nmに限定しています.  
                         これは, 380 nm未満, 780 nmを超える波長は人間が色として知覚できないためです.""")
