"""Module for level-set related operations"""

import numpy
import skimage.measure as skimage_measure

from numba import jit

import boxkit


def lset_plot_contour_2d(ax, merged_dataset, filled=False, *args, **kwargs):
    """
    Plot lset from a dataset to a figure

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
    Plot normal vectors to lset from a dataset to a figure

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


def lset_quant_measurement_2d(merged_dataset):
    """
    Perform velocity measurement on level set
    """
    if len(merged_dataset.blocklist) > 1:
        raise ValueError(
            "[boxkit.resources.flash.lset_vel_measurement_2d] dataset must only have one block"
        )

    merged_dataset.addvar("bwlabel", dtype=int)

    quantlist = []

    for block in merged_dataset.blocklist:
        block["bwlabel"] = skimage_measure.label(block["dfun"] >= 0)
        shape_num = numpy.max(block["bwlabel"][:])

        mean_vel = numpy.zeros([shape_num, 2], dtype=float)
        mean_label = numpy.zeros([shape_num, 1], dtype=float)
        mean_pos = numpy.zeros([shape_num, 2], dtype=float)

        xcenter = block.xrange("center")
        ycenter = block.yrange("center")

        lset_quant_blk_2d(
            block["bwlabel"],
            block["velx"],
            block["vely"],
            xcenter,
            ycenter,
            block.nxb,
            block.nyb,
            block.xguard,
            block.yguard,
            block.dx,
            block.dy,
            mean_vel,
            mean_pos,
            mean_label,
        )

        mean_vel = mean_vel / mean_label
        mean_pos = mean_pos / mean_label

        for shape_index in range(shape_num):
            shape_dict = {
                "velocity": mean_vel[shape_index, :],
                "centroid": mean_pos[shape_index, :],
            }

            quantlist.append(shape_dict)

    merged_dataset.delvar("bwlabel")

    return quantlist


def lset_shape_measurement_2d(merged_dataset, correction=False):
    """
    Perform shape measurement on level set
    """
    if len(merged_dataset.blocklist) > 1:
        raise ValueError(
            "[boxkit.resources.flash.lset_shape_measurement_2d] dataset must only have one block"
        )

    shapelist = boxkit.regionprops(merged_dataset, "dfun")

    if correction:

        merged_dataset.addvar("bwlabel", dtype=int)
        merged_dataset.addvar("nrmx", dtype=float)
        merged_dataset.addvar("nrmy", dtype=float)

        lset_compute_normals_2d(merged_dataset, ["nrmx", "nrmy"])

        modified_perimeter = numpy.zeros([len(shapelist), 1], dtype=float)
        sol_points = numpy.zeros([2, 2], dtype=float)

        for block in merged_dataset.blocklist:
            block["bwlabel"] = skimage_measure.label(block["dfun"] >= 0)
            xcenter = block.xrange("center")
            ycenter = block.yrange("center")

            lset_perimeter_blk_2d(
                block["dfun"],
                block["bwlabel"],
                block["nrmx"],
                block["nrmy"],
                xcenter,
                ycenter,
                modified_perimeter,
                block.nxb,
                block.nyb,
                block.xguard,
                block.yguard,
                block.dx,
                block.dy,
                sol_points,
            )

        for shape_index, shape in enumerate(shapelist):
            shape["perimeter"] = modified_perimeter[shape_index]

        merged_dataset.delvar("bwlabel")
        merged_dataset.delvar("nrmx")
        merged_dataset.delvar("nrmy")

    return shapelist


@jit(nopython=True)
def lset_quant_blk_2d(
    label,
    velx,
    vely,
    xcenter,
    ycenter,
    nxb,
    nyb,
    xguard,
    yguard,
    dx,
    dy,
    mean_vel,
    mean_pos,
    mean_label,
):  # pylint: disable=too-many-arguments disable=too-many-locals
    """
    perform quant measurement on a block
    """
    k = 0
    for j in range(yguard, nyb + yguard):
        for i in range(xguard, nxb + xguard):
            if label[k, j, i] > 0:
                shape_index = label[k, j, i] - 1

                mean_vel[shape_index, 0] = (
                    mean_vel[shape_index, 0] + vely[k, j, i] * dx * dy
                )
                mean_vel[shape_index, 1] = (
                    mean_vel[shape_index, 1] + velx[k, j, i] * dx * dy
                )

                mean_pos[shape_index, 0] = (
                    mean_pos[shape_index, 0] + ycenter[j] * dx * dy
                )
                mean_pos[shape_index, 1] = (
                    mean_pos[shape_index, 1] + xcenter[i] * dx * dy
                )

                mean_label[shape_index] = mean_label[shape_index] + dx * dy


@jit(nopython=True)
def lset_perimeter_blk_2d(
    dfun,
    label,
    nrmx,
    nrmy,
    xcenter,
    ycenter,
    perimeter,
    nxb,
    nyb,
    xguard,
    yguard,
    dx,
    dy,
    sol_points,
):  # pylint: disable=too-many-arguments disable=too-many-locals
    """
    Get perimeter using level-set
    """
    k = 0
    for j in range(yguard, nyb + yguard):
        for i in range(xguard, nxb + xguard):
            if (
                (dfun[k, j, i] * dfun[k, j, i - 1] <= 0)
                or (dfun[k, j, i] * dfun[k, j, i + 1] <= 0)
                or (dfun[k, j, i] * dfun[k, j - 1, i] <= 0)
                or (dfun[k, j, i] * dfun[k, j + 1, i] <= 0)
            ):
                labels = [
                    label[k, j, i],
                    label[k, j, i + 1],
                    label[k, j, i - 1],
                    label[k, j + 1, i],
                    label[k, j - 1, i],
                ]

                shape_index = (
                    list(set([label for label in labels if label != 0]))[0] - 1
                )

                if abs(dfun[k, j, i]) <= numpy.sqrt(dx**2 + dy**2):

                    lset_intersect_blk_2d(
                        dfun[k, j, i],
                        nrmx[k, j, i],
                        nrmy[k, j, i],
                        xcenter[i],
                        ycenter[j],
                        dx,
                        dy,
                        sol_points,
                    )

                    perimeter[shape_index] = perimeter[shape_index] + numpy.sqrt(
                        (sol_points[1, 1] - sol_points[0, 1]) ** 2
                        + (sol_points[1, 0] - sol_points[0, 0]) ** 2
                    )


@jit(nopython=True)
def lset_intersect_blk_2d(
    dfun, nrmx, nrmy, xcenter, ycenter, dx, dy, sol_points
):  # pylint: disable=too-many-arguments disable=too-many-locals
    """
    Get intersection of level-set with block
    """
    (
        xquery,
        yquery,
    ) = [xcenter + dfun * nrmx, ycenter + dfun * nrmy]

    line_slope = -nrmx / nrmy
    line_constant = yquery - line_slope * xquery

    xlow, xhigh = [xcenter - dx / 2, xcenter + dx / 2]
    ylow, yhigh = [ycenter - dy / 2, ycenter + dy / 2]

    p1 = [xlow, line_slope * xlow + line_constant]
    p2 = [xhigh, line_slope * xhigh + line_constant]
    p3 = [(ylow - line_constant) / line_slope, ylow]
    p4 = [(yhigh - line_constant) / line_slope, yhigh]

    num_points = 0
    sol_points[:] = 0.0

    for point in [p1, p2, p3, p4]:
        if (
            point[0] >= xlow
            and point[0] <= xhigh
            and point[1] >= ylow
            and point[1] <= yhigh
        ):
            sol_points[num_points, 0] = point[0]
            sol_points[num_points, 1] = point[1]
            num_points = num_points + 1

    return sol_points
