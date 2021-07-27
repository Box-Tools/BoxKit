#include <bubblebox.h>
/* 
 *
 *
External routines to interface with core bubblebox library 
*/
extern "C" {

    PyObject* Parallel_PyWrapper (PyObject* target_function, PyObject* object_list, PyObject* args_tuple,
                                  PyObject* progress_bar, int num_threads) {

        return bubblebox::Parallel_PyWrapper(target_function, object_list, args_tuple,
                                             progress_bar, num_threads);
    }

    //

}
