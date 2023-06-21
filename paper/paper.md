---
title: 'BoxKit: A Python library to manage analysis of block-structured simulation datasets'
tags:
  - Python
  - block structured datasets
  - simulation analysis
  - machine learning
  - performance optimization
authors:
  - name: Akash Dhruv
    orcid: 0000-0003-4997-321X
affiliations:
 - name: Argonne National Laboratory, USA
date: 15 June 2023
bibliography: paper.bib
---

# Summary

BoxKit is a library that provides building blocks to parallelize and 
scale data science, statistical analysis, and machine learning
applications for block-structured datasets. Spatial data from
simulations can be accessed and managed using tools
available in this library when working with Python-based
packages like SciKit, PyTorch, and OpticalFlow.

The library provides a Python interface to efficiently access Adaptive 
Mesh Refinement (AMR) data typical of simulation outputs, and leverages
multiprocessing libraries like JobLib and Dask to scale analysis on 
Non-Uniform Memory Access (NUMA) and distributed computing architectures.

# Statement of need

Simulation sofware instruments like Flash-X [@DUBEY2022] store output in 
the form of Hierarchical Data Format (HDF5) datasets. Each dataset is often
terabytes (TB) in size and requires cache efficient techniques to enable its 
integration with Python packages. BoxKit datastructures act as a wrapper around 
simulation output stored in HDF5 files and provide metadata for AMR blocks that 
describe the simulation domain. The wrapper objects are lightweight in nature and
represent chunks of data stored on disk, acting as array like input for Python
functions/methods. This approach allows for selective loading of data from disk to
memory in form of chunks/blocks which improves cache efficiency. The library also enables 
creation of new datasets for data-intensive workflows, and can be extended beyond its current 
application to numerical simulations.

![BoxKit is designed to integrate simulation software instruments like Flash-X 
with Python-based machine learning and data analysis packages. Large simulation 
datasets (~TB) can leverage BoxKit to improve performance of offline training/analysis. 
This mechanism is part of a broader workflow to  integrate simulations with machine 
learning using a Fortran-Python bridge shown with dotted lines. \label{fig:workflow}](../media/workflow.png)

BoxKit also offers wrappers to scale the process of deploying workflows on NUMA and distributed
computing architectures by providing decorators that can parallelize Python operations over a
single datastructure to operate over a list. This can be understood better using the 
workflow described in Figure \autoref{fig:workflow} that has been applied to data analysis and 
machine learning applications in chemical and thermal science engineering [@DHRUV2023; @HASSAN2023].
Output from Flash-X boiling simulations is created and stored on multinode clusters. Processing 
this output through BoxKit allows for scaling a simple operation over block to a list of blocks as
shown below,

```python

# Decorate function on a block with desired configuration for parallelization
@Action(num_procs, parallel_backend)
def operation_on_block(block, *args):
    pass

# Call the function with list of blocks as the first argument
operation_on_block((block for block in list_of_blocks), *args)
```

The `Action` wrapperer converts the function, `operation_on_block`, into a parallel method which 
can be deployed on a multinode cluster with the desired backend (JobLib/Dask). BoxKit does not
interfere with parallelization schema of target applications like SciKit, OpticalFlow, and PyTorch 
which function independently using available resources.

We aim to use BoxKit as part of a broader workflow that integrates Fortran/C++ based applications
with state-of-art machine learning packages available in Python, described using dotted line in 
Figure \autoref{fig:workflow}.

# Acknowledgements

We acknowledge contributions from Laboratory Directed Research and Development
(LDRD) program supported by Argonne National Laboratory [@argonne].

# References
