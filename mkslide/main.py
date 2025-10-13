import streamlit as st
import io
import pandas as pd
from PIL import Image
from .mkcsv import mkcsv_gui
from .mkpptx import mkpptx0_gui
from .hachida import condition_selector
from .display import display_images

def mkslide_gui():

    # ファイルアップロード
    uploaded_file = st.file_uploader("Excel/CSVファイルをアップロード", type=["xlsx", "xls", "csv"])
    option_form = st.radio("MKSLIDEが作成したCSVファイルですか？", ["Yes", "No"], index = 1, horizontal = True)
    
    if uploaded_file and option_form == "No":
       mkcsv_gui(uploaded_file)
    elif uploaded_file and option_form == "Yes":
       df = pd.read_csv(uploaded_file)
       st.dataframe(df)
    
    uploaded_pict = st.file_uploader("画像ファイルを選択してください（複数可）",
                    type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if uploaded_pict:
       st.success(f"{len(uploaded_pict)} 件の画像をアップロードしました")
       disply_form = st.radio("アップロードした画像を表示しますか？", ["Yes", "No"], index = 1, horizontal = True) 
       images = {pic.name: Image.open(pic) for pic in uploaded_pict}
       if disply_form == "Yes":
          cols = st.columns(3)
          for i, (name, image) in enumerate(images.items()):
              col = cols[i % 3]
              col.image(image, caption=name, use_container_width=True)

       if "condition_count" not in st.session_state:
          st.session_state.condition_count = 1
       if "conditions" not in st.session_state:
          st.session_state.conditions = [{} for _ in range(st.session_state.condition_count)]

       if st.button("➕ 条件を追加"):
          st.session_state.condition_count += 1
          st.session_state.conditions.append({})

       results_all = [] 
       st.subheader("🧩 条件設定")
       for i in range(st.session_state.condition_count): 
           st.markdown(f"### 条件セット str{i+1}")
           with st.container():
                result = condition_selector(df, images, key_prefix=f"{i}")
                #display_images(result, images, f"条件{i+1}")
                results_all.append((f"条件{i+1}", result))
        
       if len(result) == 0:
          st.warning("該当する画像がありません。")
       else:
          result_cols = st.columns(3)
          for i, name in enumerate(result):
              if name in images:
                 image = images[name]
                 col_result = result_cols[i % 3]
                 col_result.image(image, caption=name, use_container_width=True)
       
       # パワーポイント作成
       pptx_choice = ["Yes（ファイル名配列）",
                      "Yes（指定条件配列）",
                      "No"]
       pptx_form = st.radio("パワーポイントを作成しますか？", pptx_choice, index = 2, horizontal = True) 
       if len(result) > 0 and pptx_form == "Yes（ファイル名配列）":
          mkpptx0_gui(df, images, result)

# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
