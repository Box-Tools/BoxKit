"""Module with implementation of Action utility"""

import copy

from .. import library


class Action:
    """Default class for an action."""

    type_ = "default"

    @staticmethod
    def toparg(*args):
        """Method to get top argument from *args"""

        top = args[0]

        args = list(args)
        args.pop(0)
        args = tuple(args)

        return top, args

    def __init__(
        self,
        target=None,
        nthreads=1,
        monitor=False,
        backend="serial",
        unit=None,
    ):
        """Initialize the  object and allocate the data.

        Parameters
        ----------
        target   : function/task operates on an unit ---> def target(unit, *args)
                   actual call passes unitlist ---> target(unitlist, *args)
        nthreads : number of nthreads (only relevant for parallel operations)
        monitor  : flag (True or False) to show progress bar for task
        backend  : 'serial', 'loky', 'dask'
        unit     : unit type
        """
        super().__init__()
        self.target = target
        self.nthreads = nthreads
        self.monitor = monitor
        self.backend = backend
        self.unit = unit
        self.batch = "auto"

    def __call__(self, *args, **kwargs):
        """Call wrapper"""

        if self.target is None:
            self.target = args[0]
            retval = self

        else:
            retval = self.execute(*args, **kwargs)

        return retval

    def copy(self):
        """Custom copy method"""

        return copy.copy(self)

    def execute(self, *args, **kwargs):
        """Custom call signature"""

        unitlist, args = Action.toparg(*args)

        self._check_unitlist(unitlist)

        return library.Exectask(self, unitlist, *args, **kwargs)

    def _check_unitlist(self, unitlist):
        """Check if unitlist matches the unit type"""

        if not isinstance(unitlist, list):
            raise ValueError(
                "[boxkit.library.Action] Top argument must be a list of units"
            )

        for unit in unitlist:
            if not isinstance(unit, self.unit):
                raise ValueError(
                    "[boxkit.library.Action] Unit type not consistent."
                    + f'Expected "{self.unit}" but got "{type(unit)}"'
                )
