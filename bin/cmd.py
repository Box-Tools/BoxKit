"""Custom commands for BoxKit setup."""
import os
import sys
import subprocess
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import cbox_build, and cbox_install from cbox
# module located in the 'bin' folder of the
# package directory
from cbox import cbox_build, cbox_install
from boost import boost_install


def _set_options(
    with_cbox=0,
    with_pyarrow=0,
    with_zarr=0,
    with_dask=0,
    with_server=0,
    enable_testing=0,
):
    """
    Create environment file
    """
    with open("boxkit/options.py", "w") as optfile:

        optfile.write(f"cbox={with_cbox}\n")
        optfile.write(f"pyarrow={with_pyarrow}\n")
        optfile.write(f"zarr={with_zarr}\n")
        optfile.write(f"dask={with_dask}\n")
        optfile.write(f"server={with_server}\n")
        optfile.write(f"testing={enable_testing}\n")


# custom build command
# replaces the default build command for setup.py
class BuildCmd(build_py):
    """Custom build_py command."""

    user_options = build_py.user_options + [
        ("with-cbox", None, "With C++ backend"),
        ("with-pyarrow", None, "With pyarrow data backend"),
        ("with-zarr", None, "With zarr data backend"),
        ("with-dask", None, "With dask data/parallel backend"),
        ("with-server", None, "With remote server utilitiy"),
        ("enable-testing", None, "Enable testing mode"),
    ]

    def initialize_options(self):
        build_py.initialize_options(self)
        self.with_cbox = 0
        self.with_pyarrow = 0
        self.with_zarr = 0
        self.with_dask = 0
        self.with_server = 0
        self.enable_testing = 0

    def finalize_options(self):
        build_py.finalize_options(self)

    def run(self):

        build_py.run(self)

        if self.with_cbox:
            cbox_build()
            cbox_install()
            boost_install()

        _set_options(
            self.with_cbox,
            self.with_pyarrow,
            self.with_zarr,
            self.with_dask,
            self.with_server,
            self.enable_testing,
        )

        subprocess.run(
            "cp boxkit/options.py build/lib/boxkit/.",
            shell=True,
            check=True,
            executable="/bin/bash",
        )


# custom develop command
# replaces custom develop command for setup.py
class DevelopCmd(develop):
    """Custom develop command."""

    user_options = develop.user_options + [
        ("with-cbox", None, "With C++ backend"),
        ("with-pyarrow", None, "With pyarrow data backend"),
        ("with-zarr", None, "With zarr data backend"),
        ("with-dask", None, "With dask data/parallel backend"),
        ("with-server", None, "With remote server utilitiy"),
        ("enable-testing", None, "Enable testing mode"),
    ]

    def initialize_options(self):
        develop.initialize_options(self)
        self.with_cbox = 0
        self.with_pyarrow = 0
        self.with_zarr = 0
        self.with_dask = 0
        self.with_server = 0
        self.enable_testing = 0

    def finalize_options(self):
        develop.finalize_options(self)

    def run(self):

        develop.run(self)

        if self.with_cbox:
            cbox_build()

        _set_options(
            self.with_cbox,
            self.with_pyarrow,
            self.with_zarr,
            self.with_dask,
            self.with_server,
            self.enable_testing,
        )
