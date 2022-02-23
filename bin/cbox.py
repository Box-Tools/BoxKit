"""Custom commands for BubbleBox setup."""

import os
import sys
import subprocess
from distutils.sysconfig import get_python_version, BASE_PREFIX

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Custom variables
CBOX_MAKE_DICT = {
    "python_version": get_python_version(),
    "python_path": BASE_PREFIX,
    "boost_version": "".join(get_python_version().split(".")),
    "boost_path": (
        os.getenv("PWD") + "/bubblebox/depends/boost"
        if os.path.exists(os.getenv("PWD") + "/bubblebox/depends/boost")
        else BASE_PREFIX
    ),
}


print(CBOX_MAKE_DICT["boost_path"])

CBOX_MAKE_ARGS = ""

for key, value in CBOX_MAKE_DICT.items():
    CBOX_MAKE_ARGS = CBOX_MAKE_ARGS + " " + f"{key}={value}"

# cbox install command
def cbox_install():
    """installation for cbox"""
    subprocess.run(
        f"cd bubblebox/cbox/source && make {CBOX_MAKE_ARGS}",
        shell=True,
        check=True,
    )
