#ifndef BUBBLEBOX_UTILITIES_H
#define BUBBLEBOX_UTILITIES_H

#include <bubblebox/pytypes.hpp>
#include <indicators/progress_bar.hpp>
#include <indicators/progress_spinner.hpp>

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
        Monitor(const char *_type);

        //destructors
        virtual ~Monitor() {}

        //methods
        void setlimit(int iterlimit);
        void update(std::string _msg="", int _progress=0);

    private:

        //private attributes
        int max_progress;
        int progress;
        const char *type;
        indicators::ProgressBar bar;
        indicators::ProgressSpinner spinner;

    };
   /*
    *
    */
}
#endif
