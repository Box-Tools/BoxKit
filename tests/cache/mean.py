"""Tests for `boxkit/api`."""

import os
import unittest
import pymorton
import numpy
import h5py
import boxkit
from boxkit.library import Timer, Action, Dataset


class TestMean(unittest.TestCase):
    """boxkit unit test for 3D boiling data"""

    def customSetUp(self, spacing=10):
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

        if os.getenv("SITE") == "sedona":
            basedir = (
                os.getenv("HOME")
                + f"/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/domain3D/not-chunked/"
            )

        elif os.getenv("SITE") == "summit":
            basedir = "/gpfs/alpine/ast136/proj-shared/adhruv/Boxkit/"

        else:
            raise NotImplementedError

        filetags = [*range(0, 58, spacing)]
        prefix = "INS_Pool_Boiling_hdf5_"
        self.filenames = [
            "".join([basedir, prefix, str(filetag).zfill(4)]) for filetag in filetags
        ]

    def test_spacing_10_3D(self):
        """ """
        self.customSetUp(spacing=10)

        timer_test = Timer(self.id())

        dataframes = [
            boxkit.read_dataset(filename, storage="numpy-memmap")
            for filename in self.filenames
        ]

        nthreads = int(os.getenv("NTHREADS"))
        print(f"nthreads: {nthreads}")

        timer_mean_serial = Timer("[mergblocks.optimized]")

        mean_dataset = boxkit.mean_temporal(
            dataframes,
            "vvel",
            nthreads=nthreads,
            backend="loky",
        )

        del timer_mean_serial

        mean = numpy.mean(mean_dataset["vvel"][:])

        mean_dataset.purge()
        del mean_dataset

        for dataset in dataframes:
            dataset.purge()

        self.assertEqual(mean, 0.1163331131117178)
        del timer_test

    def test_spacing_5_3D(self):
        """ """
        self.customSetUp(spacing=5)

        timer_test = Timer(self.id())

        dataframes = [
            boxkit.read_dataset(filename, storage="numpy-memmap")
            for filename in self.filenames
        ]

        nthreads = int(os.getenv("NTHREADS"))
        print(f"nthreads: {nthreads}")

        timer_mean_serial = Timer("[mergblocks.optimized]")

        mean_dataset = boxkit.mean_temporal(
            dataframes,
            "vvel",
            nthreads=nthreads,
            backend="loky",
        )

        del timer_mean_serial

        mean = numpy.mean(mean_dataset["vvel"][:])

        mean_dataset.purge()
        del mean_dataset

        for dataset in dataframes:
            dataset.purge()

        self.assertEqual(mean, 0.12023532554531322)
        del timer_test


if __name__ == "__main__":
    unittest.main()
