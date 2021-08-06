#ifndef UTILITIES_EXECUTE_H
#define UTILITIES_EXECUTE_H

#include "pytypes.hpp"

using namespace bubblebox::pytypes;

namespace bubblebox::utilities
{
    CPyList executePyTask (Action& action, CPyList& unitList, CPyTuple& argsTuple);
}

#endif
