#ifndef CBOX_UTILITIES_H
#define CBOX_UTILITIES_H

#include <cbox/pytypes.hpp>
#include <indicators/progress_bar.hpp>
#include <indicators/progress_spinner.hpp>
#include <boost/python.hpp>

namespace pytypes = cbox::pytypes;
namespace python  = boost::python;

namespace cbox::utilities
{
   /*
    *
    *
    */
    class CPyAction: public pytypes::CPyObject
    {
    public:

        //constructors
	CPyAction() {}
	CPyAction(PyObject* _pyObj);

        //destructors
	virtual ~CPyAction() {}

        //attributes
        int nthreads;
        bool monitor;
        PyObject* target;
    };
   /*
    *
    *
    */
    class Action
    {
    public:

        //constructors
        Action() {}

        //destructors
        virtual ~Action() {}

        //attributes
        int nthreads;
        bool monitor;
    };
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
        void settype(const char* type);

    private:

        //private attributes
        int max_progress;
        int progress;
        const char *type = "none";
        indicators::ProgressBar *bar = new indicators::ProgressBar;
        indicators::ProgressSpinner *spinner = new indicators::ProgressSpinner;

    };
   /*
    *
    */
    pytypes::CPyList executePyTask (CPyAction& action, pytypes::CPyList& unitList, pytypes::CPyTuple& argsTuple);
    pytypes::CPyList executePyTask (Action& action, pytypes::CPyList& unitList, pytypes::CPyTuple& argsTuple);
   /*
    *
    *
    */
}
#endif
