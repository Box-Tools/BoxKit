"""Top level intialization of BoxKit"""

import os
import toml

from . import api
from . import library
from . import resources

from . import options

if options.cbox:
    from . import cbox
