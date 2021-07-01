"""Tests for `bubblebox/api/default`."""

import bubblebox.api as box
import unittest
import pymorton
import time
import os
from progress.bar import Bar

class TestHeater(unittest.TestCase):
    """bubblebox unit test for 2D Heater Data"""

    def _setup(self,prefix):
        """
        Setup test parameters

        timestart : tag start time
        basedir   : base directory of the input data
        filetags  : list of file tags
        prefix    : prefix for input file
        filenames : list of filenames generated from basedir, prefix and filetags

        """
        self.timestart= time.time()

        basedir  = '/home/akash/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/heater2D/'
        filetags = [*range(0,60,5)]
        prefix   = "".join([prefix,'/INS_Pool_Boiling_Heater_hdf5_'])
        self.filenames = ["".join([basedir,prefix,str(filetag).zfill(4)]) for filetag in filetags]

    def test_neighbors_oneblk_2D(self):
        """
        Test if neighbors are morton order
        """
        self._setup('oneblk')
        dataframes = [box.create.dataset(filename) for filename in self.filenames]

        bar = Bar('Dataframes',max=len(dataframes))
        for dataset in dataframes:
            for block in dataset.blocklist:
                self.assertEqual([None]*4,block.neighlist, 'Single block data structure has no neighbors')
            bar.next()
        bar.finish()

        [dataset.close() for dataset in dataframes]

    def test_neighbors_blocks_2D(self):
        """
        Test if neighbors are in morton order
        """
        self._setup('blocks')
        dataframes = [box.create.dataset(filename) for filename in self.filenames]

        bar = Bar('Dataframes',max=len(dataframes))
        for dataset in dataframes:
            for block in dataset.blocklist:
                iloc,jloc   = pymorton.deinterleave2(block.tag)

                neighlist = [pymorton.interleave(iloc-1,jloc),
                             pymorton.interleave(iloc+1,jloc),
                             pymorton.interleave(iloc,jloc-1),
                             pymorton.interleave(iloc,jloc+1)]

                neighlist = [None if neighbor > block.data.nblocks-1 else neighbor for neighbor in neighlist]

                self.assertEqual(neighlist,block.neighlist, 'Neigbhors are inconsitent with morton order')
            bar.next()
        bar.finish()

        [dataset.close() for dataset in dataframes]

    def test_measure_bubbles_oneblk_2D(self):
        """
        Test bubble measurement
        """
        self._setup('oneblk')
        dataframes = [box.create.dataset(filename,uservars=['bubble']) for filename in self.filenames]
        regionframes = [box.create.region(dataset) for dataset in dataframes]

        bubbleframes = []
        bar = Bar('Dataframes',max=len(regionframes))
        for region in regionframes:
            bubbleframes.append(box.measure.bubbles(region,['phi','bubble']))
            bar.next()
        bar.finish()

        numbubbles = [len(listbubbles) for listbubbles in bubbleframes]        
        #self.assertEqual(numbubbles,[488,163,236,236,242,234,257,223,259,291,235,223])

        [dataset.close() for dataset in dataframes]

    def test_measure_bubbles_blocks_2D(self):
        """
        Test bubble measurement
        """
        self._setup('blocks')
        dataframes = [box.create.dataset(filename,uservars=['bubble']) for filename in self.filenames]
        regionframes = [box.create.region(dataset) for dataset in dataframes]

        os.environ['BUBBLEBOX_NTHREADS_BACKEND'] = '2'
        bubbleframes = []
        bar = Bar('Dataframes',max=len(regionframes))
        for region in regionframes:
            bubbleframes.append(box.measure.bubbles(region,['phi','bubble']))
            bar.next()
        bar.finish()
        del os.environ['BUBBLEBOX_NTHREADS_BACKEND']

        numbubbles    = [len(listbubbles) for listbubbles in bubbleframes]

        [dataset.close() for dataset in dataframes]

    def tearDown(self):
        """Clean up and timing"""
        timetest = time.time() - self.timestart

        print('%s: %.3fs\n' % (self.id(),timetest))
    
if __name__ == '__main__':
    unittest.main()

