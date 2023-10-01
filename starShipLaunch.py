import krpc
import time
import numpy as np

conn = krpc.connect(
    name='launch',
    address='127.0.0.1',
    rpc_port=50000,
    stream_port=50001
)
space_center = conn.space_center
vessel = space_center.active_vessel

target_altitude = 75000
turn_start_altitude = 0
gimbal_changing_altitude = 10000
turn_end_altitude = 30000
turning_theta = 10
alpha = np.log(91 - turning_theta) / (turn_end_altitude - turn_start_altitude)

time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
max_thrust = conn.add_stream(getattr, vessel, 'available_thrust')
mass = conn.add_stream(getattr, vessel, 'mass')

vessel.control.sas = False
vessel.control.rcs = False
vessel.control.throttle = 1.0

# find the wings and disable them during the low altitude
root = vessel.parts.root
stack = [(root, 0)]
wing_parts = []
KS25Engine_parts = []
while stack:
    part, depth = stack.pop()
    if part.title == "大S型升降副翼1" or part.title == "升降副翼3":
        wing_parts.append(part)
    if part.title == "S3 KS-25“矢量”液体燃料引擎":
        KS25Engine_parts.append(part)
    for child in part.children:
        stack.append((child, depth+1))


def set_main_engine_gimbal(lists: list, gim: float):
    gim = max(min(gim, 1), 0)
    for item in lists:
        item.engine.gimbal_limit = gim


def set_control_surface_enable(lists: list, status: bool):
    for item in lists:
        item.control_surface.roll_enabled = status
        item.control_surface.pitch_enabled = status
        item.control_surface.yaw_enabled = status


set_control_surface_enable(wing_parts, False)
bControlWingsRoll = True
set_main_engine_gimbal(KS25Engine_parts, 0.25)
bGimbalChanged = True

vessel.auto_pilot.target_pitch_and_heading(90, 90)
vessel.auto_pilot.engage()

vessel.control.activate_next_stage()
print("auto launch started")

while apoapsis() < target_altitude * 0.99:
    time.sleep(0.05)
    vessel.control.throttle = min(20 * mass() / max_thrust(), 1.0)

    if bGimbalChanged:
        if altitude() > gimbal_changing_altitude:
            print("change engine gimbal")
            bGimbalChanged = False
            set_main_engine_gimbal(KS25Engine_parts, 0.5)

    if bControlWingsRoll:
        if altitude() > turn_end_altitude:
            print("enable aerodynamic control")
            bControlWingsRoll = False
            vessel.auto_pilot.target_roll = 0
            set_control_surface_enable(wing_parts, True)

    if turn_start_altitude < altitude() < turn_end_altitude:
        vessel.auto_pilot.target_pitch_and_heading(91 - np.exp(alpha * (altitude() - turn_start_altitude)), 90)

    if altitude() > turn_end_altitude:
        vessel.auto_pilot.target_pitch_and_heading(turning_theta, 90)

vessel.control.throttle = 0.2
while apoapsis() < target_altitude * 1.002:
    time.sleep(0.5)

vessel.control.throttle = 0
print('apoapsis reached')
vessel.auto_pilot.target_pitch_and_heading(0, 90)

while time_to_apoapsis() > 30:
    time.sleep(0.5)

vessel.control.throttle = 1
while vessel.flight(vessel.orbit.body.orbital_reference_frame).speed < 1500:
    time.sleep(0.02)

time.sleep(0.5)
vessel.control.throttle = 0
time.sleep(0.5)

while altitude() < 70001:
    time.sleep(0.5)

vessel.control.toggle_action_group(9)
vessel.control.activate_next_stage()  # separation

print('launch finished')
