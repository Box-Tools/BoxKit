"""Module to read attributes from FLASH output files"""

import h5pickle as h5py


def read_flash(filename):
    """
    Read dataset from FLASH output file

    Parameters
    ----------
    filename : string containing file name

    Returns
    -------
    data_attributes  : dictionary containing data attributes
    block_attributes : dictionary containg block attributes
    """

    # Read the hdf5 file
    inputfile = h5py.File(filename, "r", skip_cache=False)

    # Set variable dictionary for datasets
    variables = {}

    # Loop over unknowns and populate variable dict
    # with simulation datasets
    for unkvar in inputfile["unknown names"][:]:
        varkey = unkvar[0].decode()
        variables.update({varkey: inputfile[varkey]})

    # Extract shape
    var_shape = list(variables.values())[0].shape

    # Extract block info
    nblocks = var_shape[0]
    nzb = var_shape[1]
    nyb = var_shape[2]
    nxb = var_shape[3]

    # Create data attributes
    data_attributes = {
        "nblocks": int(nblocks),
        "nxb": int(nxb),
        "nyb": int(nyb),
        "nzb": int(nzb),
        "inputfile": inputfile,
        "variables": variables,
    }

    # Create block attributes
    block_attributes = [
        {
            "dx": inputfile["block size"][lblock][0] / nxb,
            "dy": (
                1.0
                if inputfile["block size"][lblock][1] == 0.0
                else inputfile["block size"][lblock][1] / nyb
            ),
            "dz": (
                1.0
                if inputfile["block size"][lblock][2] == 0.0
                else inputfile["block size"][lblock][2] / nzb
            ),
            "xmin": inputfile["bounding box"][lblock][0][0],
            "ymin": inputfile["bounding box"][lblock][1][0],
            "zmin": inputfile["bounding box"][lblock][2][0],
            "xmax": inputfile["bounding box"][lblock][0][1],
            "ymax": inputfile["bounding box"][lblock][1][1],
            "zmax": inputfile["bounding box"][lblock][2][1],
            "tag": lblock,
            "level": inputfile["refine level"][lblock],
            "leaf": (True if inputfile["node type"][lblock] == 1 else False),
        }
        for lblock in range(nblocks)
    ]

    return data_attributes, block_attributes
