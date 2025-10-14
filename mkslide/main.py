import streamlit as st
import io
import pandas as pd
from typing import List
from PIL import Image
from .mkcsv import mkcsv_gui
from .mkpptx import mkpptx_gui

FILTER_COLS = ["試験", "測定面", "正極", "測定", "電解液", "倍率"]
COLUMNS_PER_ROW = 3

def get_filtered_names_by_multiselect_full_order(df: pd.DataFrame, condition_id: int, filter_cols: List[str]) -> List[str]:
    
    current_df = df.copy()
    category_definitions = {}

    for col_name in filter_cols:
        key_multiselect = f'condition_{condition_id}_{col_name}'
        selected_values = st.session_state.get(key_multiselect, ["全て選択"])

        if selected_values and "全て選択" not in selected_values:
           current_df = current_df[current_df[col_name].astype(str).isin(selected_values)]
           category_definitions[col_name] = selected_values

    if category_definitions:
       sort_by_cols = []
       for col_name, categories in category_definitions.items():
           cat_type = pd.CategoricalDtype(categories=categories, ordered=True)
           current_df[col_name] = current_df[col_name].astype(str).astype(cat_type)
           sort_by_cols.append(col_name)
       current_df = current_df.sort_values(by=sort_by_cols)

    return current_df["ファイル名"].astype(str).tolist()

def mkslide_gui():
    
    # INITIALIZE SESSIONS
    if 'data_df' not in st.session_state:
        st.session_state.data_df = None
    if 'condition_count' not in st.session_state:
        st.session_state.condition_count = 1
    if 'all_images' not in st.session_state:
        st.session_state.all_images = {}

    # CSV FILE READER
    uploaded_file = st.file_uploader("Excel/CSVファイルをアップロード", type=["xlsx", "xls", "csv"])
    option_form = st.radio("MKSLIDEが作成したCSVファイルですか？", ["Yes", "No"], 
                           index=1 if st.session_state.data_df is None else 0,
                           horizontal=True)

    if uploaded_file:
        if option_form == "No":
            mkcsv_gui(uploaded_file)
        elif option_form == "Yes":
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.data_df = df
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
                st.session_state.data_df = None
                st.stop()
    
    df = st.session_state.data_df
    if df is None:
        st.info("データファイル（CSV）をアップロードして「Yes」を選択してください。")
        return

    st.markdown("---")

    # UPLOADED FILES
    uploaded_pict = st.file_uploader("画像ファイルを選択してください（複数可）",
                                     type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    if uploaded_pict:
        st.session_state.all_images = {pic.name: Image.open(pic) for pic in uploaded_pict}
        st.success(f"{len(uploaded_pict)} 件の画像をアップロードしました")

    images = st.session_state.all_images
    if not images:
        st.info("画像ファイルをアップロードしてください。")
        return

    # SELECT
    condition_id = 1
    current_df_ui = df.copy()
    condition_container = st.expander(f"条件を設定/確認", expanded=True)

    for col_name in FILTER_COLS:
        options = ["全て選択"] + current_df_ui[col_name].astype(str).unique().tolist()
        key_multiselect = f'condition_{condition_id}_{col_name}'
        selected_values = st.session_state.get(key_multiselect, ["全て選択"])

        condition_container.multiselect(
            f"▼ {col_name} を選んでください（複数選択可）",
            options=options,
            default=selected_values,
            key=key_multiselect
        )

        if selected_values and "全て選択" not in selected_values:
           current_df_ui = current_df_ui[current_df_ui[col_name].astype(str).isin(selected_values)]

    # FILLTERING RESULTS
    final_results = get_filtered_names_by_multiselect_full_order(df, condition_id=condition_id, filter_cols=FILTER_COLS)

    condition_container.subheader(f"✅ 条件に合致する画像 ({len(final_results)} 件)")
    if len(final_results) == 0:
       condition_container.warning("条件に合致する画像はありません。")
    else:
       cols = condition_container.columns(COLUMNS_PER_ROW)
       for j, name in enumerate(final_results):
           if name in images:
              cols[j % COLUMNS_PER_ROW].image(
                   images[name], 
                   caption=name if len(name) <= 40 else name[:40] + "...", 
                   use_container_width=True)

    # PPTX GENERATOR
    if final_results:
       st.subheader("PPTXファイル生成")
       st.info(f"PPTXファイルには、全ての条件で選択された画像 ({len(final_results)} 件) が含まれます。")
       mkpptx_gui(df, images, final_results)

# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
