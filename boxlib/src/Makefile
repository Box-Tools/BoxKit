BASEDIR = $(PWD)

CC = g++

COMPFLAGS = -shared -fPIC -fopenmp

INCLUDE = -I/usr/include/python3.8 -I$(BASEDIR)/../include

BOXOBJS = utilities.o bubblebox.o

BOXLIB = libbubblebox.a

$(BOXLIB): $(BOXOBJS)
	$(CC) $(COMPFLAGS) -o $(BOXLIB) $(BOXOBJS)

%.o : %.cxx
	$(CC) $(COMPFLAGS) $(INCLUDE) -c $<

clean:
	rm -f *.o
	rm -f *.a
