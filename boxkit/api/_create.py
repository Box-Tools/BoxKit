"""Module with implemenetation of api methods"""

from types import SimpleNamespace

import pymorton

from .. import library


def create_dataset(storage=None, **attributes):
    """
    Create a dataset from a file

    Returns
    -------
    Dataset object

    """
    if not storage:
        storage = "numpy-memmap"

    self = SimpleNamespace(
        xmin=0.0,
        ymin=0.0,
        zmin=0.0,
        xmax=0,
        ymax=0.0,
        zmax=0.0,
        nxb=1,
        nyb=1,
        nzb=1,
        nblockx=1,
        nblocky=1,
        nblockz=1,
    )

    for key, value in attributes.items():
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise ValueError(f"[boxkit.create_dataset]: Invalid attributes {key}")

    # Create data_attributes
    data_attributes = {
        "nblocks": int(self.nblockx * self.nblocky * self.nblockz),
        "nxb": int(self.nxb),
        "nyb": int(self.nyb),
        "nzb": int(self.nzb),
    }

    data = library.Data(storage=storage, **data_attributes)

    self.dx, self.dy, self.dz = [
        (self.xmax - self.xmin) / (self.nblockx * self.nxb),
        (self.ymax - self.ymin) / (self.nblocky * self.nyb),
        (self.zmax - self.zmin) / (self.nblockz * self.nzb),
    ]

    if self.dx == 0:
        self.dx = 1

    if self.dy == 0:
        self.dy = 1

    if self.dz == 0:
        self.dz = 1

    blocklist = []

    for lblock in range(self.nblockx * self.nblocky * self.nblockz):
        block_attributes = {}

        block_attributes["dx"] = self.dx
        block_attributes["dy"] = self.dy
        block_attributes["dz"] = self.dz

        if self.nblockz == 1:
            block_attributes["xmin"] = (
                self.xmin + pymorton.deinterleave2(lblock)[0] * self.nxb * self.dx
            )
            block_attributes["ymin"] = (
                self.ymin + pymorton.deinterleave2(lblock)[1] * self.nyb * self.dy
            )
            block_attributes["zmin"] = self.zmin

        else:
            block_attributes["xmin"] = (
                self.xmin + pymorton.deinterleave3(lblock)[0] * self.nxb * self.dx
            )
            block_attributes["ymin"] = (
                self.ymin + pymorton.deinterleave3(lblock)[1] * self.nyb * self.dy
            )
            block_attributes["zmin"] = (
                self.zmin + pymorton.deinterleave3(lblock)[2] * self.nzb * self.dz
            )

        block_attributes["xmax"] = block_attributes["xmin"] + self.nxb * self.dx
        block_attributes["ymax"] = block_attributes["ymin"] + self.nyb * self.dy
        block_attributes["zmax"] = block_attributes["zmin"] + self.nzb * self.dz

        block_attributes["tag"] = lblock

        blocklist.append(library.Block(data, **block_attributes))

    return library.Dataset(blocklist, data)


def create_region(dataset, **attributes):
    """
    Create a region from a dataset

    Parameters
    ----------
    dataset    : Dataset object
    attributes : dictionary of attributes
                 { 'xmin' : low x bound
                   'ymin' : low y bound
                   'zmin' : low z bound
                   'xmax' : high x bound
                   'ymax' : high y bound
                   'zmax' : high z bound }
    Returns
    -------
    Region object
    """

    self = SimpleNamespace(
        xmin=dataset.xmin,
        ymin=dataset.ymin,
        zmin=dataset.zmin,
        xmax=dataset.xmax,
        ymax=dataset.ymax,
        zmax=dataset.zmax,
    )

    for key, value in attributes.items():
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise ValueError(f"[boxkit.create_region]: Invalid attributes {key}")

    blocklist = []

    for block in dataset.blocklist:
        if block.leaf:
            blocklist.append(block)

    return library.Region(blocklist, **vars(self))


def create_slice(dataset, **attributes):
    """
    Create a slice from a dataset

    Parameters
    ----------
    dataset    : Dataset object
    attributes : dictionary of attributes
                 { 'xmin' : low x bound
                   'ymin' : low y bound
                   'zmin' : low z bound
                   'xmax' : high x bound
                   'ymax' : high y bound
                   'zmax' : high z bound }

    Returns
    -------
    Slice object
    """

    self = SimpleNamespace(
        xmin=dataset.xmin,
        ymin=dataset.ymin,
        zmin=dataset.zmin,
        xmax=dataset.xmax,
        ymax=dataset.ymax,
        zmax=dataset.zmax,
    )

    for key, value in attributes.items():
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise ValueError(f"[boxkit.create_slice]: Invalid attributes {key}")

    blocklist = []

    for block in dataset.blocklist:
        if block.leaf:
            blocklist.append(block)

    return library.Slice(blocklist, **vars(self))
