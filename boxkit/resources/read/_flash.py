"""Module to read attributes from FLASH output files"""

import h5py
import h5pickle

from boxkit.library import Action


def read_flash(
    filename, server, nthreads, batch, monitor, backend
):  # pylint: disable=too-many-locals disable=too-many-arguments
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

    get_blk_attributes.nthreads = nthreads
    get_blk_attributes.backend = backend
    get_blk_attributes.batch = batch
    get_blk_attributes.monitor = monitor

    # Create block attributes
    block_attributes = get_blk_attributes(
        (lblock for lblock in range(nblocks)),
        inputfile["block size"][:],
        inputfile["bounding box"][:],
        inputfile["refine level"][:],
        inputfile["node type"][:],
        inputfile["processor number"][:],
        nxb,
        nyb,
        nzb,
    )

    return data_attributes, block_attributes


@Action
def get_blk_attributes(
    lblock, block_size, bounding_box, refine_level, node_type, proc_num, nxb, nyb, nzb
):  # pylint: disable=too-many-arguments
    """
    lblock: block number
    inputfile: HDF5 file handle

    Returns
    -------
    block_dict
    """
    block_dict = {
        "dx": block_size[lblock][0] / nxb,
        "dy": (1.0 if block_size[lblock][1] == 0.0 else block_size[lblock][1] / nyb),
        "dz": (1.0 if block_size[lblock][2] == 0.0 else block_size[lblock][2] / nzb),
        "xmin": bounding_box[lblock][0][0],
        "ymin": bounding_box[lblock][1][0],
        "zmin": bounding_box[lblock][2][0],
        "xmax": bounding_box[lblock][0][1],
        "ymax": bounding_box[lblock][1][1],
        "zmax": bounding_box[lblock][2][1],
        "tag": lblock,
        "level": refine_level[lblock],
        "leaf": bool(node_type[lblock] == 1),
        "inputproc": proc_num[lblock],
    }

    return block_dict
