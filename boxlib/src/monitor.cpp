#include<bubblebox.h>
/*
*
*/
using namespace indicators;

namespace bubblebox::utilities
{

    Monitor::Monitor(int _numIter) : numIter(_numIter), progress(0)
    {}

    void Monitor::update()
    {
        ++progress;
        bar.set_option(option::PostfixText{std::to_string(progress) + "/" + std::to_string(numIter)});
        bar.tick();
    }

    void Monitor::finish()
    {
       bar.mark_as_completed();
    }
}
