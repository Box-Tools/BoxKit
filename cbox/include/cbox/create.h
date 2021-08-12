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
	Data() : nblocks(1), nxb(1), nyb(1), nzb(1) {}

        //destructors
	virtual ~Data() {}

        //attributes
        int nxb,nyb,nzb,nblocks;
    };
   /*
    *
    *
    */
    class Block
    {
    public:

        //constructors
	Block() : nxb(1), nyb(1), nzb(1), 
                  xmin(0.0), ymin(0.0), zmin(0.0),
                  xmax(0.0), ymax(0.0), zmax(0.0),
                  tag(0) {}

        //destructors
	virtual ~Block() {}

        //attributes
        int tag,nxb,nyb,nzb;
        float xmin,ymin,zmin,xmax,ymax,zmax;
    };
   /*
    *
    *
    */
}
#endif
