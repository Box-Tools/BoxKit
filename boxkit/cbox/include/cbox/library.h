#ifndef CBOX_LIBRARY_H
#define CBOX_LIBRARY_H

#include <indicators/progress_bar.hpp>
#include <indicators/progress_spinner.hpp>
#include <cbox/pytypes.hpp>

namespace pytypes = cbox::pytypes;

namespace cbox::library {
/*
 */
class Data {
public:
  // constructors
  Data() {}

  // destructors
  virtual ~Data() {}

  // attributes
  unsigned int nxb = 1, nyb = 1, nzb = 1, nblocks = 1;
  unsigned int xguard = 0, yguard = 0, zguard = 0;
};
/*
 */
class Block {
public:
  // constructors
  Block() {}
  Block(Data &data);

  // destructors
  virtual ~Block() {}

  // attributes
  unsigned int tag = 0;
  unsigned int nxb = 1, nyb = 1, nzb = 1;
  float xmin = 0, ymin = 0, zmin = 0;
  float xmax = 0, ymax = 0, zmax = 0;
  float dx = 0, dy = 0, dz = 0;
  unsigned int xguard = 0, yguard = 0, zguard = 0;

private:
  Data data;
};
/*
 */
class Region {
public:
  // constructors
  Region() {}

  // destructors
  virtual ~Region() {}

  // attributes
  float xmin = 0, ymin = 0, zmin = 0;
  float xmax = 0, ymax = 0, zmax = 0;
};
/*
 */
class Action : public pytypes::CPyObject {
public:
  // constructors
  Action();
  Action(PyObject *ptrAction);

  // destructors
  virtual ~Action();

  // attributes
  unsigned int nthreads = 1;
  bool monitor = false;

  PyObject *pyTarget = NULL;

  // methods
  PyObject *pyAction() { return this->getPyObject(); }
};
/*
 */
class Monitor {
public:
  // constructors
  Monitor() {}
  Monitor(const char *type);

  // destructors
  virtual ~Monitor() {}

  // methods
  void setlimit(int iterlimit);
  void update(std::string msg = "", int progress = 0);
  const char *gettype();

private:
  // private attributes
  int max_progress = 0;
  int progress = 0;
  const char *type = "none";
  indicators::ProgressBar *bar = new indicators::ProgressBar;
  indicators::ProgressSpinner *spinner = new indicators::ProgressSpinner;
};
/*
 */
pytypes::CPyList execute_pyTask(Action &action, pytypes::CPyList &unitList,
                                pytypes::CPyTuple &argsTuple);
/*
 */
} // namespace cbox::library
#endif
/*
 *
 *
 */
