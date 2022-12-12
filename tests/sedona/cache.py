"""Tests for `boxkit/api`."""

import os
import time
import unittest
import pymorton
import tqdm
import numpy
import h5py

from progress.spinner import PieSpinner as Spinner

import boxkit
from boxkit.library import Timer, Action, Dataset


class TestCache(unittest.TestCase):
    """boxkit unit test for 3D boiling data"""

    def customSetUp(self, basedir):
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
            + f"/Box/Jarvis-DataShare/Bubble-Box-Sample/boiling-earth/domain3D/{basedir}/"
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

        self.spinner = Spinner("")

    def test_01_optimized_3D(self):
        """
        Test optimize implementation
        """
        self.customSetUp("not-chunked")

        dataframes = [
            boxkit.read_dataset(filename, storage="numpy")
            for filename in self.filenames
        ]

        for dataset, mean_ref in zip(dataframes, self.mean_refs):

            timer_mergeblock_opt = Timer("[mergblocks.optimized]")

            merged_dataset = boxkit.mergeblocks(
                dataset,
                ["uvel", "vvel", "wvel", "temp", "phi"],
                nthreads=8,
                backend="loky",
                monitor=False,
            )

            del timer_mergeblock_opt

            self.assertEqual(numpy.mean(merged_dataset["vvel"][:]), mean_ref)

            merged_dataset.purge()
            del merged_dataset

        for dataset in dataframes:
            dataset.purge()

    def test_02_naive_3D(self):
        """
        Test naiver implementation
        """
        self.customSetUp("not-chunked")

        dataframes = [h5py.File(filename, "r") for filename in self.filenames]

        for dataset, mean_ref in zip(dataframes, self.mean_refs):

            timer_mergeblocks_naive = Timer("[mergeblocks.naive]")

            nxb, nyb, nzb = dataset["sizebox"][:]
            nblockx, nblocky, nblockz = dataset["numbox"][:]

            merged_uvel = numpy.zeros([nblockz * nzb, nblocky * nyb, nblockx * nxb])
            merged_vvel = numpy.zeros_like(merged_uvel)
            merged_wvel = numpy.zeros_like(merged_uvel)
            merged_temp = numpy.zeros_like(merged_uvel)
            merged_phi = numpy.zeros_like(merged_uvel)

            for lblock in range(nblockx * nblocky * nblockz):
                iloc, jloc, kloc = pymorton.deinterleave3(lblock)

                merged_uvel[
                    nzb * kloc : nzb * (kloc + 1),
                    nyb * jloc : nyb * (jloc + 1),
                    nxb * iloc : nxb * (iloc + 1),
                ] = dataset["quantities"]["uvel"][lblock, :, :, :]

                merged_vvel[
                    nzb * kloc : nzb * (kloc + 1),
                    nyb * jloc : nyb * (jloc + 1),
                    nxb * iloc : nxb * (iloc + 1),
                ] = dataset["quantities"]["vvel"][lblock, :, :, :]

                merged_wvel[
                    nzb * kloc : nzb * (kloc + 1),
                    nyb * jloc : nyb * (jloc + 1),
                    nxb * iloc : nxb * (iloc + 1),
                ] = dataset["quantities"]["wvel"][lblock, :, :, :]

                merged_temp[
                    nzb * kloc : nzb * (kloc + 1),
                    nyb * jloc : nyb * (jloc + 1),
                    nxb * iloc : nxb * (iloc + 1),
                ] = dataset["quantities"]["temp"][lblock, :, :, :]

                merged_phi[
                    nzb * kloc : nzb * (kloc + 1),
                    nyb * jloc : nyb * (jloc + 1),
                    nxb * iloc : nxb * (iloc + 1),
                ] = dataset["quantities"]["phi"][lblock, :, :, :]

                self.spinner.next()
            del timer_mergeblocks_naive

            self.assertEqual(numpy.mean(merged_vvel[:]), mean_ref)
            del merged_uvel, merged_vvel, merged_wvel

    def test_03_naive_blk_dset_3D(self):
        """
        Test naiver implementation
        """
        self.customSetUp("block-dset")

        dataframes = [h5py.File(filename, "r") for filename in self.filenames]

        for dataset, mean_ref in zip(dataframes, self.mean_refs):

            timer_mergeblocks_naive = Timer("[mergeblocks.naive]")

            nxb, nyb, nzb = dataset["sizebox"][:]
            nblockx, nblocky, nblockz = dataset["numbox"][:]

            merged_uvel = numpy.zeros([nblockz * nzb, nblocky * nyb, nblockx * nxb])
            merged_vvel = numpy.zeros_like(merged_uvel)
            merged_wvel = numpy.zeros_like(merged_uvel)
            merged_temp = numpy.zeros_like(merged_uvel)
            merged_phi = numpy.zeros_like(merged_uvel)

            for lblock in range(nblockx * nblocky * nblockz):
                iloc, jloc, kloc = pymorton.deinterleave3(lblock)

                merged_uvel[
                    nzb * kloc : nzb * (kloc + 1),
                    nyb * jloc : nyb * (jloc + 1),
                    nxb * iloc : nxb * (iloc + 1),
                ] = dataset["quantities"]["uvel"][str(lblock)][:, :, :]

                merged_vvel[
                    nzb * kloc : nzb * (kloc + 1),
                    nyb * jloc : nyb * (jloc + 1),
                    nxb * iloc : nxb * (iloc + 1),
                ] = dataset["quantities"]["vvel"][str(lblock)][:, :, :]

                merged_wvel[
                    nzb * kloc : nzb * (kloc + 1),
                    nyb * jloc : nyb * (jloc + 1),
                    nxb * iloc : nxb * (iloc + 1),
                ] = dataset["quantities"]["wvel"][str(lblock)][:, :, :]

                merged_temp[
                    nzb * kloc : nzb * (kloc + 1),
                    nyb * jloc : nyb * (jloc + 1),
                    nxb * iloc : nxb * (iloc + 1),
                ] = dataset["quantities"]["temp"][str(lblock)][:, :, :]

                merged_phi[
                    nzb * kloc : nzb * (kloc + 1),
                    nyb * jloc : nyb * (jloc + 1),
                    nxb * iloc : nxb * (iloc + 1),
                ] = dataset["quantities"]["phi"][str(lblock)][:, :, :]

                self.spinner.next()
            del timer_mergeblocks_naive

            self.assertEqual(numpy.mean(merged_vvel[:]), mean_ref)
            del merged_uvel, merged_vvel, merged_wvel

    def tearDown(self):
        """Clean up and timing"""
        self.spinner.finish()
        del self.timer


if __name__ == "__main__":
    unittest.main()
