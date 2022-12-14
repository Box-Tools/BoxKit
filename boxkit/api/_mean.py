""" Module with implemenation of measure methods"""

from .. import library
from .. import api


def mean_temporal(datasets, varlist, backend="serial", nthreads=1, monitor=False):
    """
    Compute average across a dataset list
    """
    # Set timer for monitoring
    if monitor:
        time_mean_temporal = library.Timer("[boxkit.mean_temporal]")

    # Check if varlist is actually a string
    # of one variable and convert to a list
    if isinstance(varlist, str):
        varlist = [varlist]

    # TODO: Add more error handling here to account
    # for consistency between multiple datasets
    #
    # Handle errors, compute level of the first
    # block and raise error if not same for the rest
    level = datasets[0].blocklist[0].level
    for dataset in datasets:
        for block in dataset.blocklist:
            if block.level != level:
                raise ValueError(
                    f"[boxkit.mean_temporal] All blocks must be at level 1"
                )

    # Create an mean dataset
    mean_dataset = datasets[0].clone(storage="numpy-memmap")

    # Create a block list for reduction, first add
    # blocks from average_dataset and then loop over
    # datasets to add blocks from their respective blocklist
    blk_reduce_list = [[block] for block in mean_dataset.blocklist]

    for dataset in datasets:
        for block, reduce_list in zip(dataset.blocklist, blk_reduce_list):
            reduce_list.append(block)

    # loop over varlist append values to
    # add it to the mean dataset and perform mean
    for varkey in varlist:
        mean_dataset.addvar(varkey)

    mean_blk_list.nthreads = nthreads
    mean_blk_list.backend = backend

    for varkey in varlist:
        if monitor:
            time_reduction = library.Timer("[boxkit.mean_temporal.mean_blk_list]")

        mean_blk_list(blk_reduce_list, varkey)

        if monitor:
            del time_reduction

    if monitor:
        del time_mean_temporal

    return mean_dataset


@library.Action(parallel_obj=list)
def mean_blk_list(parallel_obj, varkey):
    """
    Reduce dataset / compute average
    """
    mean_blk = parallel_obj[0]
    sample_size = len(parallel_obj[1:])

    for work_blk in parallel_obj[1:]:
        mean_blk[varkey] = mean_blk[varkey] + work_blk[varkey] / sample_size
