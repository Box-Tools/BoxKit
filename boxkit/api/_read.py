"""Module with implemenetation of api read methods"""

from .. import library
from .. import resources
from ..library import Action


def read_dataset(
    filename,
    source=None,
    storage=None,
    server=None,
    force_memmap=False,
    nthreads=1,
    backend="serial",
    monitor=False,
    batch="auto",
):  # pylint: disable=too-many-arguments disable=too-many-locals
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

    force_memamp : flag

    nthreads : integer

    backend : string parameter for parallel backend

    monitor : flag

    (see tests/boiling.py and tests/heater.py for references)

    Returns
    -------
    Dataset object

    """
    if not source:
        source = "sample"

    if not storage:
        storage = "numpy-memmap"

    source = getattr(resources, source)

    data_attributes, block_attributes = source.read(
        filename, server, nthreads, batch, monitor, backend
    )

    data = library.Data(storage=storage, **data_attributes)
    blocklist = [library.Block(data, **attributes) for attributes in block_attributes]

    dataset = library.Dataset(blocklist, data)

    if force_memmap:

        memmap_dataset = dataset.clone(storage="numpy-memmap")
        for varkey in dataset.varlist:
            memmap_dataset.addvar(varkey)

        blk_map_list = [
            [block_memmap, block_read]
            for block_memmap, block_read in zip(
                memmap_dataset.blocklist, dataset.blocklist
            )
        ]

        copy_blk_to_memmap.nthreads = nthreads
        copy_blk_to_memmap.backend = backend

        timer_force_memmap = library.Timer("[boxkit.read.force_memmap]")
        for varkey in memmap_dataset.varlist:
            copy_blk_to_memmap((blk_list for blk_list in blk_map_list), varkey)
        del timer_force_memmap

        dataset.purge()
        return memmap_dataset

    return dataset


@Action
def copy_blk_to_memmap(blk_list, varkey):
    """copy_blk_to_memmap"""
    blk_list[0][varkey] = blk_list[1][varkey]
