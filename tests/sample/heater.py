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

        prefix         = "".join([prefix,'/INS_Pool_Boiling_Heater_hdf5_'])
        filenames      = ["".join([basedir,prefix,str(filetag).zfill(4)]) for filetag in filetags]
        self.datasets  = [box.read_dataset2D(filename) for filename in filenames]

    def test_heater_oneblk(self):
        """test neighbors"""

        self._setup('oneblk')

        for dataset in self.datasets:
            for block in dataset.blocks:

                neighbors = [None]*4
                self.assertTrue(neighbors == block.neighbors2, 'Neigbhors are inconsitent with morton order')                
    def test_heater_blocks(self):
        """test neighbors"""

        self._setup('blocks')

        for dataset in self.datasets:
            for block in dataset.blocks:

                ibx,iby   = pymorton.deinterleave2(block.tag)

                neighbors = [pymorton.interleave(ibx+1,iby),
                             pymorton.interleave(ibx-1,iby),
                             pymorton.interleave(ibx,iby+1),
                             pymorton.interleave(ibx,iby-1)]

                neighbors = [None if   neighbor > block.data.lblocks
                                  else neighbor
                                  for  neighbor in neighbors]

                self.assertTrue(neighbors == block.neighbors2, 'Neigbhors are inconsitent with morton order')                
    def test_measure_bubbles(self):
        """test bubble measurement"""

        self._setup('oneblk')

        slices = [box.create_slice(dataset) for dataset in self.datasets]

        bubbleprops = [box.measure_regionprops(slice,'phi') for slice in slices]
       
    def tearDown(self):
        """close files """

        [dataset.inputfile.close for dataset in (self.datasets)]

if __name__ == '__main__':
    unittest.main()

