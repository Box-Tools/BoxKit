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
        PyObject *pyObject;
    public:
        CPyObject() : pyObject(NULL)
        {}

        CPyObject(PyObject* _p) : pyObject(_p)
	{}
	
        virtual ~CPyObject()
        {
            DelPyRef();
	}

	PyObject* getPyObject()
	{
	    return pyObject;
	}

	PyObject* setPyObject(PyObject* _p)
	{
	    return (pyObject=_p);
	}

	PyObject* AddPyRef()
	{
	    if(pyObject)
	    {
	        Py_INCREF(pyObject);
	    }
	    return pyObject;
	}

	void DelPyRef()
	{
	    if(pyObject)
	    {
	        Py_DECREF(pyObject);
	    }

	    pyObject = NULL;
	}

	PyObject* operator ->()
	{
	    return pyObject;
	}

	bool is()
	{
	    return pyObject ? true : false;
	}

	operator PyObject*()
	{
	    return pyObject;
	}

	PyObject* operator = (PyObject* pp)
	{
		pyObject = pp;
		return pyObject;
	}

	operator bool()
	{
	    return pyObject ? true : false;
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
            if(pyObject)
            {
                return PyList_Size(pyObject);
            } else { 
                return 0;
            }
        }

        PyObject* getItem(Py_ssize_t loc)
        {
            if(pyObject)
            {
                return PyList_GetItem(pyObject, loc);
            } else { 
                return NULL;
            }
        }

        void setItem(Py_ssize_t loc, PyObject* value)
        {
            if(pyObject)
            {
                PyList_SetItem(pyObject, loc, value);
            }
        }

	PyObject* operator = (PyObject* pp)
	{
		pyObject = pp;
		return pyObject;
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
            if(pyObject)
            {
                return PyTuple_Size(pyObject);
            } else { 
                return 0;
            }
        }

        PyObject* getItem(Py_ssize_t loc)
        {
            if(pyObject)
            {
                return PyTuple_GetItem(pyObject, loc);
            } else { 
                return NULL;
            }
        }

        void setItem(Py_ssize_t loc, PyObject* value)
        {
            if(pyObject)
            {
                PyTuple_SetItem(pyObject, loc, value);
            }            
        }

	PyObject* operator = (PyObject* pp)
	{
		pyObject = pp;
		return pyObject;
	}
    };

}
#endif
