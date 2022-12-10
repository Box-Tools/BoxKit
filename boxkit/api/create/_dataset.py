"""Module with implemenetation of api create methods"""

import pymorton

from ... import library


def Dataset(
    xmin=0.,
    xmax=0.,
    ymin=0.,
    ymax=0.,
    zmin=0.,
    zmax=0.,
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

    dx, dy, dz = [
        (xmax - xmin) / (nblockx * nxb),
        (ymax - ymin) / (nblocky * nyb),
        (zmax - zmin) / (nblockz * nzb),
    ]

    blocklist = []

    for lblock in range(nblockx * nblocky * nblockz):
        block_attributes = {}

        block_attributes["dx"] = dx
        block_attributes["dy"] = dy
        block_attributes["dz"] = dz

        if nblockz == 1:
            block_attributes["xmin"] = (
                xmin + pymorton.deinterleave2(lblock)[0] * nxb * dx
            )
            block_attributes["ymin"] = (
                ymin + pymorton.deinterleave2(lblock)[1] * nyb * dy
            )
            block_attributes["zmin"] = zmin

        else:
            block_attributes["xmin"] = (
                xmin + pymorton.deinterleave3(lblock)[0] * nxb * dx
            )
            block_attributes["ymin"] = (
                ymin + pymorton.deinterleave3(lblock)[1] * nyb * dy
            )
            block_attributes["zmin"] = (
                zmin + pymorton.deinterleave3(lblock)[2] * nzb * dz
            )

        block_attributes["xmax"] = block_attributes["xmin"] + nxb * dx
        block_attributes["ymax"] = block_attributes["ymin"] + nyb * dy
        block_attributes["zmax"] = block_attributes["zmin"] + nzb * dz

        block_attributes["tag"] = lblock

        blocklist.append(library.Block(data, **block_attributes))

    return library.Dataset(blocklist, data)
