"""Tests for `boxkit/api`."""

import os
import time
import unittest
import pymorton
import boxkit
from boxkit.library import Monitor


class TestBoiling(unittest.TestCase):
    """boxkit unit test for 3D boiling data"""

    def setUp(self):
        """
        Setup test parameters

        timestart : tag start time
        basedir   : base directory of the input data
        filetags  : list of file tags
        prefix    : prefix for input file
        filenames : list of filenames generated from basedir, prefix and filetags

        """
        print("-------------------------------------------------------------------------------------------------")
        self.timestart = time.time()
        basedir = (
            os.getenv("HOME")
            + "/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/domain3D/not-chunked/"
        )
        filetags = [*range(0, 58, 10)]
        prefix = "INS_Pool_Boiling_hdf5_"
        self.filenames = [
            "".join([basedir, prefix, str(filetag).zfill(4)]) for filetag in filetags
        ]

    def test_data_pointers_3D(self):
        """
        Test to check that blocks in a given dataset point to the same
        data location

        dataframes : list of Dataset objects

        """
        dataframes = [boxkit.read_dataset(filename) for filename in self.filenames]

        testMonitor = Monitor("test")
        testMonitor.setlimit(len(dataframes))
        monitorMsg = "run:" + self.id() + ": "

        for dataset in dataframes:
            for block in dataset.blocklist:
                self.assertTrue(
                    block._data is dataset.blocklist[0]._data,
                    "Data pointers are inconsistent",
                )
            testMonitor.update(monitorMsg)

        for dataset in dataframes:
            dataset.purge("boxmem")

    def test_neighbors_3D(self):
        """
        Test if neighbors are in morton order
        """
        dataframes = [boxkit.read_dataset(filename) for filename in self.filenames]

        testMonitor = Monitor("test")
        testMonitor.setlimit(len(dataframes))
        monitorMsg = "run:" + self.id() + ": "

        for dataset in dataframes:
            for block in dataset.blocklist:
                xloc, yloc, zloc = pymorton.deinterleave3(block.tag)

                neighlist = [
                    pymorton.interleave(xloc - 1, yloc, zloc),
                    pymorton.interleave(xloc + 1, yloc, zloc),
                    pymorton.interleave(xloc, yloc - 1, zloc),
                    pymorton.interleave(xloc, yloc + 1, zloc),
                    pymorton.interleave(xloc, yloc, zloc - 1),
                    pymorton.interleave(xloc, yloc, zloc + 1),
                ]

                neighlist = [
                    None if neighbor > dataset.nblocks - 1 else neighbor
                    for neighbor in neighlist
                ]

                self.assertEqual(
                    neighlist,
                    list(block.neighdict.values()),
                    "Neigbhors are inconsitent with morton order",
                )
            testMonitor.update(monitorMsg)

        for dataset in dataframes:
            dataset.purge("boxmem")

    def test_slice_3D(self):
        """
        Test slice
        """
        dataframes = [boxkit.read_dataset(filename) for filename in self.filenames]
        regionframes = [
            boxkit.create_slice(dataset, zmin=0.01, zmax=0.01) for dataset in dataframes
        ]

        testMonitor = Monitor("test")
        testMonitor.setlimit(len(regionframes))
        monitorMsg = "run:" + self.id() + ": "

        for region in regionframes:
            self.assertEqual(int(len(region.blocklist) ** (1 / 2)), 16)
            testMonitor.update(monitorMsg)

        for dataset in dataframes:
            dataset.purge("boxmem")

    def test_regionprops_3D(self):
        """
        Test measure bubbles
        """
        dataframes = [
            boxkit.read_dataset(filename, storage="numpy-memmap")
            for filename in self.filenames
        ]

        _time_measure = time.time()

        bubbleframes = []

        for dataset in dataframes:
            bubbleframes.append(
                boxkit.regionprops(
                    dataset, "phi", backend="loky", monitor=True, nthreads=8
                )
            )

        _time_measure = time.time() - _time_measure
        print("%s: %.3fs" % ("boxkit.regionprops", _time_measure))

        numbubbles = [len(listbubbles) for listbubbles in bubbleframes]

        self.assertEqual(numbubbles, [1341, 1380, 1262, 1255, 1351, 1362])

        for dataset in dataframes:
            dataset.purge("boxmem")

    def test_mergeblocks_3D(self):
        """
        Test reshape
        """
        dataframes = [
            boxkit.read_dataset(filename, storage="numpy-memmap")
            for filename in [self.filenames[0]]
        ]

        for dataset in dataframes:
            reshaped_dataset = boxkit.mergeblocks(
                dataset, "phi", nthreads=8, monitor=True, backend="loky"
            )
            reshaped_dataset.purge("boxmem")

        for dataset in dataframes:
            dataset.purge("boxmem")

    def test_temporal_mean_3D(self):
        """
        Test reshape
        """
        dataframes = [
            boxkit.read_dataset(filename, storage="numpy-memmap")
            for filename in self.filenames
        ]

        average_dataset = boxkit.temporal_mean(dataframes, "vvel", nthreads=8, backend="loky", monitor=True)

        for dataset in dataframes:
            dataset.purge("boxmem")

        average_dataset.purge("boxmem")

    def tearDown(self):
        """Clean up and timing"""
        timetest = time.time() - self.timestart
        print("%s: %.3fs\n" % (self.id(), timetest))


if __name__ == "__main__":
    unittest.main()
