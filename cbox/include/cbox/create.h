#ifndef CBOX_CREATE_H
#define CBOX_CREATE_H

#include <cbox/pytypes.hpp>

namespace pytypes = cbox::pytypes;

namespace cbox::create
{
   /*
    */
    class Data
    {
    public:

        //constructors
	Data() {}

        //destructors
	virtual ~Data() {}

        //attributes
        unsigned int nxb=1, nyb=1, nzb=1, nblocks=1;
        unsigned int xguard=0, yguard=0, zguard=0;
    };
   /*
    */
    class Block
    {
    public:

        //constructors
	Block() {}
        Block(Data &data);

        //destructors
	virtual ~Block() {}

        //attributes
        unsigned int tag=0;
        unsigned int nxb=1,  nyb=1,  nzb=1;
        float xmin=0, ymin=0, zmin=0;
        float xmax=0, ymax=0, zmax=0;
        float dx=0, dy=0, dz=0;
        unsigned int xguard=0, yguard=0, zguard=0;

    private:
        Data data;

    };
   /*
    */
    class Region
    {
    public:

        //constructors
        Region() {}

        //destructors
	virtual ~Region() {}

        //attributes
        float xmin=0, ymin=0, zmin=0;
        float xmax=0, ymax=0, zmax=0;
    };
   /*
    */
}
#endif
