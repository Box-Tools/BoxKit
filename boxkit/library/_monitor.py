"""Module with implementaion of Monitor class"""

from progress.bar import Bar, ChargingBar

from .. import options

if options.cbox:
    from ..cbox.lib import boost as cbox


class Monitor:
    """
    Dervied class of a Boost.Python.Class
    """

    def __init__(self, msg="", iters=1):
        """
        Initialize and create object
        """
        if options.cbox:
            self._bar = cbox.library.Monitor("action")
            self._bar._setlimit(iters)
            self.msg = msg

        else:
            self._bar = ChargingBar(msg, max=iters)

    def update(self):
        """
        update monitor
        """
        if options.cbox:
            self._bar._update(self.msg, 0)
        else:
            self._bar.next()

    def finish(self):
        """
        finish
        """
        if not options.cbox:
            self._bar.finish()
