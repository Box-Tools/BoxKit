"""Module with implemenetation of api methods"""

import pymorton

from .. import library


def create_dataset(
    xmin=0.0,
    xmax=0.0,
    ymin=0.0,
    ymax=0.0,
    zmin=0.0,
    zmax=0.0,
    nxb=1,
    nyb=1,
    nzb=1,
    nblockx=1,
    nblocky=1,
    nblockz=1,
    storage="numpy-memmap",
):
    """
    Create a dataset from a file

    Returns
    -------
    Dataset object

    """
    # Create data_attributes
    data_attributes = {
        "nblocks": int(nblockx * nblocky * nblockz),
        "nxb": int(nxb),
        "nyb": int(nyb),
        "nzb": int(nzb),
    }

    data = library.Data(storage=storage, **data_attributes)

    delta_x, delta_y, delta_z = [
        (xmax - xmin) / (nblockx * nxb),
        (ymax - ymin) / (nblocky * nyb),
        (zmax - zmin) / (nblockz * nzb),
    ]

    blocklist = []

    for lblock in range(nblockx * nblocky * nblockz):
        block_attributes = {}

        block_attributes["dx"] = delta_x
        block_attributes["dy"] = delta_y
        block_attributes["dz"] = delta_z

        if nblockz == 1:
            block_attributes["xmin"] = (
                xmin + pymorton.deinterleave2(lblock)[0] * nxb * delta_x
            )
            block_attributes["ymin"] = (
                ymin + pymorton.deinterleave2(lblock)[1] * nyb * delta_y
            )
            block_attributes["zmin"] = zmin

        else:
            block_attributes["xmin"] = (
                xmin + pymorton.deinterleave3(lblock)[0] * nxb * delta_x
            )
            block_attributes["ymin"] = (
                ymin + pymorton.deinterleave3(lblock)[1] * nyb * delta_y
            )
            block_attributes["zmin"] = (
                zmin + pymorton.deinterleave3(lblock)[2] * nzb * delta_z
            )

        block_attributes["xmax"] = block_attributes["xmin"] + nxb * delta_x
        block_attributes["ymax"] = block_attributes["ymin"] + nyb * delta_y
        block_attributes["zmax"] = block_attributes["zmin"] + nzb * delta_z

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

    region_attributes = {
        "xmin": dataset.xmin,
        "ymin": dataset.ymin,
        "zmin": dataset.zmin,
        "xmax": dataset.xmax,
        "ymax": dataset.ymax,
        "zmax": dataset.zmax,
    }

    for key, value in attributes.items():
        region_attributes[key] = value

    blocklist = []

    for block in dataset.blocklist:
        if block.leaf:
            blocklist.append(block)

    return library.Region(blocklist, **region_attributes)


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

    slice_attributes = {
        "xmin": dataset.xmin,
        "ymin": dataset.ymin,
        "zmin": dataset.zmin,
        "xmax": dataset.xmax,
        "ymax": dataset.ymax,
        "zmax": dataset.zmax,
    }

    for key, value in attributes.items():
        slice_attributes[key] = value

    blocklist = []

    for block in dataset.blocklist:
        if block.leaf:
            blocklist.append(block)

    return library.Slice(blocklist, **slice_attributes)
