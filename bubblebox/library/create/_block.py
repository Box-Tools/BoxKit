"""Module with implementation of the Block class."""

import pymorton

class Block(object):
    """Default class for a Block."""

    type_ = 'default'

    def __init__(self, attributes={}, data=None):
        """Initialize the  object and allocate the data.

        Parameters
        ----------
        attributes : dictionary
                     { 'nxb'  : number of grid points per block in x dir
                       'nyb'  : number of grid points per block in y dir
                       'nzb'  : number of grid points per block in z dir
                       'xmin' : low  bound in x dir
                       'ymin' : low  bound in y dir
                       'zmin' : low  bound in z dir
                       'xmax' : high bound in x dir
                       'ymax' : high bound in y dir
                       'zmax' : high bound in z dir
                       'tag'  : block ID }

        data : data object

        """

        self._set_attributes(attributes)
        self._map_data(data)

    def __repr__(self):
        """Return a representation of the object."""
        return ("Block:\n" +
                " - type   : {}\n".format(type(self)) +
                " - size   : {} x {} x {}\n".format(self.nxb, self.nyb, self.nzb) +
                " - bound  : [{}, {}] x [{}, {}] x [{}, {}]\n".format(self.xmin,
                                                                         self.xmax,
                                                                         self.ymin,
                                                                         self.ymax,
                                                                         self.zmin,
                                                                         self.zmax) +
                " - tag    : {}\n".format(self.tag))

    def __getitem__(self,varkey):
        """
        Get variable data
        """
        return self.data[varkey][self.tag] #.to_numpy()[:]

    def __setitem__(self,varkey,value):
        """
        Set variable data
        """
        self.data[varkey][self.tag] = value #.to_numpy()[:] = value

    def _set_attributes(self,attributes):
        """
        Private method for intialization
        """        

        default_attributes = {'nxb'  : 1 , 'nyb'  : 1 , 'nzb'  : 1 ,
                              'xmin' : 0., 'ymin' : 0., 'zmin' : 0.,
                              'xmax' : 0., 'ymax' : 0., 'zmax' : 0.,
                              'tag'  : 0}

        for key in attributes:
            if key in default_attributes:
                default_attributes[key] = attributes[key]
            else:
                raise ValueError('Attribute "{}" not present in class Block'.format(key))

        for key, value in default_attributes.items(): setattr(self, key, value)

        self.xcenter = (self.xmin + self.xmax)/2.
        self.ycenter = (self.ymin + self.ymax)/2.
        self.zcenter = (self.zmin + self.zmax)/2.

        self.dx = 1 if self.nxb == 1 else abs(self.xmax - self.xmin) / self.nxb
        self.dy = 1 if self.nyb == 1 else abs(self.ymax - self.ymin) / self.nyb
        self.dz = 1 if self.nzb == 1 else abs(self.zmax - self.zmin) / self.nzb

    def _map_data(self,data):
        """
        Private method for initialization
        """
        self.data = None
        self.neighlist = []

        if not data: return

        self.data = data

        if 1 in [self.nxb,self.nyb,self.nzb]:
            self.neighlist = self._get_neighlist_2D()
        else:
            self.neighlist = self._get_neighlist_3D()


    def _get_neighlist_2D(self):
        """class property python
        Return neighbor tags

        order - imins,iplus,jmins,jplus
        """
          
        if self.data.nblocks > 1:
            iloc,jloc = pymorton.deinterleave2(self.tag)

            neighlist = [pymorton.interleave(iloc-1,jloc),
                         pymorton.interleave(iloc+1,jloc),
                         pymorton.interleave(iloc,jloc-1),
                         pymorton.interleave(iloc,jloc+1)]

            neighlist = [None if neighbor > self.data.nblocks-1 else neighbor for neighbor in neighlist]

        else:
            neighlist = [None]*4

        return neighlist

    def _get_neighlist_3D(self):
        """
        Return neighbor tags

        order - xmins,xplus,ymins,yplus,zmins,zplus        
        """

        if self.data.nblocks > 1:
            xloc,yloc,zloc = pymorton.deinterleave3(self.tag)

            neighlist = [pymorton.interleave(xloc-1,yloc,zloc),
                         pymorton.interleave(xloc+1,yloc,zloc),
                         pymorton.interleave(xloc,yloc-1,zloc),
                         pymorton.interleave(xloc,yloc+1,zloc),
                         pymorton.interleave(xloc,yloc,zloc-1),
                         pymorton.interleave(xloc,yloc,zloc+1)]
 
            neighlist = [None if neighbor > self.data.nblocks-1 else neighbor for neighbor in neighlist]

        else:
            neighlist = [None]*6

        return neighlist

    def neighdata(self,varkey,neighbor):
        """
        Get neighbor data
        """
        if neighbor is not None:
            return self.data[varkey][neighbor] #.to_numpy()[:]
        else:
            return None
