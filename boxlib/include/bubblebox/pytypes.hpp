#ifndef BUBBLEBOX_PYTYPES_H
#define BUBBLEBOX_PYTYPES_H
#pragma once

#include <Python.h>

namespace bubblebox::pytypes
{

    class CPyInstance
    {
    public:
        CPyInstance()
        {
	    Py_Initialize();
        }

        ~CPyInstance()
        {
	    Py_Finalize();
        }
    };


    class CPyObject
    {
    protected:
        PyObject *pyObj;
    public:
        CPyObject() : pyObj(NULL)
        {}

        CPyObject(PyObject* _p) : pyObj(_p)
	{}
	
        virtual ~CPyObject()
        {
            DelPyRef();
	}

	PyObject* getPyObject()
	{
	    return this->pyObj;
	}

	PyObject* setPyObject(PyObject* _p)
	{
	    return (this->pyObj=_p);
	}

	PyObject* AddPyRef()
	{
	    if(this->pyObj)
	    {
	        Py_INCREF(this->pyObj);
	    }
	    return this->pyObj;
	}

	void DelPyRef()
	{
	    if(this->pyObj)
	    {
	        Py_DECREF(this->pyObj);
	    }

	    this->pyObj = NULL;
	}

	PyObject* operator ->()
	{
	    return this->pyObj;
	}

	bool is()
	{
	    return this->pyObj ? true : false;
	}

	operator PyObject*()
	{
	    return this->pyObj;
	}

	PyObject* operator = (PyObject* pp)
	{
		this->pyObj = pp;
		return this->pyObj;
	}

	operator bool()
	{
	    return this->pyObj ? true : false;
	}
    };


    class CPyList: public CPyObject
    {
    public:
        CPyList() {}

        CPyList(PyObject* _p) : CPyObject(_p) {}

        virtual ~CPyList() {}

        Py_ssize_t len()
        {
            if(this->pyObj)
            {
                return PyList_Size(this->pyObj);
            } else { 
                return 0;
            }
        }

        PyObject* getItem(Py_ssize_t loc)
        {
            if(this->pyObj)
            {
                return PyList_GetItem(this->pyObj, loc);
            } else { 
                return NULL;
            }
        }

        void setItem(Py_ssize_t loc, PyObject* value)
        {
            if(this->pyObj)
            {
                PyList_SetItem(this->pyObj, loc, value);
            }
        }

	PyObject* operator = (PyObject* pp)
	{
		this->pyObj = pp;
		return this->pyObj;
	}
    };


    class CPyTuple: public CPyObject
    {
    public:
        CPyTuple() {}

        CPyTuple(PyObject* _p) : CPyObject(_p) {}

        virtual ~CPyTuple() {}

        Py_ssize_t len()
        {
            if(this->pyObj)
            {
                return PyTuple_Size(this->pyObj);
            } else { 
                return 0;
            }
        }

        PyObject* getItem(Py_ssize_t loc)
        {
            if(this->pyObj)
            {
                return PyTuple_GetItem(this->pyObj, loc);
            } else { 
                return NULL;
            }
        }

        void setItem(Py_ssize_t loc, PyObject* value)
        {
            if(this->pyObj)
            {
                PyTuple_SetItem(this->pyObj, loc, value);
            }            
        }

	PyObject* operator = (PyObject* pp)
	{
		this->pyObj = pp;
		return this->pyObj;
	}
    };

}
#endif
