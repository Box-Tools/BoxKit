"""Tests for `boxkit/api`."""

import os
import time
import unittest
import pymorton
import numpy
import boxkit
from boxkit.library import Monitor, Timer


class TestAstrophysics(unittest.TestCase):
    """boxkit unit test for 3D astrophysics data"""

    def setUp(self):
        """
        Setup test parameters

        timestart : tag start time
        basedir   : base directory of the input data
        filetags  : list of file tags
        prefix    : prefix for input file
        filenames : list of filenames generated from basedir, prefix and filetags

        """
        print(
            f"\n-------------------------Running: {self.id()}-------------------------\n"
        )
        self.timer = Timer(self.id())

        basedir = (
            os.getenv("HOME") + "/Box/Jarvis-DataShare/Bubble-Box-Sample/astrophysics/"
        )
        filetags = [1000]
        prefix = "25m_3d_32km_hdf5_plt_cnt_"
        self.filenames = [
            "".join([basedir, prefix, str(filetag).zfill(4)]) for filetag in filetags
        ]

    # def test_read_nthreads_4_3D(self):
    #    """
    #    Test read dataset with 4 threads
    #    """
    #    dataframes = [
    #        boxkit.read_dataset(
    #            filename, source="flash", nthreads=4, backend="loky", monitor=True
    #        )
    #        for filename in self.filenames
    #    ]
    #    for dataset in dataframes:
    #        dataset.purge()

    def test_read_nthreads_12_3D(self):
        """
        Test read dataset with 12 threads
        """
        dataframes = [
            boxkit.read_dataset(
                filename, source="flash", nthreads=12, backend="loky", monitor=True
            )
            for filename in self.filenames
        ]
        for dataset in dataframes:
            dataset.purge()

    def tearDown(self):
        """Clean up and timing"""
        del self.timer


if __name__ == "__main__":
    unittest.main()
