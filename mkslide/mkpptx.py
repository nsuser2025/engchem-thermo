import streamlit as st
from pptx import Presentation
from pptx.util import Inches

def mkpptx_gui(images, result):
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[5])

    slide_width = prs.slide_width
    slide_height = prs.slide_height

    bottom_margin = Inches(0.5)  
    rows, cols_num = 2, 3
    width = Inches(2.8) 
    height = Inches(2.0)
    spacing_x, spacing_y = Inches(0.2), Inches(0.2)

    for idx, name in enumerate(result[:6]):
        if name in images:
           image = images[name]
           tmp_path = f"tmp_{name}"
           image.save(tmp_path)
           row = idx // cols_num
           col = idx % cols_num
           left = Inches(0.5) + col * (width + spacing_x)
           total_height = rows * height + (rows - 1) * spacing_y
           top = slide_height - total_height - bottom_margin + row * (height + spacing_y)
           slide.shapes.add_picture(tmp_path, left, top, width=width, height=height)
    
    pptx_path = "output.pptx"
    prs.save(pptx_path)
    st.success(f"PPTXに画像を追加しました: {pptx_path}")

    with open(pptx_path, "rb") as f:
         st.download_button("PPTXをダウンロード", f, file_name="output.pptx")

# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
