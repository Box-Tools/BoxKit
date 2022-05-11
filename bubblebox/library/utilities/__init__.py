"""Initialization of parallel interface"""

import os

from ._execute import exectask
from ._action import Action
from ._process import Process

if os.getenv("cbox_backend") == "TRUE":
    from ._monitor import Monitor
