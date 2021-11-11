"""Module with implementation of Action utility"""

import copy
import cbox.lib.boost as cbox

from .. import utilities

class Action(object):
    """Default class for an action."""

    type_ = 'default'

    def __init__(self, target=None, nthreads=1, monitor=False, backend='serial', actions=None, unit=None):
        """Initialize the  object and allocate the data.

        Parameters
        ----------
        target   : function/task operates on an unit ---> def target(unit, *args)
                   actual call passes unitlist ---> target(unitlist, *args)
        nthreads : number of nthreads (only relevant for parallel operations)
        monitor  : flag (True or False) to show progress bar for task
        backend  : 'serial', 'loky', 'dask'
        actions  : dictionary of actions
        unit     : unit type
        """
        super().__init__()
        self.target   = target
        self.nthreads = nthreads
        self.monitor  = monitor
        self.backend  = backend
        self.actions  = actions
        self.unit     = unit
        self.batch    = 'auto'

    def __call__(self,*args):
        """Call wrapper"""

        if self.target is None:
            self.target = args[0]
            return self

        else: 
            return self.execute(*args)

    def copy(self):
        """Custom copy method"""

        return copy.copy(self)

    def toparg(self,*args):
        """Method to get top argument from *args"""

        top = args[0]

        args = list(args)
        args.pop(0)
        args = tuple(args)

        return top,args

    def execute(self,*args):
        """ Custom call signature """

        unitlist,args = self.toparg(*args)

        self._check_unitlist(unitlist)

        return utilities.exectask(self,unitlist,*args)

    def _check_unitlist(self,unitlist):
        """ Check if unitlist matches the unit type"""

        if(type(unitlist) is not list):
            raise ValueError('[bubblebox.utilities.Action] Top argument must be a list of units')

        for unit in unitlist:
            if(type(unit) is not self.unit): 
                raise ValueError('[bubblebox.utilities.Action] Unit type not consistent.' +
                                 'Expected "{}" but got "{}"'.format(self.unit,type(unit)))

