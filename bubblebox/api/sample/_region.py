""" Module with implemenation of region methods"""

from ...library import domain, measure

def region_create(dataset,attributes={}):
    """
    dataset    : Dataset object
 
    attributes : dictionary of attributes
    """
 
    region_attributes = {'xmin' : dataset.xmin, 'ymin' : dataset.ymin, 'zmin' : dataset.zmin,
                         'xmax' : dataset.xmax, 'ymax' : dataset.ymax, 'zmax' : dataset.zmax}

    for key in attributes: region_attributes[key] = attributes[key]

    return domain.Region(attributes=region_attributes,blocks=dataset.blocks)

def region_bubbles(region,key):
    """
    regions : list of regions (Volume or Slice)

    key     : key for the variable to measure
    """

    regionprops = measure.region_props(region,key)

    bubbleprops = [ {'area' : props['area']} for props in regionprops]

    return bubbleprops
