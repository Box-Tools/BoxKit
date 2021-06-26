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

        self.dataframes   = [box.create.dataset3D(filename) for filename in filenames]
        self.regionframes = [box.create.region(dataset)     for dataset  in self.dataframes]

    def test_data_pointers(self):
        """test data pointers"""

        for dataset in self.dataframes:

            data_assert  = [True if   block.data is dataset.blocklist[0].data
                                 else False
                                 for  block in dataset.blocklist]

            self.assertTrue(not False in data_assert, 'Data pointers are inconsistent')

        print("Data pointers are consistent\n")

    def test_neighbors(self):
        """test neighbors"""
    
        for dataset in self.dataframes:
            for block in dataset.blocklist:

                ibx,iby,ibz  = pymorton.deinterleave3(block.tag)

                neighborlist = [pymorton.interleave(ibx+1,iby,ibz),
                                pymorton.interleave(ibx-1,iby,ibz),
                                pymorton.interleave(ibx,iby+1,ibz),
                                pymorton.interleave(ibx,iby-1,ibz),
                                pymorton.interleave(ibx,iby,ibz+1),
                                pymorton.interleave(ibx,iby,ibz-1)]

                neighborlist = [None if   neighbor > block.data.numblocks
                                     else neighbor
                                     for  neighbor in neighborlist]

                self.assertTrue(neighborlist == block.neighbors3D, 'Neigbhors are inconsitent with morton order')                
        print("3D neighbors are in morton order\n")

    def tearDown(self):
        """close files"""

        [dataset.inputfile.close() for dataset in self.dataframes] 

if __name__ == '__main__':
    unittest.main()

