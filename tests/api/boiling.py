"""Tests for `bubblebox/api/default`."""

import bubblebox.api as box
import unittest
import pymorton
import time
import os
from progress.bar import Bar

class TestBoiling(unittest.TestCase):
    """bubblebox unit test for 3D boiling data"""

    def setUp(self):
        """setup test parameters"""

        self.startTime = time.time()

        basedir        = '/home/akash/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/domain3D/'
        filetags       = [*range(0,58,10)]
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

        bar = Bar('Testing data pointers...',max=len(dataframes))
        data_assert = [_test_data_pointers(dataset) for dataset  in dataframes if not bar.next()]
        bar.finish()

        [dataset.close() for dataset in dataframes]

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

                neighlist = [None if   neighbor > block.data.nblocks-1
                                  else neighbor
                                  for  neighbor in neighlist]

                self.assertTrue(neighlist == block.neighlist, 'Neigbhors are inconsitent with morton order')

        dataframes   = [box.create.dataset(filename) for filename in self.filenames]

        bar = Bar('Testing morton order in 3D...',max=len(dataframes))
        neigh_assert = [_test_neighbors(dataset) for dataset  in dataframes if not bar.next()]
        bar.finish()
    
        [dataset.close() for dataset in dataframes]

    def test_slice(self):
        """test slice"""

        dataframes   = [box.create.dataset(filename) for filename in self.filenames]
        regionframes = [box.create.slice(dataset,{'zmin':0.01,'zmax':0.01}) for dataset in dataframes]

        bar = Bar('Testing slices for 3D data...',max=len(regionframes)) 
        [self.assertEqual(int(len(region.blocklist)**(1/2)),16) for region in regionframes if not bar.next()]
        bar.finish()

        [dataset.close() for dataset in dataframes]

    def test_measure_bubbles(self):

        os.environ['BUBBLEBOX_NPOOL_BACKEND'] = '4'

        dataframes   = [box.create.dataset(filename,uservars=['bubble']) for filename in self.filenames]
        regionframes = [box.create.region(dataset) for dataset in dataframes]

        bar = Bar('Measuring 3D bubbles...',max=len(regionframes))
        bubbleframes = [box.measure.bubbles(region,['phi','bubble']) for region in regionframes if not bar.next()]
        bar.finish()

        numbubbles   = [len(listbubbles) for listbubbles in bubbleframes]

        [dataset.close() for dataset in dataframes]

        del os.environ['BUBBLEBOX_NPOOL_BACKEND']

    def tearDown(self):
        """close files"""

        testTime = time.time() - self.startTime
        print('%s: %.3fs\n' % (self.id(), testTime))

if __name__ == '__main__':
    unittest.main()

