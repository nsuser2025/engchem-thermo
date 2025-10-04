import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d.art3d import Line3DCollection

def lorenz_gui():
    st.title("Lorenz Attractor 3D Visualization")

    # -----------------------------------
    # データ生成
    # -----------------------------------
    init = [1.0, 0.0, 0.0]
    t_span = [0.0, 50.0]
    t_eval = np.linspace(t_span[0], t_span[1], 3000)
    p, r, b = 10.0, 28.0, 8.0/3.0

    def lorenz(t, X, p, r, b):
        x, y, z = X
        return [-p * x + p * y,
                -x * z + r * x - y,
                 x * y - b * z]

    sol = solve_ivp(lorenz, t_span, init, method="RK45",
                    t_eval=t_eval, args=(p, r, b))

    x_data, y_data, z_data = sol.y

    # -----------------------------------
    # 3Dプロット
    # -----------------------------------
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")

    points = np.array([x_data, y_data, z_data]).T.reshape(-1, 1, 3)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    norm = Normalize(t_eval.min(), t_eval.max())
    lc = Line3DCollection(segments, cmap='plasma', norm=norm)
    lc.set_array(t_eval[:-1])
    lc.set_linewidth(0.5)

    ax.add_collection(lc)
    fig.colorbar(lc, ax=ax, label="Time")

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Lorenz Attractor")

    ax.set_xlim(x_data.min(), x_data.max())
    ax.set_ylim(y_data.min(), y_data.max())
    ax.set_zlim(z_data.min(), z_data.max())

    plt.tight_layout()

    # Streamlit に表示
    st.pyplot(fig)
