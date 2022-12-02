"""Custom commands for BoxKit setup."""

import os
import sys
import subprocess
from distutils import sysconfig

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Dictionary of Makefile variables for CBox
# These variables are defined in boxkit/cbox/source/Make.inc
# and are assigned here to build and compile when setting up the
# Python library
CBOX_MAKE_DICT = {
    "cc": "g++",
    "python_version": sysconfig.get_python_version(),
    "boost_version": "".join(sysconfig.get_python_version().split(".")),
    "python_include_path": sysconfig.get_python_inc(),
    "python_lib_path": sysconfig.BASE_PREFIX + "/inclue" + f"/python{sysconfig.get_python_version()}/config",
    "boost_include_path": (
        os.getenv("PWD") + "/boxkit/depends/boost/include"
        if os.path.exists(os.getenv("PWD") + "/boxkit/depends/boost")
        else ""
    ),
    "boost_lib_path": (
        os.getenv("PWD") + "/boxkit/depends/boost/lib"
        if os.path.exists(os.getenv("PWD") + "/boxkit/depends/boost")
        else ""
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
        executable="/bin/bash",
    )


# CBox install command which install cbox libraries
# to package directory
def cbox_install():
    """Install cbox"""
    subprocess.run(
        "cp boxkit/cbox/lib/*.so build/lib/boxkit/cbox/lib/.",
        shell=True,
        check=True,
        executable="/bin/bash",
    )


# Clean CBox environment
def cbox_clean():
    """Clean cbox objects"""
    subprocess.run(
        "cd boxkit/cbox/source && make clean && cd ../../../",
        shell=True,
        check=True,
        executable="/bin/bash",
    )
