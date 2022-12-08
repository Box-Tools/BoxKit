"""Tests for `boxkit/api`."""

import os
import time
import unittest
import pymorton
import boxkit
# from boxkit.library import Monitor


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
        dataframes = [boxkit.read.Dataset(filename) for filename in self.filenames]

        # testMonitor = Monitor("test")
        # testMonitor.setlimit(len(dataframes))
        monitorMsg = "run:" + self.id() + ": "

        for dataset in dataframes:

            for block in dataset.blocklist:
                self.assertEqual(
                    [None] * 6,
                    list(block.neighdict.values()),
                    "Single block data structure has no neighbors",
                )

            # testMonitor.update(monitorMsg)

        for dataset in dataframes:
            dataset.purge("boxmem")

    def test_measure_bubbles_oneblk_2D(self):
        """
        Test bubble measurement
        """
        self.customSetUp("oneblk")

        dataframes = [boxkit.read.Dataset(filename) for filename in self.filenames]

        bubbleframes = []
        for dataset in dataframes:
            bubbleframes.append(boxkit.measure.Regionprops(dataset, "phi"))

        numbubbles = [len(listbubbles) for listbubbles in bubbleframes]

        self.assertEqual(numbubbles, [257])

        for dataset in dataframes:
            dataset.purge("boxmem")

    def tearDown(self):
        """Clean up and timing"""
        timetest = time.time() - self.timestart

        print("%s: %.3fs\n" % (self.id(), timetest))


if __name__ == "__main__":
    unittest.main()
