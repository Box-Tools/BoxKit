"""Initialize resources"""
import os

from . import read

if os.getenv("BBOX_TESTING") == "TRUE":
    from . import stencils
