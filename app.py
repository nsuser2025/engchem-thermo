import streamlit as st
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

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
