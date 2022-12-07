"""Module with implementation of the Slice class."""

from . import Region


class Slice(Region):
    """Derived class for a Slice."""

    type_ = "derived"

    def __init__(self, blocklist=[], **attributes):
        """Initialize the Slice object and allocate the data.

        Parameters
        ----------
        blocklist  : list of blocks
        attributes : dictionary
                     { 'xmin' : low  bound in x dir
                       'ymin' : low  bound in y dir
                       'zmin' : low  bound in z dir
                       'xmax' : high bound in x dir
                       'ymax' : high bound in y dir
                       'zmax' : high bound in z dir}
        """

        super().__init__(blocklist, **attributes)

    def __repr__(self):
        """Return a representation of the object."""
        return (
            "Region:\n"
            + f" - type          : {type(self)}\n"
            + f" - bound (z-y-x) : [{self.zmin}, {self.zmax}] x "
            + f"[{self.ymin}, {self.ymax}] x "
            + f"[{self.xmin}, {self.xmax}]\n"
        )
