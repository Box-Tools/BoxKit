"""Module with implemenetation of Dataset class"""

from . import Block
from . import Data
from . import Action


class Dataset:
    """API class for storing Dataset info"""

    type_ = "default"

    def __init__(self, blocklist=[], data=None):
        """Constructor for Dataset

        Parameters
        ----------
        blocklist : list of block objects
        data      : Data object

        """
        super().__init__()
        self._map_blocklist(blocklist)
        self._map_data(data)

    def __repr__(self):
        """Return a representation of the object."""
        return (
            "Dataset:\n"
            + f" - type         : {type(self)}\n"
            + f" - file         : {self._data.inputfile}\n"
            + f" - keys         : {self._data.varlist}\n"
            + f" - dtype	: {list(self._data.dtype.values())}\n"
            + f" - bound(z-y-x) : [{self.zmin}, {self.zmax}] x "
            + f"[{self.ymin}, {self.ymax}] x "
            + f"[{self.xmin}, {self.xmax}]\n"
            + f" - shape(z-y-x) : {self.nzb} x {self.nyb} x {self.nxb}\n"
            + f" - guard(z-y-x) : {self.zguard} x {self.yguard} x {self.xguard}\n"
            + f" - nblocks      : {self.nblocks}\n"
            + f" - dtype        : {self._data.dtype}"
        )

    def __getitem__(self, varkey):
        """
        Get variable data
        """
        return self._data[varkey]

    def __setitem__(self, varkey, value):
        """
        Set variable data
        """
        self._data[varkey] = value

    def _map_blocklist(self, blocklist):
        """
        Private method for initialization
        """
        self.blocklist = []
        self.xmin, self.ymin, self.zmin = [1e10] * 3
        self.xmax, self.ymax, self.zmax = [-1e10] * 3

        if not blocklist:
            return

        self.blocklist = blocklist

        for block in self.blocklist:
            self.xmin = min(self.xmin, block.xmin)
            self.ymin = min(self.ymin, block.ymin)
            self.zmin = min(self.zmin, block.zmin)

            self.xmax = max(self.xmax, block.xmax)
            self.ymax = max(self.ymax, block.ymax)
            self.zmax = max(self.zmax, block.zmax)

    def _map_data(self, data):
        """
        Private method for initialization
        """
        self._data = None

        if not data:
            return

        self._data = data

    @property
    def nblocks(self):
        return self._data.nblocks

    @property
    def nxb(self):
        return self._data.nxb

    @property
    def nyb(self):
        return self._data.nyb

    @property
    def nzb(self):
        return self._data.nzb

    @property
    def xguard(self):
        return self._data.xguard

    @property
    def yguard(self):
        return self._data.yguard

    @property
    def zguard(self):
        return self._data.zguard

    @property
    def varlist(self):
        return self._data.varlist

    @property
    def source(self):
        return self._data.source

    @property
    def dtype(self):
        return self._data.dtype

    def addvar(self, varkey, dtype=float):
        self._data.addvar(varkey, dtype)

    def delvar(self, varkey):
        self._data.delvar(varkey)

    def purge(self, purgeflag="all"):
        """
        Clean up the dataset and close it
        """
        self._data.purge(purgeflag)

    def halo_exchange(
        self, varlist, nthreads=1, batch="auto", backend="serial", monitor=False
    ):
        """
        Perform halo exchange
        """
        # Convert single string to a list
        if isinstance(varlist, str):
            varlist = [varlist]

        halo_exchange_block.nthreads = nthreads
        halo_exchange_block.batch = batch
        halo_exchange_block.backend = backend
        halo_exchange_block.monitor = monitor

        for varkey in varlist:
            halo_exchange_block(self.blocklist, varkey)


@Action(parallel_obj=Block)
def halo_exchange_block(parallel_obj, varkey):
    """
    Halo exchange
    """
    parallel_obj.exchange_neighdata(varkey)
