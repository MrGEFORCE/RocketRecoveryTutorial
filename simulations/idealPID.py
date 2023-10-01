import numpy as np
from simple_pid import PID
import matplotlib.pyplot as plt

dt = 2
target = 100
# 典型值 Kp=0.04, Ki=0.001, Kd=0.02
# 过阻尼 Kp=0.04, Ki=0.000, Kd=0.02
# 欠阻尼 Kp=0.02, Ki=0.001, Kd=0.02
controller = PID(Kp=0.04, Ki=0.001, Kd=0.02, setpoint=target, differential_on_measurement=False,output_limits=(0, 5))

steps = 500
value = 0
array = np.ndarray([steps], dtype=float)
target_array = np.ndarray([steps], dtype=float)
target_array[:] = target
for i in range(steps):
    value += controller(value, dt)
    array[i] = value

plt.figure(0)
plt.plot(array)
plt.plot(target_array)
plt.show()
