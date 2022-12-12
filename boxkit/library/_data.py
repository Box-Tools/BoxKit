"""Module with implementation of the Data class."""

import os
import string
import random
import shutil

import h5pickle
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
        set_attributes(self, attributes)
        set_data(self)

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
        set_data(self)

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


def set_attributes(data, attributes):
    """
    Private method for intialization
    """

    data.nblocks = 1
    data.inputfile = None
    data.remotefile = None
    data.boxmem = None
    data.variables = {}
    data.nxb, data.nyb, data.nzb = [1, 1, 1]
    data.xguard, data.yguard, data.zguard = [0, 0, 0]
    data.storage = "numpy-memmap"
    data.dtype = {}
    data.varlist = []
    data.source = ""

    for key, value in attributes.items():
        if hasattr(data, key):
            if (type(getattr(data, key)) != type(value)) and (
                key not in ["inputfile", "remotefile"]
            ):
                print(key, type(getattr(data, key)), type(value))
                raise ValueError(
                    "[boxkit.library.create.Data] "
                    + f'Type mismatch for attribute "{key}" in class Data'
                )

            setattr(data, key, value)

        else:
            raise ValueError(
                "[boxkit.library.create.Data] "
                + f'Attribute "{key}" not present in class Data'
            )

    for key, value in data.variables.items():
        data.varlist.append(key)
        if value != None:
            data.dtype[key] = type(value)
        else:
            data.dtype[key] = float


def set_data(data):
    """
    Private method for setting new data
    """
    if data.storage == "numpy":
        create_numpy_arrays(data)
    elif data.storage == "numpy-memmap":
        create_numpy_memmap(data)
    elif data.storage == "h5-datasets":
        create_h5_datasets(data)
    elif data.storage == "zarr":
        create_zarr_objects(data)
    elif data.storage == "dask":
        create_numpy_memmap(data)
        create_dask_objects(data)
    else:
        raise NotImplementedError(
            "[boxkit.library.create.Data] "
            + f'Storage format "{data.storage}" not implemented'
        )


def create_h5_datasets(data):
    """
    Create h5 datasets for empty keys in variables dictionary
    """
    emptykeys = [
        key for key, value in data.variables.items() if isinstance(value, type(None))
    ]
    if not emptykeys:
        return

    if not data.boxmem:
        namerandom = "".join(random.choice(string.ascii_lowercase) for i in range(5))
        data.boxmem = "".join(["./boxmem/", namerandom])
    try:
        os.makedirs(data.boxmem)
    except FileExistsError:
        pass

    for varkey in emptykeys:
        outputfile = h5pickle.File(os.path.join(data.boxmem, varkey), "w")

        outputshape = [
            data.nblocks,
            data.nzb + 2 * data.zguard,
            data.nyb + 2 * data.yguard,
            data.nxb + 2 * data.xguard,
        ]

        outputfile.create_dataset(
            varkey, data=numpy.zeros(outputshape, dtype=data.dtype[varkey])
        )
        outputfile.close()

        data.variables[varkey] = h5pickle.File(
            os.path.join(data.boxmem, varkey), "r+", skip_cache=False
        )[varkey]


def create_numpy_memmap(data):
    """
    Create numpy memory maps for empty keys in variables dictionary
    """
    emptykeys = [
        key for key, value in data.variables.items() if isinstance(value, type(None))
    ]
    if not emptykeys:
        return

    if not data.boxmem:
        namerandom = "".join(random.choice(string.ascii_lowercase) for i in range(5))
        data.boxmem = "".join(["./boxmem/", namerandom])
    try:
        os.makedirs(data.boxmem)
    except FileExistsError:
        pass

    for varkey in emptykeys:
        outputfile = os.path.join(data.boxmem, varkey)
        outputshape = (
            data.nblocks,
            data.nzb + 2 * data.zguard,
            data.nyb + 2 * data.yguard,
            data.nxb + 2 * data.xguard,
        )
        data.variables[varkey] = numpy.memmap(
            outputfile, dtype=data.dtype[varkey], shape=outputshape, mode="w+"
        )


def create_zarr_objects(data):
    """
    Create zarr objects
    """

    if options.zarr:
        emptykeys = [
            key
            for key, value in data.variables.items()
            if isinstance(value, type(None))
        ]
        if not emptykeys:
            return

        if not data.boxmem:
            namerandom = "".join(
                random.choice(string.ascii_lowercase) for i in range(5)
            )
            data.boxmem = "".join(["./boxmem_", namerandom])
        try:
            os.mkdir(data.boxmem)
        except FileExistsError:
            pass

        for varkey in emptykeys:
            outputfile = os.path.join(data.boxmem, varkey)
            outputshape = (
                data.nblocks,
                data.nzb + 2 * data.zguard,
                data.nyb + 2 * data.yguard,
                data.nxb + 2 * data.xguard,
            )
            data.variables[varkey] = zarr.open(
                outputfile,
                mode="w",
                shape=outputshape,
                chunks=(
                    1,
                    data.nzb + 2 * data.zguard,
                    data.nyb + 2 * data.yguard,
                    data.nxb + 2 * data.xguard,
                ),
                dtype=data.dtype[varkey],
            )

    else:
        raise NotImplementedError(
            "[boxkit.library.data] enable zarr using --with-zarr during install"
        )


def create_numpy_arrays(data):
    """
    Create numpy arrays for empty keys in variables dictionary
    """
    emptykeys = [
        key for key, value in data.variables.items() if isinstance(value, type(None))
    ]
    if not emptykeys:
        return

    for varkey in emptykeys:
        outputshape = (
            data.nblocks,
            data.nzb + 2 * data.zguard,
            data.nyb + 2 * data.yguard,
            data.nxb + 2 * data.xguard,
        )
        data.variables[varkey] = numpy.ndarray(
            dtype=data.dtype[varkey], shape=outputshape
        )


def create_dask_objects(data):
    """
    Create dask array representation of data
    """
    if options.dask:
        emptykeys = [
            key
            for key, value in data.variables.items()
            if isinstance(value, type(None))
        ]
        if not emptykeys:
            return

        for varkey in emptykeys:
            if not isinstance(data.variables[varkey], dsarray.core.Array):
                data.variables[varkey] = dsarray.from_array(
                    data.variables[varkey],
                    chunks=(
                        1,
                        data.nzb + 2 * data.zguard,
                        data.nyb + 2 * data.yguard,
                        data.nxb + 2 * data.xguard,
                    ),
                )

    else:
        raise NotImplementedError(
            "[boxkit.library.data] enable dask using --with-dask during install"
        )


def create_pyarrow_objects(data):
    """
    Create a pyarrow tensor objects
    """
    if options.pyarrow:
        emptykeys = [
            key
            for key, value in data.variables.items()
            if isinstance(value, type(None))
        ]
        if not emptykeys:
            return

        for varkey in emptykeys:
            if not isinstance(data.variables[varkey], pyarrow.lib.Tensor):
                templist = []
                for lblock in range(data.nblocks):
                    templist.append(
                        pyarrow.Tensor.from_numpy(data.variables[varkey][lblock])
                    )
                data.variables[varkey] = templist

    else:
        raise NotImplementedError(
            "[boxkit.library.data] enable pyarrow using --with-pyarrow during install"
        )
