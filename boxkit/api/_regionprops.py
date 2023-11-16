""" Module with implemenation of measure methods"""
import numpy
import itertools
import skimage.measure as skimage_measure

from boxkit import api  # pylint: disable=cyclic-import
from boxkit.library import Action  # pylint: disable=cyclic-import


def regionprops(dataset, lsetkey, backend="serial", nthreads=1, monitor=False):
    """
    Parameters
    ----------
    dataset : Dataset object
    lsetkey : key containing level-set/binary data

    Returns
    -------
    listprops : list of bubble properties
    """

    labelkey = "bwlabel"
    dataset.addvar(labelkey, dtype=int)

    normals = ["normx", "normy"]
    for norm in normals:
        dataset.addvar(norm)

    region = api.create_region(dataset)

    skimage_props_blk.nthreads = nthreads
    skimage_props_blk.backend = backend
    skimage_props_blk.monitor = monitor

    listprops = skimage_props_blk(
        (block for block in region.blocklist), lsetkey, labelkey
    )
    listprops = list(itertools.chain.from_iterable(listprops))

    dataset.delvar(labelkey)
    for norm in normals:
        dataset.delvar(norm)

    return listprops


@Action
def skimage_props_blk(block, lsetkey, labelkey):
    """
    Measure properties for a block

    Parameters
    ----------
    block     : Block object
    lsetkey  : key to the level-set/binary data
    labelkey : key to store stratch data

    Returns
    -------
    listprops : list of properties
    """
    block[labelkey][:, :, :] = skimage_measure.label(block[lsetkey] >= 0)

    shape, deltas, corners = [list(), list(), list()]

    for idim, nblocks in enumerate([block.nzb, block.nyb, block.nxb]):
        if nblocks == 1:
            continue
        else:
            shape.append(nblocks)
            deltas.append([block.dz, block.dy, block.dx][idim])
            corners.append([block.zmin, block.ymin, block.xmin][idim])

    listprops = skimage_measure.regionprops(
        numpy.reshape(
            block[labelkey][
                block.zguard : block.nzb + block.zguard,
                block.yguard : block.nyb + block.yguard,
                block.xguard : block.nxb + block.xguard,
            ],
            shape,
        ).astype(int)
    )
    ndim = len(shape)

    modified_props = list()
    for props in listprops:

        modified_dict = dict()

        modified_dict["area"] = props["area"] * numpy.prod(deltas)
        modified_dict["centroid"] = [
            corners[idim] + deltas[idim] * props["centroid"][idim]
            for idim in range(ndim)
        ]

        if ndim == 2:
            modified_dict["perimeter"] = props["perimeter"] * deltas[0]

        modified_props.append(modified_dict)

    return modified_props
