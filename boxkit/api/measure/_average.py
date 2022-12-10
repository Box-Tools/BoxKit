""" Module with implemenation of measure methods"""

from ... import library

from ...library import Timer, Action

from .. import reshape


def Average(datasets, varlist, level=1, backend="serial", nthreads=1, monitor=False):
    """
    Compute average across a dataset list
    """
    if monitor:
        time_average = Timer("[boxkit.measure.average]")

    if isinstance(varlist, str):
        varlist = [varlist]

    reshaped_datasets = [
        reshape.Mergeblocks(
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
        reshaped_datasets[0].nxb,
        reshaped_datasets[0].nyb,
        reshaped_datasets[0].nzb,
        reshaped_datasets[0].blocklist[0].dx,
        reshaped_datasets[0].blocklist[0].dy,
        reshaped_datasets[0].blocklist[0].dz,
        reshaped_datasets[0].xmin,
        reshaped_datasets[0].ymin,
        reshaped_datasets[0].zmin,
        reshaped_datasets[0].xmax,
        reshaped_datasets[0].ymax,
        reshaped_datasets[0].zmax,
    ]

    for dataset in reshaped_datasets:
        if [nxb, nyb, nzb] != [dataset.nxb, dataset.nyb, dataset.nzb]:
            raise ValueError("[boxkit.measure.average] inconsistent sizes for datasets")

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

        reduce_dset.nthreads = nthreads
        reduce_dset.backend = backend

        if monitor:
            time_atomic = Timer("[boxkit.measure.reduce_dset]")

        reduce_dset(reshaped_datasets, average_dataset, varkey, len(reshaped_datasets))

        if monitor:
            del time_atomic

    for dataset in reshaped_datasets:
        dataset.purge("boxmem")

    if monitor:
        del time_average

    return average_dataset


@Action(unit=library.Dataset)
def reduce_dset(unit, average_dataset, varkey, sample_size):
    average_dataset[varkey][:] = unit[varkey][:] / sample_size
