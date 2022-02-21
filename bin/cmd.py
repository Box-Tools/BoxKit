"""Custom commands for BubbleBox setup."""
import os
import sys
import subprocess
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cbox import cbox_install

# custom build command
class BuildCmd(build_py):
    """Custom build_py command."""

    def run(self):
        build_py.run(self)
        cbox_install()
        subprocess.run(
            "cp bubblebox/cbox/lib/*.so build/lib/bubblebox/cbox/lib/.",
            shell=True,
            check=True,
        )


# custom develop command
class DevelopCmd(develop):
    """Custom develop command."""

    def run(self):
        develop.run(self)
        cbox_install()
