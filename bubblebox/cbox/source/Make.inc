# -------------------------------
# Bubblebox C++ Makefile include
# -------------------------------

basedir = $(shell pwd)/../..
cc      = g++
flags   = -shared -fPIC -fopenmp --std=c++11 -Wl,--export-dynamic
linkers = -L/usr/lib/python3.8/config -lpython3.8 -lboost_python38
headers = -I$(basedir)/include -I/usr/include/python3.8 -I/usr/include

%.so: %.o
	$(cc) $(flags) -o $@ $^ $(linkers)
	cp $@ $(basedir)/lib/$*.so

%.o: %.cpp
	$(cc) $(flags) $(headers) -c $<

clean:
	rm -rf *.o
	rm -rf *.so