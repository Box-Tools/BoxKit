"""Custom commands for BoxKit setup."""
import os
import sys
import subprocess
from setuptools.command.build import build
from setuptools.command.develop import develop

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import cbox_build, and cbox_install from cbox
# module located in the 'bin' folder of the
# package directory
from cbox import cbox_build, cbox_install
from boost import boost_install

# custom command
class CustomCmd:
    """Custom command."""

    user_options = [
        ("with-cbox", None, "With C++ backend"),
        ("with-pyarrow", None, "With pyarrow data backend"),
        ("with-zarr", None, "With zarr data backend"),
        ("with-dask", None, "With dask data/parallel backend"),
        ("with-server", None, "With remote server utilitiy"),
        ("enable-testing", None, "Enable testing mode"),
    ]

    def initialize_options(self):
        self.with_cbox = 0
        self.with_pyarrow = 0
        self.with_zarr = 0
        self.with_dask = 0
        self.with_server = 0
        self.enable_testing = 0

    def finalize_options(self):
        pass

    def run(self):

        with open("boxkit/options.py", "w") as optfile:

            optfile.write(f"cbox={self.with_cbox}\n")
            optfile.write(f"pyarrow={self.with_pyarrow}\n")
            optfile.write(f"zarr={self.with_zarr}\n")
            optfile.write(f"dask={self.with_dask}\n")
            optfile.write(f"server={self.with_server}\n")
            optfile.write(f"testing={self.enable_testing}\n")


# replaces the default build command for setup.py
class BuildCmd(build, CustomCmd):
    """Custom build command."""

    user_options = build.user_options + CustomCmd.user_options

    def initialize_options(self):
        build.initialize_options(self)
        CustomCmd.initialize_options(self)

    def finalize_options(self):
        build.finalize_options(self)
        CustomCmd.finalize_options(self)

    def run(self):

        build.run(self)

        if self.with_cbox:
            cbox_build()
            cbox_install()
            boost_install()

        CustomCmd.run(self)

        subprocess.run(
            "cp boxkit/options.py build/lib/boxkit/.",
            shell=True,
            check=True,
            executable="/bin/bash",
        )


# replaces custom develop command for setup.py
class DevelopCmd(develop, CustomCmd):
    """Custom develop command."""

    user_options = develop.user_options + CustomCmd.user_options

    def initialize_options(self):
        develop.initialize_options(self)
        CustomCmd.initialize_options(self)

    def finalize_options(self):
        develop.finalize_options(self)
        CustomCmd.finalize_options(self)

    def run(self):

        develop.run(self)

        if self.with_cbox:
            cbox_build()

        CustomCmd.run(self)
