#---------------------------------------------------------
# BubbleBox C++ library Makefile
#---------------------------------------------------------

basedir = $(PWD)
include = -I/usr/include/python3.8 -I$(basedir)/../include

cc = g++
compflags = -shared -fPIC -fopenmp

util = monitor.o action.o execute.o utilities.o
libutil = utilities.lib

libdir = $(basedir)/../lib

$(libutil): $(util)
	$(cc) $(compflags) -o $(libutil) $(util)
	mkdir -p $(libdir)
	cp $(libutil) $(libdir)

%.o : %.cpp
	$(cc) $(compflags) $(include) -c $<

clean:
	rm -f *.o
	rm -f *.lib
