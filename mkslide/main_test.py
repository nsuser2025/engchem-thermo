import streamlit as st
import io
import pandas as pd
from PIL import Image
from .mkcsv import mkcsv_gui
from .mkpptx_test import mkpptx0_gui

# フィルタリング対象の列名リスト
FILTER_COLS = ["試験", "測定面", "正極", "測定", "電解液", "倍率"]
COLUMNS_PER_ROW = 3 # 画像表示の列数

# --- 条件選択UIブロックを生成する関数 ---
def create_filter_block(df, condition_index, condition_container):
    """一つの独立したフィルタリングブロック（条件）を生成する"""
    
    # フィルタリングはこのブロック内だけで完結させる
    current_df = df.copy() 
    
    condition_container.markdown(f"### ⚙️ 条件 {condition_index}")
    
    # 各フィルタを順番に適用（カスケードフィルタリング）
    for col_name in FILTER_COLS:
        # その列のユニークな値を取得
        options = ["**全て選択**"] + current_df[col_name].astype(str).unique().tolist()
        
        # セッションステートのキーを条件番号と列名で一意にする
        key_multiselect = f'condition_{condition_index}_{col_name}'
        
        selected_values = condition_container.multiselect(
            f"▼ {col_name} を選んでください（複数選択可）", 
            options=options,
            default=["**全て選択**"],
            key=key_multiselect
        )

        # フィルタを適用して次の選択肢を絞り込む
        if selected_values and "**全て選択**" not in selected_values:
            current_df = current_df[current_df[col_name].astype(str).isin(selected_values)]
            
    # フィルタリングされたファイル名リストを取得
    result_names = current_df["ファイル名"].astype(str).tolist()
    return result_names, condition_container


def mkslide_gui():
    # --- セッションステートの初期化 ---
    if 'data_df' not in st.session_state:
        st.session_state.data_df = None
    if 'condition_count' not in st.session_state:
        st.session_state.condition_count = 1 # 初期条件数は1つ
    if 'all_images' not in st.session_state:
        st.session_state.all_images = {} # 全ての画像を保持

    st.header("データと画像のアップロード")

    # --- 1. データファイル処理 ---
    uploaded_file = st.file_uploader("Excel/CSVファイルをアップロード", type=["xlsx", "xls", "csv"])
    option_form = st.radio("MKSLIDEが作成したCSVファイルですか？", ["Yes", "No"], 
                           index = 1 if st.session_state.data_df is None else 0,
                           horizontal = True)

    if uploaded_file:
        if option_form == "No":
            mkcsv_gui(uploaded_file)
        elif option_form == "Yes":
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.data_df = df # セッションステートに保存
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
    
    # --- 2. 画像ファイル処理 ---
    uploaded_pict = st.file_uploader("画像ファイルを選択してください（複数可）",
                                     type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    if uploaded_pict:
        st.session_state.all_images = {pic.name: Image.open(pic) for pic in uploaded_pict}
        st.success(f"{len(uploaded_pict)} 件の画像をアップロードしました")
    
    images = st.session_state.all_images
    if not images:
        st.info("画像ファイルをアップロードしてください。")
        return
        
    # --- 画像表示のラジオボタン（これはそのまま残す） ---
    disply_form = st.radio("アップロードした画像を表示しますか？", ["Yes", "No"], index = 1, horizontal = True)
    if disply_form == "Yes":
        cols = st.columns(COLUMNS_PER_ROW)
        for i, (name, image) in enumerate(images.items()):
            cols[i % COLUMNS_PER_ROW].image(image, caption=name, use_container_width=True)
    
    st.markdown("---")
    #st.header("🔍 独立した条件フィルタリング")

    # --- 3. 動的条件ブロックの管理 ---
    
    # 条件ブロック全体を保持するコンテナ
    result_container = st.container()
    
    # 条件追加ボタン
    #if st.button("➕ 条件を追加"):
    #    # ボタンを押すと条件の数を増やす
    #    st.session_state.condition_count += 1
    #    # ボタンを押すとStreamlitは再実行され、新しいUIが表示される

    st.markdown("---")

    all_filtered_results = []

    # 既存の条件ブロックをループで生成・表示
    for i in range(1, st.session_state.condition_count + 1):
        # 独立した条件UIのためのコンテナを作成
        condition_container = st.expander(f"条件 {i} を設定/確認", expanded=True)

        # フィルタリングブロックを実行
        filtered_names, block_container = create_filter_block(df, i, condition_container)
        
        # 実際にアップロードされた画像の名前だけを残す
        final_results = [name for name in filtered_names if name in images]

        result_container.subheader(f"✅ 条件 {i} に合致する画像 ({len(final_results)} 件)")
        
        if len(final_results) == 0:
            result_container.warning(f"条件 {i} に合致する画像はありません。")
        else:
            # 各条件に一致する画像を3列で表示
            cols = result_container.columns(COLUMNS_PER_ROW)
            for j, name in enumerate(final_results):
                image = images[name]
                cols[j % COLUMNS_PER_ROW].image(image, caption=name, use_container_width=True)

        result_container.markdown("---")
        
        # PowerPoint生成用に全ての画像結果をリストに保持
        all_filtered_results.extend(final_results)

    # --- 4. PowerPointファイル生成 (全ての条件でフィルタされた結果を統合) ---
    # ここでは、すべての条件ブロックで表示された画像を重複排除してPPTXに渡すのが一般的です。
    unique_results_for_pptx = list(set(all_filtered_results))
    
    if unique_results_for_pptx:
        st.subheader("PPTXファイル生成")
        st.info(f"PPTXファイルには、全ての条件で選択された画像 ({len(unique_results_for_pptx)} 件) が含まれます。")
        mkpptx0_gui(df, images, unique_results_for_pptx)
        
# MODULE ERROR MESSAGE
if __name__ == "__main__":
    raise RuntimeError("Do not run this file directly; use it as a module.")
