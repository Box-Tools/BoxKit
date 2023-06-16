"""Module with implemenetation of Dataset class"""

from boxkit.library import Block  # pylint: disable=cyclic-import
from boxkit.library import Data  # pylint: disable=cyclic-import
from boxkit.library import Action  # pylint: disable=cyclic-import


class Dataset:  # pylint: disable=too-many-instance-attributes
    """API class for storing Dataset info"""

    type_ = "default"

    def __init__(self, blocklist, data):
        """Constructor for Dataset

        Parameters
        ----------
        blocklist : list of block objects
        data      : Data object

        """
        super().__init__()

        self.blocklist = []
        self.xmin, self.ymin, self.zmin = [1e10] * 3
        self.xmax, self.ymax, self.zmax = [-1e10] * 3
        self._data = None

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
        if not data:
            return

        self._data = data

    @property
    def nblocks(self):
        """nblocks"""
        return self._data.nblocks

    @property
    def nxb(self):
        """nxb"""
        return self._data.nxb

    @property
    def nyb(self):
        """nyb"""
        return self._data.nyb

    @property
    def nzb(self):
        """nzb"""
        return self._data.nzb

    @property
    def xguard(self):
        """xguard"""
        return self._data.xguard

    @property
    def yguard(self):
        """yguard"""
        return self._data.yguard

    @property
    def zguard(self):
        """zguard"""
        return self._data.zguard

    @property
    def varlist(self):
        """varlist"""
        return self._data.varlist

    @property
    def source(self):
        """source"""
        return self._data.source

    @property
    def dtype(self):
        """dtype"""
        return self._data.dtype

    def addvar(self, varkey, dtype=float):
        """addvar"""
        self._data.addvar(varkey, dtype)

    def delvar(self, varkey):
        """delvar"""
        self._data.delvar(varkey)

    def purge(self, purgeflag="all"):
        """
        Clean up the dataset and close it
        """
        self._data.purge(purgeflag)

    def clone(self, storage="numpy-memmap"):
        """
        Clone dataset
        """
        # Create data attributes
        data_attributes = {
            "nblocks": int(self.nblocks),
            "nxb": int(self.nxb),
            "nyb": int(self.nyb),
            "nzb": int(self.nzb),
            "storage": storage,
        }

        data = Data(**data_attributes)

        # Create block attributes
        block_attributes = [
            {
                "dx": block.dx,
                "dy": block.dy,
                "dz": block.dz,
                "xmin": block.xmin,
                "ymin": block.ymin,
                "zmin": block.zmin,
                "xmax": block.xmax,
                "ymax": block.ymax,
                "zmax": block.zmax,
                "tag": block.tag,
                "leaf": block.leaf,
                "level": block.level,
            }
            for block in self.blocklist
        ]

        blocklist = [Block(data, **attributes) for attributes in block_attributes]

        return self.__class__(blocklist, data)

    def halo_exchange(  # pylint: disable=too-many-arguments
        self,
        varlist,
        nthreads=1,
        batch="auto",
        backend="serial",
        monitor=False,
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
            halo_exchange_block((block for block in self.blocklist), varkey)


@Action
def halo_exchange_block(block, varkey):
    """
    Halo exchange
    """
    block.exchange_neighdata(varkey)
