import numpy as np
import matplotlib.pyplot as plt

signal = np.ndarray([3, 500], dtype=float)

x = np.arange(0, np.pi, np.pi / 500)
signal[0] = np.cos(2 * np.pi * x * 3)
signal[1] = np.cos(2 * np.pi * x * 1)
signal[2] = np.cos(2 * np.pi * x * 7)

plt.figure(0)
for i in range(3):
    plt.plot(signal[i])
plt.title("sine wave")
plt.legend(["w=3", "w=1", "w=7"])
plt.show()
