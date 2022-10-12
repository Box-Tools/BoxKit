BoxKit
=========

|Code style: black|

|FlashX| |FlowX| |Minimal| |Publish|

Introduction
------------

BoxKit is a library that provides building blocks to parallelize and scale data science, high performance computing, and machine learning applications for block-structured spatial datasets. 

Spatial data from simulations and experiments can be organized and managed using the tools available in this library. 

The library is designed into two broad categories:

**CREATE** - contains classes/structures to store spatial data in a rectangular/cubic frame, along with auxillary tools to manage irregular geometries composed of unstructured triangular mesh.

**UTILITIES** - contains classes/structures to improve memory managment of data on NUMA nodes.

This library is designed to facilitate the use of scientific datasets with more data analysis oriented packages.

Installation
------------

Using Python Package Index (PyPI)
::
   pip3 install BoxKit

Development mode
::
   pip3 install click && ./setup develop

.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
.. |FlashX| image:: https://github.com/akashdhruv/BoxKit/workflows/FlashX/badge.svg
.. |FlowX| image:: https://github.com/akashdhruv/BoxKit/workflows/FlowX/badge.svg
.. |Minimal| image:: https://github.com/akashdhruv/BoxKit/workflows/Minimal/badge.svg
.. |Publish| image:: https://github.com/akashdhruv/BoxKit/workflows/Publish/badge.svg
