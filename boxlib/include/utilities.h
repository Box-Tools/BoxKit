#include <Python.h>

namespace bubblebox {

    PyObject* parallel_wrapper_pyobj (PyObject* progress_bar, int num_threads,
                                      PyObject* target_function, PyObject* object_list, PyObject* args_tuple);

}

extern "C" {

    PyObject* parallel_wrapper_pyobj (PyObject* progress_bar, int num_threads,
                                      PyObject* target_function, PyObject* object_list, PyObject* args_tuple);

}
