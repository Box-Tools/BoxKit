"""Build and installation script for BoxKit."""

# standard libraries
import os
import sys
import re
import platform
from setuptools import setup, find_packages

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import bin from current working directory
# sys.path.insert makes sure that current file path is searched
# first to find this module
import bin.cmd as bin_cmd  # pylint: disable=wrong-import-position

# Parse README and get long
# description
with open("README.rst", mode="r", encoding="ascii") as readme:
    long_description = readme.read()


# Open metadata file to extract package information
with open("boxkit/__meta__.py", mode="r", encoding="ascii") as source:
    content = source.read().strip()
    metadata = {
        key: re.search(key + r'\s*=\s*[\'"]([^\'"]*)[\'"]', content).group(1)
        for key in [
            "__pkgname__",
            "__version__",
            "__authors__",
            "__license__",
            "__description__",
        ]
    }

# core dependancies for the package
with open("requirements/core.txt", mode="r", encoding="ascii") as core_reqs:
    DEPENDENCIES = core_reqs.read()

# Call setup command with necessary arguments
# replace existing build and develop commands
# with custom commands defined in 'bin.cmd'
if platform.system() == "Windows":
    PACKAGE_DIR = ".\\"
else:
    PACKAGE_DIR = "./"

setup(
    name=metadata["__pkgname__"],
    version=metadata["__version__"],
    author=metadata["__authors__"],
    description=metadata["__description__"],
    license=metadata["__license__"],
    packages=find_packages(where=PACKAGE_DIR),
    package_dir={"": PACKAGE_DIR},
    package_data={
        "": [
            "options.py",
            "cbox/lib/library.so",
        ]
    },
    include_package_data=True,
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires=DEPENDENCIES,
    cmdclass={
        "develop": bin_cmd.DevelopCmd,
        "install": bin_cmd.InstallCmd,
    },
)
