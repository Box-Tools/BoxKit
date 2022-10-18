.. |icon| image:: ./icon.svg
  :width: 30
 
=============
|icon| BoxKit
=============

|Code style: black|

|FlashX| |FlowX| |Minimal| |Publish|

BoxKit is a library that provides building blocks to parallelize and scale data science, high performance computing, and machine learning applications for block-structured datasets. Spatial data from simulations and experiments can be organized and managed using the tools available in this library. 

Organization
------------

The library is designed into two broad categories:

Create
======

Interface containing classes/structures to store spatial data in a rectangular/cubic frame, along with auxillary tools to manage irregular geometries composed of unstructured triangular mesh.

Utilities
=========

Interface containing classes/structures to improve memory managment of data on NUMA nodes.

This library is designed to facilitate the use of scientific datasets with more data analysis oriented packages.

Installation
------------

Stable releases of BoxKit are hosted on Python Package Index website (`<https://pypi.org/project/BoxKit/>`_) and can be installed by executing,

::

   pip install BoxKit
   
Note that ``pip`` should point to ``python3+`` installation package ``pip3``. 

Upgrading and uninstallation is easily managed through this interface using,

::

   pip install --upgrade BoxKit
   pip uninstall BoxKit

There maybe situations where users may want to install BoxKit in development mode $\\textemdash$ to design new features, debug, or customize classes/methods to their needs. This can be easily accomplished using the ``setup`` script located in the project root directory and executing,

::

   ./setup develop

Development mode enables testing of features/updates directly from the source code and is an effective method for debugging. Note that the ``setup`` script relies on ``click``, which can be installed using,

::

  pip install click


.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   
.. |FlashX| image:: https://github.com/akashdhruv/BoxKit/workflows/FlashX/badge.svg
.. |FlowX| image:: https://github.com/akashdhruv/BoxKit/workflows/FlowX/badge.svg
.. |Minimal| image:: https://github.com/akashdhruv/BoxKit/workflows/Minimal/badge.svg
.. |Publish| image:: https://github.com/akashdhruv/BoxKit/workflows/Publish/badge.svg
