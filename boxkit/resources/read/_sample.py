"""Module to read attributes from default files"""

from types import SimpleNamespace

import h5pickle as h5py


def read_test_sample(filename, server):
    """
    Read dataset from BoxKit test sample

    Parameters
    ----------
    filename : string containing file name
    server : server dictionary

    Returns
    -------
    data_attributes  : dictionary containing data attributes
    block_attributes : dictionary containg block attributes
    """
    if server:
        raise NotImplementedError("[boxkit.read.test_sample] Cannot read from server")

    # Create a local namespace
    self = SimpleNamespace()

    # Read the hdf5 file
    self.inputfile = h5py.File(filename, "r", skip_cache=True)

    # Extract data
    self.nblocks = (
        self.inputfile["numbox"][0]
        * self.inputfile["numbox"][1]
        * self.inputfile["numbox"][2]
    )
    self.nxb = self.inputfile["sizebox"][0]
    self.nyb = self.inputfile["sizebox"][1]
    self.nzb = self.inputfile["sizebox"][2]
    self.xmin = self.inputfile["boundbox/min"][:, 0]
    self.ymin = self.inputfile["boundbox/min"][:, 1]
    self.zmin = self.inputfile["boundbox/min"][:, 2]
    self.xmax = self.inputfile["boundbox/max"][:, 0]
    self.ymax = self.inputfile["boundbox/max"][:, 1]
    self.zmax = self.inputfile["boundbox/max"][:, 2]
    self.dx = self.inputfile["deltas"][0]
    self.dy = self.inputfile["deltas"][1]
    self.dz = self.inputfile["deltas"][2]

    self.variables = {}
    self.variables.update(self.inputfile["quantities"])

    # Create data attributes
    data_attributes = {
        "nblocks": int(self.nblocks),
        "nxb": int(self.nxb),
        "nyb": int(self.nyb),
        "nzb": int(self.nzb),
        "inputfile": self.inputfile,
        "variables": self.variables,
    }

    # Create block attributes
    block_attributes = [
        {
            "dx": self.dx,
            "dy": self.dy,
            "dz": self.dz,
            "xmin": self.xmin[lblock],
            "ymin": self.ymin[lblock],
            "zmin": self.zmin[lblock],
            "xmax": self.xmax[lblock],
            "ymax": self.ymax[lblock],
            "zmax": self.zmax[lblock],
            "tag": lblock,
        }
        for lblock in range(self.nblocks)
    ]

    return data_attributes, block_attributes
