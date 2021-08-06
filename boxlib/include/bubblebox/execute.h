#ifndef BUBBLEBOX_EXECUTE_H
#define BUBBLEBOX_EXECUTE_H

#include <bubblebox/pytypes.hpp>

using namespace bubblebox::pytypes;

namespace bubblebox::utilities
{
    CPyList executePyTask (Action& action, CPyList& unitList, CPyTuple& argsTuple);
}

#endif
