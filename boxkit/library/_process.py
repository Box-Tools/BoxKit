"""Module with implementation of Process utility"""

import copy


class Process:
    """Default class for a Process."""

    type_ = "default"

    def __init__(self, target=None, stencils=None):
        """Initialize the  object and allocate the data.

        Parameters
        ----------
        target : target function
        tasks  : dictionary of tasks
        """
        super().__init__()
        self.target = target

        self.tasks = {}

        for module in stencils:
            self.tasks.update(module())

    def __call__(self, *args, **kwargs):
        """
        Call wrapper for process

        If target is None, define the target, else call the target
        """

        if self.target is None:
            self.target = args[0]
            retval = self

        else:
            retval = self.target(self, *args, **kwargs)

        return retval

    def clone(self):
        """
        Clone process
        """
        return copy.deepcopy(self)
