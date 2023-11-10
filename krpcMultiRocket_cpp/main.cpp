// std
#include <iostream>
#include <windows.h>
#include <thread>
#include <vector>

// krpc
#include <krpc.hpp>
#include <krpc/services/space_center.hpp>

void launch(int vessel_num, int port1, int port2) {
    auto conn = krpc::connect("launch", "127.0.0.1", port1, port2);
    krpc::services::SpaceCenter sc(&conn);
    auto vessel = sc.vessels()[vessel_num]; // return value type: std::vector
    auto altitude = vessel.flight().mean_altitude_stream();

    vessel.control().set_sas(false);
    vessel.control().set_rcs(false);
    vessel.control().set_throttle(1.0);
    vessel.control().set_gear(false);

    vessel.auto_pilot().engage();
    vessel.auto_pilot().target_pitch_and_heading(90, 90);

    for (auto &eng: vessel.parts().engines()) {
        eng.set_active(true);
    }

    while (altitude() < 500) {
        Sleep(100);
    }
    vessel.auto_pilot().disengage();

    std::cout << "thread " << vessel_num << " finished" << std::endl;
}

int main() {
    std::vector<std::thread> thread_list(4);

    thread_list[0] = std::thread(launch, 0, 50000, 50001);
    thread_list[1] = std::thread(launch, 1, 50000, 50001);
    thread_list[2] = std::thread(launch, 2, 50000, 50001);
    thread_list[3] = std::thread(launch, 3, 50000, 50001);

    for (int i=0;i<4;i++) {
        thread_list[i].join();
    }
    return 0;
}
