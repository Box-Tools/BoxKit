"""Module with implementation of the Data class."""

import os
import string
import random
import shutil

import numpy
import dask.array as dsarray
import pyarrow

import cbox.lib.boost as cbox

class Data(cbox.create.Data):
    """Default class to store data"""

    type_ = "default"

    def __init__(self, **attributes):
        """Initialize the class object

        Parameters
        ----------
        attributes : dictionary
                     { 'nblocks'   : total number of blocks,
                       'nxb'       : number of grid points per block in x dir,
                       'nyb'       : number of grid points per block in y dir,
                       'nzb'       : number of grid points per block in z dir,
                       'inputfile' : hdf5 inputfile default (None),
                       'variables' : dictionary of variables default ({})
                       'storage'   : 'disk' }

        """
        super().__init__()
        self._set_attributes(attributes)
        self._set_data()

    def __repr__(self):
        """
        Return a representation of the object
        """
        return ("Data:\n" +
                " - type   : {}\n".format(type(self)) +
                " - keys   : {}\n".format(self.listkeys))

    def __getitem__(self,varkey):
        """
        Get variable data
        """
        if not varkey in self.listkeys: 
            raise ValueError('[bubblebox.library.create.Data] '+
                             'Variable "{}" does not exist in "{}"'.format(varkey,self.listkeys))
        else:
            return self.variables[varkey]

    def __setitem__(self,varkey,value):
        """
        Set variable data
        """
        if not varkey in self.listkeys:
            raise ValueError('[bubblebox.library.create.Data] '+
                             'Variable "{}" does not exist in "{}"'.format(varkey,self.listkeys))

        else:
            self.variables[varkey] = value

    def _set_attributes(self,attributes):
        """
        Private method for intialization
        """

        default_attributes = {'nblocks'   : 1,              
                              'inputfile' : None,
                              'memmap'    : {},
                              'variables' : {},
                                    'nxb' : 1, 'nyb' : 1, 'nzb' : 1,
                                'storage' : 'disk'}

        for key in attributes:
            if key in default_attributes:
                default_attributes[key] = attributes[key]
            else:
                raise ValueError('[bubblebox.library.create.Data] '+
                                 'Attribute "{}" not present in class Data'.format(key))

        for key, value in default_attributes.items(): setattr(self, key, value)

    def _set_data(self):
        """
        Private method for setting new data
        """

        self.listkeys = list(self.variables.keys())

        if self.storage == 'disk':
            self._create_numpy_memmap()

        elif self.storage == 'dask':
            self._create_numpy_arrays()
            self._create_dask_objects()
  
        else:
            raise NotImplementedError('[bubblebox.library.create.Data] '+
                                      'Storage format "{}" not implemented'.format(self.storage))

    def _create_numpy_memmap(self):
        """
        Create numpy memory maps for empty keys in variables dictionary
        """
        emptykeys = [key for key,value in self.variables.items() if type(value) is type(None)]
    
        if not emptykeys: return

        if not self.memmap:
            namerandom  = ''.join(random.choice(string.ascii_lowercase) for i in range(5)) 
            self.memmap = "".join(['./memmap_',namerandom])

        try:
            os.mkdir(self.memmap)
        except FileExistsError:
            pass

        for varkey in emptykeys:
            outputfile  = os.path.join(self.memmap,varkey)
            outputshape = (self.nblocks,self.nzb,self.nyb,self.nxb)
            self.variables[varkey] = numpy.memmap(outputfile, dtype=float, shape=outputshape, mode='w+')

    def _create_numpy_arrays(self):
        """
        Create numpy arrays for empty keys in variables dictionary
        """
        emptykeys = []

        emptykeys = [key for key,value in self.variables.items() if type(value) is type(None)]
     
        if not emptykeys: return

        for varkey in emptykeys:
            outputshape = (self.nblocks,self.nzb,self.nyb,self.nxb)
            self.variables[varkey] = numpy.ndarray(dtype=float, shape=outputshape)

    def _create_dask_objects(self):
        """
        Create dask array representation of data
        """
        for varkey in self.listkeys:
            if type(self.variables[varkey]) is not dsarray.core.Array:
                self.variables[varkey] = dsarray.from_array(self.variables[varkey],
                                                            chunks=(1,self.nzb,self.nyb,self.nxb))

    def _create_pyarrow_tensor(self):
        """
        Create a pyarrow tensor objects
        """
        for varkey in self.listkeys:

            if type(self.variables[varkey]) is not pyarrow.lib.Tensor:

                templist = []

                for lblock in range(self.nblocks):
                    templist.append(pyarrow.Tensor.from_numpy(self.variables[varkey][lblock]))

                self.variables[varkey] = templist
   
    def purge(self,purgeflag='all'):
        """
        Clean up data and close it
        """
        if self.memmap and (purgeflag == 'all' or purgeflag == 'memmap'):
            try:
                shutil.rmtree(self.memmap)
            except:
                pass

        if self.inputfile and (purgeflag == 'all' or purgeflag == 'inputfile'): 
            self.inputfile.close()

    def addvar(self,varkey):

        self.variables[varkey] = None
        self._set_data()

    def delvar(self,varkey):

        del self.variables[varkey]
       
        if self.memmap: 
            outputfile  = os.path.join(self.memmap,varkey)

            try:
                shutil.rmtree(outputfile)
            except:
                pass 

        self.listkeys = list(self.variables.keys())
         
