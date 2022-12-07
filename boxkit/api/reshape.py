"""Module with implemenetation of api reshape methods"""

from .. import library

from ..resources import stencils

from ..library import Process, Timer


@Process(stencils=[stencils.reshape])
def dataset(self, dataset, varlist, level=1, nthreads=1, **attributes):
    """
    Reshaped dataset at a level
    """
    _time0 = Timer("Reshape dataset")
    if isinstance(varlist, str):
        varlist = [varlist]

    level_dx, level_dy, level_dz = [None] * 3

    blocklist_level = []

    _time1 = Timer("Block level")
    for block in dataset.blocklist:
        if block.level == level:
            blocklist_level.append(block)
    del _time1

    if not blocklist_level:
        raise ValueError(
            f"[boxkit.library.dataset]: level={level} does not exist in input dataset"
        )

    region_level = library.Region(blocklist_level)

    nblockx = int((dataset.xmax - dataset.xmin) / blocklist_level[0].dx / dataset.nxb)
    nblocky = int((dataset.ymax - dataset.ymin) / blocklist_level[0].dy / dataset.nyb)
    nblockz = int((dataset.zmax - dataset.zmin) / blocklist_level[0].dz / dataset.nzb)

    if nblockx == 0:
        nblockx = 1

    if nblocky == 0:
        nblocky = 1

    if nblockz == 0:
        nblockz = 1

    data_reshaped = library.Data(
        nblocks=1,
        nxb=nblockx * dataset.nxb,
        nyb=nblocky * dataset.nyb,
        nzb=nblockz * dataset.nzb,
    )

    blocklist_reshaped = [
        library.Block(
            data_reshaped,
            dx=blocklist_level[0].dx,
            dy=blocklist_level[0].dy,
            dz=blocklist_level[0].dz,
            xmin=region_level.xmin,
            ymin=region_level.ymin,
            zmin=region_level.zmin,
            xmax=region_level.xmax,
            ymax=region_level.ymax,
            zmax=region_level.zmax,
        )
    ]

    dataset_reshaped = library.Dataset(blocklist_reshaped, data_reshaped)

    for varkey in varlist:

        _time2 = Timer("Addvar")
        dataset_reshaped.addvar(varkey, dtype=dataset._data.dtype[varkey])
        del _time2

        self.tasks["reshape"]["block"].nthreads = nthreads
        self.tasks["reshape"]["block"].monitor = True

        _time3 = Timer("Reshape block")
        self.tasks["reshape"]["block"](blocklist_level, dataset_reshaped, varkey)
        del _time3

    del _time0
    return dataset_reshaped
