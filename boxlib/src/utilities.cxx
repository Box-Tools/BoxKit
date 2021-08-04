#include <bubblebox.h>
#include <omp.h>
/*
*
*
*/
namespace bubblebox::utilities{

    PyObject* executePyTask (PyObject* progressBar, PyObject* action, PyObject* unitList, PyObject* argsTuple) {
        // Set target 
        Py_ssize_t numUnits = PyList_Size(unitList);           
        Py_ssize_t numArgs = PyTuple_Size(argsTuple) + 2;

        PyObject* resultList = PyList_New(numUnits);
        PyObject* target = PyObject_GetAttrString(action,"target");

        int numThreads = PyLong_AsLong(PyObject_GetAttrString(action,"nthreads"));
        bool monitor = PyObject_IsTrue(PyObject_GetAttrString(action,"monitor"));

        PyObject* targetArgs = PyTuple_New(numArgs);
        PyObject *arg, *result, *progressItor, *unit;

        PyGILState_STATE gstate;

        omp_set_dynamic(0);
        omp_set_num_threads(numThreads);

        //#pragma omp parallel default(shared)
        for (int i = 0; i < numUnits; i++) {

            unit = PyList_GetItem(unitList, i);

            Py_INCREF(action);
            PyTuple_SetItem(targetArgs, 0, action);

            Py_INCREF(unit);
            PyTuple_SetItem(targetArgs, 1, unit);
 
            for (int j = 2; j < numArgs; j++) { 
                arg = PyTuple_GetItem(argsTuple, j-2);

                Py_INCREF(arg);
                PyTuple_SetItem(targetArgs, j, arg);         
            }     

            gstate = PyGILState_Ensure();
            result = PyObject_CallObject(target, targetArgs);
            PyGILState_Release(gstate);

            Py_INCREF(result);
            PyList_SetItem(resultList, i, result);

            progressItor = PyObject_GetAttrString(progressBar,"next");
            
            gstate = PyGILState_Ensure();
            result = PyObject_CallObject(progressItor,NULL);
            PyGILState_Release(gstate);

        }

        return resultList;
    };
}
