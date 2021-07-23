#include <boxlib.h>
/* 
 *
 *
External routines to interface with core parallelbox library 
*/
extern "C" {

    PyObject* parallel_wrapper(PyObject* target_function, PyObject* object_list) {

        return parallelbox::parallel_wrapper_omp(target_function,object_list);

    }
}
