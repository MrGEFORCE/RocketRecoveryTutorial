import numpy as np
from simple_pid import PID
import matplotlib.pyplot as plt

# 火箭悬停问题物理场景仿真

dt = 0.05  # s
mass = 5e3 + 1  # unit:kg
g = 9.82  # m/s^2
max_thrust = 1e5  # N, twr max = 2
alpha = -0.02e3  # if max thrust, rate = . t/s

target = 1000
h = 0
v = 0

controller = PID(Kp=0.05, Ki=0.0001, Kd=0.2, setpoint=target, output_limits=(0, 1), differential_on_measurement=False)

simu_steps = 2000
h_array = np.ndarray([simu_steps], dtype=float)
v_array = np.ndarray([simu_steps], dtype=float)
ctrl_array = np.ndarray([simu_steps], dtype=float)
m_array = np.ndarray([simu_steps], dtype=float)

for i in range(simu_steps):
    ctrl = controller(h, dt)
    F = max_thrust * ctrl - mass * g
    mass += alpha * ctrl
    acc = F / mass
    v += acc * dt
    h += v * dt

    h_array[i] = h
    v_array[i] = v
    ctrl_array[i] = ctrl
    m_array[i] = mass
    if mass < 0:
        h_array[i:] = 0
        v_array[i:] = 0
        ctrl_array[i:] = 0
        m_array[i:] = 0
        break


f, ax = plt.subplots(4, 1)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=1)

plt.subplot(4, 1, 1)
plt.plot(h_array)
plt.title("height(m)")

plt.subplot(4, 1, 2)
plt.plot(v_array)
plt.title("velocity(m/s)")

plt.subplot(4, 1, 3)
plt.plot(ctrl_array)
plt.title("control")

plt.subplot(4, 1, 4)
plt.plot(m_array/1e3)
plt.title("mass(t)")

plt.show()
