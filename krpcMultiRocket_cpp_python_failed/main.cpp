// std
#include <iostream>
#include <vector>

// threading
#include <thread>  // c++ 11 and later

// python
#include <Python.h>

#define NUM_THREADS 4

void* launch1(void* args)
{
    PyObject *pModule = PyImport_ImportModule("test1");
    return nullptr;
}

void* launch2(void* args)
{
    PyObject *pModule = PyImport_ImportModule("test2");
    return nullptr;
}

void* launch3(void* args)
{
    PyObject *pModule = PyImport_ImportModule("test3");
    return nullptr;
}

void* launch4(void* args)
{
    PyObject *pModule = PyImport_ImportModule("test4");
    return nullptr;
}

int main() {
    Py_SetPythonHome((wchar_t*)L"D:/apps/programming/python310_11");
    Py_Initialize();
    std::vector<std::thread> thread_list(4);
    thread_list[0] = std::thread(launch1, nullptr);
    thread_list[1] = std::thread(launch2, nullptr);
    thread_list[2] = std::thread(launch3, nullptr);
    thread_list[3] = std::thread(launch4, nullptr);

    for (int i=0;i<NUM_THREADS;i++) {
        thread_list[i].join();
    }

    Py_Finalize();
    return 0;
}
