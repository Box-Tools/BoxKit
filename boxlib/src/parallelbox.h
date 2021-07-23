#include <Python.h>
#include <iostream>

namespace parallelbox {

    PyObject* parallel_wrapper_omp(PyObject* target_function, PyObject* object_list);

}
