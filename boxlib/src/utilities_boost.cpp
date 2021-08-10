#include <bubblebox/utilities.h>
#include <boost/python.hpp>
#include <omp.h>
/*
*
*
*/
using namespace bubblebox;
using namespace boost::python;

BOOST_PYTHON_MODULE(utilities_boost)
{
    class_<utilities::Monitor>("Monitor")
        .def(init<const char *>())
        .def("setlimit", &utilities::Monitor::setlimit)
        .def("update", &utilities::Monitor::update)
    ;
}
