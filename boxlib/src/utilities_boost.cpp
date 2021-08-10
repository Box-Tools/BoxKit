#include <bubblebox/utilities.h>
/*
*
*
*/
namespace utilities = bubblebox::utilities;
namespace python = boost::python;

BOOST_PYTHON_MODULE(utilities_boost)
{
    python::class_<utilities::Monitor>("Monitor")
        .def(python::init<>())
        .def(python::init<const char *>())
        .def("setlimit", &utilities::Monitor::setlimit)
        .def("update", &utilities::Monitor::update)
    ;
   /*
    *
    */
    python::def("executePyTask",&utilities::executeBoostTask);
}
