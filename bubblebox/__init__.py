"""Top level intialization of BubbleBox"""

import os

from . import api
from . import library
from . import resources

if os.getenv("cbox_backend"):
    from . import cbox
