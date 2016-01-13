#setup.py
from distutils.core import setup, Extension
from distutils.sysconfig import get_python_version

import sys
import os

# NRNPYTHON_DEFINES which were enabled at configure time
extern_defines = ""
nrnpython_exec = "/usr/bin/python"
nrnpython_pyver = "2.7"
nrn_srcdir = "."
build_rx3d = 1
ivlibdir = "/home/dilawars/Work/GITHUB/Packages/neuron-sim/_iv/x86_64/lib"
if ivlibdir == "" :
    ivlibdir = '.'

destdir = os.getenv("DESTDIR")
if not destdir:
  destdir = ""

instdir = destdir + "/home/dilawars/Work/GITHUB/Packages/neuron-sim/_nrn"
if nrn_srcdir[0] != '/' :
    nrn_srcdir = '../../' + nrn_srcdir

if nrnpython_pyver!=get_python_version():
    print "Error:"
    print "NEURON configure time python: "+nrnpython_exec+"  "+ nrnpython_pyver
    print "Python presently executing setup.py: "+sys.executable+"   "+ get_python_version()
    print "These do not match, and they should!"


## ldefs = extern_defines.split('-D')
##
### if using MPI then at least for linking need special paths and libraries
##mpicc_bin = "gcc"
##mpicxx_bin = "g++"
##import os
##os.environ["CC"]=mpicc_bin
##os.environ["CXX"]=mpicxx_bin
##
# apparently we do not need the following
#################################
## following http://code.google.com/p/maroonmpi/wiki/Installation
## hack into distutils to replace the compiler in "linker_so" with mpicxx_bin
#
#import distutils
#import distutils.unixccompiler
#
#class MPI_UnixCCompiler(distutils.unixccompiler.UnixCCompiler):
#    __set_executable = distutils.unixccompiler.UnixCCompiler.set_executable
#
#    def set_executable(self,key,value):
#	print "MPI_UnixCCompiler ", key, " | ", value
#        if key == 'linker_so' and type(value) == str:
#            value = mpicxx_bin + ' ' + ' '.join(value.split()[1:])
#
#        return self.__set_executable(key,value)
#    
#distutils.unixccompiler.UnixCCompiler = MPI_UnixCCompiler
#################################

include_dirs = [nrn_srcdir+'/src/oc', '../oc', nrn_srcdir+'/src/nrnmpi']
defines = []

libdirs = [destdir + "/home/dilawars/Work/GITHUB/Packages/neuron-sim/_nrn/x86_64/lib64 -L/home/dilawars/Work/GITHUB/Packages/neuron-sim/_nrn/x86_64/lib",
  ivlibdir
]
# epre='-Wl,-R'



hoc_module = Extension(
      "neuron.hoc",
      ["inithoc.cpp"],
      library_dirs=libdirs,
      # extra_link_args = [ epre+libdirs[0],epre+libdirs[1] ],
      #extra_objects = [],
      libraries = [
	"nrnpython",
        "nrnoc", "oc", "nrniv", "ivoc",
        "memacs",
	"meschach", "neuron_gnu",
	"nrnmpi",
        "scopmath", "sparse13", "sundials",
	"readline",
	"IVhines",
      ],
      include_dirs = include_dirs,
      define_macros=defines
    )

# specify that the data_files paths are relative to same place as python files
# from http://stackoverflow.com/questions/1612733/including-non-python-files-with-setup-py
from distutils.command.install import INSTALL_SCHEMES
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

ext_modules = [hoc_module]
if build_rx3d:
  try:
    import numpy
    # TODO: do we need to use os.path.join?
    src_path = nrn_srcdir + '/share/lib/python/neuron/rxd/geometry3d/'
    build_path = '../../share/lib/python/neuron/rxd/geometry3d/'
    include_dirs = [nrn_srcdir + '/share/lib/python/neuron/rxd/geometry3d', '.', numpy.get_include()]
    ext_modules=[hoc_module,
                   Extension("neuron.rxd.geometry3d.graphicsPrimitives",
                             sources=[build_path + "graphicsPrimitives.cpp"],
                             include_dirs=include_dirs),
                   Extension("neuron.rxd.geometry3d.ctng",
                             sources=[build_path + "ctng.cpp"],
                             include_dirs=include_dirs),
                   Extension("neuron.rxd.geometry3d.surfaces",
                             sources=[build_path + "surfaces.cpp", src_path + "marching_cubes2.c", src_path + "llgramarea.c"],
                             include_dirs=include_dirs)]    
  except:
    pass

packages=['neuron','neuron.neuroml','neuron.tests', 'neuron.rxd']
if build_rx3d:
  packages +=['neuron.rxd.geometry3d']

setup(name="NEURON", version="7.4",
      description = "NEURON bindings for python",
      package_dir = {'':instdir+'/share/nrn/lib/python'},
      packages=packages,
      data_files = [('neuron', [nrn_srcdir + '/share/lib/python/neuron/help_data.dat'])],
      ext_modules=ext_modules
)

