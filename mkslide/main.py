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

       results_all = [] 
       st.subheader("🧩 条件設定")
       if "current_condition" not in st.session_state:
          st.session_state.current_condition = 0
       if "conditions" not in st.session_state:
          st.session_state.conditions = {}
       if st.button("次の条件設定"): 
          st.session_state.current_condition += 1

       idx = st.session_state.current_condition
       st.markdown(f"### 条件セット {idx+1}")
       result = condition_selector(df, images, key_prefix=f"{idx}") 
       st.session_state.conditions[idx] = result

       if len(result) == 0:
          st.warning("該当する画像がありません。") 
       elif len(result) > 0:
          result_cols = st.columns(3)
          for i, name in enumerate(result):
              if name in images:
                 col_result = result_cols[i % 3]
                 col_result.image(images[name], caption=name, use_container_width=True)    
       
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
