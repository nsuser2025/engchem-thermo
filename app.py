import streamlit as st
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

page = st.selectbox("ページを選択してください", ["ホーム", "設定", "結果"])

if page == "ホーム":
    st.title("ホームページ")
    st.write("ここはホームです")

elif page == "設定":
    st.title("設定ページ")
    st.number_input("パラメータを入力", value=10)

elif page == "結果":
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
