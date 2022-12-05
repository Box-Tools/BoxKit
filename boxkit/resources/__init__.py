"""Initialize resources"""
import os

from .. import options

from . import read

if options.testing:
    from . import stencils
