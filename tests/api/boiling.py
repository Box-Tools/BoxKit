"""Tests for `bubblebox/api/default`."""

import bubblebox.api as box
import unittest
import itertools
import pymorton
import time

class TestBoiling(unittest.TestCase):
    """bubblebox unit test for 3D boiling data"""

    def setUp(self):
        """setup test parameters"""

        self.startTime = time.time()

        basedir        = '/home/akash/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/domain3D/'
        filetags       = [*range(0,50,10)]
        prefix         = 'INS_Pool_Boiling_hdf5_'
        self.filenames = ["".join([basedir,prefix,str(filetag).zfill(4)]) for filetag in filetags]

    def test_data_pointers(self):
        """test data pointers"""

        def _test_data_pointers(dataset):
            data_assert  = [True if   block.data is dataset.blocklist[0].data
                                 else False
                                 for  block in dataset.blocklist]

            self.assertTrue(not False in data_assert, 'Data pointers are inconsistent')
       
        dataframes  = [box.create.dataset(filename) for filename in self.filenames]
        data_assert = [_test_data_pointers(dataset) for dataset  in dataframes]

        [dataset.close() for dataset in dataframes]

        print("Data pointers are consistent")

    def test_neighbors(self):
        """test neighbors"""

        def _test_neighbors(dataset):
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

        dataframes   = [box.create.dataset(filename) for filename in self.filenames]
        neigh_assert = [_test_neighbors(dataset)     for dataset  in dataframes]
    
        [dataset.close() for dataset in dataframes]

        print("3D neighbors are in morton order")

    def test_slice(self):
        """test slice"""

        dataset = box.create.dataset(self.filenames[0])
        slice   = box.create.slice(dataset,{'zmin':0.01,'zmax':0.01})

        self.assertEqual(int(len(slice.blocklist)**(1/2)),16)

        dataset.close()

        print("Slice blocklist length matches setup")

    def test_measure_bubbles(self):
    
        dataset    = box.create.dataset(self.filenames[0],uservars=['bubble'])
        region     = box.create.region(dataset)
        bubblelist = box.measure.bubbles(region,['phi','bubble'],nparallel=4)

        self.assertEqual(len(bubblelist),1341)     

        dataset.close()

        print("Ran 3D bubble measurements on multiple blocks")

    def tearDown(self):
        """close files"""

        testTime = time.time() - self.startTime
        print('%s: %.3fs\n' % (self.id(), testTime))

if __name__ == '__main__':
    unittest.main()

