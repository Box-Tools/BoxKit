"""Initializate flash module"""

from ._read import read
from ... import options

if options.ANALYSIS == 1:
    from ._lset import (
        bubble_contour_plot,
        bubble_normal_vectors,
        bubble_shape_measurement,
    )
