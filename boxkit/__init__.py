"""Top level intialization of BoxKit"""

import os
import toml

envfile = os.path.dirname(os.path.realpath(__file__)) + "/envfile"

for key, value in toml.load(envfile).items():
    os.environ[key] = str(value)

from . import api
from . import library
from . import resources

if os.getenv("CBOX_BACKEND") == "TRUE":
    from . import cbox
