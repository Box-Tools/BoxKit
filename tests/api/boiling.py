"""Tests for `bubblebox/api/flow`."""

import bubblebox.api.flow as flowbox
import unittest
import pymorton
import time
import os

from bubblebox.utilities import CboxMonitor as Monitor

class TestBoiling(unittest.TestCase):
    """bubblebox unit test for 3D boiling data"""

    def setUp(self):
        """
        Setup test parameters

        timestart : tag start time
        basedir   : base directory of the input data
        filetags  : list of file tags
        prefix    : prefix for input file
        filenames : list of filenames generated from basedir, prefix and filetags

        """
        self.timestart = time.time()

        basedir  = '/home/akash/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/domain3D/not-chunked/'
        filetags = [*range(0,58,10)]
        prefix   = 'INS_Pool_Boiling_hdf5_'
        self.filenames = ["".join([basedir,prefix,str(filetag).zfill(4)]) for filetag in filetags]

    def test_data_pointers_3D(self):
        """
        Test to check that blocks in a given dataset point to the same
        data location

        dataframes : list of Dataset objects

        """      
        dataframes  = [flowbox.create.dataset(filename) for filename in self.filenames]

        monitorTest = Monitor("test")
        monitorTest.setlimit(len(dataframes))
        monitorMsg = 'run:'+self.id()+': '

        for dataset in dataframes:
            for block in dataset.blocklist:
                self.assertTrue(block.data is dataset.blocklist[0].data,'Data pointers are inconsistent')
            monitorTest.update(monitorMsg)

        for dataset in dataframes:
            dataset.purge('memmap')

    def test_neighbors_3D(self):
        """
        Test if neighbors are in morton order
        """
        dataframes   = [flowbox.create.dataset(filename) for filename in self.filenames]

        monitorTest = Monitor("test")
        monitorTest.setlimit(len(dataframes))
        monitorMsg = 'run:'+self.id()+': '

        for dataset in dataframes:
            for block in dataset.blocklist:
                xloc,yloc,zloc  = pymorton.deinterleave3(block.tag)

                neighlist = [pymorton.interleave(xloc-1,yloc,zloc),
                             pymorton.interleave(xloc+1,yloc,zloc),
                             pymorton.interleave(xloc,yloc-1,zloc),
                             pymorton.interleave(xloc,yloc+1,zloc),
                             pymorton.interleave(xloc,yloc,zloc-1),
                             pymorton.interleave(xloc,yloc,zloc+1)]

                neighlist = [None if neighbor > block.data.nblocks-1 else neighbor for neighbor in neighlist]

                self.assertEqual(neighlist,block.neighlist, 'Neigbhors are inconsitent with morton order')
            monitorTest.update(monitorMsg)

        for dataset in dataframes:
            dataset.purge('memmap')

    def test_slice_3D(self):
        """
        Test slice
        """
        dataframes   = [flowbox.create.dataset(filename) for filename in self.filenames]
        regionframes = [flowbox.create.slice(dataset, zmin=0.01, zmax=0.01) for dataset in dataframes]

        monitorTest = Monitor("test")
        monitorTest.setlimit(len(regionframes))
        monitorMsg = 'run:'+self.id()+': '

        for region in regionframes:
            self.assertEqual(int(len(region.blocklist)**(1/2)),16)
            monitorTest.update(monitorMsg)

        for dataset in dataframes:
            dataset.purge('memmap')

    def test_measure_bubbles_3D(self):
        """
        Test measure bubbles
        """
        dataframes = [flowbox.create.dataset(filename,storage='disk') for filename in self.filenames]

        _time_measure = time.time()
        measure_bubbles = flowbox.measure.bubbles.clone()

        measure_bubbles.tasks['region'].nthreads = 4
        measure_bubbles.tasks['region'].backend = 'loky' 
        measure_bubbles.tasks['region'].monitor = True

        measure_bubbles.tasks['block'].nthreads = None
        measure_bubbles.tasks['block'].backend = 'serial'

        bubbleframes = measure_bubbles(dataframes,'phi')

        _time_measure = time.time() - _time_measure
        print('%s: %.3fs' % ('flowbox.measure.bubbles', _time_measure))

        numbubbles   = [len(listbubbles) for listbubbles in bubbleframes]

        self.assertEqual(numbubbles,[1341, 1380, 1262, 1255, 1351, 1362])

        for dataset in dataframes:
            dataset.purge('memmap')

    def tearDown(self):
        """Clean up and timing"""
        timetest = time.time() - self.timestart

        print('%s: %.3fs\n' % (self.id(), timetest))

if __name__ == '__main__':
    unittest.main()
