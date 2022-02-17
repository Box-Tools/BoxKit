"""Module with implementation of the Data class."""

import os
import string
import random
import shutil

import numpy
import dask.array as dsarray
import pyarrow
import zarr

import cbox.lib.boost as cbox


class Data(cbox.create.Data):
    """Default class to store data"""

    type_ = "default"

    def __init__(self, **attributes):
        """Initialize the class object

        Parameters
        ----------
        attributes : dictionary
                     { 'nblocks'   : total number of blocks,
                       'nxb'       : number of grid points per block in x dir,
                       'nyb'       : number of grid points per block in y dir,
                       'nzb'       : number of grid points per block in z dir,
                       'xguard'    : number of guard cells in x dir,
                       'yguard'    : number of guard cells in y dir,
                       'zguard'    : number of guard cells in z dir,
                       'inputfile' : hdf5 inputfile default (None),
                       'variables' : dictionary of variables default ({})
                       'storage'   : 'numpy', 'zarr', 'dask', 'pyarrow' }

        """
        super().__init__()
        self._set_attributes(attributes)
        self._set_data()

    def __repr__(self):
        """
        Return a representation of the object
        """
        return (
            "Data:\n"
            + " - type   : {}\n".format(type(self))
            + " - keys   : {}\n".format(self.varlist)
        )

    def __getitem__(self, varkey):
        """
        Get variable data
        """
        return self.variables[varkey]

    def __setitem__(self, varkey, value):
        """
        Set variable data
        """
        self.variables[varkey] = value

    def _set_attributes(self, attributes):
        """
        Private method for intialization
        """

        default_attributes = {
            "nblocks": 1,
            "inputfile": None,
            "boxmem": None,
            "variables": {},
            "nxb": 1,
            "nyb": 1,
            "nzb": 1,
            "xguard": 0,
            "yguard": 0,
            "zguard": 0,
            "storage": "numpy-memmap",
        }

        for key in attributes:
            if key in default_attributes:
                default_attributes[key] = attributes[key]
            else:
                raise ValueError(
                    "[bubblebox.library.create.Data] "
                    + 'Attribute "{}" not present in class Data'.format(key)
                )

        for key, value in default_attributes.items():
            setattr(self, key, value)

    def _set_data(self):
        """
        Private method for setting new data
        """
        self.varlist = list(self.variables.keys())

        if self.storage == "numpy":
            self._create_numpy_arrays()
        elif self.storage == "numpy-memmap":
            self._create_numpy_memmap()
        elif self.storage == "zarr":
            self._create_zarr_objects()
        elif self.storage == "dask":
            self._create_numpy_memmap()
            self._create_dask_objects()
        else:
            raise NotImplementedError(
                "[bubblebox.library.create.Data] "
                + 'Storage format "{}" not implemented'.format(self.storage)
            )

    def _create_numpy_memmap(self):
        """
        Create numpy memory maps for empty keys in variables dictionary
        """
        emptykeys = [
            key for key, value in self.variables.items() if type(value) is type(None)
        ]
        if not emptykeys:
            return

        if not self.boxmem:
            namerandom = "".join(
                random.choice(string.ascii_lowercase) for i in range(5)
            )
            self.boxmem = "".join(["./boxmem_", namerandom])
        try:
            os.mkdir(self.boxmem)
        except FileExistsError:
            pass

        for varkey in emptykeys:
            outputfile = os.path.join(self.boxmem, varkey)
            outputshape = (
                self.nblocks,
                self.nzb + 2 * self.zguard,
                self.nyb + 2 * self.yguard,
                self.nxb + 2 * self.xguard,
            )
            self.variables[varkey] = numpy.memmap(
                outputfile, dtype=float, shape=outputshape, mode="w+"
            )

    def _create_zarr_objects(self):
        """
        Create zarr objects
        """
        emptykeys = [
            key for key, value in self.variables.items() if type(value) is type(None)
        ]
        if not emptykeys:
            return

        if not self.boxmem:
            namerandom = "".join(
                random.choice(string.ascii_lowercase) for i in range(5)
            )
            self.boxmem = "".join(["./boxmem_", namerandom])
        try:
            os.mkdir(self.boxmem)
        except FileExistsError:
            pass

        for varkey in emptykeys:
            outputfile = os.path.join(self.boxmem, varkey)
            outputshape = (
                self.nblocks,
                self.nzb + 2 * self.zguard,
                self.nyb + 2 * self.yguard,
                self.nxb + 2 * self.xguard,
            )
            self.variables[varkey] = zarr.open(
                outputfile,
                mode="w",
                shape=outputshape,
                chunks=(
                    1,
                    self.nzb + 2 * self.zguard,
                    self.nyb + 2 * self.yguard,
                    self.nxb + 2 * self.xguard,
                ),
                dtype=float,
            )

    def _create_numpy_arrays(self):
        """
        Create numpy arrays for empty keys in variables dictionary
        """
        emptykeys = [
            key for key, value in self.variables.items() if type(value) is type(None)
        ]
        if not emptykeys:
            return

        for varkey in emptykeys:
            outputshape = (
                self.nblocks,
                self.nzb + 2 * self.zguard,
                self.nyb + 2 * self.yguard,
                self.nxb + 2 * self.xguard,
            )
            self.variables[varkey] = numpy.ndarray(dtype=float, shape=outputshape)

    def _create_dask_objects(self):
        """
        Create dask array representation of data
        """
        emptykeys = [
            key for key, value in self.variables.items() if type(value) is type(None)
        ]
        if not emptykeys:
            return

        for varkey in emptykeys:
            if type(self.variables[varkey]) is not dsarray.core.Array:
                self.variables[varkey] = dsarray.from_array(
                    self.variables[varkey],
                    chunks=(
                        1,
                        self.nzb + 2 * self.zguard,
                        self.nyb + 2 * self.yguard,
                        self.nxb + 2 * self.xguard,
                    ),
                )

    def _create_pyarrow_objects(self):
        """
        Create a pyarrow tensor objects
        """
        emptykeys = [
            key for key, value in self.variables.items() if type(value) is type(None)
        ]
        if not emptykeys:
            return

        for varkey in emptykeys:
            if type(self.variables[varkey]) is not pyarrow.lib.Tensor:
                templist = []
                for lblock in range(self.nblocks):
                    templist.append(
                        pyarrow.Tensor.from_numpy(self.variables[varkey][lblock])
                    )
                self.variables[varkey] = templist

    def purge(self, purgeflag="all"):
        """
        Clean up data and close it
        """
        if self.boxmem and (purgeflag == "all" or purgeflag == "boxmem"):
            try:
                shutil.rmtree(self.boxmem)
            except:
                pass

        if self.inputfile and (purgeflag == "all" or purgeflag == "inputfile"):
            self.inputfile.close()

    def addvar(self, varkey):
        """
        Add a variables to data
        """
        self.variables[varkey] = None
        self._set_data()

    def delvar(self, varkey):
        """
        Delete a variable
        """
        del self.variables[varkey]

        if self.boxmem:
            outputfile = os.path.join(self.boxmem, varkey)
            try:
                shutil.rmtree(outputfile)
            except:
                pass

        self.varlist = list(self.variables.keys())
