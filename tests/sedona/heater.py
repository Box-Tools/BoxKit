"""Tests for `boxkit/api`."""

import os
import time
import unittest
import pymorton
import boxkit.api as boxkit
from boxkit.library import Monitor


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
        self.timestart = time.time()

        basedir = (
            os.getenv("HOME")
            + "/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/heater2D/"
        )
        filetags = [*range(0, 60, 5)]
        prefix = "".join([prefix, "/INS_Pool_Boiling_Heater_hdf5_"])
        self.filenames = [
            "".join([basedir, prefix, str(filetag).zfill(4)]) for filetag in filetags
        ]

    def test_neighbors_oneblk_2D(self):
        """
        Test if neighbors are morton order
        """
        self.customSetUp("oneblk")
        dataframes = [boxkit.read.dataset(filename) for filename in self.filenames]

        testMonitor = Monitor("test")
        testMonitor.setlimit(len(dataframes))
        monitorMsg = "run:" + self.id() + ": "

        for dataset in dataframes:

            for block in dataset.blocklist:
                self.assertEqual(
                    [None] * 6,
                    list(block.neighdict.values()),
                    "Single block data structure has no neighbors",
                )

            testMonitor.update(monitorMsg)

        for dataset in dataframes:
            dataset.purge("boxmem")

    def test_measure_bubbles_oneblk_2D(self):
        """
        Test bubble measurement
        """
        self.customSetUp("oneblk")

        dataframes = [boxkit.read.dataset(filename) for filename in self.filenames]

        process = boxkit.measure.bubbles
        process.tasks["skimeasure"]["region"].monitor = True
        print(process.tasks["skimeasure"]["region"].backend)

        bubbleframes = boxkit.measure.bubbles(dataframes, "phi")

        numbubbles = [len(listbubbles) for listbubbles in bubbleframes]

        self.assertEqual(
            numbubbles, [488, 163, 236, 236, 242, 234, 257, 223, 259, 291, 235, 223]
        )

        for dataset in dataframes:
            dataset.purge("boxmem")

    def test_measure_bubbles_blocks_2D(self):
        """
        Test bubble measurement
        """
        self.customSetUp("blocks")

        dataframes = [boxkit.read.dataset(filename) for filename in self.filenames]

        dataframes = [boxkit.create.reshaped_dataset(dataset, "phi") for dataset in dataframes]

        process = boxkit.measure.bubbles
        process.tasks["skimeasure"]["region"].monitor = True
        print(process.tasks["skimeasure"]["region"].backend)

        bubbleframes = boxkit.measure.bubbles(dataframes, "phi")

        numbubbles = [len(listbubbles) for listbubbles in bubbleframes]

        self.assertEqual(
            numbubbles, [488, 163, 236, 236, 242, 234, 257, 223, 259, 291, 235, 223]
        )

        for dataset in dataframes:
            dataset.purge("boxmem")

    def tearDown(self):
        """Clean up and timing"""
        timetest = time.time() - self.timestart

        print("%s: %.3fs\n" % (self.id(), timetest))


if __name__ == "__main__":
    unittest.main()
