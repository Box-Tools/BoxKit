"""Build and installation script for BubbleBox."""

# standard libraries
import re
from setuptools import setup, find_packages

# get long description from README.rst
with open('README.rst', mode='r') as readme:
    long_description = readme.read()

with open('bubblebox/__meta__.py', mode='r') as source:
    content = source.read().strip()
    metadata = {key: re.search(key + r'\s*=\s*[\'"]([^\'"]*)[\'"]', content).group(1)
                for key in ['__pkgname__', '__version__', '__authors__',
                            '__license__', '__description__']}

# core dependancies
DEPENDENCIES = ['numpy',    'h5py', 'h5pickle', 'pymorton', 'scikit-image', 
                'progress', 'dask', 'pyarrow',  'joblib',   'distributed', 'tqdm']

setup(
    name                 = metadata['__pkgname__'],
    version              = metadata['__version__'],
    author               = metadata['__authors__'],
    description          = metadata['__description__'],
    license              = metadata['__license__'],
    packages             = find_packages(where='./'),
    package_dir          = {'': './'},
    include_package_data = True,
    long_description     = long_description,
    classifiers          = ['Programming Language :: Python :: 3.8',
                            'License :: OSI Approved :: MIT License', ],
    install_requires     = DEPENDENCIES)
