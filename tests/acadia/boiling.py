"""Tests for `boxkit/api`."""

import os
import time
import unittest
import pymorton
import boxkit
from boxkit.library import Timer

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
        print(f"\n-------------------------Running: {self.id()}-------------------------\n")
 
        self.timer = Timer(self.id())

        basedir = (
            os.getenv("HOME")
            + "/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/domain3D/not-chunked/"
        )
        filetags = [30]
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

        for dataset in dataframes:
            for block in dataset.blocklist:
                self.assertTrue(
                    block._data is dataset.blocklist[0]._data,
                    "Data pointers are inconsistent",
                )

        for dataset in dataframes:
            dataset.purge()

    def test_neighbors_3D(self):
        """
        Test if neighbors are in morton order
        """
        dataframes = [boxkit.read_dataset(filename) for filename in self.filenames]

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

        for dataset in dataframes:
            dataset.purge()

    def test_slice_3D(self):
        """
        Test slice
        """
        dataframes = [boxkit.read_dataset(filename) for filename in self.filenames]
        regionframes = [
            boxkit.create_slice(dataset, zmin=0.01, zmax=0.01) for dataset in dataframes
        ]

        for region in regionframes:
            self.assertEqual(int(len(region.blocklist) ** (1 / 2)), 16)

        for dataset in dataframes:
            dataset.purge()

    def test_regionprops_3D(self):
        """
        Test measure bubbles
        """
        dataframes = [
            boxkit.read_dataset(filename, storage="numpy-memmap")
            for filename in self.filenames
        ]

        timer = Timer("boxkit.regionprops")

        bubbleframes = []

        for dataset in dataframes:
            bubbleframes.append(
                boxkit.regionprops(
                    dataset, "phi", backend="loky", monitor=True, nthreads=8
                )
            )

        del timer

        numbubbles = [len(listbubbles) for listbubbles in bubbleframes]

        self.assertEqual(numbubbles, [1255])

        for dataset in dataframes:
            dataset.purge()

    def test_mergeblocks_3D(self):
        """
        Test reshape
        """
        dataframes = [
            boxkit.read_dataset(filename, storage="numpy-memmap")
            for filename in self.filenames
        ]

        for dataset in dataframes:
            reshaped_dataset = boxkit.mergeblocks(
                dataset, "phi", nthreads=1, monitor=True, backend="loky"
            )
            reshaped_dataset.purge()

        for dataset in dataframes:
            dataset.purge()

    def tearDown(self):
        """Clean up and timing"""
        del self.timer

if __name__ == "__main__":
    unittest.main()
