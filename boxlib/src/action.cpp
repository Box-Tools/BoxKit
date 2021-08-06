#include <bubblebox.h>
/*
*
*
*/
using namespace bubblebox::pytypes;

namespace bubblebox::utilities{

    Action::Action(PyObject* _pyObject) : CPyObject(_pyObject)
    {
        nthreads = PyLong_AsLong(PyObject_GetAttrString(pyObject,"nthreads"));
        monitor  = PyObject_IsTrue(PyObject_GetAttrString(pyObject,"monitor"));
        target   = PyObject_GetAttrString(pyObject,"target");
    }
}
