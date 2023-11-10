import krpc
import time
import threading


def launch(vessel_num, port1, port2):
    conn = krpc.connect(
        name='launch',
        address='127.0.0.1',
        rpc_port=port1,
        stream_port=port2
    )
    space_center = conn.space_center
    vessel = space_center.vessels[vessel_num]

    altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')

    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.throttle = 1.0
    vessel.control.gear = False

    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, 90)

    for eng in vessel.parts.engines:
        eng.active = True

    # vessel.control.activate_next_stage()

    while altitude() < 500:
        time.sleep(0.1)

    vessel.auto_pilot.disengage()
    print("finished")


thread_list = []

# thread_list.append(threading.Thread(target=launch, args=(0, 50000, 50001)))
# thread_list.append(threading.Thread(target=launch, args=(1, 50002, 50003)))
# thread_list.append(threading.Thread(target=launch, args=(2, 50004, 50005)))
# thread_list.append(threading.Thread(target=launch, args=(3, 50006, 50007)))

thread_list.append(threading.Thread(target=launch, args=(0, 50000, 50001)))
thread_list.append(threading.Thread(target=launch, args=(1, 50000, 50001)))
thread_list.append(threading.Thread(target=launch, args=(2, 50000, 50001)))
thread_list.append(threading.Thread(target=launch, args=(3, 50000, 50001)))

for i in range(4):
    thread_list[i].start()
