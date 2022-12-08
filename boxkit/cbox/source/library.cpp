#include <boost/python.hpp>
#include <cbox/library.h>

namespace library = cbox::library;
namespace python = boost::python;
namespace pytypes = cbox::pytypes;
/*
 *
 *
 */
BOOST_PYTHON_MODULE(library) {
  python::class_<library::Data>("Data")
      .enable_pickling()
      .def(python::init<>())
      .def_readwrite("nblocks", &library::Data::nblocks)
      .def_readwrite("nxb", &library::Data::nxb)
      .def_readwrite("nyb", &library::Data::nyb)
      .def_readwrite("nzb", &library::Data::nzb)
      .def_readwrite("xguard", &library::Data::xguard)
      .def_readwrite("yguard", &library::Data::yguard)
      .def_readwrite("zguard", &library::Data::zguard);
  /*
   */
  python::class_<library::Block>("Block")
      .enable_pickling()
      .def(python::init<>())
      .def_readwrite("tag", &library::Block::tag)
      .def_readwrite("nxb", &library::Block::nxb)
      .def_readwrite("nyb", &library::Block::nyb)
      .def_readwrite("nzb", &library::Block::nzb)
      .def_readwrite("xguard", &library::Block::xguard)
      .def_readwrite("yguard", &library::Block::yguard)
      .def_readwrite("zguard", &library::Block::zguard)
      .def_readwrite("dx", &library::Block::dx)
      .def_readwrite("dy", &library::Block::dy)
      .def_readwrite("dz", &library::Block::dz)
      .def_readwrite("xmin", &library::Block::xmin)
      .def_readwrite("ymin", &library::Block::ymin)
      .def_readwrite("zmin", &library::Block::zmin)
      .def_readwrite("xmax", &library::Block::xmax)
      .def_readwrite("ymax", &library::Block::ymax)
      .def_readwrite("zmax", &library::Block::zmax);
  /*
   */
  python::class_<library::Region>("Region")
      .enable_pickling()
      .def(python::init<>())
      .def_readwrite("xmin", &library::Region::xmin)
      .def_readwrite("ymin", &library::Region::ymin)
      .def_readwrite("zmin", &library::Region::zmin)
      .def_readwrite("xmax", &library::Region::xmax)
      .def_readwrite("ymax", &library::Region::ymax)
      .def_readwrite("zmax", &library::Region::zmax);
  /*
   */
  python::class_<library::Monitor>("Monitor")
      .enable_pickling()
      .def(python::init<>())
      .def(python::init<const char *>())
      .def("_setlimit", &library::Monitor::setlimit)
      .def("_gettype", &library::Monitor::gettype)
      .def("_update", &library::Monitor::update);
  /*
   */
  python::class_<library::Action>("Action")
      .enable_pickling()
      .def(python::init<>())
      .def(python::init<PyObject *>())
      .def_readwrite("nthreads", &library::Action::nthreads)
      .def_readwrite("monitor", &library::Action::monitor)
      .def_readwrite("target", &library::Action::pyTarget);
}
/*
 *
 *
 */
extern "C" {
PyObject *execute_pyTask(PyObject *PyAction, PyObject *PyUnitList,
                         PyObject *PyArgsTuple) {
  library::Action action = PyAction;
  cbox::pytypes::CPyList unitList = PyUnitList;
  cbox::pytypes::CPyTuple argsTuple = PyArgsTuple;

  return library::execute_pyTask(action, unitList, argsTuple);
}
}
/*
 *
 *
 */
