"""Build and installation script for BubbleBox."""

# standard libraries
import re
import subprocess
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py

# custom build command
class BuildPyCommand(build_py):
    """Custom build command."""

    def run(self):
        build_py.run(self)
        subprocess.run("cd bubblebox/cbox/source && make", shell=True, check=True)
        subprocess.run(
            "cp bubblebox/cbox/lib/*.so build/lib/bubblebox/cbox/lib/.",
            shell=True,
            check=True,
        )


# get long description from README
with open("README.rst", mode="r") as readme:
    long_description = readme.read()

with open("bubblebox/__meta__.py", mode="r") as source:
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

# core dependancies
DEPENDENCIES = [
    "numpy==1.21",
    "h5py",
    "h5pickle",
    "pymorton",
    "scikit-image",
    "dask",
    "pyarrow",
    "joblib",
    "distributed",
    "tqdm",
    "zarr",
]

setup(
    name=metadata["__pkgname__"],
    version=metadata["__version__"],
    author=metadata["__authors__"],
    description=metadata["__description__"],
    license=metadata["__license__"],
    packages=find_packages(where="./"),
    package_dir={"": "./"},
    package_data={
        "": [
            "bubblebox/cbox/lib/create.so",
            "bubblebox/cbox/lib/utilities.so",
        ]
    },
    include_package_data=True,
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=DEPENDENCIES,
    cmdclass={"build_py": BuildPyCommand},
)
