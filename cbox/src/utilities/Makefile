# ----------------------
# Bubblebox C++ Makefile
# ----------------------

lib := utilities.so
objects := action.o monitor.o execute.o

all: $(lib)

$(lib): %.so: $(objects) %.o

include ../Make.inc
