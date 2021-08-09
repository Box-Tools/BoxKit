#include <bubblebox/utilities.h>
#include <omp.h>
/*
*
*
*/
using namespace bubblebox::pytypes;

namespace bubblebox::utilities{

    CPyList executePyTask (Action& action, CPyList& unitList, CPyTuple& argsTuple) 
    {
        Py_ssize_t numUnits = unitList.len();
        Py_ssize_t numArgs = argsTuple.len() + 2;

        CPyList resultList = PyList_New(numUnits);

        CPyTuple targetArgs;
        CPyObject arg, unit, result;

        omp_set_dynamic(0);
        omp_set_num_threads(action.nthreads);

        Monitor monitor("action");
        monitor.setlimit(numUnits);

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
            result = PyObject_CallObject(action.target, targetArgs);

            result.AddPyRef();
            resultList.setItem(i,result);

            PyGILState_Release(gstate);

            if(action.monitor)
            {
                //#pragma omp critical
                monitor.update("Executing Py Task from C++");
            }
        }

        resultList.AddPyRef();
        return resultList;
    };
}
