"""Tests for `bubblebox/api/flow`."""

import bubblebox.api.flow as flowbox
import unittest
import pymorton
import time
import os

from bubblebox.library.utilities import Monitor

class TestHeater(unittest.TestCase):
    """bubblebox unit test for 2D Heater Data"""

    def customSetUp(self,prefix):
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
        self.customSetUp('oneblk')
        dataframes = [flowbox.create.dataset(filename) for filename in self.filenames]

        testMonitor = Monitor("test")
        testMonitor.setlimit(len(dataframes))
        monitorMsg = 'run:'+self.id()+': '

        for dataset in dataframes:

            for block in dataset.blocklist:
                self.assertEqual([None]*4,block.neighlist, 'Single block data structure has no neighbors')

            testMonitor.update(monitorMsg)

        for dataset in dataframes:
            dataset.purge('memmap')

    def test_neighbors_blocks_2D(self):
        """
        Test if neighbors are in morton order
        """
        self.customSetUp('blocks')
        dataframes = [flowbox.create.dataset(filename) for filename in self.filenames]

        testMonitor = Monitor("test")
        testMonitor.setlimit(len(dataframes))
        monitorMsg = 'run:'+self.id()+': '

        for dataset in dataframes:

            taglist = [*range(0,dataset.nblocks)]

            for tag,block in zip(taglist,dataset.blocklist):
                iloc,jloc   = pymorton.deinterleave2(tag)

                neighlist = [pymorton.interleave(iloc-1,jloc),
                             pymorton.interleave(iloc+1,jloc),
                             pymorton.interleave(iloc,jloc-1),
                             pymorton.interleave(iloc,jloc+1)]

                neighlist = [None if neighbor > dataset.nblocks-1 else neighbor for neighbor in neighlist]

                self.assertEqual(neighlist,block.neighlist, 'Neigbhors are inconsitent with morton order')

            testMonitor.update(monitorMsg)

        for dataset in dataframes:
            dataset.purge('memmap')

    def test_measure_bubbles_oneblk_2D(self):
        """
        Test bubble measurement
        """
        self.customSetUp('oneblk')

        dataframes = [flowbox.create.dataset(filename) for filename in self.filenames]

        process = flowbox.measure.bubbles    
        process.tasks['skimeasure']['region'].monitor = True
        print(process.tasks['skimeasure']['region'].backend)

        bubbleframes = flowbox.measure.bubbles(dataframes,'phi')

        numbubbles = [len(listbubbles) for listbubbles in bubbleframes]        

        self.assertEqual(numbubbles,[488,163,236,236,242,234,257,223,259,291,235,223])

        for dataset in dataframes:
            dataset.purge('memmap')

    def test_measure_bubbles_blocks_2D(self):
        """
        Test bubble measurement
        """
        self.customSetUp('blocks')

        dataframes = [flowbox.create.dataset(filename) for filename in self.filenames]

        process = flowbox.measure.bubbles    
        process.tasks['skimeasure']['region'].monitor = True
 
        bubbleframes = flowbox.measure.bubbles(dataframes,'phi')

        numbubbles = [len(listbubbles) for listbubbles in bubbleframes]

        for dataset in dataframes:
            dataset.purge('memmap')

    def tearDown(self):
        """Clean up and timing"""
        timetest = time.time() - self.timestart

        print('%s: %.3fs\n' % (self.id(),timetest))
    
if __name__ == '__main__':
    unittest.main()
