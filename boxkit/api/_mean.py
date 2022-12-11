""" Module with implemenation of measure methods"""

from .. import library
from .. import api


def mean_temporal(
    datasets, varlist, level=1, backend="serial", nthreads=1, monitor=False
):
    """
    Compute average across a dataset list
    """
    if monitor:
        time_mean_temporal = library.Timer("[boxkit.mean_temporal]")

    if isinstance(varlist, str):
        varlist = [varlist]

    merged_datasets = [
        api.mergeblocks(
            dataset,
            varlist,
            level=level,
            backend=backend,
            nthreads=nthreads,
            monitor=monitor,
        )
        for dataset in datasets
    ]

    nxb, nyb, nzb, dx, dy, dz, xmin, ymin, zmin, xmax, ymax, zmax = [
        merged_datasets[0].nxb,
        merged_datasets[0].nyb,
        merged_datasets[0].nzb,
        merged_datasets[0].blocklist[0].dx,
        merged_datasets[0].blocklist[0].dy,
        merged_datasets[0].blocklist[0].dz,
        merged_datasets[0].xmin,
        merged_datasets[0].ymin,
        merged_datasets[0].zmin,
        merged_datasets[0].xmax,
        merged_datasets[0].ymax,
        merged_datasets[0].zmax,
    ]

    for dataset in merged_datasets:
        if [nxb, nyb, nzb] != [dataset.nxb, dataset.nyb, dataset.nzb]:
            raise ValueError("[boxkit.mean_temporal] inconsistent sizes for datasets")

    average_data = library.Data(nblocks=1, nxb=nxb, nyb=nyb, nzb=nzb)

    average_blocklist = [
        library.Block(
            average_data,
            dx=dx,
            dy=dy,
            dz=dz,
            xmin=xmin,
            ymin=ymin,
            zmin=zmin,
            xmax=xmax,
            ymax=ymax,
            zmax=zmax,
        )
    ]

    average_dataset = library.Dataset(average_blocklist, average_data)

    for varkey in varlist:
        average_dataset.addvar(varkey)

        reduce_dset_list.nthreads = 1
        reduce_dset_list.backend = "serial"

        if monitor:
            time_reduction = library.Timer("[boxkit.mean_temporal.reduce_dset_list]")

        reduce_dset_list(merged_datasets, average_dataset, varkey, len(merged_datasets))

        if monitor:
            del time_reduction

    for dataset in merged_datasets:
        dataset.purge("boxmem")

    if monitor:
        del time_mean_temporal

    return average_dataset


@library.Action(unit=library.Dataset)
def reduce_dset_list(unit, average_dataset, varkey, sample_size):
    """
    Reduce dataset / compute average
    """
    for block_avg, block_unit in zip(average_dataset.blocklist, unit.blocklist):
        block_avg[varkey][:] = (
            block_avg[varkey][:] + block_unit[varkey][:] / sample_size
        )
