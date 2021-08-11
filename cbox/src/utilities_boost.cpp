#include <bubblebox/utilities.h>
/*
*
*
*/
namespace utilities = bubblebox::utilities;
namespace python    = boost::python;

namespace
{
    PyObject* executePyTask(utilities::Monitor& monitor)
    {
        return utilities::executePyTask(monitor);
    }
}
/*
 *
 *
 */
BOOST_PYTHON_MODULE(utilities)
{
    python::class_<utilities::Monitor>("Monitor")
        .def(python::init<>())
        .def(python::init<const char *>())
        .def("_setlimit", &utilities::Monitor::setlimit)
        .def("_update",   &utilities::Monitor::update)
        .def("_gettype",  &utilities::Monitor::gettype)
    ;
   /*
    *
    */
    python::def("executePyTask", &executePyTask);
}
