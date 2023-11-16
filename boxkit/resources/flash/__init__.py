"""Initializate flash module"""

from ._read import read
from ... import options

if options.ANALYSIS == 1:
    from ._lset import (
        lset_plot_contour_2d,
        lset_plot_normals_2d,
        lset_shape_measurement_2d,
        lset_compute_normals_2d,
    )
