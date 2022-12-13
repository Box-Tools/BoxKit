import boxkit
import sys

sys.modules["bubblebox"] = boxkit
sys.modules["bubblebox.library.create"] = boxkit.library
sys.modules["bubblebox.library.utilities"] = boxkit.library

class MyAction(boxkit.library.Action):
      def __init__(self, unit=None, *args, **kwargs):
          super().__init__(parallel_obj=unit, *args, **kwargs)

sys.modules["bubblebox.library.utilities._action.Action"] = MyAction

import flowx
import numpy
import time


def example():

    start = time.time()

    # Define grid parameters
    nx, ny = 40, 40
    xmin, xmax = 0.0, 1.0
    ymin, ymax = 0.0, 1.0

    # Define cell-centered variable names
    center_vars = ["pres", "divv", "asol", "eror", "delp"]
    face_vars = ["velc", "hvar", "asol", "eror"]
    ins_vars = ["velc", "hvar", "divv", "pres", "delp"]
    poisson_vars = ["delp", "divv"]

    scalar_info = dict(tmax=10, dt=0.001, Re=100.0)

    simulation_info = dict(time_stepping="ab2", poisson_solver="superlu", with_ib=False)

    # Define boundary conditions for variable pressure and velocity [left, right, bottom, top]
    bc_type_center = dict(delp=["neumann", "neumann", "neumann", "neumann"])
    bc_val_center = dict(delp=[0.0, 0.0, 0.0, 0.0])

    bc_type_facex = dict(velc=["dirichlet", "dirichlet", "dirichlet", "dirichlet"])
    bc_val_facex = dict(velc=[0.0, 0.0, 0.0, 1.0])

    bc_type_facey = dict(velc=["dirichlet", "dirichlet", "dirichlet", "dirichlet"])
    bc_val_facey = dict(velc=[0.0, 0.0, 0.0, 0.0])

    gridc, gridx, gridy, scalars, particles = flowx.domain.Domain(
        nx,
        ny,
        xmin,
        xmax,
        ymin,
        ymax,
        center_vars,
        face_vars,
        scalar_info,
        bc_type_center=bc_type_center,
        bc_val_center=bc_val_center,
        bc_type_facex=bc_type_facex,
        bc_val_facex=bc_val_facex,
        bc_type_facey=bc_type_facey,
        bc_val_facey=bc_val_facey,
    )

    domain_data_struct = [gridc, gridx, gridy, scalars, particles]

    poisson = flowx.poisson.Poisson(gridc, poisson_vars, simulation_info)
    imbound = flowx.imbound.ImBound(imbound_info=simulation_info)
    ins = flowx.ins.IncompNS(
        poisson, imbound, domain_data_struct, ins_vars, simulation_info
    )

    while scalars.time <= scalars.tmax:

        ins.advance()

        # Display stats
        if scalars.nstep % 10 == 0:
            flowx.io.display_stats(scalars)

        scalars.advance()

    end = time.time()

    print("Simulation time: ", end - start)

    maxdivv, mindivv = numpy.max(gridc["divv"]), numpy.min(gridc["divv"])

    if abs(maxdivv) <= 1e-11 and abs(mindivv) <= 1e-11 and maxdivv * mindivv < 0.0:
        print("Divergence is within tolerance")
    else:
        raise ValueError("Divergence is not within tolerance")


if __name__ == "__main__":
    example()
