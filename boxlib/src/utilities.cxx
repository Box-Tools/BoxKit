#include <bubblebox.h>
#include <omp.h>

namespace bubblebox{

    PyObject* Parallel_PyWrapper (PyObject* target_function, PyObject* object_list, PyObject* args_tuple,
                                  PyObject* progress_bar, int num_threads) {

        Py_ssize_t target_num_objs = PyList_Size(object_list);           
        Py_ssize_t target_num_args = PyTuple_Size(args_tuple) + 1;

        PyObject* result_list = PyList_New(target_num_objs);

        omp_set_dynamic(0);
        omp_set_num_threads(num_threads);

        //#pragma omp parallel default(shared)
        for (int i = 0; i < target_num_objs; i++) {

            PyObject* target_object = PyList_GetItem(object_list, i);
            PyObject* target_args_tuple = PyTuple_New(target_num_args);
            PyObject *target_arg, *target_result, *progress_itor, *progress_result;
            PyGILState_STATE gstate;

            PyTuple_SetItem(target_args_tuple, 0, target_object);
      
            for (int j = 1; j < target_num_args; j++) { 
                target_arg = PyTuple_GetItem(args_tuple, j-1);
                PyTuple_SetItem(target_args_tuple, j, target_arg);         
            }     

            gstate = PyGILState_Ensure();
            target_result = PyObject_CallObject(target_function, target_args_tuple);
            PyGILState_Release(gstate);

            PyList_SetItem(result_list, i, target_result);

            progress_itor = PyObject_GetAttrString(progress_bar,"next");
            
            gstate = PyGILState_Ensure();
            progress_result = PyObject_CallObject(progress_itor,NULL);
            PyGILState_Release(gstate);

        }

        return result_list;

    };
}
