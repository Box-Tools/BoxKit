#ifndef CBOX_CREATE_H
#define CBOX_CREATE_H

namespace cbox::create
{
   /*
    *
    *
    */
    class Data
    {
    public:

        //constructors
	Data() {}

        //destructors
	virtual ~Data() {}

        //attributes
        int nxb=1, nyb=1, nzb=1, nblocks=1;
    };
   /*
    *
    *
    */
    class Block
    {
    public:

        //constructors
	Block() {}

        //destructors
	virtual ~Block() {}

        //attributes
        int   tag=0;
        int   nxb=1,  nyb=1,  nzb=1;
        float xmin=0, ymin=0, zmin=0;
        float xmax=0, ymax=0, zmax=0;
    };
   /*
    *
    *
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
    *
    *
    */
}
#endif
