"""Module with implementation of the Region class."""


class Region:
    """Base class for a Region."""

    type_ = "base"

    def __init__(self, blocklist=[], **attributes):
        """Initialize the Region object and allocate the data.

        Parameters
        ----------
        blocklist  : list of objects
        attributes : dictionary
                     { 'xmin' : low  bound in x dir
                       'ymin' : low  bound in y dir
                       'zmin' : low  bound in z dir
                       'xmax' : high bound in x dir
                       'ymax' : high bound in y dir
                       'zmax' : high bound in z dir}

        """
        super().__init__()
        self._set_attributes(attributes)
        self._map_blocklist(blocklist)

    def __repr__(self):
        """Return a representation of the object."""
        return (
            "Region:\n"
            + f" - type         : {type(self)}\n"
            + f" - bound(z-y-x) : [{self.zmin}, {self.zmax}] x "
            + f"[{self.ymin}, {self.ymax}] x "
            + f"[{self.xmin}, {self.xmax}]\n"
        )

    def _set_attributes(self, attributes):
        """`
        Private method for intialization
        """

        self.xmin, self.ymin, self.zmin = [0.0, 0.0, 0.0]
        self.xmax, self.ymax, self.zmax = [0.0, 0.0, 0.0]

        for key, value in attributes.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(
                    "[bubblebox.library.create.Region] "
                    + f'Attribute "{key}" not present in class Region'
                )

        self.xcenter = (self.xmin + self.xmax) / 2.0
        self.ycenter = (self.ymin + self.ymax) / 2.0
        self.zcenter = (self.zmin + self.zmax) / 2.0

    def _map_blocklist(self, blocklist):
        """
        Private method for initialization
        """
        self.blocklist = []

        if not blocklist:
            return

        self.blocklist = [block for block in blocklist if self._in_collision(block)]

        self._update_bounds()

    def _in_collision(self, block):
        """
        Check if a block is in collision with the region
        """
        xcollision = (
            abs(self.xcenter - block.xcenter)
            - (self.xmax - self.xmin) / 2.0
            - (block.xmax - block.xmin) / 2.0
            <= 0.0
        )
        ycollision = (
            abs(self.ycenter - block.ycenter)
            - (self.ymax - self.ymin) / 2.0
            - (block.ymax - block.ymin) / 2.0
            <= 0.0
        )
        zcollision = (
            abs(self.zcenter - block.zcenter)
            - (self.zmax - self.zmin) / 2.0
            - (block.zmax - block.zmin) / 2.0
            <= 0.0
        )

        incollision = xcollision and ycollision and zcollision

        return incollision

    def _update_bounds(self):
        """
        Update block bounds using the blocklist
        """
        if not self.blocklist:
            raise ValueError(
                "[bubblebox.library.create.Region] "
                + "is empty and outside scope of Blocks\n"
            )

        for block in self.blocklist:
            self.xmin = min(self.xmin, block.xmin)
            self.ymin = min(self.ymin, block.ymin)
            self.zmin = min(self.zmin, block.zmin)

            self.xmax = max(self.xmax, block.xmax)
            self.ymax = max(self.ymax, block.ymax)
            self.zmax = max(self.zmax, block.zmax)

        self.xcenter = (self.xmin + self.xmax) / 2.0
        self.ycenter = (self.ymin + self.ymax) / 2.0
        self.zcenter = (self.zmin + self.zmax) / 2.0
