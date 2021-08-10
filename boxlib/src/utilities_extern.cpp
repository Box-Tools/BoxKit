#include <bubblebox/utilities.h>
/*
*
*
*/

namespace utilities = bubblebox::utilities;
namespace pytypes = bubblebox::pytypes;

extern "C" 
{
    PyObject* executePyTask (PyObject* py_action, PyObject* py_unitList, PyObject* py_argsTuple)
    {
        utilities::ActionExtern action = py_action;
        pytypes::CPyList unitList = py_unitList;
        pytypes::CPyTuple argsTuple = py_argsTuple;

        return utilities::executeExternTask(action, unitList, argsTuple);
    }
}
