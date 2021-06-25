""" Module with implemenation of measurement API"""

from ... import library

def measure_regionprops(region,key):
    """
    region : object (Volume or Slice)
    key    : key for the variable to measure
    """

    regionprops = list(map(library.analysis.BlockProps,region.blocks,[key]))

    return regionprops
