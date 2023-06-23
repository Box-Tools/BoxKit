"""Custom commands for BoxKit setup."""
import os
import sys
import subprocess
from setuptools.command.install import install
from setuptools.command.develop import develop

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import cbox_build from cbox
# module located in the 'bin' folder of the
# package directory
from cbox import cbox_build  # pylint: disable=wrong-import-position
from boost import boost_install  # pylint: disable=wrong-import-position

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
        """
        Initialize options
        """
        self.with_cbox = None  # pylint: disable=attribute-defined-outside-init
        self.with_pyarrow = None  # pylint: disable=attribute-defined-outside-init
        self.with_zarr = None  # pylint: disable=attribute-defined-outside-init
        self.with_dask = None  # pylint: disable=attribute-defined-outside-init
        self.with_server = None  # pylint: disable=attribute-defined-outside-init
        self.enable_testing = None  # pylint: disable=attribute-defined-outside-init

    def finalize_options(self):
        """
        Finalize options
        """
        for option in [
            "with_cbox",
            "with_pyarrow",
            "with_zarr",
            "with_dask",
            "with_server",
            "enable_testing",
        ]:
            if getattr(self, option) not in [None, 1]:
                raise ValueError(f"{option} is a flag")

    def run(self, user):
        """
        Run command
        """
        if user:
            with_user = "--user"
        else:
            with_user = ""

        if self.with_cbox:
            subprocess.run(
                f"{sys.executable} -m pip install -r requirements/cbox.txt {with_user}",
                shell=True,
                check=True,
                executable="/bin/bash",
            )

        if self.with_pyarrow:
            subprocess.run(
                f"{sys.executable} -m pip install -r requirements/pyarrow.txt {with_user}",
                shell=True,
                check=True,
                executable="/bin/bash",
            )

        if self.with_zarr:
            subprocess.run(
                f"{sys.executable} -m pip install -r requirements/zarr.txt {with_user}",
                shell=True,
                check=True,
                executable="/bin/bash",
            )

        if self.with_dask:
            subprocess.run(
                f"{sys.executable} -m pip install -r requirements/dask.txt {with_user}",
                shell=True,
                check=True,
                executable="/bin/bash",
            )

        if self.with_server:
            subprocess.run(
                f"{sys.executable} -m pip install -r requirements/server.txt {with_user}",
                shell=True,
                check=True,
                executable="/bin/bash",
            )

        if self.enable_testing:
            subprocess.run(
                f"{sys.executable} -m pip install -r requirements/testing.txt {with_user}",
                shell=True,
                check=True,
                executable="/bin/bash",
            )

        with open("boxkit/options.py", "w", encoding="ascii") as optfile:

            optfile.write(f"CBOX={self.with_cbox}\n")
            optfile.write(f"PYARROW={self.with_pyarrow}\n")
            optfile.write(f"ZARR={self.with_zarr}\n")
            optfile.write(f"DASK={self.with_dask}\n")
            optfile.write(f"SERVER={self.with_server}\n")
            optfile.write(f"TESTING={self.enable_testing}\n")


# replaces the default build command for setup.py
class InstallCmd(install, CustomCmd):
    """Custom build command."""

    user_options = install.user_options + CustomCmd.user_options

    def initialize_options(self):
        install.initialize_options(self)
        CustomCmd.initialize_options(self)

    def finalize_options(self):
        install.finalize_options(self)
        CustomCmd.finalize_options(self)

    def run(self):

        CustomCmd.run(self, self.user)

        if self.with_cbox:
            cbox_build()
            boost_install()

        install.run(self)


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
        CustomCmd.run(self, self.user)

        if self.with_cbox:
            cbox_build()
