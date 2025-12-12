import streamlit as st


def cielab_core (df):

    base_dir = os.path.dirname(__file__)
    cie_path = os.path.join(base_dir, "CIE_xyz_1931_2deg.csv")
    ill_path = os.path.join(base_dir, "CIE_std_illum_D65.csv")
    df_cie = pd.read_csv(cie_path)
    df_ill = pd.read_csv(ill_path)   
    
    st.dataframe(df_cie)
