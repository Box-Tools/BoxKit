"""Module for level-set related operations"""

import numpy
import boxkit
import skimage.measure as skimage_measure


def lset_plot_contour_2d(ax, merged_dataset, filled=False, *args, **kwargs):
    """
    Plot bubble from a dataset to a figure

    Arguments
    ---------
    ax         : Axes handle
    dataset    : Dataset object
    """
    if len(merged_dataset.blocklist) > 1:
        raise ValueError(
            "[boxkit.resources.flash.lset_contour_plot_2d] dataset must only have one block"
        )

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
                *args,
                **kwargs,
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
                *args,
                **kwargs,
            )


def lset_plot_normals_2d(ax, merged_dataset, *args, **kwargs):
    """
    Plot normal vectors to bubble from a dataset to a figure

    Arguments
    ---------
    ax         : Axes handle
    dataset    : Dataset object
    """
    if len(merged_dataset.blocklist) > 1:
        raise ValueError(
            "[boxkit.resources.flash.lset_normal_vectors_2d] dataset must only have one block"
        )

    varlist = ["normx", "normy"]
    for ivar in varlist:
        merged_dataset.addvar(ivar, dtype=float)

    lset_compute_normals_2d(merged_dataset, varlist)

    for block in merged_dataset.blocklist:
        xmesh, ymesh = numpy.meshgrid(block.xrange("center"), block.yrange("center"))
        ax.quiver(
            xmesh[
                block.yguard : block.nyb + block.yguard : 5,
                block.xguard : block.nxb + block.xguard : 5,
            ],
            ymesh[
                block.yguard : block.nyb + block.yguard : 5,
                block.xguard : block.nxb + block.xguard : 5,
            ],
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

    for var in varlist:
        merged_dataset.delvar(var)


def lset_compute_normals_2d(dataset, varlist):
    """
    Compute normals
    """
    nrmx, nrmy = varlist
    for block in dataset.blocklist:

        grad_x = (block["dfun"][0, 1:-1, 2:] - block["dfun"][0, 1:-1, :-2]) / (
            2 * block.dx
        )
        grad_y = (block["dfun"][0, 2:, 1:-1] - block["dfun"][0, :-2, 1:-1]) / (
            2 * block.dy
        )

        block[nrmx][0, 1:-1, 1:-1] = -grad_x / numpy.sqrt(
            grad_x**2 + grad_y**2 + 1e-13
        )

        block[nrmy][0, 1:-1, 1:-1] = -grad_y / numpy.sqrt(
            grad_x**2 + grad_y**2 + 1e-13
        )

    dataset.fill_guard_cells(varlist)


def lset_shape_measurement_2d(merged_dataset):
    """
    Perform measurements on the bubble
    """
    if len(merged_dataset.blocklist) > 1:
        raise ValueError(
            "[boxkit.resources.flash.lset_shape_measurement_2d] dataset must only have one block"
        )

    bubblelist = boxkit.regionprops(merged_dataset, "dfun", backend="loky", nthreads=1)

    merged_dataset.addvar("bwlabel", dtype=int)
    merged_dataset.addvar("nrmx", dtype=float)
    merged_dataset.addvar("nrmy", dtype=float)

    for block in merged_dataset.blocklist:
        block["bwlabel"] = skimage_measure.label(block["dfun"] >= 0)

    lset_compute_normals_2d(merged_dataset, ["nrmx", "nrmy"])

    modified_perimeter = [0.0] * len(bubblelist)

    for block in merged_dataset.blocklist:

        xcenter = block.xrange("center")
        ycenter = block.yrange("center")

        for k in range(block.zguard, block.nzb + block.zguard):
            for j in range(block.yguard, block.nyb + block.yguard):
                for i in range(block.xguard, block.nxb + block.xguard):
                    if (
                        False
                        or (block["dfun"][k, j, i] * block["dfun"][k, j, i - 1] <= 0)
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

                        if abs(block["dfun"][k, j, i]) <= numpy.sqrt(
                            block.dx**2 + block.dy**2
                        ):

                            xquery, yquery, = [
                                xcenter[i]
                                + block["dfun"][k, j, i] * block["nrmx"][k, j, i],
                                ycenter[j]
                                + block["dfun"][k, j, i] * block["nrmy"][k, j, i],
                            ]

                            line_slope = (
                                -block["nrmx"][k, j, i] / block["nrmy"][k, j, i]
                            )
                            line_constant = yquery - line_slope * xquery

                            xlow, xhigh = [
                                xcenter[i] - block.dx / 2,
                                xcenter[i] + block.dx / 2,
                            ]
                            ylow, yhigh = [
                                ycenter[j] - block.dy / 2,
                                ycenter[j] + block.dy / 2,
                            ]

                            p1 = [xlow, line_slope * xlow + line_constant]
                            p2 = [xhigh, line_slope * xhigh + line_constant]
                            p3 = [(ylow - line_constant) / line_slope, ylow]
                            p4 = [(yhigh - line_constant) / line_slope, yhigh]

                            num_points = 0
                            sol_points = numpy.zeros([2, 2], dtype=float)

                            for point in [p1, p2, p3, p4]:
                                if (
                                    True
                                    and point[0] >= xlow
                                    and point[0] <= xhigh
                                    and point[1] >= ylow
                                    and point[1] <= yhigh
                                ):
                                    sol_points[num_points, 0] = point[0]
                                    sol_points[num_points, 1] = point[1]
                                    num_points = num_points + 1

                            modified_perimeter[bubble_index] = modified_perimeter[
                                bubble_index
                            ] + numpy.sqrt(
                                (sol_points[1, 1] - sol_points[0, 1]) ** 2
                                + (sol_points[1, 0] - sol_points[0, 0]) ** 2
                            )

    for bubble_index, bubble in enumerate(bubblelist):
        bubble["perimeter"] = modified_perimeter[bubble_index]

    merged_dataset.delvar("bwlabel")
    merged_dataset.delvar("nrmx")
    merged_dataset.delvar("nrmy")

    return bubblelist
