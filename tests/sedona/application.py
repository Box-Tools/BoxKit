import flowx
import time
import unittest
import numpy


class TestApplication(unittest.TestCase):
    """boxkit unit test for boxkit applications"""

    def test_flowx(self):
        """test flowx library"""

        print(
            f"\n-------------------------Running: {self.id()}-------------------------\n"
        )

        # Define grid parameters
        nx, ny = 448, 448
        xmin, xmax = -1, 1
        ymin, ymax = -1, 1
        xblocks, yblocks = 32, 32

        # Create flowx objects
        varlist = ["phi"]
        grid = flowx.domain.Grid(
            "cell-centered", varlist, nx, ny, xmin, xmax, ymin, ymax, xblocks, yblocks
        )

        particle_file = "/home/akash/Desktop/Akash/Workbench/FlowX/examples/imbound/levelset_mapping/sm_tshape.h5"
        particle_info = dict(input="HDF5", file=particle_file)
        particle = flowx.domain.Particles(
            particle_info, xmin, xmax, ymin, ymax, scalars=None
        )

        search_options = dict(monitor=True, nthreads=8, backend="loky")

        start = time.time()
        ites = flowx.imbound.utils.shapely_search(grid, particle, "phi", search_options)
        end = time.time()

        self.assertEqual(ites, 262144)

        print("Search time: ", end - start)

        grid.addvar("eror")
        grid.addvar("gamma")

        grid["gamma"][:, :, :, :] = grid["phi"][:, :, :, :]

        start = time.time()
        grid.halo_exchange("phi", nthreads=1, backend="serial")
        end = time.time()

        grid.compute_error("eror", "phi", "gamma")

        errors = abs(grid["gamma"][:, :, :, :] - grid["phi"][:, :, :, :])
        expected_errors = numpy.zeros(
            (
                grid.nblocks,
                grid.nzb + 2 * grid.zguard,
                grid.nyb + 2 * grid.yguard,
                grid.nxb + 2 * grid.xguard,
            )
        )

        self.assertTrue(numpy.allclose(errors, expected_errors, atol=1e-12))

        print("[fill guardcells time]: ", end - start)


if __name__ == "__main__":
    unittest.main()
