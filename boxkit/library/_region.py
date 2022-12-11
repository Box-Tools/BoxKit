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
        set_attributes(self, attributes)
        map_blocklist(self, blocklist)

    def __repr__(self):
        """Return a representation of the object."""
        return (
            "Region:\n"
            + f" - type         : {type(self)}\n"
            + f" - bound(z-y-x) : [{self.zmin}, {self.zmax}] x "
            + f"[{self.ymin}, {self.ymax}] x "
            + f"[{self.xmin}, {self.xmax}]\n"
        )


def set_attributes(region, attributes):
    """`
    Private method for intialization
    """

    region.xmin, region.ymin, region.zmin = [-1e10, -1e10, -1e10]
    region.xmax, region.ymax, region.zmax = [1e10, 1e10, 1e10]

    for key, value in attributes.items():
        if hasattr(region, key):
            setattr(region, key, value)
        else:
            raise ValueError(
                "[boxkit.library.create.Region] "
                + f'Attribute "{key}" not present in class Region'
            )

    region.xcenter = (region.xmin + region.xmax) / 2.0
    region.ycenter = (region.ymin + region.ymax) / 2.0
    region.zcenter = (region.zmin + region.zmax) / 2.0


def map_blocklist(region, blocklist):
    """
    Private method for initialization
    """
    region.blocklist = []

    if not blocklist:
        return

    region.blocklist = [block for block in blocklist if in_collision(region, block)]

    update_bounds(region)


def in_collision(region, block):
    """
    Check if a block is in collision with the region
    """
    xcollision = (
        abs(region.xcenter - block.xcenter)
        - (region.xmax - region.xmin) / 2.0
        - (block.xmax - block.xmin) / 2.0
        <= 0.0
    )
    ycollision = (
        abs(region.ycenter - block.ycenter)
        - (region.ymax - region.ymin) / 2.0
        - (block.ymax - block.ymin) / 2.0
        <= 0.0
    )
    zcollision = (
        abs(region.zcenter - block.zcenter)
        - (region.zmax - region.zmin) / 2.0
        - (block.zmax - block.zmin) / 2.0
        <= 0.0
    )

    incollision = xcollision and ycollision and zcollision

    return incollision


def update_bounds(region):
    """
    Update block bounds using the blocklist
    """
    if not region.blocklist:
        raise ValueError(
            "[boxkit.library.create.Region] " + "is empty and outside scope of Blocks\n"
        )

    region.xmin, region.ymin, region.zmin = [
        region.blocklist[0].xmin,
        region.blocklist[0].ymin,
        region.blocklist[0].zmin,
    ]
    region.xmax, region.ymax, region.zmax = [
        region.blocklist[0].xmax,
        region.blocklist[0].ymax,
        region.blocklist[0].zmax,
    ]

    for block in region.blocklist:
        region.xmin = min(region.xmin, block.xmin)
        region.ymin = min(region.ymin, block.ymin)
        region.zmin = min(region.zmin, block.zmin)

        region.xmax = max(region.xmax, block.xmax)
        region.ymax = max(region.ymax, block.ymax)
        region.zmax = max(region.zmax, block.zmax)

    region.xcenter = (region.xmin + region.xmax) / 2.0
    region.ycenter = (region.ymin + region.ymax) / 2.0
    region.zcenter = (region.zmin + region.zmax) / 2.0
