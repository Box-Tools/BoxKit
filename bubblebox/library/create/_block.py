"""Module with implementation of the Block class."""

import pymorton
import numpy
import cbox.lib.boost as cbox

class Block(object):
    """Default class for a Block."""

    type_ = 'default'

    def __init__(self, data=None, **attributes):
        """Initialize the  object and allocate the data.

        Parameters
        ----------
        data       : data object
        attributes : dictionary
                     { 'dx'   : grid spacing in x dir
                       'dy'   : grid spacing in y dir
                       'dz'   : grid spacing in z dir
                       'xmin' : low  bound in x dir
                       'ymin' : low  bound in y dir
                       'zmin' : low  bound in z dir
                       'xmax' : high bound in x dir
                       'ymax' : high bound in y dir
                       'zmax' : high bound in z dir
                       'tag'  : block ID }

        """
        super().__init__()

        self._set_attributes(attributes)
        self._map_data(data)

    def __repr__(self):
        """Return a representation of the object."""
        return ("Block:\n" +
                " - type         : {}\n".format(type(self)) +
                " - deltas       : {} x {} x {}\n".format(self.dx, self.dy, self.dz) +
                " - bound(z-y-x) : [{}, {}] x [{}, {}] x [{}, {}]\n".format(self.zmin,self.zmax,
                                                                            self.ymin,self.ymax,
                                                                            self.xmin,self.xmax) +
                " - tag          : {}\n".format(self.tag))

    def __getitem__(self,varkey):
        """
        Get variable data
        """
        return self._data[varkey][self.tag] #.to_numpy()[:]

    def __setitem__(self,varkey,value):
        """
        Set variable data
        """
        self._data[varkey][self.tag] = value #.to_numpy()[:] = value

    def _set_attributes(self,attributes):
        """
        Private method for intialization
        """        

        default_attributes = {'dx'   : 1 , 'dy'   : 1 , 'dz'   : 1 ,
                              'xmin' : 0., 'ymin' : 0., 'zmin' : 0.,
                              'xmax' : 0., 'ymax' : 0., 'zmax' : 0.,
                              'tag'  : 0}

        for key in attributes:
            if key in default_attributes:
                default_attributes[key] = attributes[key]
            else:
                raise ValueError('[bubblebox.library.create.Block] '+
                                 'Attribute "{}" not present in class Block'.format(key))

        for key, value in default_attributes.items(): setattr(self, key, value)

        self.xcenter = (self.xmin + self.xmax)/2.
        self.ycenter = (self.ymin + self.ymax)/2.
        self.zcenter = (self.zmin + self.zmax)/2.

    def _map_data(self,data):
        """
        Private method for initialization
        """
        self._data = None
        self.neighdict = []

        if not data: return

        self._data = data

        if 1 in [self.dx,self.dy,self.dz]:
            self.neighdict = self._get_neighdict_2D()
        else:
            self.neighdict = self._get_neighdict_3D()
 
        self.nxb, self.xguard = self._data.nxb, self._data.xguard
        self.nyb, self.yguard = self._data.nyb, self._data.yguard
        self.nzb, self.zguard = self._data.nzb, self._data.zguard

    def _get_neighdict_2D(self):
        """class property python
        Return neighbor tags

        order - imins,iplus,jmins,jplus
        """
        if self.dz == 1:
            locations = ['xlow','xhigh','ylow','yhigh']
        elif self.dy == 1:
            locations = ['xlow','xhigh','zlow','zhigh']          
        else:
            locations = ['ylow','yhigh','zlow','zhigh']

        if self._data.nblocks > 1:
            iloc,jloc = pymorton.deinterleave2(self.tag)

            neighlist = [pymorton.interleave(iloc-1,jloc),
                         pymorton.interleave(iloc+1,jloc),
                         pymorton.interleave(iloc,jloc-1),
                         pymorton.interleave(iloc,jloc+1)]

            neighlist = [None if neighbor > self._data.nblocks-1 else neighbor for neighbor in neighlist]

        else:
            neighlist = [None]*4

        return dict(zip(locations,neighlist))

    def _get_neighdict_3D(self):
        """
        Return neighbor tags

        order - xmins,xplus,ymins,yplus,zmins,zplus        
        """
        locations = ['xlow','xhigh','ylow','yhigh','zlow','zhigh']

        if self._data.nblocks > 1:
            xloc,yloc,zloc = pymorton.deinterleave3(self.tag)

            neighlist = [pymorton.interleave(xloc-1,yloc,zloc),
                         pymorton.interleave(xloc+1,yloc,zloc),
                         pymorton.interleave(xloc,yloc-1,zloc),
                         pymorton.interleave(xloc,yloc+1,zloc),
                         pymorton.interleave(xloc,yloc,zloc-1),
                         pymorton.interleave(xloc,yloc,zloc+1)]
 
            neighlist = [None if neighbor > self._data.nblocks-1 else neighbor for neighbor in neighlist]

        else:
            neighlist = [None]*6

        return dict(zip(locations,neighlist))

    def neighdata(self,varkey,neighkey):
        """
        Get neighbor data
        """
        if self.neighdict[neighkey] is not None:
            return self._data[varkey][self.neighdict[neighkey]] #.to_numpy()[:]
        else:
            return None

    def exchange_neighdata(self,varkey):
        """
        Exchange information
        """
        blockdata = self._data[varkey][self.tag]

        for guard in range(self.xguard):
            if self.neighdict['xlow']:
                blockdata[:,:,guard] = self.neighdata(varkey,'xlow')[:,:,self.nxb+guard]
            if self.neighdict['xhigh']:
                blockdata[:,:,self.nxb+self.xguard+guard] = self.neighdata(varkey,'xhigh')[:,:,self.xguard+guard]

        for guard in range(self.yguard):
            if self.neighdict['ylow']:
                blockdata[:,guard,:] = self.neighdata(varkey,'ylow')[:,self.nyb+guard,:]
            if self.neighdict['yhigh']:
                blockdata[:,self.nyb+self.yguard+guard,:] = self.neighdata(varkey,'yhigh')[:,self.yguard+guard,:]

        for guard in range(self.zguard):
            if self.neighdict['zlow']:
                blockdata[guard,:,:] = self.neighdata(varkey,'zlow')[self.nzb+guard,:,:]
            if self.neighdit['zhigh']:
                blockdata[self.nzb+self.zguard+guard,:,:] = self.neighdata(varkey,'zhigh')[self.zguard+guard,:,:]

