from ... import options

from ._reshape import map_dataset_block

if options.testing:
    from ._measure import regionprops_block
