BASEDIR = $(PWD)

CC = g++

COMPFLAGS = -shared -fPIC -fopenmp

INCLUDE = -I/usr/include/python3.8 -I$(BASEDIR)/../include

BOXOBJS = utilities.o bubblebox.o

BOXLIB = libbubblebox.a

BUILDDIR = $(BASEDIR)/../build

$(BOXLIB): $(BOXOBJS)
	$(CC) $(COMPFLAGS) -o $(BOXLIB) $(BOXOBJS)
	mkdir -p $(BUILDDIR)
	cp $(BOXLIB) $(BUILDDIR)

%.o : %.cxx
	$(CC) $(COMPFLAGS) $(INCLUDE) -c $<

clean:
	rm -f *.o
	rm -f *.a
