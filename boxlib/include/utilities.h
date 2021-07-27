#include <Python.h>

namespace bubblebox {

    PyObject* Parallel_PyWrapper (PyObject* target_function, PyObject* object_list, PyObject* args_tuple,
                                  PyObject* progress_bar, int num_threads);

}

extern "C" {

    PyObject* Parallel_PyWrapper (PyObject* target_function, PyObject* object_list, PyObject* args_tuple,
                                  PyObject* progress_bar, int num_threads);

}
