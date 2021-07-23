#include <parallelbox.h>

extern "C" {

    PyObject* parallel_wrapper(PyObject* target_function, PyObject* object_list);

}
