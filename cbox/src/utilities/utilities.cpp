#include <cbox/utilities.h>
#include <boost/python.hpp>

namespace utilities = cbox::utilities;
namespace pytypes = cbox::pytypes;
namespace python  = boost::python;
/*
 *
 *
 */
extern "C" 
{
    PyObject* execute_pyTask (PyObject* PyAction, PyObject* PyUnitList, PyObject* PyArgsTuple)
    {
        utilities::Action action = PyAction;
        cbox::pytypes::CPyList unitList = PyUnitList;
        cbox::pytypes::CPyTuple argsTuple = PyArgsTuple;

        return utilities::execute_pyTask(action, unitList, argsTuple);
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
    */
    python::class_<utilities::Action>("Action")
        .enable_pickling()
        .def(python::init<>())
        .def(python::init<PyObject *>())
        .def_readwrite("nthreads", &utilities::Action::nthreads)
        .def_readwrite("monitor", &utilities::Action::monitor)
        .def_readwrite("target", &utilities::Action::pyTarget)
    ;
}
/*
 *
 */
