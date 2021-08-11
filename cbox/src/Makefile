#---------------------------------------------------------
# BubbleBox C++ library Makefile
#---------------------------------------------------------

basedir = $(PWD)/..

cc      = g++
flags   = -shared -fPIC -fopenmp --std=c++11 -Wl,--export-dynamic -Wdeprecated-declarations
link    = -L/usr/lib/python3.8/config -lpython3.8 -lboost_python38
include = -I$(basedir)/include -I/usr/include/python3.8 -I/usr/include -I$(INDICATORS_HOME)/include

extern = extern_utilities.so
boost  = boost_utilities.so

cbox = cbox_utilities.o

all: $(extern) $(boost)

$(extern): extern_%.so: $(cbox) extern_%.o
	$(cc) $(flags) -o $@ $^ $(link)
	cp $@ $(basedir)/extern/$*.so

$(boost): boost_%.so : $(cbox) boost_%.o
	$(cc) $(flags) -o $@ $^ $(link)
	cp $@ $(basedir)/boost/$*.so

%.o : %.cpp
	$(cc) $(flags) $(include) -c $<

clean:
	rm -rf *.o
	rm -rf *.so
