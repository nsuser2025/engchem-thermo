import streamlit as st
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches

def mkpptx_gui(images, result):
    uploaded_template = st.file_uploader("PPTXテンプレートをアップロード", type=["pptx"])
    if uploaded_template is None:
        st.warning("PPTXテンプレートをアップロードしてください。")
        return
    template_bytes = BytesIO(uploaded_template.read())
    prs = Presentation(template_bytes)
    base_slide = prs.slides[0]

    slide_width = prs.slide_width

    rows, cols_num = 2, 3
    width = Inches(3.4) 
    height = Inches(2.4)
    spacing_x, spacing_y = Inches(0.2), Inches(0.2)
    left_margin, bottom_margin = Inches(0.5), Inches(0.5)
    slide_height = prs.slide_height
    total_height = rows * height + (rows - 1) * spacing_y
        
    for idx, name in enumerate(result[:6]):
        if name in images:
           image = images[name]
           tmp_path = f"tmp_{name}"
           image.save(tmp_path)
           row = idx // cols_num
           col = idx % cols_num
           left = left_margin + col * (width + spacing_x)
           top = slide_height - total_height - bottom_margin + row * (height + spacing_y)
           base_slide.shapes.add_picture(tmp_path, left, top, width=width, height=height)
    
    pptx_path = "output.pptx"
    prs.save(pptx_path)
    st.success(f"PPTXに画像を追加しました: {pptx_path}")

    with open(pptx_path, "rb") as f:
         st.download_button("PPTXをダウンロード", f, file_name="output.pptx")

# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
