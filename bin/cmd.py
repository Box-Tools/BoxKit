"""Custom commands for BubbleBox setup."""
import os
import sys
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import cbox_build, and cbox_install from cbox
# module located in the 'bin' folder of the
# package directory
from cbox import cbox_build, cbox_install
from boost import boost_install

# custom build command
# replaces the default build command for setup.py
class BuildCmd(build_py):
    """Custom build_py command."""

    def run(self):
        build_py.run(self)
        cbox_build()
        cbox_install()
        boost_install()


# custom develop command
# replaces custom develop command for setup.py
class DevelopCmd(develop):
    """Custom develop command."""

    def run(self):
        develop.run(self)
        cbox_build()
