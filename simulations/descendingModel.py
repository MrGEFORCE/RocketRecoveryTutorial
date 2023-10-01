import numpy as np
import matplotlib.pyplot as plt


# 仅考虑垂直场景，主要用于确定引擎的控制参数


class PIDUsingV:
    def __init__(self):
        self.kp = 1
        self.ki = 0
        self.kd = 0
        self.maximum = 1
        self.minimum = -1
        self.integral = 0

    def init(self, kp, ki, kd, upper, lower):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.maximum = upper
        self.minimum = lower

    def update(self, err, v):
        self.integral += err * self.ki * dt
        self.integral = max(min(self.integral, self.maximum), self.minimum)
        return max(min(err * self.kp + self.integral + v * self.kd, self.maximum), self.minimum)


mass = 80e3  # 80t
mass0 = mass
mass_min = mass0 - 21.6e3
g = 9.82
v = -150
h = 1000
alpha = -0.3237e3 * 7
dt = 0.05
target = 0
simu_limits = 2000
max_thrust = 7e6
controller = PIDUsingV()
controller.init(kp=0.01, ki=0, kd=0.03, upper=0.8, lower=0)
times = 0

h_array = np.ndarray([simu_limits], dtype=float)
v_array = np.ndarray([simu_limits], dtype=float)
ctrl_array = np.ndarray([simu_limits], dtype=float)

while abs(target - h) > 0.2 and -v > 0.1:
    ctrl = controller.update(target - h, -v)

    F = - mass * g + ctrl * max_thrust
    mass += alpha * ctrl * dt
    acc = F / mass
    v += acc * dt
    h += v * dt

    h_array[times] = h
    v_array[times] = v
    ctrl_array[times] = ctrl

    if mass < mass_min:
        print("fuel used up")
        break

    times += 1
    if times >= simu_limits:
        print("simulation steps exceed")
        break

    if h < 0:
        print("touch the ground, h:", h, " v:", v)
        break

print("simu steps:", times)
print("time consume:", times * dt, "s")
print("mass consume:", (mass0 - mass) / 1e3, "t")
f, ax = plt.subplots(3, 1)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=1)

plt.subplot(3, 1, 1)
plt.plot(h_array[:times])
plt.title("height(m)")

plt.subplot(3, 1, 2)
plt.plot(v_array[:times])
plt.title("velocity(m/s)")

plt.subplot(3, 1, 3)
plt.plot(ctrl_array[:times])
plt.title("control")

plt.show()
