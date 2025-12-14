import streamlit as st

def cielab_overview():
    with st.expander("CIE Lab変換の概要"):
         st.markdown(r"""色の見え方を定量的に扱うために, 色を色空間上の座標として表す方法が用いられます.
                         L*a*b*座標系は, 座標間距離 $\approx$ 知覚色差""")
         #- **L\***：明度（0–100）
         #- **a\***：赤（＋）↔ 緑（−）
         #- **b\***：黄（＋）↔ 青（−）
         #a\* や b\* が負になるのは正常です。""")
