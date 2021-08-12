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
        int nblocks = 1;
        int nxb = 1;
        int nyb = 1;
        int nzb = 1;
    };
   /*
    *
    *
    */
}
#endif
