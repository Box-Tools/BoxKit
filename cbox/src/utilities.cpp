#include <bubblebox/utilities.h>
#include <string.h>
#include <omp.h>
/*
*
*
*/
namespace pytypes = bubblebox::pytypes;
namespace python  = boost::python;

namespace bubblebox::utilities
{
   /*
    *
    *
    */
    CPyAction::CPyAction(PyObject* pyObj) : pytypes::CPyObject(pyObj)
    {
        this->nthreads = PyLong_AsLong(PyObject_GetAttrString(this->pyObj,"nthreads"));
        this->monitor  = PyObject_IsTrue(PyObject_GetAttrString(this->pyObj,"monitor"));
        this->target   = PyObject_GetAttrString(this->pyObj,"target");
    }
   /*
    *
    *
    */
    Monitor::Monitor(const char *type): max_progress(0), progress(0)
    {
        if (strcmp(type,"action") == 0)
        {
            this->type = "action";

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

        } else if (strcmp(type,"test") == 0) {
       
            this-> type = "test";

            this->bar->set_option(indicators::option::BarWidth{0});
            this->bar->set_option(indicators::option::Start{""});
            this->bar->set_option(indicators::option::Fill{""});
            this->bar->set_option(indicators::option::Lead{""});
            this->bar->set_option(indicators::option::Remainder{""});
            this->bar->set_option(indicators::option::End{""});
            this->bar->set_option(indicators::option::ForegroundColor{indicators::Color::white});
            this->bar->set_option(indicators::option::ShowPercentage{true});
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
        if(strcmp(type,"action") == 0 || strcmp(type,"test") == 0)
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
    pytypes::CPyList executePyTask (CPyAction& action, pytypes::CPyList& unitList, pytypes::CPyTuple& argsTuple) 
    {
        Py_ssize_t numUnits = unitList.len();
        Py_ssize_t numArgs = argsTuple.len() + 2;

        pytypes::CPyList resultList = PyList_New(numUnits);

        pytypes::CPyTuple targetArgs;
        pytypes::CPyObject arg, unit, result;

        omp_set_dynamic(0);
        omp_set_num_threads(action.nthreads);

        Monitor monitor("action");
        monitor.setlimit(numUnits);

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
            result = PyObject_CallObject(action.target, targetArgs);

            result.AddPyRef();
            resultList.setItem(i,result);

            PyGILState_Release(gstate);

            if(action.monitor)
            {
                //#pragma omp critical
                monitor.update();
            }
        }

        resultList.AddPyRef();
        return resultList;
    }
   /*
    *
    *
    */
    pytypes::CPyList executePyTask (Monitor& monitor)
    {
        std::cout<<"C++ call"<<std::endl;
        std::cout<<"Monitor type: "<<monitor.gettype()<<std::endl;

        pytypes::CPyList resultList;

        resultList.AddPyRef();
        return resultList;
    }
   /*
    *
    *
    */
}
