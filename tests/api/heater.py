"""Tests for `bubblebox/api/sample`."""

import bubblebox.api.sample as box
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

    def test_heater_oneblk(self):
        """test neighbors"""

        self._setup('oneblk')

        dataframes = [box.create.dataset2D(filename) for filename in self.filenames]

        for dataset in dataframes:
            for block in dataset.blocklist:

                neighborlist = [None]*4
                self.assertTrue(neighborlist == block.neighbors2D, 'Single block data structure has no neighbors')
                
        [dataset.inputfile.close() for dataset in dataframes]

        print("Single block returns None neigbhors\n")

    def test_heater_blocks(self):
        """test neighbors"""

        self._setup('blocks')

        dataframes  = [box.create.dataset2D(filename) for filename in self.filenames]

        for dataset in dataframes:
            for block in dataset.blocklist:

                ibx,iby   = pymorton.deinterleave2(block.tag)

                neighborlist = [pymorton.interleave(ibx+1,iby),
                                pymorton.interleave(ibx-1,iby),
                                pymorton.interleave(ibx,iby+1),
                                pymorton.interleave(ibx,iby-1)]

                neighborlist = [None if   neighbor > block.data.numblocks
                                     else neighbor
                                     for  neighbor in neighborlist]

                self.assertTrue(neighborlist == block.neighbors2D, 'Neigbhors are inconsitent with morton order')                
        [dataset.inputfile.close() for dataset in dataframes]

        print("2D neighbors are in morton order\n")

    def test_measure_bubbles(self):
        """test bubble measurement"""

        self._setup('oneblk')

        dataframes    = [box.create.dataset2D(filename,['bubbles']) for filename in self.filenames]
        regionframes  = [box.create.region(dataset) for dataset in dataframes]
        bubbleframes  = [box.measure.bubbles(region,'phi') for region in regionframes]

        numbubbles = [len(bubblelist) for bubblelist in bubbleframes]
        
        self.assertEqual(numbubbles,[488,163,236,236,242,234,257,223,259,291,235,223])

        [dataset.inputfile.close() for dataset in dataframes]

        print("Bubble measurements succesfull\n")
    
if __name__ == '__main__':
    unittest.main()

