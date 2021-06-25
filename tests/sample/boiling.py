"""Tests for `bubblebox/api/sample`."""

import bubblebox.api.sample as box
import unittest
import pymorton

class TestBoiling(unittest.TestCase):
    """bubblebox unit test for 3D boiling data"""

    def setUp(self):
        """setup test parameters"""

        basedir   = '/home/akash/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/domain3D/'
        filetags  = [0,5,10,15,20,25,30,35,40,45,50,55]

        prefix    = 'INS_Pool_Boiling_hdf5_'
        filenames = ["".join([basedir,prefix,str(filetag).zfill(4)]) for filetag in filetags]

        self.datasets  = [box.read_dataset3D(filename) for filename in filenames]
        self.volumes   = [box.create_volume(dataset)   for dataset  in self.datasets]

    def test_data_pointers(self):
        """test data pointers"""

        for dataset in self.datasets:

            data_assert  = [ True if   block.data is dataset.blocks[0].data
                                  else False
                                  for  block in dataset.blocks ]

            self.assertTrue(not False in data_assert, 'Data pointers are inconsistent')

    def test_neighbors(self):
        """test neighbors"""
    
        for dataset in self.datasets:
            for block in dataset.blocks:

                ibx,iby,ibz = pymorton.deinterleave3(block.tag)

                neighbors   = [pymorton.interleave(ibx+1,iby,ibz),
                               pymorton.interleave(ibx-1,iby,ibz),
                               pymorton.interleave(ibx,iby+1,ibz),
                               pymorton.interleave(ibx,iby-1,ibz),
                               pymorton.interleave(ibx,iby,ibz+1),
                               pymorton.interleave(ibx,iby,ibz-1)]

                neighbors   = [None if   neighbor > block.data.lblocks
                                    else neighbor
                                    for  neighbor in neighbors]

                self.assertTrue(neighbors == block.neighbors3, 'Neigbhors are inconsitent with morton order')                
    def tearDown(self):
        """close files"""

        [dataset.inputfile.close() for dataset in self.datasets] 

if __name__ == '__main__':
    unittest.main()

