"""Module to read attributes from default files"""

import h5pickle as h5py


def read(
    filename, server, nthreads, batch, monitor, backend
):  # pylint: disable=too-many-locals disable=too-many-arguments disable=unused-argument
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

    # Read the hdf5 file
    inputfile = h5py.File(filename, "r", skip_cache=True)

    # Extract data
    nblocks = inputfile["numbox"][0] * inputfile["numbox"][1] * inputfile["numbox"][2]
    nxb = inputfile["sizebox"][0]
    nyb = inputfile["sizebox"][1]
    nzb = inputfile["sizebox"][2]
    xmin = inputfile["boundbox/min"][:, 0]
    ymin = inputfile["boundbox/min"][:, 1]
    zmin = inputfile["boundbox/min"][:, 2]
    xmax = inputfile["boundbox/max"][:, 0]
    ymax = inputfile["boundbox/max"][:, 1]
    zmax = inputfile["boundbox/max"][:, 2]
    dx = inputfile["deltas"][0]  # pylint: disable=invalid-name
    dy = inputfile["deltas"][1]  # pylint: disable=invalid-name
    dz = inputfile["deltas"][2]  # pylint: disable=invalid-name

    variables = {}
    variables.update(inputfile["quantities"])

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
            "dx": dx,
            "dy": dy,
            "dz": dz,
            "xmin": xmin[lblock],
            "ymin": ymin[lblock],
            "zmin": zmin[lblock],
            "xmax": xmax[lblock],
            "ymax": ymax[lblock],
            "zmax": zmax[lblock],
            "tag": lblock,
        }
        for lblock in range(nblocks)
    ]

    return data_attributes, block_attributes
