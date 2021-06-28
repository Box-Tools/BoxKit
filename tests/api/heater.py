"""Tests for `bubblebox/api/default`."""

import bubblebox.api as box
import unittest
import pymorton

class TestHeater(unittest.TestCase):
    """bubblebox unit test for 2D Heater Data"""

    def _setup(self,prefix):
        """setup test parameters"""

        basedir  = '/home/akash/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/heater2D/'
        filetags = [0,5,10,15,20,25,30,35,40,45,50,55]
        prefix   = "".join([prefix,'/INS_Pool_Boiling_Heater_hdf5_'])

        self.filenames = ["".join([basedir,prefix,str(filetag).zfill(4)]) for filetag in filetags]

    def test_neighbors_oneblk(self):
        """test neighbors"""

        self._setup('oneblk')

        dataframes = [box.create.dataset(filename) for filename in self.filenames]

        for dataset in dataframes:
            for block in dataset.blocklist:

                neighlist = [None]*4
                self.assertTrue(neighlist == block.neighlist, 'Single block data structure has no neighbors')
                
        [dataset.inputfile.close() for dataset in dataframes]

        print("Single block returns None neigbhors\n")

    def test_neighbors_blocks(self):
        """test neighbors"""

        self._setup('blocks')

        dataframes  = [box.create.dataset(filename) for filename in self.filenames]

        for dataset in dataframes:
            for block in dataset.blocklist:

                iloc,jloc   = pymorton.deinterleave2(block.tag)

                neighlist = [pymorton.interleave(iloc-1,jloc),
                             pymorton.interleave(iloc+1,jloc),
                             pymorton.interleave(iloc,jloc-1),
                             pymorton.interleave(iloc,jloc+1)]

                neighlist = [None if   neighbor > block.data.nblocks
                                  else neighbor
                                  for  neighbor in neighlist]

                self.assertTrue(neighlist == block.neighlist, 'Neigbhors are inconsitent with morton order')

        [dataset.inputfile.close() for dataset in dataframes]

        print("2D neighbors are in morton order\n")

    def test_measure_bubbles_oneblk(self):
        """test bubble measurement"""

        self._setup('oneblk')

        dataframes    = [box.create.dataset(filename,uservars=['bubble']) for filename in self.filenames]
        regionframes  = [box.create.region(dataset) for dataset in dataframes]
        bubbleframes  = [box.measure.bubbles(region,['phi','bubble']) for region in regionframes]

        bubblenum     = [len(bubblelist) for bubblelist in bubbleframes]
        
        self.assertEqual(bubblenum,[488,163,236,236,242,234,257,223,259,291,235,223])

        [dataset.inputfile.close() for dataset in dataframes]

        print("Single block bubble measurements successful\n")
    
if __name__ == '__main__':
    unittest.main()

