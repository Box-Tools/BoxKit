"""Module with implementation of Action utility"""
from types import GeneratorType
import copy

from boxkit import library  # pylint: disable=cyclic-import


class Action:  # pylint: disable=too-many-arguments
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

        toparg, args = Action.toparg(*args)

        if not isinstance(toparg, GeneratorType) and not isinstance(toparg, list):
            raise ValueError(
                "[boxkit.library.Action] First argument "
                + f"must be {GeneratorType!r} or {list!r} not {type(toparg)!r}"
            )

        obj_list = list(toparg)
        del toparg
        self.__class__.chk_obj_list(obj_list)

        return library.exectask(self, obj_list, *args, **kwargs)

    @staticmethod
    def chk_obj_list(obj_list):
        """Check if obj_list matches the parallel_obj type"""

        first_obj = obj_list[0]
        for index, parallel_obj in enumerate(obj_list):
            if not isinstance(parallel_obj, type(first_obj)):
                raise ValueError(
                    "[boxkit.library.Action] Inconsistent type "
                    + f"{type(parallel_obj)} vs {type(first_obj)} at index "
                    + f'"{index}" in parallel object list'
                )
