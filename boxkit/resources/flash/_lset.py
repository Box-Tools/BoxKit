"""Module for level-set related operations"""

import numpy
import boxkit
import skimage.measure as skimage_measure


def bubble_contour_plot(ax, dataset, filled=False):
    """
    Plot bubble from a dataset to a figure

    Arguments
    ---------
    ax         : Axes handle
    dataset    : Dataset object
    """
    merged_dataset = boxkit.mergeblocks(dataset, "dfun", nthreads=1, backend="loky")
    for block in merged_dataset.blocklist:
        xmesh, ymesh = numpy.meshgrid(block.xrange("center"), block.yrange("center"))

        if filled:
            ax.contourf(
                xmesh[
                    block.yguard : block.nyb + block.yguard,
                    block.xguard : block.nxb + block.xguard,
                ],
                ymesh[
                    block.yguard : block.nyb + block.yguard,
                    block.xguard : block.nxb + block.xguard,
                ],
                block["dfun"][
                    0,
                    block.yguard : block.nyb + block.yguard,
                    block.xguard : block.nxb + block.xguard,
                ],
            )

        else:
            ax.contour(
                xmesh[
                    block.yguard : block.nyb + block.yguard,
                    block.xguard : block.nxb + block.xguard,
                ],
                ymesh[
                    block.yguard : block.nyb + block.yguard,
                    block.xguard : block.nxb + block.xguard,
                ],
                block["dfun"][
                    0,
                    block.yguard : block.nyb + block.yguard,
                    block.xguard : block.nxb + block.xguard,
                ],
                levels=[0],
            )


def bubble_normal_vectors(ax, merged_dataset, *args, **kwargs):
    """
    Plot normal vectors to bubble from a dataset to a figure

    Arguments
    ---------
    ax         : Axes handle
    dataset    : Dataset object
    """
    for block in merged_dataset.blocklist:
        xmesh, ymesh = numpy.meshgrid(block.xrange("center"), block.yrange("center"))
        ax.contour(
            xmesh[
                block.yguard : block.nyb + block.yguard,
                block.xguard : block.nxb + block.xguard,
            ],
            ymesh[
                block.yguard : block.nyb + block.yguard,
                block.xguard : block.nxb + block.xguard,
            ],
            block["dfun"][
                0,
                block.yguard : block.nyb + block.yguard,
                block.xguard : block.nxb + block.xguard,
            ],
            levels=[0],
        )
        ax.quiver(
            xmesh[::5, ::5],
            ymesh[::5, ::5],
            block["normx"][
                0,
                block.yguard : block.nyb + block.yguard : 5,
                block.xguard : block.nxb + block.xguard : 5,
            ],
            block["normy"][
                0,
                block.yguard : block.nyb + block.yguard : 5,
                block.xguard : block.nxb + block.xguard : 5,
            ],
            *args,
            **kwargs,
        )


def bubble_shape_measurement(dataset):
    """
    Perform measurements on the bubble
    """
    merged_varlist = ["dfun", "velx", "vely"]
    merged_dataset = boxkit.mergeblocks(
        dataset, merged_varlist, nthreads=1, backend="loky"
    )
    merged_dataset.fill_guard_cells(merged_varlist)

    bubblelist = boxkit.regionprops(merged_dataset, "dfun", backend="loky", nthreads=1)

    max_area = 1e-13
    main_bubble = None
    main_bubble_index = 0

    for index, bubble in enumerate(bubblelist):
        if bubble["area"] > max_area:
            main_bubble = bubble
            main_bubble_index = index

    aux_varlist = {"bwlabel": int, "normx": float, "normy": float}
    for var, dtype in aux_varlist.items():
        merged_dataset.addvar(var, dtype=dtype)

    for block in merged_dataset.blocklist:
        block["bwlabel"] = skimage_measure.label(block["dfun"] >= 0)

        grad_x = (block["dfun"][0, 1:-1, 2:] - block["dfun"][0, 1:-1, :-2]) / (
            2 * block.dx
        )
        grad_y = (block["dfun"][0, 2:, 1:-1] - block["dfun"][0, :-2, 1:-1]) / (
            2 * block.dy
        )

        block["normx"][0, 1:-1, 1:-1] = -grad_x / numpy.sqrt(
            grad_x**2 + grad_y**2 + 1e-13
        )
        block["normy"][0, 1:-1, 1:-1] = -grad_y / numpy.sqrt(
            grad_x**2 + grad_y**2 + 1e-13
        )

    merged_dataset.fill_guard_cells(aux_varlist)

    modified_perimeter = [0.0] * len(bubblelist)

    for block in merged_dataset.blocklist:
        for k in range(block.zguard, block.nzb + block.zguard):
            for j in range(block.yguard, block.nyb + block.yguard):
                for i in range(block.xguard, block.nxb + block.xguard):
                    if (
                        (block["dfun"][k, j, i] * block["dfun"][k, j, i - 1] <= 0)
                        or (block["dfun"][k, j, i] * block["dfun"][k, j, i + 1] <= 0)
                        or (block["dfun"][k, j, i] * block["dfun"][k, j - 1, i] <= 0)
                        or (block["dfun"][k, j, i] * block["dfun"][k, j + 1, i] <= 0)
                    ):
                        labels = [
                            block["bwlabel"][k, j, i],
                            block["bwlabel"][k, j, i + 1],
                            block["bwlabel"][k, j, i - 1],
                            block["bwlabel"][k, j + 1, i],
                            block["bwlabel"][k, j - 1, i],
                        ]

                        labels = list(set(labels))

                        if 0 not in labels:
                            raise ValueError(
                                f"[boxkit.resources.flash.bubble_shape_measurement] 0 does not exist in "
                                + f"{labels} near point {[k,j,i]}"
                            )

                        labels.pop(0)
                        if len(labels) > 1:
                            raise ValueError(
                                f"[boxkit.resources.flash.bubble_shape_measurement] More than 1 "
                                + f"non-zeros values exist in {labels} near point {[k,j,i]}"
                            )

                        bubble_index = labels[0] - 1
                        modified_perimeter[bubble_index] = (
                            modified_perimeter[bubble_index] + block.dx
                        )

    # for var in aux_varlist:
    #    merged_dataset.delvar(var)

    return modified_perimeter, bubblelist, main_bubble, merged_dataset
