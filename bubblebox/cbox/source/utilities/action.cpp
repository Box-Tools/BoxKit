#include <cbox/utilities.h>

namespace pytypes = cbox::pytypes;
/*
 *
 *
 */
namespace cbox::utilities {
Action::Action() : pytypes::CPyObject() {}

Action::Action(PyObject *ptrAction) : pytypes::CPyObject(ptrAction) {
  this->nthreads =
      PyLong_AsLong(PyObject_GetAttrString(this->pyAction(), "nthreads"));
  this->monitor =
      PyObject_IsTrue(PyObject_GetAttrString(this->pyAction(), "monitor"));
  this->pyTarget = PyObject_GetAttrString(this->pyAction(), "target");
}

Action::~Action() {
  if (this->pyAction()) {
    PyObject_SetAttrString(this->pyAction(), "nthreads",
                           Py_BuildValue("i", this->nthreads));
    PyObject_SetAttrString(this->pyAction(), "monitor",
                           Py_BuildValue("i", this->monitor));
  }
}

} // namespace cbox::utilities
