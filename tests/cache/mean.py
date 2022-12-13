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

    def test_06_datasets_3D(self):
        """ """
        self.customSetUp(spacing=10)

        timer_test = Timer(self.id())

        dataframes = [
            boxkit.read_dataset(filename, storage="numpy-memmap")
            for filename in self.filenames
        ]

        nthreads = int(os.getenv("NTHREADS"))
        print(f"nthreads: {nthreads}")

        timer_mean = Timer("[mean_06_datasets]")
        mean_dataset = boxkit.mean_temporal(
            dataframes,
            ["uvel", "vvel", "wvel"],
            nthreads=nthreads,
            backend="loky",
            monitor=True,
        )
        del timer_mean

        timer_mergeblocks = Timer("[mergeblocks]")
        merged_dataset = boxkit.mergeblocks(
            mean_dataset, "vvel", nthreads=nthreads, backend="loky"
        )
        del timer_mergeblocks

        mean_dataset.purge()
        del mean_dataset

        mean = numpy.mean(merged_dataset["vvel"][:])

        merged_dataset.purge()
        del merged_dataset

        for dataset in dataframes:
            dataset.purge()

        self.assertEqual(mean, 0.1163331131117178)
        del timer_test

    def test_12_datasets_3D(self):
        """ """
        self.customSetUp(spacing=5)

        timer_test = Timer(self.id())

        dataframes = [
            boxkit.read_dataset(filename, storage="numpy-memmap")
            for filename in self.filenames
        ]

        nthreads = int(os.getenv("NTHREADS"))
        print(f"nthreads: {nthreads}")

        timer_mean = Timer("[mean_12_datasets]")
        mean_dataset = boxkit.mean_temporal(
            dataframes,
            ["uvel", "vvel", "wvel"],
            nthreads=nthreads,
            backend="loky",
            monitor=True,
        )
        del timer_mean

        timer_mergeblocks = Timer("[mergeblocks]")
        merged_dataset = boxkit.mergeblocks(
            mean_dataset, "vvel", nthreads=nthreads, backend="loky"
        )
        del timer_mergeblocks

        mean_dataset.purge()
        del mean_dataset

        mean = numpy.mean(merged_dataset["vvel"][:])

        merged_dataset.purge()
        del merged_dataset

        for dataset in dataframes:
            dataset.purge()

        self.assertEqual(mean, 0.12023532554531322)
        del timer_test

    def test_29_datasets_3D(self):
        """ """
        self.customSetUp(spacing=2)

        timer_test = Timer(self.id())

        dataframes = [
            boxkit.read_dataset(filename, storage="numpy-memmap")
            for filename in self.filenames
        ]

        nthreads = int(os.getenv("NTHREADS"))
        print(f"nthreads: {nthreads}")

        timer_mean = Timer("[mean_29_datasets]")
        mean_dataset = boxkit.mean_temporal(
            dataframes,
            ["uvel", "vvel", "wvel"],
            nthreads=nthreads,
            backend="loky",
            monitor=True,
        )
        del timer_mean

        timer_mergeblocks = Timer("[mergeblocks]")
        merged_dataset = boxkit.mergeblocks(
            mean_dataset, "vvel", nthreads=nthreads, backend="loky"
        )
        del timer_mergeblocks

        mean_dataset.purge()
        del mean_dataset

        mean = numpy.mean(merged_dataset["vvel"][:])

        merged_dataset.purge()
        del merged_dataset

        for dataset in dataframes:
            dataset.purge()

        self.assertEqual(mean, 0.12102168610938696)
        del timer_test


if __name__ == "__main__":
    unittest.main()
