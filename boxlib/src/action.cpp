#include <bubblebox/utilities.h>
/*
*
*
*/
using namespace bubblebox::pytypes;

namespace bubblebox::utilities
{

    Action::Action(PyObject* _pyObject) : CPyObject(_pyObject)
    {
        nthreads = PyLong_AsLong(PyObject_GetAttrString(pyObject,"nthreads"));
        monitor  = PyObject_IsTrue(PyObject_GetAttrString(pyObject,"monitor"));
        target   = PyObject_GetAttrString(pyObject,"target");
    }


    void Action::setbar(int iterlimit)
    {
        max_progress = iterlimit;
        progress = 0;
        bar.set_option(indicators::option::MaxProgress{max_progress});
    }


    void Action::updatebar()
    {
        if(monitor)
        {
            ++progress;
            bar.set_option(indicators::option::PostfixText{std::to_string(progress) + "/" + 
                                                           std::to_string(max_progress)});
            bar.tick();
        }
    }

}
