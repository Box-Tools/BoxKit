#---------------------------------------------------------
# BubbleBox C++ library Makefile
#---------------------------------------------------------

BASEDIR = $(PWD)

CC = g++
FLAGS = -shared -fPIC -fopenmp --std=c++11 -Wl,--export-dynamic
INCLUDE = -I$(BASEDIR)/../include -I/usr/include/python3.8 -I/usr/include

LINK_PYTHON = -L/usr/lib/python3.8/config -lpython3.8
LINK_BOOST = -lboost_python38

LIB_EXTERN = utilities_extern.so
LIB_BOOST = utilities_boost.so

all: $(LIB_EXTERN) $(LIB_BOOST)

extern: $(LIB_EXTERN)

boost: $(LIB_BOOST)

$(LIB_EXTERN): %_extern.so: %.o %_extern.o
	$(CC) $(FLAGS) -o $@ $^ $(LINK_PYTHON)
	cp $@ $(BASEDIR)/../extern/$*.so

$(LIB_BOOST): %_boost.so : %.o %_boost.o
	$(CC) $(FLAGS) -o $@ $^ $(LINK_BOOST) $(LINK_PYTHON)
	cp $@ $(BASEDIR)/../boost/$*.so

%.o : %.cpp
	$(CC) $(FLAGS) $(INCLUDE) -c $<

%_extern.o : %_extern.cpp
	$(CC) $(FLAGS) $(INCLUDE) -c $<


%_boost.o : %_boost.cpp
	$(CC) $(FLAGS) $(INCLUDE) -c $<

clean:
	rm -rf *.o
	rm -rf *.so
