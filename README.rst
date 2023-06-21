###############
 |icon| BoxKit
###############

|Code style: black|

|FlashX| |FlowX| |Minimal| |Publish| |Linting|

**********
 Overview
**********

An overview of BoxKit is available in ``paper/paper.md`` that provides a
summary and statement of need for the package. You can compile it into a
pdf by running ``make`` in the ``paper`` directory. Please note that the
``Makefile`` requires a functioning Docker service on the machine.

**************
 Installation
**************

Stable releases of BoxKit are hosted on Python Package Index website
(https://pypi.org/project/BoxKit/) and can be installed by executing,

.. code::

   pip install BoxKit --user

Note that ``pip`` should point to ``python3+`` installation package
``pip3``.

Upgrading and uninstallation is easily managed through this interface
using,

.. code::

   pip install --upgrade BoxKit --user
   pip uninstall BoxKit

Pre-release version can be installed directly from the git reposity by
executing,

.. code::

   pip install git+ssh://git@github.com/akashdhruv/BoxKit.git --user

BoxKit provides various installation options that can be used to
configure the library with desired features. Following is a list of
options,

.. code::

   with-cbox      - With C++ backend
   with-pyarrow   - With Apache Arrow data backend
   with-zarr      - With Zarr data backend
   with-dask      - With Dask data/parallel backend
   enable-testing - Enabling testing mode for development

Correspondingly, the installation command can be modified to include
necessary options as follows,

.. code::

   export CXX=$(CPP_COMPILER)
   pip install BoxKit --user --install-option="--enable-testing" --install-option="--with-cbox"

There maybe situations where users may want to install BoxKit in
development mode $\\textemdash$ to design new features, debug, or
customize classes/methods to their needs. This can be easily
accomplished using the ``setup`` script located in the project root
directory and executing,

.. code::

   ./setup develop

Development mode enables testing of features/updates directly from the
source code and is an effective method for debugging. Note that the
``setup`` script relies on ``click``, which can be installed using,

.. code::

   pip install click

*******
 Usage
*******

.. code:: python

   import boxkit

Add usage details here

**********
 Citation
**********

.. code::

   @software{akash_dhruv_2022_7255632,
     author       = {Akash Dhruv},
     title        = {akashdhruv/BoxKit: October 2022},
     month        = oct,
     year         = 2022,
     publisher    = {Zenodo},
     version      = {22.10},
     doi          = {10.5281/zenodo.7255632},
     url          = {https://doi.org/10.5281/zenodo.7255632}
   }

**************
 Contribution
**************

Developers are encouraged to fork the repository and contribute to the
source code in the form of pull requests to the ``development`` branch.
Please read ``DESIGN.rst`` for an overview of software design and
developer guide

****************
 Help & Support
****************

Please file an issue on the repository page to report bugs, request
features, and ask questions about usage

.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

.. |FlashX| image:: https://github.com/akashdhruv/BoxKit/workflows/FlashX/badge.svg

.. |FlowX| image:: https://github.com/akashdhruv/BoxKit/workflows/FlowX/badge.svg

.. |Minimal| image:: https://github.com/akashdhruv/BoxKit/workflows/Minimal/badge.svg

.. |Publish| image:: https://github.com/akashdhruv/BoxKit/workflows/Publish/badge.svg

.. |Linting| image:: https://github.com/akashdhruv/BoxKit/workflows/Linting/badge.svg

.. |icon| image:: ./media/icon.svg
   :width: 30
