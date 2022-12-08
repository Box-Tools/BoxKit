# --------------------
# Boxkit C++ Makefile
# --------------------

.PHONY: all clean

lib = library.so
objects = data.o \
	  block.o \
	  region.o \
	  action.o \
          monitor.o \
          execute.o

all: $(lib)

$(lib): %.so: $(objects) %.o

include Make.inc
