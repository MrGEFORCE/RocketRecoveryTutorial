import krpc
import time
import numpy as np
from simple_pid import PID

conn = krpc.connect(
    name='recovery',
    address='127.0.0.1',
    rpc_port=50000,
    stream_port=50001
)
space_center = conn.space_center
vessel = space_center.active_vessel

USING_AP = False
root = vessel.parts.root
stack = [(root, 0)]
KS25Engine_parts = []
while stack:
    part, depth = stack.pop()
    if part.title == "S3 KS-25“矢量”液体燃料引擎":
        KS25Engine_parts.append(part)
    for child in part.children:
        stack.append((child, depth+1))


class PIDUsingV:
    def __init__(self):
        self.kp = 1
        self.ki = 0
        self.kd = 0

        self.maximum = 1
        self.minimum = -1

        self.prev_t = time.time()
        self.integral = 0

    def init(self, kp, ki, kd, upper, lower):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.maximum = upper
        self.minimum = lower

    def update(self, err, v):
        dt = time.time() - self.prev_t
        self.prev_t = time.time()
        self.integral += err * self.ki * dt
        self.integral = max(min(self.integral, self.maximum), self.minimum)
        return max(min(err * self.kp + self.integral + v * self.kd, self.maximum), self.minimum)


def set_engine_gimbal(lists: list, gim: float):
    gim = max(min(gim, 1), 0)
    for item in lists:
        item.engine.gimbal_limit = gim


def reference_rotate():
    lon = vessel.flight().longitude
    ref = space_center.ReferenceFrame.create_relative(vessel.orbit.body.reference_frame, rotation=(
        0, np.sin(-lon / 2. * np.pi / 180), 0, np.cos(-lon / 2. * np.pi / 180)))
    return ref


def steering(pitch_bias: float, ref: space_center.ReferenceFrame):
    v = vessel.flight(ref).velocity
    retro_steering = v / np.linalg.norm(v)

    pitch_controller.setpoint = - np.arcsin(retro_steering[0]) / np.pi * 180 + pitch_bias
    heading_controller.setpoint = - np.arctan(retro_steering[1] / retro_steering[2]) / np.pi * 180 + 270

    vessel.control.pitch = pitch_controller(vessel.flight(ref).pitch)
    vessel.control.yaw = heading_controller(vessel.flight(ref).heading)
    vessel.control.roll = roll_controller(vessel.flight(ref).roll)


def steering_ap(pitch_bias: float, ref: space_center.ReferenceFrame):
    vessel.auto_pilot.reference_frame = ref
    v = vessel.flight(ref).velocity
    retro_steering = v / np.linalg.norm(v)
    target_pitch = - np.arcsin(retro_steering[0]) / np.pi * 180 + pitch_bias
    target_heading = - np.arctan(retro_steering[1] / retro_steering[2]) / np.pi * 180 + 270
    vessel.auto_pilot.target_pitch_and_heading(target_pitch, target_heading)


print("auto landing started")
vessel.control.gear = False
vessel.control.sas = False
vessel.control.rcs = True
vessel.control.toggle_action_group(8)  # grid fin deploy

if USING_AP:
    vessel.auto_pilot.engage()
    vessel.auto_pilot.reference_frame = reference_rotate()
    vessel.auto_pilot.target_roll = 0
else:
    pitch_controller = PID(Kp=0.1, Ki=0.01, Kd=0.4, output_limits=(-1, 1), differential_on_measurement=False)
    heading_controller = PID(Kp=0.1, Ki=0.01, Kd=0.4, output_limits=(-1, 1), differential_on_measurement=False)
    roll_controller = PID(Kp=0.02, Ki=0, Kd=0.01, output_limits=(-1, 1), differential_on_measurement=False, setpoint=0)

final_throttle = PIDUsingV()
final_throttle.init(kp=0.01, ki=0, kd=0.03, upper=0.8, lower=0)

set_engine_gimbal(KS25Engine_parts, 0.2)

while vessel.flight().mean_altitude > 1000:
    ref = reference_rotate()
    if USING_AP:
        steering_ap(-10, ref)
    else:
        steering(-10, ref)

    if vessel.flight().mean_altitude < 26000 and vessel.flight(ref).speed > 1300:
        vessel.control.throttle = 0.33
    else:
        vessel.control.throttle = 0
    time.sleep(0.05)

print("final stage")
if not USING_AP:
    pitch_controller.tunings = (0.4, 0.01, 1)
    heading_controller.tunings = (0.4, 0.01, 1)
bGearDeploy = True
while vessel.flight().surface_altitude > 14:
    ref = reference_rotate()
    vessel.control.throttle = final_throttle.update(13 - vessel.flight(ref).surface_altitude, -vessel.flight(ref).vertical_speed)
    if np.linalg.norm(vessel.flight(ref).velocity[1:]) > 50:
        if USING_AP:
            steering_ap(-10, ref)
        else:
            steering(-10, ref)
    else:
        if USING_AP:
            steering_ap(0, ref)
        else:
            steering(0, ref)

    if bGearDeploy and vessel.flight().surface_altitude < 250:
        bGearDeploy = False
        vessel.control.gear = True
    time.sleep(0.01)

vessel.control.throttle = 0
vessel.control.rcs = False
print("landing complete")
