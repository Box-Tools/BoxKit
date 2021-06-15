"""Set up package."""

import os
from setuptools import setup, find_packages

# Get version and release info.
version_file = os.path.join('bubblebox', 'version.py')
with open(version_file) as infile:
    exec(infile.read())

options = dict(name=NAME)

if __name__ == '__main__':
    setup(**options)
