"""Tests for `boxkit/api`."""

import os
import time
import unittest
import pymorton
import tqdm
import numpy
import h5py

import boxkit
from boxkit.library import Timer, Action, Dataset


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
        print(
            f"\n-------------------------Running: {self.id()}-------------------------\n"
        )

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

        self.mean_refs = [
            0.09109748979981146,
            0.0997722935402521,
            0.11196033087810948,
            0.11828425437773828,
            0.12960478109109547,
            0.1472795289832985,
        ]

    def test_optimized_3D(self):
        """
        Test optimize implementation
        """
        dataframes = [
            boxkit.read_dataset(filename, storage="numpy-memmap")
            for filename in self.filenames
        ]

        for dataset, mean_ref in zip(dataframes, self.mean_refs):

            timer_mergeblock_opt = Timer("[mergblocks.optimized]")
            merged_dataset = boxkit.mergeblocks(
                dataset, "vvel", nthreads=8, backend="loky"
            )
            del timer_mergeblock_opt

            self.assertEqual(numpy.mean(merged_dataset["vvel"][:]), mean_ref)

            del merged_dataset

    def test_naive_3D(self):
        """
        Test naiver implementation
        """
        dataframes = [h5py.File(filename, "r") for filename in self.filenames]

        for dataset, mean_ref in zip(dataframes, self.mean_refs):

            timer_mergeblocks_naive = Timer("[mergeblocks.naive]")

            nblocks, nxb, nyb, nzb = dataset["quantities"]["vvel"].shape
            nblockx = int(numpy.cbrt(nblocks))
            nblocky = nblockx
            nblockz = nblockx

            merged_dataset = numpy.zeros([nblockz * nzb, nblocky * nyb, nblockx * nxb])
            vvel = numpy.array(dataset["quantities"]["vvel"][:])

            for lblock in range(nblocks):
                iloc, jloc, kloc = pymorton.deinterleave3(lblock)

                merged_dataset[
                    nzb * kloc : nzb * (kloc + 1),
                    nyb * jloc : nyb * (jloc + 1),
                    nxb * iloc : nxb * (iloc + 1),
                ] = vvel[lblock, :, :, :]

            del timer_mergeblocks_naive

            self.assertEqual(numpy.mean(merged_dataset[:]), mean_ref)

    def tearDown(self):
        """Clean up and timing"""
        del self.timer


if __name__ == "__main__":
    unittest.main()
