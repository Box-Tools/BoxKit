#ifndef UTILITIES_ACTION_H
#define UTILITIES_ACTION_H

#include "pytypes.hpp"

using namespace bubblebox::pytypes;

namespace bubblebox::utilities
{

    class Action: public CPyObject
    {
    public:
	Action() {}
	Action(PyObject* _pyObject);
	virtual ~Action() {}
        int nthreads;
        bool monitor;
        PyObject* target;
    };

}
#endif
