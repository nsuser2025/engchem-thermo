
# 条件を指定して結果ファイル名を返す
def condition_selector(df, images, key_prefix=""):
    selected_exam = st.selectbox("試験を選んでください", ["指定しない"]+df["試験"].unique().tolist(), key=f"exam_{key_prefix}")
    selected_face = st.selectbox("測定面を選んでください", ["指定しない"]+df["測定面"].unique().tolist(), key=f"face_{key_prefix}")
    selected_cath = st.selectbox("正極を選んでください", ["指定しない"]+df["正極"].unique().tolist(), key=f"cath_{key_prefix}") 
    selected_mesu = st.selectbox("測定を選んでください", ["指定しない"]+df["測定"].unique().tolist(), key=f"mesu_{key_prefix}")
    selected_elec = st.selectbox("電解液を選んでください", ["指定しない"]+df["電解液"].unique().tolist(), key=f"elec_{key_prefix}")
    selected_magn = st.selectbox("倍率を選んでください", ["指定しない"]+df["倍率"].unique().tolist(), key=f"magn_{key_prefix}")

    
