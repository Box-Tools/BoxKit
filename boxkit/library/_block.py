"""Module with implementation of the Block class."""

import math
import numpy
import pymorton


class Block:
    """Default class for a Block.

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

    Auxillary attributes
    --------------------
    { 'nxb' : number of points in x dir
      'nyb' : number of points in y dir
      'nzb' : number of points in z dir
      'xguard' : number of guard cells in x dir
      'yguard' : number of guard cells in y dir
      'zguard' : number of guard cells in z dir
      'xcenter' : block xcenter
      'ycenter' : block ycenter
      'zcenter' : block zcenter }
    """

    type_ = "default"

    def __init__(self, data=None, **attributes):
        """Initialize the  object and allocate the data."""
        super().__init__()

        self._set_attributes(attributes)
        self._map_data(data)

    def __repr__(self):
        """Return a representation of the object."""
        return (
            "Block:\n"
            + f" - type         : {type(self)}\n"
            + f" - deltas       : {self.dx} x {self.dy} x {self.dz}\n"
            + f" - bound(z-y-x) : [{self.zmin}, {self.zmax}] x"
            + f"[{self.ymin}, {self.ymax}] x"
            + f"[{self.xmin}, {self.xmax}]\n"
            + f" - tag          : {self.tag}\n"
            + f" - level        : {self.level}\n"
            + f" - leaf         : {self.leaf}\n"
        )

    def __getitem__(self, varkey):
        """
        Get variable data
        """
        return self._data[varkey][self.tag]  # .to_numpy()[:]

    def __setitem__(self, varkey, value):
        """
        Set variable data
        """
        self._data[varkey][self.tag] = value  # .to_numpy()[:] = value

    def xrange(self, location):
        """
        Get xrange of the block
        """
        range_dict = {
            "center": self.__class__._get_center_loc,
            "node": self.__class__._get_node_loc,
        }

        return range_dict[location](
            self.xmin, self.xmax, self.dx, self.xguard, self.nxb
        )

    def yrange(self, location):
        """
        Get yrange of the block
        """
        range_dict = {
            "center": self.__class__._get_center_loc,
            "node": self.__class__._get_node_loc,
        }

        return range_dict[location](
            self.ymin, self.ymax, self.dy, self.yguard, self.nyb
        )

    def zrange(self, location):
        """
        Get zrange of the block
        """
        range_dict = {
            "center": self.__class__._get_center_loc,
            "node": self.__class__._get_node_loc,
        }

        return range_dict[location](
            self.zmin, self.zmax, self.dz, self.zguard, self.nzb
        )

    @staticmethod
    def _get_center_loc(min_val, max_val, delta, guard, num_points):
        """Private method for center location"""
        return numpy.linspace(min_val + delta / 2, max_val - delta / 2, num_points)

    @staticmethod
    def _get_node_loc(min_val, max_val, delta, guard, num_points):
        """Private method for face location"""
        return numpy.linspace(min_val, max_val, num_points + 1)

    def _set_attributes(self, attributes):
        """
        Private method for intialization
        """
        self.dx, self.dy, self.dz = [1.0, 1.0, 1.0]
        self.xmin, self.ymin, self.zmin = [0.0, 0.0, 0.0]
        self.xmax, self.ymax, self.zmax = [0.0, 0.0, 0.0]
        self.tag = 0
        self.level = 1
        self.inputproc = None
        self.leaf = True

        for key, value in attributes.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(
                    "[boxkit.library.create.Block] "
                    + f"Attribute {key} not present in class Block"
                )

        self.xcenter = (self.xmin + self.xmax) / 2.0
        self.ycenter = (self.ymin + self.ymax) / 2.0
        self.zcenter = (self.zmin + self.zmax) / 2.0

    def _map_data(self, data):
        """
        Private method for initialization
        """
        self._data = None

        self.neighdict = {
            "xlow": None,
            "xhigh": None,
            "ylow": None,
            "yhigh": None,
            "zlow": None,
            "zhigh": None,
        }

        if not data:
            return

        self._data = data

        if 1 in [self.dx, self.dy, self.dz]:
            self._set_neighdict_2d()
        else:
            self._set_neighdict_3d()

        self.nxb, self.xguard = self._data.nxb, self._data.xguard
        self.nyb, self.yguard = self._data.nyb, self._data.yguard
        self.nzb, self.zguard = self._data.nzb, self._data.zguard

    def _set_neighdict_2d(self):
        """class property python
        Return neighbor tags

        order - imins,iplus,jmins,jplus
        """
        if self.dz == 1:
            locations = ["xlow", "xhigh", "ylow", "yhigh"]
        elif self.dy == 1:
            locations = ["xlow", "xhigh", "zlow", "zhigh"]
        else:
            locations = ["ylow", "yhigh", "zlow", "zhigh"]

        if self._data.nblocks > 1:
            iloc, jloc = pymorton.deinterleave2(self.tag)

            neighlist = [
                pymorton.interleave(iloc - 1, jloc),
                pymorton.interleave(iloc + 1, jloc),
                pymorton.interleave(iloc, jloc - 1),
                pymorton.interleave(iloc, jloc + 1),
            ]

            neighlist = [
                None if neighbor > self._data.nblocks - 1 else neighbor
                for neighbor in neighlist
            ]

        else:
            neighlist = [None] * 4

        self.neighdict.update(dict(zip(locations, neighlist)))

    def _set_neighdict_3d(self):
        """
        Return neighbor tags

        order - xmins,xplus,ymins,yplus,zmins,zplus
        """
        locations = ["xlow", "xhigh", "ylow", "yhigh", "zlow", "zhigh"]

        if self._data.nblocks > 1:
            xloc, yloc, zloc = pymorton.deinterleave3(self.tag)

            neighlist = [
                pymorton.interleave(xloc - 1, yloc, zloc),
                pymorton.interleave(xloc + 1, yloc, zloc),
                pymorton.interleave(xloc, yloc - 1, zloc),
                pymorton.interleave(xloc, yloc + 1, zloc),
                pymorton.interleave(xloc, yloc, zloc - 1),
                pymorton.interleave(xloc, yloc, zloc + 1),
            ]

            neighlist = [
                None if neighbor > self._data.nblocks - 1 else neighbor
                for neighbor in neighlist
            ]

        else:
            neighlist = [None] * 6

        self.neighdict.update(dict(zip(locations, neighlist)))

    def write_neighbuffer(self, varkey):
        """
        Write block data to buffer for halo exchange
        """

    def read_neighbuffer(self, varkey):
        """
        Read neighbor buffer and perform halo exchange
        """

    def neighdata(self, varkey, neighkey):
        """
        Get neighbor data
        """
        neighdata = None

        if self.neighdict[neighkey] is not None:
            neighdata = self._data[varkey][self.neighdict[neighkey]]  # .to_numpy()[:]

        return neighdata

    def get_location(self, origin=[None]*3):
        """
        Get offset from origin
        """
        iloc, jloc, kloc = [
            math.ceil((self.xmin - origin[0]) / (self.xmax - self.xmin + 1e-13)),
            math.ceil((self.ymin - origin[1]) / (self.ymax - self.ymin + 1e-13)),
            math.ceil((self.zmin - origin[2]) / (self.zmax - self.zmin + 1e-13)),
        ]

        return iloc, jloc, kloc

    def exchange_neighdata(self, varkey):
        """
        Exchange information
        """
        blockdata = self._data[varkey][self.tag]

        for guard in range(self.xguard):
            if self.neighdict["xlow"]:
                blockdata[:, :, guard] = self.neighdata(varkey, "xlow")[
                    :, :, self.nxb + guard
                ]
            if self.neighdict["xhigh"]:
                blockdata[:, :, self.nxb + self.xguard + guard] = self.neighdata(
                    varkey, "xhigh"
                )[:, :, self.xguard + guard]

        for guard in range(self.yguard):
            if self.neighdict["ylow"]:
                blockdata[:, guard, :] = self.neighdata(varkey, "ylow")[
                    :, self.nyb + guard, :
                ]
            if self.neighdict["yhigh"]:
                blockdata[:, self.nyb + self.yguard + guard, :] = self.neighdata(
                    varkey, "yhigh"
                )[:, self.yguard + guard, :]

        for guard in range(self.zguard):
            if self.neighdict["zlow"]:
                blockdata[guard, :, :] = self.neighdata(varkey, "zlow")[
                    self.nzb + guard, :, :
                ]
            if self.neighdict["zhigh"]:
                blockdata[self.nzb + self.zguard + guard, :, :] = self.neighdata(
                    varkey, "zhigh"
                )[self.zguard + guard, :, :]
