#include <cbox/utilities.h>
/*
 *
 *
 */
namespace utilities = cbox::utilities;
namespace python    = boost::python;
/*
 *
 *
 */
namespace cbox::boost
{
    //add boost implementation here
}
/*
 *
 *
 */
BOOST_PYTHON_MODULE(utilities)
{
    python::class_<utilities::Monitor>("Monitor")
        .enable_pickling()
        .def(python::init<>())
        .def(python::init<const char *>())
        .def("_setlimit", &utilities::Monitor::setlimit)
        .def("_gettype", &utilities::Monitor::gettype)
        .def("_update", &utilities::Monitor::update)
    ;
   /*
    *
    */
    python::class_<utilities::Action>("Action")
        .enable_pickling()
        .def(python::init<>())
        .def(python::init<PyObject *>())
        .def_readwrite("nthreads", &utilities::Action::nthreads)
        .def_readwrite("monitor", &utilities::Action::monitor)
        .def_readwrite("target", &utilities::Action::pyTarget)
    ;
   /*
    *
    */
}
