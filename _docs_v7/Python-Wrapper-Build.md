---
title: Python Wrapper Build
permalink: /docs_v7/Python-Wrapper-Build/
---

It is recommended to read the information at [Build from Source](/docs_v7/Build-from-Source/) first prior reading this section.

In order to use the Python Wrapper of SU2, an additional compilation step is required. The wrapper is based on the CDriver structure of SU2 and the compilation is performed with [Swig](http://www.swig.org/) that is required to be installed on your system. For a parallel build, Python bindings for MPI are also required. We recommend to use [mpi4py](https://pythonhosted.org/mpi4py/usrman/). You will find a few notes that will help you install the required packages at the end of this tutorial.

## Configuration with the Python wrapper
The Py wrapper build configuration is still based on the `configure` script but has to be enabled by adding the option `--enable-PY_WRAPPER`. 

### Example for Linux
To configure a parallel build in a specified location with the Python wrapper, the command should be:

    $ ./configure --prefix=/path/to/install/SU2 CXXFLAGS="-O3" --enable-mpi 
      --with-cc=/path/to/mpicc --with-cxx=/path/to/mpicxx --enable-PY_WRAPPER

followed by the classical `make -j N` and `make install` commands.

This will first compile the SU2 code, and all the required libraries from `./externals`, to generate the executables (SU2_CFD, SU2_SOL, SU2_DEF, ...). Then it will wrap the CDriver structure in order to create the Python module `pysu2.py` that is linked to the library `_pysu2.so` (also coming from the wrapper compilation). The `pysu2` module can be imported in a Python script so that any SU2 driver (general, fluid, ...) can be instantiated and used as a classical Py object.

Make sure to note the **SU2_RUN** and **SU2_HOME** environment variables displayed at the conclusion of configure. It is recommended that you add the SU2_RUN and SU2_HOME variables to your ~/.bashrc file and update your PATH and PYTHONPATH variables to include the install location ($SU2_RUN, specified by --prefix).

### Note : How to install Swig and mpi4py
On **Linux**, Swig can be easily installed with the APT:

    $ sudo apt-get install swig

If you have a working distribution of MPI on your system, mpi4py can be installed with Python pip:

    $ sudo apt-get install python-pip
    $ sudo pip install mpi4py

On **Mac OS X**, you can use the [Homebrew](http://brew.sh/) package manager. Once it is installed on your system, you can install Swig by running:

    $ sudo brew install swig

Note that you can also use Homebrew to easily install Open MPI on your Mac:

    $ sudo brew install open-mpi

Install mpi4py with Python pip using easy install:

    $ sudo easy_install pip
    $ sudo pip install mpi4py
