#include <cbox/library.h>
#include <omp.h>

namespace pytypes = cbox::pytypes;
/*
 *
 *
 */
namespace cbox::library {
/*
 */
pytypes::CPyList execute_pyTask(Action &action, pytypes::CPyList &unitList,
                                pytypes::CPyTuple &argsTuple) {

  Py_ssize_t numUnits = unitList.len();
  Py_ssize_t numArgs = argsTuple.len() + 2;

  pytypes::CPyList resultList = PyList_New(numUnits);

  pytypes::CPyTuple targetArgs;
  pytypes::CPyObject arg, unit, result;

  //omp_set_dynamic(0);
  //omp_set_num_threads(action.nthreads);

  Monitor actionMonitor("action");
  actionMonitor.setlimit(numUnits);

  //#pragma omp parallel default(shared) private(targetArgs,arg,unit,result)
  for (Py_ssize_t i = 0; i < numUnits; i++) {

    targetArgs = PyTuple_New(numArgs);

    action.AddPyRef();
    targetArgs.setItem(0, action);

    unit = unitList.getItem(i);
    unit.AddPyRef();
    targetArgs.setItem(1, unit);

    for (Py_ssize_t j = 2; j < numArgs; j++) {
      arg = argsTuple.getItem(j - 2);
      arg.AddPyRef();
      targetArgs.setItem(j, arg);
    }

    PyGILState_STATE gstate = PyGILState_Ensure();

    targetArgs.AddPyRef();
    result = PyObject_CallObject(action.pyTarget, targetArgs);

    result.AddPyRef();
    resultList.setItem(i, result);

    PyGILState_Release(gstate);

    if (action.monitor) {
      //#pragma omp critical
      actionMonitor.update();
    }
  }

  resultList.AddPyRef();
  return resultList;
}
} // namespace cbox::library
