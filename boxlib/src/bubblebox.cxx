#include <bubblebox.h>
/* 
 *
 *
External routines to interface with core bubblebox library 
*/
extern "C" {

    PyObject* parallel_wrapper_pyobj (PyObject* progress_bar, int num_threads,
                                      PyObject* target_function, PyObject* object_list, PyObject* args_tuple) {

        return bubblebox::parallel_wrapper_pyobj(progress_bar, num_threads, 
                                                 target_function, object_list, args_tuple);
    }

    //
}
