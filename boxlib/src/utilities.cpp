#include <bubblebox/utilities.h>
/*
*
*
*/
using namespace bubblebox;

extern "C" 
{
    PyObject* executePyTask (PyObject* py_action, PyObject* py_unitList, PyObject* py_argsTuple)
    {
        utilities::Action action = py_action;
        pytypes::CPyList unitList = py_unitList;
        pytypes::CPyTuple argsTuple = py_argsTuple;

        return utilities::executePyTask(action, unitList, argsTuple);
    }

}
