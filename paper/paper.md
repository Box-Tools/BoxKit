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
    affiliation: 1
affiliations:
 - name: Argonne National Laboratory, USA
   index: 1
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
simulation output stored in HDF5 files and provide metadata for AMR blocks. 

This library has been exercised for data analysis and machine learning applications
in recent work [@DHRUV2023; @HASSAN2023] 

![BoxKit is designed to integrate simulation software instruments like Flash-X 
with Python-based machine learning and data analysis packages. Large simulation 
datasets (~TB) can leverage BoxKit to improve performance of offline training/analysis. 
This mechanism is part of a broader workflow to  integrate simulations with machine 
learning using a Fortran-Python bridge shown with dotted lines. \label{fig:workflow}](../media/workflow.png)


# Mathematics

Single dollars ($) are required for inline mathematics e.g. $f(x) = e^{\pi/x}$

Double dollars make self-standing equations:

$$\Theta(x) = \left\{\begin{array}{l}
0\textrm{ if } x < 0\cr
1\textrm{ else}
\end{array}\right.$$

You can also use plain \LaTeX for equations
\begin{equation}\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}
and refer to \autoref{eq:fourier} from text.

# Acknowledgements

We acknowledge contributions from Laboratory Directed Research and Development
(LDRD) program supported by Argonne National Laboratory.

# References
