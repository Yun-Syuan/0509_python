import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 設定中文字型（微軟正黑體，支援 Windows）
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 建立圖表與軸
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.3)  # 預留下方空間給滑桿

# X 軸範圍：0 ~ 4π
x = np.linspace(0, 4 * np.pi, 1000)

# 初始參數
A_init = 1.0
omega_init = 1.0
phi_init = 0.0

# 繪製初始波形
sin_line, = ax.plot(x, A_init * np.sin(omega_init * x + phi_init),
                    label='y = A·sin(ωx + φ)', linewidth=2)
cos_line, = ax.plot(x, A_init * np.cos(omega_init * x + phi_init),
                    label='y = A·cos(ωx + φ)', linewidth=2)

# 設定圖表樣式
ax.set_title('正弦與餘弦波形')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_xlim(0, 4 * np.pi)
ax.set_ylim(-5.5, 5.5)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()

# ---------- 建立滑桿 ----------

# 滑桿顏色
slider_color = 'lightgoldenrodyellow'

# 振幅滑桿
ax_amp = plt.axes([0.25, 0.20, 0.50, 0.03])
slider_amp = Slider(ax_amp, '振幅 (A)', 0.1, 5.0, valinit=A_init)

# 頻率滑桿
ax_freq = plt.axes([0.25, 0.15, 0.50, 0.03])
slider_freq = Slider(ax_freq, '頻率 (ω)', 0.1, 10.0, valinit=omega_init)

# 相位偏移滑桿
ax_phase = plt.axes([0.25, 0.10, 0.50, 0.03])
slider_phase = Slider(ax_phase, '相位偏移 (φ)', 0, 2 * np.pi,
                      valinit=phi_init)


# 更新波形函數
def update(val):
    A = slider_amp.val
    omega = slider_freq.val
    phi = slider_phase.val

    sin_line.set_ydata(A * np.sin(omega * x + phi))
    cos_line.set_ydata(A * np.cos(omega * x + phi))

    fig.canvas.draw_idle()


# 註冊滑桿事件
slider_amp.on_changed(update)
slider_freq.on_changed(update)
slider_phase.on_changed(update)

plt.show()
