import os

from .. import options

from ._create import create_dataset, create_region, create_slice
from ._read import read_dataset
from ._mergeblocks import mergeblocks
from ._filter_level import filter_level
from ._temporal_mean import temporal_mean

if options.testing:
    from ._regionprops import regionprops
