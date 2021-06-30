"""Module with implementation of Parallel class"""

import joblib

class Parallel(object):
    """Default class for a Parallel object """

    type_ = 'default'
 
    def __init__(self,nparallel=1):
        """
        Initialize the object

        Parameters
        ----------
        nparallel : number of parallel jobs
        """
        self.nparallel = nparallel

    def __repr__(self):
        """
        Return a representation of the object
        """
        return ("Parallel:\n" +
                " - type      : {}\n".format(type(self)) +
                " - nparallel : {}\n".format(self.nparallel))


    def map(self,target,blocklist,*args):
        """
        Map and run a method in parallel

        Parameters
        ----------
        target    : function to map

        blocklist : list of blocks to run in parallel

        *args     : addtional arguments to the target 

        """
        result = joblib.Parallel(n_jobs=self.nparallel)(        
                     joblib.delayed(target)(block,*args) for block in blocklist)

        return result
