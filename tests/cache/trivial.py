import numpy
from boxkit.library import Action, Timer


@Action(parallel_obj=float, backend="serial", nthreads=1, monitor=True)
def multiply(parallel_obj):
    return parallel_obj * 10


array_size = 1000000
array = numpy.linspace(0.0, 1e6, int(array_size))

timer = Timer(f"serial")
result_serial = multiply(array.tolist())
del timer

nthreads = 1
multiply.nthreads = nthreads
multiply.backend = "loky"
timer = Timer(f"loky-[nthreads: {nthreads}]")
result_parallel = multiply(array.tolist())
del timer
if not (result_serial == result_parallel):
    raise ValueError

nthreads = 2
multiply.nthreads = nthreads
multiply.backend = "loky"
timer = Timer(f"loky-[nthreads: {nthreads}]")
result_parallel = multiply(array.tolist())
del timer
if not (result_serial == result_parallel):
    raise ValueError

nthreads = 4
multiply.nthreads = nthreads
timer = Timer(f"loky-[nthreads: {nthreads}]")
result_parallel = multiply(array.tolist())
del timer
if not (result_serial == result_parallel):
    raise ValueError

nthreads = 8
multiply.nthreads = nthreads
timer = Timer(f"loky-[nthreads: {nthreads}]")
result_parallel = multiply(array.tolist())
del timer
if not (result_serial == result_parallel):
    raise ValueError
