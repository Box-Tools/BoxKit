"""Tests for `bubblebox/api/flow`."""

import bubblebox.api as bubblebox
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

        basedir  = os.getenv('HOME')+'/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/heater2D/'
        filetags = [*range(0,60,5)]
        prefix   = "".join([prefix,'/INS_Pool_Boiling_Heater_hdf5_'])
        self.filenames = ["".join([basedir,prefix,str(filetag).zfill(4)]) for filetag in filetags]

    def test_neighbors_blocks_2D(self):
        """
        Test if neighbors are in morton order
        """
        self.customSetUp('blocks')
        dataframes = [bubblebox.read.dataset(filename) for filename in self.filenames]

        testMonitor = Monitor("test")
        testMonitor.setlimit(len(dataframes))
        monitorMsg = 'run:'+self.id()+': '

        for dataset in dataframes:

            taglist = [*range(0,dataset.nblocks)]

            for tag,block in zip(taglist,dataset.blocklist):

                locations = ['xlow','xhigh','ylow','yhigh','zlow','zhigh']
                neighdict = dict(zip(locations,[None]*6))

                iloc,jloc   = pymorton.deinterleave2(tag)

                neighlist = [pymorton.interleave(iloc-1,jloc),
                             pymorton.interleave(iloc+1,jloc),
                             pymorton.interleave(iloc,jloc-1),
                             pymorton.interleave(iloc,jloc+1)]

                neighlist = [None if neighbor > dataset.nblocks-1 else neighbor for neighbor in neighlist]

                neighdict['xlow'] = neighlist[0]
                neighdict['xhigh'] = neighlist[1]
                neighdict['zlow'] = neighlist[2]
                neighdict['zhigh'] = neighlist[3]

                self.assertEqual(neighdict, block.neighdict, 'Neigbhors are inconsitent with morton order')

            testMonitor.update(monitorMsg)

        for dataset in dataframes:
            dataset.purge('boxmem')

    def test_measure_bubbles_blocks_2D(self):
        """
        Test bubble measurement
        """
        self.customSetUp('blocks')

        dataframes = [bubblebox.read.dataset(filename) for filename in self.filenames]

        process = bubblebox.measure.bubbles    
        process.tasks['skimeasure']['region'].monitor = True
 
        bubbleframes = bubblebox.measure.bubbles(dataframes,'phi')

        numbubbles = [len(listbubbles) for listbubbles in bubbleframes]

        for dataset in dataframes:
            dataset.purge('boxmem')

    def tearDown(self):
        """Clean up and timing"""
        timetest = time.time() - self.timestart

        print('%s: %.3fs\n' % (self.id(),timetest))
    
if __name__ == '__main__':
    unittest.main()

