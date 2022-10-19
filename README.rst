.. |icon| image:: ./media/icon.svg
  :width: 30
 
=============
|icon| BoxKit
=============

|Code style: black|

|FlashX| |FlowX| |Minimal| |Publish|

BoxKit is a library that provides building blocks to parallelize and scale data science, high performance computing, and machine learning applications for block-structured datasets. Spatial data from simulations and experiments can be accessed and managed using tools available in this library when working with more data analysis oriented packages like SciKit (https://github.com/scikit-learn/scikit-learn) and FlowNet (https://github.com/NVIDIA/flownet2-pytorch)

Installation
============

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
  
Usage
=====

BoxKit is undergoing active development and therefore design changes are frequent, however, the library is divided into two broad categories:

- **Create**: Containing interface for classes/methods to store spatial data in a rectangular/cubic frame, along with auxillary tools to manage irregular geometries composed of unstructured triangular mesh.

- **Utilities**: Containing interface for classes/method to improve memory managment of data on NUMA nodes.

We are currently setting up use cases for BoxKit, and will update this section when we are able to demonstrate proof-of-concept.


Help & Support
==============

Please file an issue on the repository page


.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   
.. |FlashX| image:: https://github.com/akashdhruv/BoxKit/workflows/FlashX/badge.svg
.. |FlowX| image:: https://github.com/akashdhruv/BoxKit/workflows/FlowX/badge.svg
.. |Minimal| image:: https://github.com/akashdhruv/BoxKit/workflows/Minimal/badge.svg
.. |Publish| image:: https://github.com/akashdhruv/BoxKit/workflows/Publish/badge.svg
