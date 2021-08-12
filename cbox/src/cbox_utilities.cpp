#include <cbox/utilities.h>
#include <string.h>
#include <omp.h>
/*
 *
 *
 */
namespace pytypes = cbox::pytypes;

namespace cbox::utilities
{
   /*
    *
    *
    */
    Monitor::Monitor(const char *type): max_progress(0), progress(0)
    {
        this->type = type;

        if (strcmp(this->type,"action") == 0)
        {
            this->bar->set_option(indicators::option::Start{"["});
            this->bar->set_option(indicators::option::Fill{"■"});
            this->bar->set_option(indicators::option::Lead{"■"});
            this->bar->set_option(indicators::option::Remainder{"-"});
            this->bar->set_option(indicators::option::End{"]"});
            this->bar->set_option(indicators::option::ShowPercentage{true});
            this->bar->set_option(indicators::option::ForegroundColor{indicators::Color::cyan});
            this->bar->set_option(indicators::option::BarWidth{50});
            this->bar->set_option(indicators::option::FontStyles{std::vector<indicators::FontStyle>
                                                                {indicators::FontStyle::bold}});

        } else if (strcmp(this->type,"test") == 0) 
        {       
            this->bar->set_option(indicators::option::BarWidth{0});
            this->bar->set_option(indicators::option::Start{""});
            this->bar->set_option(indicators::option::Fill{""});
            this->bar->set_option(indicators::option::Lead{""});
            this->bar->set_option(indicators::option::Remainder{""});
            this->bar->set_option(indicators::option::End{""});
            this->bar->set_option(indicators::option::ForegroundColor{indicators::Color::green});
            this->bar->set_option(indicators::option::ShowPercentage{true});
            this->bar->set_option(indicators::option::FontStyles{std::vector<indicators::FontStyle>
                                                                {indicators::FontStyle::bold}});
        }

    }


    void Monitor::setlimit(int iterlimit)
    {
        this->max_progress = iterlimit;
        this->bar->set_option(indicators::option::MaxProgress{this->max_progress});
        this->spinner->set_option(indicators::option::MaxProgress{this->max_progress});
    }
    

    void Monitor::update(std::string msg,int progress)
    {
        if(strcmp(this->type,"action") == 0 || strcmp(this->type,"test") == 0)
        {
            ++this->progress;
            this->bar->set_option(indicators::option::PrefixText{msg});
            this->bar->tick();
        }
    }


    const char *Monitor::gettype()
    {
        return this->type;
    }
   /*
    *
    *
    */
    pytypes::CPyList executePyTask (Action& action, pytypes::CPyList& unitList, pytypes::CPyTuple& argsTuple) 
    {

        int nthreads = PyLong_AsLong(PyObject_GetAttrString(action,"nthreads"));
        bool monitor  = PyObject_IsTrue(PyObject_GetAttrString(action,"monitor"));
        pytypes::CPyObject target = PyObject_GetAttrString(action,"target");

        Py_ssize_t numUnits = unitList.len();
        Py_ssize_t numArgs = argsTuple.len() + 2;

        pytypes::CPyList resultList = PyList_New(numUnits);

        pytypes::CPyTuple targetArgs;
        pytypes::CPyObject arg, unit, result;

        omp_set_dynamic(0);
        omp_set_num_threads(nthreads);

        Monitor actionMonitor("action");
        actionMonitor.setlimit(numUnits);

        //#pragma omp parallel default(shared) private(targetArgs,arg,unit,result)
        for (Py_ssize_t i = 0; i < numUnits; i++) 
        {

            targetArgs = PyTuple_New(numArgs);
          
            action.AddPyRef();
            targetArgs.setItem(0, action);

            unit = unitList.getItem(i);
            unit.AddPyRef();
            targetArgs.setItem(1, unit);

            for (Py_ssize_t j = 2; j < numArgs; j++) 
            { 
                arg = argsTuple.getItem(j-2);
                arg.AddPyRef();
                targetArgs.setItem(j, arg);
            }     

            PyGILState_STATE gstate = PyGILState_Ensure();

            targetArgs.AddPyRef();
            result = PyObject_CallObject(target, targetArgs);

            result.AddPyRef();
            resultList.setItem(i,result);

            PyGILState_Release(gstate);

            if(monitor)
            {
                //#pragma omp critical
                actionMonitor.update();
            }
        }

        //PyObject_SetAttrString(action,"nthreads",Py_BuildValue("i", 42));

        resultList.AddPyRef();
        return resultList;
    }
   /*
    *
    *
    */
}
