"""Custom commands for BubbleBox setup."""
import os
import sys
import subprocess
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
from distutils.sysconfig import get_python_version, BASE_PREFIX


# Custom variables
CBOX_DICT = {
    "python_version": get_python_version(),
    "python_path": BASE_PREFIX,
    "boost_version": "".join(get_python_version().split(".")),
    "boost_path": BASE_PREFIX,
}


# cbox install command
def cbox_install():
    """installation for cbox"""
    subprocess.run(
        "cd bubblebox/cbox/source && make"
        + " "
        + f"python_version={CBOX_DICT['python_version']} python_path={CBOX_DICT['python_path']}"
        + " "
        + f"boost_version={CBOX_DICT['boost_version']} boost_path={CBOX_DICT['boost_path']}",
        shell=True,
        check=True,
    )


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
