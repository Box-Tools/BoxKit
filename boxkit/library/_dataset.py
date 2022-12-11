"""Module with implemenetation of Dataset class"""

from . import Block
from . import Data
from . import Action

# DEVNOTE: The main class is separated from
# some initialization methods to investigate
# cache optimization during pickling. A call
# to these methods from parallel environment
# can result in some bottlenecks. If and when
# a need arises to use some of these methods
# in the future, then they should be assigned
# to the class object

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
        map_blocklist(self, blocklist)
        map_data(self, data)

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

        halo_exchange_blk.nthreads = nthreads
        halo_exchange_blk.batch = batch
        halo_exchange_blk.backend = backend
        halo_exchange_blk.monitor = monitor

        for varkey in varlist:
            halo_exchange_blk(self.blocklist, varkey)


@Action(unit=Block)
def halo_exchange_blk(unit, varkey):
    """
    Halo exchange
    """
    unit.exchange_neighdata(varkey)


def map_blocklist(dataset, blocklist):
    """
    Private method for initialization
    """
    dataset.blocklist = []
    dataset.xmin, dataset.ymin, dataset.zmin = [1e10] * 3
    dataset.xmax, dataset.ymax, dataset.zmax = [-1e10] * 3

    if not blocklist:
        return

    dataset.blocklist = blocklist

    for block in dataset.blocklist:
        dataset.xmin = min(dataset.xmin, block.xmin)
        dataset.ymin = min(dataset.ymin, block.ymin)
        dataset.zmin = min(dataset.zmin, block.zmin)

        dataset.xmax = max(dataset.xmax, block.xmax)
        dataset.ymax = max(dataset.ymax, block.ymax)
        dataset.zmax = max(dataset.zmax, block.zmax)


def map_data(dataset, data):
    """
    Private method for initialization
    """
    dataset._data = None

    if not data:
        return

    dataset._data = data
