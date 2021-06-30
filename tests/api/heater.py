"""Tests for `bubblebox/api/default`."""

import bubblebox.api as box
import unittest
import pymorton
import time
from progress.bar import Bar

class TestHeater(unittest.TestCase):
    """bubblebox unit test for 2D Heater Data"""

    def _setup(self,prefix):
        """setup test parameters"""

        self.startTime = time.time()

        basedir  = '/home/akash/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/heater2D/'
        filetags = [*range(0,60,5)]
        prefix   = "".join([prefix,'/INS_Pool_Boiling_Heater_hdf5_'])

        self.filenames = ["".join([basedir,prefix,str(filetag).zfill(4)]) for filetag in filetags]

    def test_neighbors_oneblk(self):
        """test neighbors"""

        def _test_neighbors_oneblk(dataset):
            for block in dataset.blocklist:

                neighlist = [None]*4
                self.assertTrue(neighlist == block.neighlist, 'Single block data structure has no neighbors')
 
        self._setup('oneblk')

        dataframes = [box.create.dataset(filename) for filename in self.filenames]

        bar = Bar('Testing neighbors for a single 2D block...',max=len(dataframes))
        neigh_assert = [_test_neighbors_oneblk(dataset) for dataset in dataframes if not bar.next()] 
        bar.finish()

        [dataset.close() for dataset in dataframes]

    def test_neighbors_blocks(self):
        """test neighbors"""

        def _test_neighbors_blocks(dataset):
            for block in dataset.blocklist:

                iloc,jloc   = pymorton.deinterleave2(block.tag)

                neighlist = [pymorton.interleave(iloc-1,jloc),
                             pymorton.interleave(iloc+1,jloc),
                             pymorton.interleave(iloc,jloc-1),
                             pymorton.interleave(iloc,jloc+1)]

                neighlist = [None if   neighbor > block.data.nblocks-1
                                  else neighbor
                                  for  neighbor in neighlist]

                self.assertTrue(neighlist == block.neighlist, 'Neigbhors are inconsitent with morton order')

        self._setup('blocks')

        dataframes = [box.create.dataset(filename) for filename in self.filenames]

        bar = Bar('Testing morton order in 2D...',max=len(dataframes))
        neigh_assert = [_test_neighbors_blocks(dataset) for dataset in dataframes if not bar.next()]
        bar.finish()

        [dataset.close() for dataset in dataframes]

    def test_measure_bubbles_oneblk(self):
        """test bubble measurement"""

        self._setup('oneblk')

        dataframes    = [box.create.dataset(filename,uservars=['bubble']) for filename in self.filenames]
        regionframes  = [box.create.region(dataset) for dataset in dataframes]

        bar = Bar('Measuring bubbles in single 2D block...',max=len(regionframes))
        bubbleframes = [box.measure.bubbles(region,['phi','bubble']) for region in regionframes if not bar.next()]
        bar.finish()

        numbubbles = [len(listbubbles) for listbubbles in bubbleframes]
        
        self.assertEqual(numbubbles,[488,163,236,236,242,234,257,223,259,291,235,223])

        [dataset.close() for dataset in dataframes]

    def test_measure_bubbles_blocks(self):
        """test neighbors"""

        self._setup('blocks')

        dataframes    = [box.create.dataset(filename,uservars=['bubble']) for filename in self.filenames]
        regionframes  = [box.create.region(dataset) for dataset in dataframes]

        bar = Bar('Measuring bubbles in multiple 2D blocks...',max=len(regionframes))
        bubbleframes = [box.measure.bubbles(region,['phi','bubble']) for region in regionframes if not bar.next()]
        bar.finish()

        numbubbles    = [len(listbubbles) for listbubbles in bubbleframes]

        [dataset.close() for dataset in dataframes]

    def tearDown(self):
        """
        Execute after each test
        """

        testTime = time.time() - self.startTime
        print('%s: %.3fs\n' % (self.id(), testTime))
    
if __name__ == '__main__':
    unittest.main()

