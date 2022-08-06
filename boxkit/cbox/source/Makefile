# ----------------------
# Boxkit C++ Makefile
# ----------------------

modules = create utilities

.PHONY: all clean $(modules)

all: command=all
all: $(modules)

clean: command=clean
clean: $(modules)

$(modules):
	$(MAKE) --directory=$@ $(command)

