"""boxkit.api module"""

import os

from .. import options

from ._create import create_dataset, create_region, create_slice
from ._read import read_dataset
from ._mergeblocks import mergeblocks
from ._resfilter import resfilter
from ._mean import mean_temporal

if options.ANALYSIS:
    from ._regionprops import regionprops
