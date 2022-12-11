"""Module with implementaion of Monitor class"""

from progress.bar import Bar, ChargingBar

from .. import options

if options.cbox:
    from ..cbox.lib import boost as cbox


class Monitor:
    """
    Dervied class of a Boost.Python.Class
    """

    def __init__(self, msg_="", iter_=1, type_="test"):
        """
        Initialize and create object
        """
        if options.cbox:
            self._bar = cbox.library.Monitor(type_)
            self._bar._setlimit(iter_)
            self.msg = msg_

        else:
            if type_ == "test":
                self._bar = Bar(msg_, max=iter_)

            elif type_ == "action":
                self._bar = ChargingBar(msg_, max=iter_)

            else:
                raise NotImplementedError

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
