#ifndef BUBBLEBOX_UTILITIES_H
#define BUBBLEBOX_UTILITIES_H

#include <bubblebox/pytypes.hpp>
#include <indicators/progress_bar.hpp>
#include <indicators/progress_spinner.hpp>
#include <boost/python.hpp>

namespace pytypes = bubblebox::pytypes;
namespace python = boost::python;

namespace bubblebox::utilities
{
   /*
    *
    *
    */
    class ActionExtern: public pytypes::CPyObject
    {
    public:

        //constructors
	ActionExtern() {}
	ActionExtern(PyObject* _pyObj);

        //destructors
	virtual ~ActionExtern() {}

        //attributes
        int nthreads;
        bool monitor;
        PyObject* target;
    };
   /*
    *
    *
    */
    pytypes::CPyList executeExternTask (ActionExtern& action, pytypes::CPyList& unitList, pytypes::CPyTuple& argsTuple);
   /*
    *
    *
    */
    class Monitor
    {
    public:

        //constructors
        Monitor() {}
        Monitor(const char *type);

        //destructors
        virtual ~Monitor() {}

        //methods
        void setlimit(int iterlimit);
        void update(std::string msg="", int progress=0);
        const char *gettype();

    private:

        //private attributes
        int max_progress;
        int progress;
        const char *type;
        indicators::ProgressBar *bar = new indicators::ProgressBar;
        indicators::ProgressSpinner *spinner = new indicators::ProgressSpinner;

    };
   /*
    *
    */
    void executeBoostTask (Monitor& monitor);
}
#endif
