# -------------------------------
# Boxkit C++ Makefile include
# -------------------------------

# set versions
python_version = 3.8
boost_version = 38

#set paths
python_path = /usr
boost_path = /usr

# Set base directory
basedir = $(shell pwd)/../..

# Set c++ compiler
cc = g++

# Set common flags
flags = -shared -fPIC -fopenmp --std=c++11 -Wl,--export-dynamic

# Set linker flags
linkers = -L$(python_path)/lib/python$(python_version)/config -lpython$(python_version) \
          -L$(boost_path)/lib -lboost_python$(boost_version)

# Set header flags
headers = -I$(basedir)/include -I$(basedir)/../depends \
          -I$(python_path)/include/python$(python_version) \
          -I$(boost_path)/include

%.so: %.o
	$(cc) $(flags) -o $@ $^ $(linkers)
	cp $@ $(basedir)/lib/$*.so

%.o: %.cpp
	$(cc) $(flags) $(headers) -c $<

clean:
	rm -rf *.o
	rm -rf *.so
