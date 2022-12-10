"""Module with implementation of the Data class."""

import os
import string
import random
import shutil

import numpy

from .. import options

if options.dask:
    import dask.array as dsarray

if options.pyarrow:
    import pyarrow

if options.zarr:
    import zarr

if options.cbox:
    from ..cbox.lib import boost as cbox

    _DataBase = cbox.library.Data

else:
    _DataBase = object


class Data(_DataBase):
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
                       'remotefile': sftp remote file default (None),
                       'variables' : dictionary of variables default ({}),
                       'storage'   : ('numpy', 'zarr', 'dask', 'pyarrow')}
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
            + f" - type   : {type(self)}\n"
            + f" - keys   : {self.varlist}\n"
            + f" - dtype  : {list(self.dtype.values())}\n"
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

        self.nblocks = 1
        self.inputfile = None
        self.remotefile = None
        self.boxmem = None
        self.variables = {}
        self.nxb, self.nyb, self.nzb = [1, 1, 1]
        self.xguard, self.yguard, self.zguard = [0, 0, 0]
        self.storage = "numpy-memmap"
        self.dtype = {}
        self.varlist = []
        self.source = ""

        for key, value in attributes.items():
            if hasattr(self, key):
                if (type(getattr(self, key)) != type(value)) and (
                    key not in ["inputfile", "remotefile"]
                ):
                    print(key, type(getattr(self, key)), type(value))
                    raise ValueError(
                        "[boxkit.library.create.Data] "
                        + f'Type mismatch for attribute "{key}" in class Data'
                    )

                setattr(self, key, value)

            else:
                raise ValueError(
                    "[boxkit.library.create.Data] "
                    + f'Attribute "{key}" not present in class Data'
                )

        for key, value in self.variables.items():
            self.varlist.append(key)
            if value != None:
                self.dtype[key] = type(value)
            else:
                self.dtype[key] = float

    def _set_data(self):
        """
        Private method for setting new data
        """
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
                "[boxkit.library.create.Data] "
                + f'Storage format "{self.storage}" not implemented'
            )

    def _create_numpy_memmap(self):
        """
        Create numpy memory maps for empty keys in variables dictionary
        """
        emptykeys = [
            key
            for key, value in self.variables.items()
            if isinstance(value, type(None))
        ]
        if not emptykeys:
            return

        if not self.boxmem:
            namerandom = "".join(
                random.choice(string.ascii_lowercase) for i in range(5)
            )
            self.boxmem = "".join(["./boxmem/", namerandom])
        try:
            os.makedirs(self.boxmem)
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
                outputfile, dtype=self.dtype[varkey], shape=outputshape, mode="w+"
            )

    def _create_zarr_objects(self):
        """
        Create zarr objects
        """

        if options.zarr:
            emptykeys = [
                key
                for key, value in self.variables.items()
                if isinstance(value, type(None))
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
                    dtype=self.dtype[varkey],
                )

        else:
            raise NotImplementedError(
                "[boxkit.library.data] enable zarr using --with-zarr during install"
            )

    def _create_numpy_arrays(self):
        """
        Create numpy arrays for empty keys in variables dictionary
        """
        emptykeys = [
            key
            for key, value in self.variables.items()
            if isinstance(value, type(None))
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
            self.variables[varkey] = numpy.ndarray(
                dtype=self.dtype[varkey], shape=outputshape
            )

    def _create_dask_objects(self):
        """
        Create dask array representation of data
        """
        if options.dask:
            emptykeys = [
                key
                for key, value in self.variables.items()
                if isinstance(value, type(None))
            ]
            if not emptykeys:
                return

            for varkey in emptykeys:
                if not isinstance(self.variables[varkey], dsarray.core.Array):
                    self.variables[varkey] = dsarray.from_array(
                        self.variables[varkey],
                        chunks=(
                            1,
                            self.nzb + 2 * self.zguard,
                            self.nyb + 2 * self.yguard,
                            self.nxb + 2 * self.xguard,
                        ),
                    )

        else:
            raise NotImplementedError(
                "[boxkit.library.data] enable dask using --with-dask during install"
            )

    def _create_pyarrow_objects(self):
        """
        Create a pyarrow tensor objects
        """
        if options.pyarrow:
            emptykeys = [
                key
                for key, value in self.variables.items()
                if isinstance(value, type(None))
            ]
            if not emptykeys:
                return

            for varkey in emptykeys:
                if not isinstance(self.variables[varkey], pyarrow.lib.Tensor):
                    templist = []
                    for lblock in range(self.nblocks):
                        templist.append(
                            pyarrow.Tensor.from_numpy(self.variables[varkey][lblock])
                        )
                    self.variables[varkey] = templist

        else:
            raise NotImplementedError(
                "[boxkit.library.data] enable pyarrow using --with-pyarrow during install"
            )

    def purge(self, purgeflag="all"):
        """
        Clean up data and close it
        """
        if self.boxmem and purgeflag in ("all", "boxmem"):
            try:
                shutil.rmtree(self.boxmem)
            except:
                pass

        if self.inputfile and purgeflag in ("all", "inputfile"):
            self.inputfile.close()

        if self.remotefile and purgeflag in ("all", "remotefile"):
            self.remotefile.close()

    def addvar(self, varkey, dtype=float):
        """
        Add a variables to data
        """
        if varkey in self.variables:
            raise ValueError(
                f"[boxkit.library.data] Variable {varkey!r} already present in dataset"
            )

        self.variables[varkey] = None
        self.dtype[varkey] = dtype if dtype in [float, int, bool] else float
        self.varlist.append(varkey)
        self._set_data()

    def delvar(self, varkey):
        """
        Delete a variable
        """
        del self.variables[varkey]
        del self.dtype[varkey]

        if self.boxmem:
            outputfile = os.path.join(self.boxmem, varkey)
            try:
                shutil.rmtree(outputfile)
            except:
                pass

        self.varlist = list(self.variables.keys())
