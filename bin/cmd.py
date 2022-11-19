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


def _create_envfile():
    """
    Create environment file
    """
    with open("boxkit/envfile", "w") as envfile:

        for env_var in [
            "CBOX_BACKEND",
            "BBOX_PYARROW",
            "BBOX_ZARR",
            "BBOX_DASK",
        ]:
            if os.getenv(env_var) == "TRUE":
                envfile.write(f'{env_var} = "TRUE"\n')

            else:
                envfile.write(f'{env_var} = "FALSE"\n')


# custom build command
# replaces the default build command for setup.py
class BuildCmd(build_py):
    """Custom build_py command."""

    def run(self):

        build_py.run(self)

        if os.getenv("CBOX_BACKEND") == "TRUE":
            cbox_build()
            cbox_install()
            boost_install()

        _create_envfile()

        subprocess.run(
            "cp boxkit/envfile build/lib/boxkit/.",
            shell=True,
            check=True,
        )


# custom develop command
# replaces custom develop command for setup.py
class DevelopCmd(develop):
    """Custom develop command."""

    def run(self):

        develop.run(self)

        if os.getenv("CBOX_BACKEND") == "TRUE":
            cbox_build()

        _create_envfile()
