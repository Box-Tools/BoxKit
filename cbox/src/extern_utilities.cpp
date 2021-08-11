#include <bubblebox/utilities.h>
/*
*
*
*/
namespace utilities = bubblebox::utilities;
namespace pytypes   = bubblebox::pytypes;

extern "C" 
{
    PyObject* executePyTask (PyObject* PyAction, PyObject* PyUnitList, PyObject* PyArgsTuple)
    {
        utilities::CPyAction action = PyAction;
        pytypes::CPyList unitList = PyUnitList;
        pytypes::CPyTuple argsTuple = PyArgsTuple;

        return utilities::executePyTask(action, unitList, argsTuple);
    }
}
