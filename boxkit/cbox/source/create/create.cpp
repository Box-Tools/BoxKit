#include <boost/python.hpp>
#include <cbox/create.h>

namespace create = cbox::create;
namespace python = boost::python;
/*
 *
 *
 */
BOOST_PYTHON_MODULE(create) {
  python::class_<create::Data>("Data")
      .enable_pickling()
      .def(python::init<>())
      .def_readwrite("nblocks", &create::Data::nblocks)
      .def_readwrite("nxb", &create::Data::nxb)
      .def_readwrite("nyb", &create::Data::nyb)
      .def_readwrite("nzb", &create::Data::nzb)
      .def_readwrite("xguard", &create::Data::xguard)
      .def_readwrite("yguard", &create::Data::yguard)
      .def_readwrite("zguard", &create::Data::zguard);
  /*
   */
  python::class_<create::Block>("Block")
      .enable_pickling()
      .def(python::init<>())
      .def_readwrite("tag", &create::Block::tag)
      .def_readwrite("nxb", &create::Block::nxb)
      .def_readwrite("nyb", &create::Block::nyb)
      .def_readwrite("nzb", &create::Block::nzb)
      .def_readwrite("xguard", &create::Block::xguard)
      .def_readwrite("yguard", &create::Block::yguard)
      .def_readwrite("zguard", &create::Block::zguard)
      .def_readwrite("dx", &create::Block::dx)
      .def_readwrite("dy", &create::Block::dy)
      .def_readwrite("dz", &create::Block::dz)
      .def_readwrite("xmin", &create::Block::xmin)
      .def_readwrite("ymin", &create::Block::ymin)
      .def_readwrite("zmin", &create::Block::zmin)
      .def_readwrite("xmax", &create::Block::xmax)
      .def_readwrite("ymax", &create::Block::ymax)
      .def_readwrite("zmax", &create::Block::zmax);
  /*
   */
  python::class_<create::Region>("Region")
      .enable_pickling()
      .def(python::init<>())
      .def_readwrite("xmin", &create::Region::xmin)
      .def_readwrite("ymin", &create::Region::ymin)
      .def_readwrite("zmin", &create::Region::zmin)
      .def_readwrite("xmax", &create::Region::xmax)
      .def_readwrite("ymax", &create::Region::ymax)
      .def_readwrite("zmax", &create::Region::zmax);
  /*
   */
}
/*
 *
 */
