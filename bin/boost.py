"""Custom commands for BoxKit setup."""

import os
import sys
import subprocess
from distutils.sysconfig import get_python_version  # pylint: disable=deprecated-module

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def boost_build():
    """Installation for Boost library"""
    subprocess.run(
        "git submodule update --init --recursive submodules/boost",
        shell=True,
        check=True,
        executable="/bin/bash",
    )

    subprocess.run(
        "cd submodules/boost && ./bootstrap.sh"
        + f" --with-python-version={get_python_version()}"
        + " --with-toolset=gcc"
        + f" --prefix={os.getenv('PWD')}/boxkit/depends/boost && ./b2 install",
        shell=True,
        check=True,
        executable="/bin/bash",
    )


def boost_clean():
    """Clean boost source environment"""
    subprocess.run(
        "git submodule deinit -f submodules/boost",
        shell=True,
        check=True,
        executable="/bin/bash",
    )


def boost_install():
    """Install Boost library"""
    if os.path.exists(os.getenv("PWD") + "/boxkit/depends/boost"):
        subprocess.run(
            "mkdir -pv build/lib/boxkit/depends/boost/lib",
            shell=True,
            check=True,
            executable="/bin/bash",
        )

        subprocess.run(
            "cp boxkit/depends/boost/lib/lib* build/lib/boxkit/depends/boost/lib/.",
            shell=True,
            check=True,
            executable="/bin/bash",
        )
