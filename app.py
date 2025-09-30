import streamlit as st
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

page = st.selectbox("計算を選択してください", ["SAFT", "KD viscosity", "Zkanics"])

if page == "SAFT":
    st.header("SAFT")
    st.write("ここはホームです")

elif page == "KD viscosity":
    st.header("Krieger-Dougherty粘性推算")
    eta0 = st.number_input("基材粘度 [mPa・s]（def. エポキシ樹脂単体の粘度 1000）", value=1000)
    eta_intrinsic = st.number_input("固有粘度（形状依存性, def. 球体2.5）", value=2.5)
    phi_max_1 = st.number_input("最大充填体積分率（粒子1を隙間なく詰めたときの上限, def. 0.58）", value=0.58)
    phi_max_2 = st.number_input("最大充填体積分率（粒子2を隙間なく詰めたときの上限, def. 0.58）", value=0.58)
    bool_comp = st.checkbox("粒子1と2を比較しますか?")
   if bool_comp:
       st.write("粒子2のグラフを表示します")
   else:
       st.write("粒子2のグラフは非表示です")
    
    
elif page == "Zkanics":
    st.title("結果ページ")
    st.write("ここに計算結果やグラフを表示")

st.title("サンプル")
st.write("上から順に表示されます")
st.button("ボタン1")
st.button("ボタン2")

st.title("Hello World")
st.write("これは Streamlit で表示しているテキストです！")

# データ作成
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Matplotlib でプロット
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title("Sin Wave")
ax.set_xlabel("x")
ax.set_ylabel("y")

# Streamlit に表示
st.pyplot(fig)
