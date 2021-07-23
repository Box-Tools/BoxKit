#include <parallelbox.h>

namespace parallelbox{

    PyObject* parallel_wrapper_omp(PyObject* target_function, PyObject* object_list) {

        Py_ssize_t object_num = PyList_Size(object_list);           
        PyObject *result_list = PyList_New(object_num);
        PyObject *object, *result, *target_args;
        PyGILState_STATE gstate;

        #pragma omp parallel for
        for (int i = 0; i < object_num; i++) {
        
            object = PyList_GetItem(object_list, i);
                
            target_args = PyTuple_Pack(1,object);

            PyGILState_STATE gstate;
            gstate = PyGILState_Ensure();
            //
            result = PyObject_CallObject(target_function, target_args);
            //
            PyGILState_Release(gstate);

            PyList_SetItem(result_list, i, result);
        }

        return result_list;

    };
}
