"""Tests for `boxkit/api`."""

import os
import time
import unittest
import pymorton
import boxkit
from boxkit.library import Monitor, Timer


class TestCache(unittest.TestCase):
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
        filetags = [*range(0, 58, 10)]
        prefix = "INS_Pool_Boiling_hdf5_"
        self.filenames = [
            "".join([basedir, prefix, str(filetag).zfill(4)]) for filetag in filetags
        ]

    def test_cache_3D(self):
        """
        Test reshape
        """
        dataframes = [
            boxkit.read_dataset(filename, storage="numpy-memmap")
            for filename in self.filenames
        ]

        average_dataset = boxkit.mean_temporal(dataframes, "vvel", nthreads=8, backend="loky", monitor=True)

        for dataset in dataframes:
            dataset.purge("boxmem")

        average_dataset.purge("boxmem")

    def tearDown(self):
        """Clean up and timing"""
        del self.timer

if __name__ == "__main__":
    unittest.main()
