"""Module to read attributes from FLASH output files"""

import h5py
import h5pickle

from boxkit.library import Action


def read_flash(filename, server):
    """
    Read dataset from FLASH output file

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
        # Read from remote path
        remotefile = server["sftp"].open(filename)
        remotefile.set_pipelined()
        inputfile = h5py.File(remotefile, "r", skip_cache=True)
        print("[boxkit.resource.read]: Avoid multiprocessing for remote files")

    else:
        # Read from local path
        remotefile = None
        inputfile = h5pickle.File(filename, "r", skip_cache=True)

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
        "remotefile": remotefile,
        "variables": variables,
    }

    # Create block attributes
    block_attributes = get_blk_attributes(
        (lblock for lblock in range(nblocks)), inputfile, nxb, nyb, nzb
    )

    return data_attributes, block_attributes


@Action(nthreads=8, backend="loky", monitor=True)
def get_blk_attributes(lblock, inputfile, nxb, nyb, nzb):
    """
    lblock: block number
    inputfile: HDF5 file handle

    Returns
    -------
    block_dict
    """
    block_dict = {
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
        "leaf": bool(inputfile["node type"][lblock] == 1),
        "inputproc": inputfile["processor number"][lblock],
    }

    return block_dict
