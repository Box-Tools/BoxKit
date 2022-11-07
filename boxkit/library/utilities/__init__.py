"""Initialization of parallel interface"""

import os

from ._execute import exectask
from ._action import Action
from ._process import Process
from ._server import Server

if os.getenv("CBOX_BACKEND") == "TRUE":
    from ._monitor import Monitor
