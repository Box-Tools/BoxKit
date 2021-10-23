# -------------------------------
# Bubblebox C++ Makefile include
# -------------------------------

#basedir = /home/akash/Desktop/Akash/Postdoc/bubblebox/cbox
basedir = /home/mount/bubblebox/cbox
cc      = g++
flags   = -shared -fPIC -fopenmp --std=c++11 -Wl,--export-dynamic
linkers = -L/usr/lib/python3.8/config -lpython3.8 -lboost_python38
headers = -I$(basedir)/include -I/usr/include/python3.8 -I/usr/include -I$(basedir)/../tools/indicators/include

%.so: %.o
	$(cc) $(flags) -o $@ $^ $(linkers)
	cp $@ $(basedir)/lib/$*.so

%.o: %.cpp
	$(cc) $(flags) $(headers) -c $<

clean:
	rm -rf *.o
	rm -rf *.so
