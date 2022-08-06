"""Initializate read unit"""

from ._default import read_default
from ._flash import read_flash

options = {"default": read_default, "flash": read_flash}
