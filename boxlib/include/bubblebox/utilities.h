#ifndef BUBBLEBOX_UTILITIES_H
#define BUBBLEBOX_UTILITIES_H

#include <bubblebox/pytypes.hpp>
#include <indicators/progress_bar.hpp>


using namespace bubblebox::pytypes;

namespace bubblebox::utilities
{
   /*
    *
    *
    */
    class Action: public CPyObject
    {
    public:

        //constructors
	Action() {}
	Action(PyObject* _pyObject);

        //destructors
	virtual ~Action() {}

        //attributes
        int nthreads;
        bool monitor;
        PyObject* target;
    };
   /*
    *
    *
    */
    CPyList executePyTask (Action& action, CPyList& unitList, CPyTuple& argsTuple);
   /*
    *
    *
    */
    class Monitor
    {
    public:

        //constructors
        Monitor() {}
        Monitor(const char *bartype);

        //destructors
        virtual ~Monitor() {}

        //methods
        void setIterLimit(int iterlimit);
        void updateBar();

    private:

        //private attributes
        int max_progress;
        int progress;
        indicators::ProgressBar progressBar;

    };
   /*
    *
    */
}
#endif
