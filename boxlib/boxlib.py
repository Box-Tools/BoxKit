import os
import sys
import ctypes

libname = "./src/boxlib.so"
libpath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + libname

boxlib  = ctypes.cdll.LoadLibrary(libpath)

boxlib.parallel_wrapper.argtypes = [ctypes.py_object,ctypes.py_object]
boxlib.parallel_wrapper.restype  = ctypes.py_object

def target_function(object):
    return object**2

def main():
    object_list = [1,2,3,4]
    result_list = boxlib.parallel_wrapper(target_function,object_list) 
    print(result_list)

if __name__ == "__main__":
    main()
