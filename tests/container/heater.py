"""Tests for `boxkit/api/flow`."""

import os
import time
import unittest
import pymorton
import boxkit
from boxkit.library import Monitor, Timer


class TestHeater(unittest.TestCase):
    """boxkit unit test for 2D Heater Data"""

    def customSetUp(self, prefix=""):
        """
        Setup test parameters

        timestart : tag start time
        basedir   : base directory of the input data
        filetags  : list of file tags
        prefix    : prefix for input file
        filenames : list of filenames generated from basedir, prefix and filetags

        """
        self.timer = Timer(self.id())

        basedir = "/home/data/boiling-earth/heater2D/"
        filetags = [*range(0, 60, 5)]
        prefix = "".join([prefix, "/INS_Pool_Boiling_Heater_hdf5_"])
        self.filenames = [
            "".join([basedir, prefix, str(filetag).zfill(4)]) for filetag in filetags
        ]

    def test_neighbors_blocks_2D(self):
        """
        Test if neighbors are in morton order
        """
        self.customSetUp()
        dataframes = [boxkit.read_dataset(filename) for filename in self.filenames]

        testMonitor = Monitor(
            msg_="run:" + self.id() + ": ", max_=len(dataframes), type_="test"
        )

        for dataset in dataframes:

            taglist = [*range(0, dataset.nblocks)]

            for tag, block in zip(taglist, dataset.blocklist):

                locations = ["xlow", "xhigh", "ylow", "yhigh", "zlow", "zhigh"]
                neighdict = dict(zip(locations, [None] * 6))

                iloc, jloc = pymorton.deinterleave2(tag)

                neighlist = [
                    pymorton.interleave(iloc - 1, jloc),
                    pymorton.interleave(iloc + 1, jloc),
                    pymorton.interleave(iloc, jloc - 1),
                    pymorton.interleave(iloc, jloc + 1),
                ]

                neighlist = [
                    None if neighbor > dataset.nblocks - 1 else neighbor
                    for neighbor in neighlist
                ]

                neighdict["xlow"] = neighlist[0]
                neighdict["xhigh"] = neighlist[1]
                neighdict["zlow"] = neighlist[2]
                neighdict["zhigh"] = neighlist[3]

                self.assertEqual(
                    neighdict,
                    block.neighdict,
                    "Neigbhors are inconsitent with morton order",
                )

            testMonitor.update()
        testMonitor.finish()

        for dataset in dataframes:
            dataset.purge("boxmem")

    def test_regionprops_blocks_2D(self):
        """
        Test bubble measurement
        """
        self.customSetUp()

        dataframes = [boxkit.read_dataset(filename) for filename in self.filenames]
        dataframes = [boxkit.mergeblocks(dataset, "phi") for dataset in dataframes]
        bubbleframes = [boxkit.regionprops(dataset, "phi") for dataset in dataframes]

        numbubbles = [len(listbubbles) for listbubbles in bubbleframes]

        self.assertEqual(
            numbubbles, [488, 163, 236, 236, 242, 234, 257, 223, 259, 291, 235, 223]
        )

        for dataset in dataframes:
            dataset.purge("boxmem")

    def tearDown(self):
        """Clean up and timing"""
        del self.timer


if __name__ == "__main__":
    unittest.main()
