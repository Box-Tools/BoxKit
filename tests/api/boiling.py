"""Tests for `bubblebox/api/default`."""

import bubblebox.api as box
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

        self.dataframes   = [box.create.dataset(filename) for filename in filenames]

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

                xloc,yloc,zloc  = pymorton.deinterleave3(block.tag)

                neighlist = [pymorton.interleave(xloc-1,yloc,zloc),
                             pymorton.interleave(xloc+1,yloc,zloc),
                             pymorton.interleave(xloc,yloc-1,zloc),
                             pymorton.interleave(xloc,yloc+1,zloc),
                             pymorton.interleave(xloc,yloc,zloc-1),
                             pymorton.interleave(xloc,yloc,zloc+1)]

                neighlist = [None if   neighbor > block.data.nblocks
                                  else neighbor
                                  for  neighbor in neighlist]

                self.assertTrue(neighlist == block.neighlist, 'Neigbhors are inconsitent with morton order')

        print("3D neighbors are in morton order\n")

    def test_slice(self):
        """test slice"""

        dataset = self.dataframes[0]
        slice   = box.create.slice(dataset,{'zmin':0.01,'zmax':0.01})

        self.assertEqual(int(len(slice.blocklist)**(1/2)),16)

        print("Slice blocklist length matches setup\n")

    def tearDown(self):
        """close files"""

        [dataset.inputfile.close() for dataset in self.dataframes] 

if __name__ == '__main__':
    unittest.main()

