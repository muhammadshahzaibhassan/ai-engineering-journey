import numpy as np
import matplotlib.pyplot as plt
# pyplot provides a user-friendly interface for plotting

x = np.array([2023, 2024, 2025, 2026])
y1 = np.array([15, 25, 30, 23])
y2 = np.array([13, 22, 27, 25])
y3 = np.array([30, 27, 23, 33])
y4 = np.array([13, 15, 17, 20])


line_style = dict(
    marker="o", 
    markersize=10,
    markerfacecolor="red",
    markeredgecolor="red",
    linestyle="solid",
    linewidth=4
)
plt.plot(x, y1, color="orange",**line_style)
plt.plot(x, y2, color="yellow",**line_style)
plt.plot(x, y3, color="limegreen",**line_style)
plt.plot(x, y4, color="purple",**line_style)


plt.show()