"""Initialization of parallel interface"""

import os

from ._execute import exectask
from ._action import Action
from ._process import Process

if os.getenv("CBOX_BACKEND") == "TRUE":
    from ._monitor import Monitor

if os.getenv("BBOX_SERVER") == "TRUE":
    from ._server import Server
