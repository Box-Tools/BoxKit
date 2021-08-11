#include <cbox/utilities.h>
/*
 *
 *
 */
namespace utilities = cbox::utilities;
namespace pytypes   = cbox::pytypes;

namespace python    = boost::python;

namespace cbox::boost
{
    PyObject* executePyTask(utilities::Action& action, PyObject* PyUnitList, PyObject* PyArgsTuple)
    {
        pytypes::CPyList unitList = PyUnitList;
        pytypes::CPyTuple argsTuple = PyArgsTuple;

        return utilities::executePyTask(action,unitList,argsTuple);
    }
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
        .def_readwrite("nthreads", &utilities::Action::nthreads)
        .def_readwrite("monitor", &utilities::Action::monitor)
    ;
   /*
    *
    */
    python::def("executePyTask", &cbox::boost::executePyTask);
}
