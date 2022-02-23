"""Custom commands for BubbleBox setup."""

import os
import sys
import subprocess
from distutils.sysconfig import get_python_version

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def boost_build():
    """Installation for Boost library"""
    subprocess.run(
        "git submodule update --init --recursive submodules/boost",
        shell=True,
        check=True,
    )

    subprocess.run(
        "cd submodules/boost && ./bootstrap.sh"
        + " "
        + f"--with-python-version={get_python_version()}"
        + " "
        + f"--prefix={os.getenv('PWD')}/bubblebox/depends/boost && ./b2 install",
        shell=True,
        check=True,
    )


def boost_clean():
    """Clean boost source environment"""
    subprocess.run(
        "git submodule deinit -f submodules/boost",
        shell=True,
        check=True,
    )


def boost_install():
    """Install Boost library"""
    if os.path.exists(os.getenv("PWD") + "/bubblebox/depends/boost"):
        subprocess.run(
            "mkdir -pv build/lib/bubblebox/depends/boost/lib",
            shell=True,
            check=True,
        )

        subprocess.run(
            "cp bubblebox/depends/boost/lib/lib* build/lib/bubblebox/depends/boost/lib/.",
            shell=True,
            check=True,
        )
