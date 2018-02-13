---
title: AD Build
permalink: /docs/AD-Build/
---

It is recommended to read the information at [Build from Source](/docs/Build-from-Source/) first prior reading this section.

The following requires a compiler which supports most of the C++11 features, i.e. GCC >= v4.7, Clang >= v3.0 or Intel C++ >= v12.0.

In order to use the discrete adjoint solver the compilation requires two additional libraries. [CoDi](https://github.com/SciCompKL/CoDiPack) provides the AD datatype and [AdjointMPI](https://github.com/michel2323/AdjointMPI) provides the infrastructure for the MPI communication when the reverse mode of AD is used. Both libraries are added as submodules in `externals/` in the git repository of SU2. 

## Configuration with AD support
The initialization and compilation of these libraries as well as the configuration of SU2 is handled by the python script `preconfigure.py` inside the main directory. This script accepts the **same arguments** as the usual configure script (except `CXXFLAGS=...`) but in addition it offers the option `--enable-autodiff` to enable AD (reverse mode) for the discrete adjoint solver.

### Example 
Assume that your configuration (see [Simple Build](/docs/Simple-Build/) or [Parallel Build](/docs/Parallel-Build/)) is done using the command:

    ./configure --enable-mpi --prefix=$SU2_INSTALLPATH CXXFLAGS="-O3 -Wall"

To enable the compilation of the binaries with AD support, you'll need to change this command to:

    export CXXFLAGS="-O3 -Wall" && ./preconfigure.py --enable-autodiff --enable-mpi --prefix=$SU2_INSTALLPATH

**Note:** If you have already called `./configure` before in the source directory, a `make distclean` is required before calling `./preconfigure.py`.

This script creates the folders `SU2_BASE` and `SU2_AD` and calls configure in each of the folders. `SU2_BASE` then contains the configuration to compile all of the base modules (`SU2_CFD`, `SU2_DOT`, `SU2_SOL` etc.) and `SU2_AD` contains the configuration to compile the modules `SU2_CFD_AD` and `SU2_DOT_AD`. Furthermore, it creates a Makefile so that you can simply call `make install` in the main folder to compile and install everything into the specified directory or `make install SU2_BASE` or `make install SU2_AD` to compile and install them separately.
