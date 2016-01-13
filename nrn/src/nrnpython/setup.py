from distutils.core import setup, Extension
from distutils.sysconfig import get_python_version
import sys
import os

# specify that the data_files paths are relative to same place as python files
# from http://stackoverflow.com/questions/1612733/including-non-python-files-with-setup-py
from distutils.command.install import INSTALL_SCHEMES
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

packages=['neuron','neuron.neuroml','neuron.tests', 'neuron.rxd']
packages +=['neuron.rxd.geometry3d']

instdir = os.path.join( os.getcwd(), '..', '..' )
nrn_srcdir = os.path.join( os.getcwd(), '..', '..' )

setup(name="NEURON", version="7.4",
      description = "NEURON bindings for python",
      package_dir = {'':instdir+'/share/nrn/lib/python'},
      packages=packages,
      data_files = [('neuron', [nrn_srcdir + '/share/lib/python/neuron/help_data.dat'])],
)

