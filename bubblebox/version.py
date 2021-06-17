"""Set up the version."""

import os


_version_major = 0
_version_minor = 0
_version_micro = ''
_version_extra = 'dev'

# construct full version string
_ver = [_version_major, _version_minor]
if _version_micro:
    _ver.append(_version_micro)
if _version_extra:
    _ver.append(_version_extra)
__version__ = '.'.join(map(str, _ver))

CLASSIFIERS = ['Development Status :: 1 - Alpha',
               'Environment :: Console',
               'License :: OSI Approved :: BSD 3-Clause License',
               'Operating System :: Unix',
               'Programming Language :: Python']

description = 'bubblebox: block-structured data analysis library'
# Long description will go up on the pypi page
long_description = """
bubblebox
=====
License
=======
"""

NAME = 'bubblebox'
MAINTAINER = ''
MAINTAINER_EMAIL = ''
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = ''
DOWNLOAD_URL = ''
LICENSE = 'BSD 3-Clause'
AUTHOR = ''
AUTHOR_EMAIL = ''
PLATFORMS = 'Unix'
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
PACKAGES = ['bubblebox']
PACKAGE_DATA = {'bubblebox': [os.path.join('styles', '*')]}
REQUIRES = ['numpy', 'matplotlib', 'h5py', 'annoy', 'numba', 'shapely', 'scipy', 'pymorton']
