#include <cbox/create.h>
#include <boost/python.hpp>
/*
 *
 *
 */
namespace create = cbox::create;
namespace python = boost::python;
/*
 *
 *
 */
BOOST_PYTHON_MODULE(create)
{
    python::class_<create::Data>("Data")
        .enable_pickling()
        .def(python::init<>())
        .def_readwrite("nblocks", &create::Data::nblocks)
        .def_readwrite("nxb", &create::Data::nxb)
        .def_readwrite("nyb", &create::Data::nyb)
        .def_readwrite("nzb", &create::Data::nzb)
    ;
   /*
    *
    */
}
