"""Module with implemenetation of api read methods"""

import h5py
import h5pickle

from ... import library


def Dataset(filename, source="test-sample", storage="numpy", server=None):
    """
    Create a dataset from a file

    Parameters
    ----------
    filename : string containing file name
    source   : string identifying source/format of the file
               'test-sample' : method to create sample dataset for BoxKit API tests
               'flash'  : method to create FLASH dataset
    storage  : storage option 'disk', 'pyarrow', or 'dask'
               default('disk')

    server : server dictionary

    (see tests/boiling.py and tests/heater.py for references)

    Returns
    -------
    Dataset object

    """
    read_options = {"test-sample": read_test_sample, "flash": read_flash}

    data_attributes, block_attributes = read_options[source](filename, server)

    data = library.Data(storage=storage, **data_attributes)
    blocklist = [library.Block(data, **attributes) for attributes in block_attributes]

    return library.Dataset(blocklist, data)


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
        inputfile = h5py.File(remotefile, "r", skip_cache=False)
        print(
            "[boxkit.resource.read]: Remote files cannot be pickled. Multithreading should not be used"
        )

    else:
        # Read from local path
        remotefile = None
        inputfile = h5pickle.File(filename, "r", skip_cache=False)

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
        "source": "flash",
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
            "inputproc": inputfile["processor number"][lblock],
        }
        for lblock in range(nblocks)
    ]

    return data_attributes, block_attributes


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

    # Read the hdf5 file
    inputfile = h5pickle.File(filename, "r", skip_cache=False)

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
    dx = inputfile["deltas"][0]
    dy = inputfile["deltas"][1]
    dz = inputfile["deltas"][2]

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
        "source": "test-sample",
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
