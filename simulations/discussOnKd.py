import numpy as np
from simple_pid import PID
import matplotlib.pyplot as plt

# kd的探讨
iterations = 5
simu_steps = 2000
h_array = np.ndarray([iterations, simu_steps], dtype=float)
v_array = np.ndarray([iterations, simu_steps], dtype=float)
ctrl_array = np.ndarray([iterations, simu_steps], dtype=float)
m_array = np.ndarray([iterations, simu_steps], dtype=float)

dt = 0.05  # s
g = 9.82  # m/s^2
max_thrust = 1e5  # N, twr max = 2
alpha = -0.02e3  # if max thrust, rate = . t/s
target = 1000

for turns in range(iterations):
    controller = PID(Kp=0.05, Ki=0.0001, Kd=0.1 + 0.1 * turns, setpoint=target, output_limits=(0, 1),
                     differential_on_measurement=False)
    controller.reset()

    mass = 5e3 + 1  # unit:t
    h = 0
    v = 0
    for i in range(simu_steps):
        ctrl = controller(h, dt)
        F = max_thrust * ctrl - mass * g
        mass += alpha * ctrl
        acc = F / mass
        v += acc * dt
        h += v * dt

        h_array[turns, i] = h
        v_array[turns, i] = v
        ctrl_array[turns, i] = ctrl
        m_array[turns, i] = mass
        if mass < 0:
            h_array[turns, i:] = 0
            v_array[turns, i:] = 0
            ctrl_array[turns, i:] = 0
            m_array[turns, i:] = 0
            break

f, ax = plt.subplots(4, 1)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=1)

plt.subplot(4, 1, 1)
string = []
for i in range(iterations):
    plt.plot(h_array[i])
    string.append("kd=" + str(0.1 + 0.1 * i)[:4])
plt.title("height(m)")
plt.legend(string)

plt.subplot(4, 1, 2)
for i in range(iterations):
    plt.plot(v_array[i])
plt.title("velocity(m/s)")

plt.subplot(4, 1, 3)
for i in range(iterations):
    plt.plot(ctrl_array[i])
plt.title("control")

plt.subplot(4, 1, 4)
for i in range(iterations):
    plt.plot(m_array[i] / 1e3)
plt.title("mass(t)")

plt.show()
