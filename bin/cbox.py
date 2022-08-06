"""Custom commands for BoxKit setup."""

import os
import sys
import subprocess
from distutils.sysconfig import get_python_version, BASE_PREFIX

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Dictionary of Makefile variables for CBox
# These variables are defined in boxkit/cbox/source/Make.inc
# and are assigned here to build and compile when setting up the
# Python library
CBOX_MAKE_DICT = {
    "python_version": get_python_version(),
    "python_path": BASE_PREFIX,
    "boost_version": "".join(get_python_version().split(".")),
    "boost_path": (
        os.getenv("PWD") + "/boxkit/depends/boost"
        if os.path.exists(os.getenv("PWD") + "/boxkit/depends/boost")
        else BASE_PREFIX
    ),
}

# Argument string for make command
# converts CBOX_MAKE_DICT into a key, value string
CBOX_MAKE_ARGS = ""

for key, value in CBOX_MAKE_DICT.items():
    CBOX_MAKE_ARGS = CBOX_MAKE_ARGS + " " + f"{key}={value}"

# CBox build command which goes into cbox directory and compiles
# the source code
def cbox_build():
    """Compile and build cbox"""
    subprocess.run(
        f"cd boxkit/cbox/source && make {CBOX_MAKE_ARGS}",
        shell=True,
        check=True,
    )


# CBox install command which install cbox libraries
# to package directory
def cbox_install():
    """Install cbox"""
    subprocess.run(
        "cp boxkit/cbox/lib/*.so build/lib/boxkit/cbox/lib/.",
        shell=True,
        check=True,
    )


# Clean CBox environment
def cbox_clean():
    """Clean cbox objects"""
    subprocess.run(
        "cd boxkit/cbox/source && make clean && cd ../../../", shell=True, check=True
    )
