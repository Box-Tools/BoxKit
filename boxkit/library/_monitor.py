"""Module with implementaion of Monitor class"""

from progress.bar import Bar, ChargingBar  # pylint: disable=unused-import

from boxkit import options

if options.CBOX:
    from ..cbox.lib import boost as cbox  # pylint: disable=c-extension-no-member


class Monitor:
    """
    Dervied class of a Boost.Python.Class
    """

    def __init__(self, msg="", iters=1):
        """
        Initialize and create object
        """
        if options.CBOX:
            self._bar = cbox.library.Monitor(  # pylint: disable=c-extension-no-member
                "action"
            )
            self._bar._setlimit(iters)
            self.msg = msg

        else:
            self._bar = ChargingBar(msg, max=iters)

    def update(self):
        """
        update monitor
        """
        if options.CBOX:
            self._bar._update(self.msg, 0)  # pylint: disable=protected-access
        else:
            self._bar.next()

    def finish(self):
        """
        finish
        """
        if not options.CBOX:
            self._bar.finish()
