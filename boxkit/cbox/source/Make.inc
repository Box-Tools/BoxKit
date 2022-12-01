# -------------------------------
# Boxkit C++ Makefile include
# -------------------------------

# Set base directory
basedir = $(shell pwd)/../..

# Set common flags
flags = -shared -fPIC --std=c++11 #-fopenmp -Wl,--export-dynamic

# Set linker flags
linkers = -L$(python_lib_path) -lpython$(python_version) \
          -L$(boost_lib_path) -lboost_python$(boost_version)

# Set header flags
headers = -I$(basedir)/include -I$(basedir)/../depends \
          -I$(python_include_path) \
          -I$(boost_include_path)

%.so: %.o
	$(cc) $(flags) -o $@ $^ $(linkers)
	cp $@ $(basedir)/lib/$*.so

%.o: %.cpp
	$(cc) $(flags) $(headers) -c $<

clean:
	rm -rf *.o
	rm -rf *.so
