#ifndef CBOX_PYTYPES_H
#define CBOX_PYTYPES_H
#pragma once

#include <Python.h>

namespace cbox::pytypes
{

    class CPyInstance
    {
    public:

        //constructors
        CPyInstance() { Py_Initialize(); }

        //destructors
        ~CPyInstance() { Py_Finalize(); }
    };

    class CPyObject
    {
    private:

        //private attributes
        PyObject *pyObj;

    public:

        //constructors
        CPyObject() : pyObj(NULL) {}
        CPyObject(PyObject* ptrObj) : pyObj(ptrObj) {}
	
        //destructors
        virtual ~CPyObject() { DelPyRef();}
 
        //methods
	PyObject* getPyObject() { return this->pyObj; }

	PyObject* setPyObject(PyObject* ptrObj) 
        { 
            this->pyObj = ptrObj;
            return this->pyObj; 
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

        //operators
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

	PyObject* operator = (PyObject* ptrObj)
	{
		this->pyObj = ptrObj;
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

        //constructors
        CPyList() {}
        CPyList(PyObject* listPtr) : CPyObject(listPtr) {}

        //destructors
        virtual ~CPyList() {}

        //methods
	PyObject* pyList() { return this->getPyObject();}

        Py_ssize_t len()
        {
            if(this->pyList())
            {
                return PyList_Size(this->pyList());
            } else 
            { 
                return 0;
            }
        }

        PyObject* getItem(Py_ssize_t loc)
        {
            if(this->pyList())
            {
                return PyList_GetItem(this->pyList(), loc);
            } else { 
                return NULL;
            }
        }

        void setItem(Py_ssize_t loc, PyObject* value)
        {
            if(this->pyList())
            {
                PyList_SetItem(this->pyList(), loc, value);
            }
        }

        //operators
	PyObject* operator = (PyObject* listPtr)
	{
		this->setPyObject(listPtr);
		return this->pyList();
	}
    };


    class CPyTuple: public CPyObject
    {
    public:

        //constructors
        CPyTuple() {}
        CPyTuple(PyObject* tuplePtr) : CPyObject(tuplePtr) {}

        //destructors
        virtual ~CPyTuple() {}

        //methods
	PyObject* pyTuple() { return this->getPyObject();}

        Py_ssize_t len()
        {
            if(this->pyTuple())
            {
                return PyTuple_Size(this->pyTuple());
            } else { 
                return 0;
            }
        }

        PyObject* getItem(Py_ssize_t loc)
        {
            if(this->pyTuple())
            {
                return PyTuple_GetItem(this->pyTuple(), loc);
            } else { 
                return NULL;
            }
        }

        void setItem(Py_ssize_t loc, PyObject* value)
        {
            if(this->pyTuple())
            {
                PyTuple_SetItem(this->pyTuple(), loc, value);
            }            
        }

        //operators
	PyObject* operator = (PyObject* tuplePtr)
	{
		this->setPyObject(tuplePtr);
		return this->pyTuple();
	}
    };

}
#endif
