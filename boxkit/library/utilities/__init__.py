"""Initialization of parallel interface"""

import os

from ... import options

from ._execute import exectask
from ._action import Action
from ._process import Process

if options.cbox:
    from ._monitor import Monitor

if options.server:
    from ._server import Server
