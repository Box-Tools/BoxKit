"""Module with implementaion of Monitor class"""

from ...cbox.lib import boost as cbox


class Monitor(cbox.utilities.Monitor):
    """
    Dervied class of a Boost.Python.Class
    """

    def __init__(self, _type):
        """
        Initialize and create object
        """
        super().__init__(_type)

    def setlimit(self, iterlimit):
        """
        set max progress for monitor
        """
        self._setlimit(iterlimit)

    def update(self, msg="", progress=0):
        """
        update monitor
        """
        self._update(msg, progress)

    def gettype(self):
        """
        Get type
        """
        return self._gettype
