#include <cbox/utilities.h>
#include <omp.h>

namespace pytypes = cbox::pytypes;
/*
 *
 *
 */
namespace cbox::utilities
{
   /*
    */
    pytypes::CPyList executePyTask (Action& action, pytypes::CPyList& unitList, pytypes::CPyTuple& argsTuple) 
    {

        int nthreads = PyLong_AsLong(PyObject_GetAttrString(action,"nthreads"));
        bool monitor  = PyObject_IsTrue(PyObject_GetAttrString(action,"monitor"));
        pytypes::CPyObject target = PyObject_GetAttrString(action,"target");

        Py_ssize_t numUnits = unitList.len();
        Py_ssize_t numArgs = argsTuple.len() + 2;

        pytypes::CPyList resultList = PyList_New(numUnits);

        pytypes::CPyTuple targetArgs;
        pytypes::CPyObject arg, unit, result;

        omp_set_dynamic(0);
        omp_set_num_threads(nthreads);

        Monitor actionMonitor("action");
        actionMonitor.setlimit(numUnits);

        //#pragma omp parallel default(shared) private(targetArgs,arg,unit,result)
        for (Py_ssize_t i = 0; i < numUnits; i++) 
        {

            targetArgs = PyTuple_New(numArgs);
          
            action.AddPyRef();
            targetArgs.setItem(0, action);

            unit = unitList.getItem(i);
            unit.AddPyRef();
            targetArgs.setItem(1, unit);

            for (Py_ssize_t j = 2; j < numArgs; j++) 
            { 
                arg = argsTuple.getItem(j-2);
                arg.AddPyRef();
                targetArgs.setItem(j, arg);
            }     

            PyGILState_STATE gstate = PyGILState_Ensure();

            targetArgs.AddPyRef();
            result = PyObject_CallObject(target, targetArgs);

            result.AddPyRef();
            resultList.setItem(i,result);

            PyGILState_Release(gstate);

            if(monitor)
            {
                //#pragma omp critical
                actionMonitor.update();
            }
        }

        //PyObject_SetAttrString(action,"nthreads",Py_BuildValue("i", 42));

        resultList.AddPyRef();
        return resultList;
    }
}
