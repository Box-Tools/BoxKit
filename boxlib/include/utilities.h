#include <Python.h>

namespace bubblebox::utilities {

    PyObject* executePyTask (PyObject* progressBar, 
                             PyObject* action, PyObject* unitList, PyObject* argsTuple);

}

extern "C" {

    PyObject* utilities_executePyTask (PyObject* progressBar, 
                                       PyObject* action, PyObject* unitList, PyObject* argsTuple);

}
