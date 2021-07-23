BASEDIR = $(PWD)

CC = g++

COMPFLAGS = -shared -fPIC -fopenmp

INCLUDE = -I/usr/include/python3.8 -I$(BASEDIR)

BOXOBJS += parallelbox.o boxlib.o

LIB = boxlib.so

$(LIB): $(BOXOBJS)
	$(CC) $(COMPFLAGS) -o $(LIB) $(BOXOBJS)

%.o : %.cxx
	$(CC) $(COMPFLAGS) $(INCLUDE) -c $<

clean:
	rm -f *.o
