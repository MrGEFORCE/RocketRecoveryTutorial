cmake_minimum_required(VERSION 3.15)
project(multi)
set(CMAKE_CXX_STANDARD 17)

include_directories(
        D:/apps/krpc_cpp/krpc-cpp-0.5.2/include
        D:/apps/krpc_cpp/krpc-cpp-0.5.2/protobuf/include
        D:/apps/programming/vcpkg/packages/protobuf_x64-windows/include
)

file(GLOB SRC "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")

add_executable(multi ${SRC})

set_property(TARGET multi PROPERTY
        MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

target_link_libraries(multi
        D:/apps/krpc_cpp/krpc-cpp-0.5.2/Debug/krpc.lib
        D:/apps/programming/vcpkg/packages/protobuf_x64-windows/debug/lib/libprotobufd.lib
)
