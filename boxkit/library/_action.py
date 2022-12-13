"""Module with implementation of Action utility"""

import copy

from .. import library


class Action: # pylint: disable=too-many-arguments
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
        parallel_obj=None,
    ):
        """Initialize the  object and allocate the data.

        Parameters
        ----------
        target   : function/task operates on an parallel_obj ---> def target(parallel_obj, *args)
                   actual call passes obj_list ---> target(obj_list, *args)
        nthreads : number of nthreads (only relevant for parallel operations)
        monitor  : flag (True or False) to show progress bar for task
        backend  : 'serial', 'loky', 'dask'
        parallel_obj     : parallel_obj type
        """
        super().__init__()
        self.target = target
        self.nthreads = nthreads
        self.monitor = monitor
        self.backend = backend
        self.parallel_obj = parallel_obj
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

        obj_list, args = Action.toparg(*args)
        self._chk_obj_list(obj_list)

        return library.exectask(self, obj_list, *args, **kwargs)

    def _chk_obj_list(self, obj_list):
        """Check if obj_list matches the parallel_obj type"""

        if not isinstance(obj_list, list):
            raise ValueError(
                "[boxkit.library.Action] Top argument must be a list of parallel_objs"
            )

        for parallel_obj in obj_list:
            if not isinstance(parallel_obj, self.parallel_obj):
                raise ValueError(
                    "[boxkit.library.Action] Unit type not consistent."
                    + f'Expected "{self.parallel_obj}" but got "{type(parallel_obj)}"'
                )
