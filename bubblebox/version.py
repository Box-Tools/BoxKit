"""Set up the version."""

import os


_version_major = 0
_version_minor = 1
_version_micro = ''
_version_extra = 'dev'

# construct full version string
_ver = [_version_major, _version_minor]

if _version_micro:
	_ver.append(_version_micro)
if _version_extra:
	_ver.append(_version_extra)

__version__ = '.'.join(map(str, _ver))

NAME = 'bubblebox'
