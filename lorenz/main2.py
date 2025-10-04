import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp
from matplotlib import cm
import tempfile

def main2():
    st.title("Lorenz Attractor Animation (Cloud-Friendly GIF)")

    # データ生成
    init = [1.0, 0.0, 0.0]
    t_span = [0.0, 50.0]
    n_points = 200
    t_eval = np.linspace(t_span[0], t_span[1], n_points)
    p, r, b = 10.0, 28.0, 8.0/3.0

    def lorenz(t, X, p, r, b):
        x, y, z = X
        return [-p*x + p*y, -x*z + r*x - y, x*y - b*z]

    sol = solve_ivp(lorenz, t_span, init, t_eval=t_eval, args=(p, r, b))
    x_data, y_data, z_data = sol.y

    # カラーマップ
    cmap = cm.plasma
    colors = cmap(np.linspace(0, 1, n_points))

    # 3Dプロット準備
    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlim(x_data.min(), x_data.max())
    ax.set_ylim(y_data.min(), y_data.max())
    ax.set_zlim(z_data.min(), z_data.max())
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Lorenz Attractor (Animation)")

    lines = []
    for _ in range(n_points):
        l, = ax.plot([], [], [], lw=2)
        lines.append(l)
    point, = ax.plot([], [], [], "ro", markersize=5)

    def init_anim():
        for l in lines:
            l.set_data([], [])
            l.set_3d_properties([])
        point.set_data([], [])
        point.set_3d_properties([])
        return lines + [point]

    def update(frame):
        trail = 100
        start = max(0, frame-trail)
        for i, l in enumerate(lines[start:frame]):
            l.set_data([x_data[start+i], x_data[start+i+1]],
                       [y_data[start+i], y_data[start+i+1]])
            l.set_3d_properties([z_data[start+i], z_data[start+i+1]])
            l.set_color(colors[start+i])
        point.set_data(x_data[frame:frame+1], y_data[frame:frame+1])
        point.set_3d_properties(z_data[frame:frame+1])
        return lines + [point]

    ani = FuncAnimation(fig, update, frames=n_points,
                        init_func=init_anim, interval=30, blit=True)

    # ---- 一時ファイルに保存 ----
    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmpfile:
        tmpfile_path = tmpfile.name
    ani.save(tmpfile_path, writer="pillow")
    plt.close(fig)

    # ---- 読み込んで表示 ----
    with open(tmpfile_path, "rb") as f:
        gif_bytes = f.read()
    st.image(gif_bytes, caption="Lorenz Attractor GIF", format="GIF")

if __name__ == "__main__":
    main2()
