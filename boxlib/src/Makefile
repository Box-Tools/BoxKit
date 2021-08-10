#---------------------------------------------------------
# BubbleBox C++ library Makefile
#---------------------------------------------------------

BASEDIR = $(PWD)

CC = g++

FLAGS_BUBBLEBOX = -shared -fPIC -fopenmp --std=c++11 -Wl,--export-dynamic

INC_BUBBLEBOX = -I$(BASEDIR)/../include
INC_PYTHON = -I/usr/include/python3.8

LINK_PYTHON = -L/usr/lib/python3.8/config -lpython3.8
LINK_BOOST = -lboost_python38

LIB_EXTERN = utilities_extern.so
LIB_BOOST = utilities_boost.so

all: $(LIB_EXTERN) $(LIB_BOOST)

$(LIB_EXTERN): %_extern.so: %.o %_extern.o
	$(CC) $(FLAGS_BUBBLEBOX) -o $@ $^ $(LINK_PYTHON)
	mkdir -p $(BASEDIR)/../lib/extern
	cp $@ $(BASEDIR)/../lib/extern

$(LIB_BOOST): %_boost.so : %.o %_boost.o
	$(CC) $(FLAGS_BUBBLEBOX) -o $@ $^ $(LINK_BOOST) $(LINK_PYTHON)
	mkdir -p $(BASEDIR)/../lib/boost
	cp $@ $(BASEDIR)/../lib/boost

%.o : %.cpp
	$(CC) $(FLAGS_BUBBLEBOX) $(INC_BUBBLEBOX) $(INC_PYTHON) -c $<

%_extern.o : %_extern.cpp
	$(CC) $(FLAGS_BUBBLEBOX) $(INC_BUBBLEBOX) $(INC_PYTHON) -c $<


%_boost.o : %_boost.cpp
	$(CC) $(FLAGS_BUBBLEBOX) $(INC_BUBBLEBOX) $(INC_PYTHON) -c $<

clean:
	rm -rf *.o
	rm -rf *.so
