import os

basedir = os.getenv('PWD')

# checkout dependencies
os.system('git submodule update --init {0}/tools/indicators'.format(basedir))
