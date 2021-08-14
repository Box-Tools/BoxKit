#ifndef CBOX_UTILITIES_H
#define CBOX_UTILITIES_H

#include <cbox/pytypes.hpp>

#include <indicators/progress_bar.hpp>
#include <indicators/progress_spinner.hpp>

namespace pytypes = cbox::pytypes;
namespace indicators = indicators;
/*
 *
 *
 */
namespace cbox::utilities
{
    class Action: public pytypes::CPyObject
    {
    public:

        //constructors
        Action();
        Action(PyObject *ptrAction);

        //destructors
        virtual ~Action();

        //attributes
        int  nthreads = 1;
        bool monitor  = false;

        PyObject *pyTarget = NULL;

        //methods
        PyObject *pyAction() { return this->getPyObject();}
    };
   /*
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
        int max_progress = 0;
        int progress = 0;
        const char *type = "none";
        indicators::ProgressBar *bar = new indicators::ProgressBar;
        indicators::ProgressSpinner *spinner = new indicators::ProgressSpinner;

    };
   /*
    */
    pytypes::CPyList executePyTask (Action& action, pytypes::CPyList& unitList, pytypes::CPyTuple& argsTuple);
   /*
    */
}
#endif
/*
 *
 *
 */
