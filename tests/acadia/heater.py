"""Tests for `boxkit/api`."""

import os
import time
import unittest
import pymorton
import boxkit
from boxkit.library import Timer

class TestHeater(unittest.TestCase):
    """boxkit unit test for 2D Heater Data"""

    def customSetUp(self, prefix):
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
            + "/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/heater2D/"
        )
        filetags = [30]
        prefix = "".join([prefix, "/INS_Pool_Boiling_Heater_hdf5_"])
        self.filenames = [
            "".join([basedir, prefix, str(filetag).zfill(4)]) for filetag in filetags
        ]

    def test_neighbors_oneblk_2D(self):
        """
        Test if neighbors are morton order
        """
        self.customSetUp("oneblk")
        dataframes = [boxkit.read_dataset(filename) for filename in self.filenames]

        for dataset in dataframes:

            for block in dataset.blocklist:
                self.assertEqual(
                    [None] * 6,
                    list(block.neighdict.values()),
                    "Single block data structure has no neighbors",
                )

        for dataset in dataframes:
            dataset.purge("boxmem")

    def test_regionprops_oneblk_2D(self):
        """
        Test bubble measurement
        """
        self.customSetUp("oneblk")

        dataframes = [boxkit.read_dataset(filename) for filename in self.filenames]

        bubbleframes = []
        for dataset in dataframes:
            bubbleframes.append(boxkit.regionprops(dataset, "phi"))

        numbubbles = [len(listbubbles) for listbubbles in bubbleframes]

        self.assertEqual(numbubbles, [257])

        for dataset in dataframes:
            dataset.purge("boxmem")

    def tearDown(self):
        """Clean up and timing"""
        del self.timer

if __name__ == "__main__":
    unittest.main()
