"""Module with implemenetation of api reshape methods"""

import math

from ... import library


def Filterblocks(
    dataset, varlist=None, level=1, nthreads=1, monitor=False, backend="serial"
):
    """
    Build a pseudo UG dataset from AMR dataset at a level
    """
    if not varlist:
        varlist = dataset.varlist

    elif isinstance(varlist, str):
        varlist = [varlist]

    pass
