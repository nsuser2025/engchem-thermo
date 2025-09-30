import streamlit as st
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

page = st.selectbox("計算を選択してください", ["SAFT", "KD viscosity", "Zkanics"])

if page == "SAFT":
    st.header("SAFT")
    st.write("ここはホームです")

elif page == "KD viscosity":
    st.header("Krieger-Dougherty（クリーガー・ドーハティ） 粘性推算")
    st.number_input("パラメータを入力", value=10)

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
