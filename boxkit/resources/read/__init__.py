"""Initializate read unit"""

from ._sample import read_test_sample
from ._flash import read_flash

options = {"test-sample": read_test_sample, "flash": read_flash}
