---
title: Build SU2 on Linux/MacOS
permalink: /docs_v7/Build-SU2-Linux-MacOS/
redirect_from: /docs/Build-SU2-From-Source/
---

For information on how to build older versions of SU2, have a look [here](/docs_v7/Build-from-Source/).

Note that the following guide works only on Linux/MacOS and on Windows using Cygwin or the [Linux Subsystem](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

---

- [Quick Compilation Guide](#quick-compilation-guide)
- [Requirements](#requirements)
  - [Compilers](#compilers)
  - [MPI](#mpi)
  - [Python](#python)
  - [Optional: swig and mpi4py](#optional-swig-and-mpi4py)
- [Automatically installed dependencies](#automatically-installed-dependencies)
  - [Meson and Ninja](#meson-and-ninja)
  - [CoDiPack and MeDiPack](#codipack-and-medipack)
- [Configuration and Compilation](#configuration-and-compilation)
  - [Basic Configuration](#basic-configuration)
  - [Advanced Configuration](#advanced-configuration)
    - [Build Type](#build-type)
    - [Compiler optimizations](#compiler-optimizations)
    - [Warning level](#warning-level)
    - [Linear algebra options](#linear-algebra-options)
  - [Compilation](#compilation)
  - [Setting environment variables](#setting-environment-variables)
- [Troubleshooting](#troubleshooting)
  - [MPI installation is not found](#mpi-installation-is-not-found)
  - [mpi4py library is not found](#mpi4py-library-is-not-found)

---

## Quick Compilation Guide ##

This is a quick guide to compile and install a *basic version* of SU2. For more information on the requirements and a more detailed description of the build system **continue reading** the rest of this page.

Short summary of the minimal requirements:

- C/C++ compiler
- Python 3

**Note:** all other necessary build tools and dependencies are shipped with the source code or are downloaded automatically.

If you have these tools installed, you can create a configuration using the `meson.py` found in the root source code folder:
```
./meson.py build
```
Use `ninja` to compile and install the code

```
./ninja -C build install
```
---


## Requirements ##

### Compilers ###
Installing SU2 from source requires a C++ compiler. The GNU compilers (gcc/g++) are open-source, widely used, and reliable for building SU2. The Intel compiler set has been optimized to run on Intel hardware and has also been used successfully by the development team to build the source code, though it is commercially licensed. The Apple LLVM compiler (Clang) is also commonly used by the developers.

- GNU gcc / g++ 
- Intel icc / icpc 
- Apple LLVM (clang)
  
**Note**: SU2 uses some C++11 features, that means at least GCC >= v4.7, Clang >= v3.0 or Intel C++ >= v12.0 is necessary.

### MPI ###
In order to build SU2 with parallel support, you need a suitable MPI installation on your machine. During the configuration the build tool does a check and enables MPI support. If no installation is found, a serial version of SU2 will be compiled.

### Python ###

SU2 requires Python 3 for compilation and for running the python scripts. Make sure that you have properly set up the `python3` executables in your environment. 

### Optional: swig and mpi4py ###
If you want to use the python wrapper capabilities, also `swig` and `mpi4py` are required. On **Linux** `swig` should be available in the package manager of your distribution and `mpi4py` can be installed using [pip](https://pip.pypa.io/en/stable/).

On **Mac OS X**, you can use the [Homebrew](http://brew.sh/) package manager. Once it is installed on your system, you can install Swig by running:

    $ brew install swig

Install mpi4py with Python pip using easy install:

    $ easy_install pip
    $ pip install mpi4py
    
---

## Automatically installed dependencies ##

The following dependencies are automatically downloaded (or initialized if source code was cloned using `git`) during the [configuration](#configuration-and-compilation). 

### Meson and Ninja ###
The build system of SU2 is based on a combination of [meson](http://mesonbuild.com/) (as the front-end) and [ninja](https://ninja-build.org/) (as the back-end). Meson is an open source build system meant to be both extremely fast, and, even more importantly, as user friendly as possible. Ninja is a small low-level build system with a focus on speed. 

### CoDiPack and MeDiPack ###
In order to use the discrete adjoint solver the compilation requires two additional (header-only) libraries. [CoDi](https://github.com/SciCompKL/CoDiPack) provides the AD datatype and [MeDi](https://github.com/SciCompKL/MeDiPack) provides the infrastructure for the MPI communication when the reverse mode of AD is used. 

--- 
## Configuration and Compilation ##

Like mentioned above, SU2 uses meson and ninja for configuration and compilation, respectively. A configuration using meson is generated first and then an invocation of ninja is used to compile SU2 with this configuration. 

### Basic Configuration ###
In the root folder of the sources you will find a python script called `meson.py`. This script generates a configuration. It will also check whether all dependencies are found and downloads some of them if necessary see [previous section](#automatically-installed-dependencies). 

**Note**: For the following steps you can also use preinstalled versions of `meson` and `ninja` available on your machine. Just replace the `./meson.py` and `./ninja` calls with the binaries of the respective installations. However, this way you have to manually make sure that the correct versions of [CoDiPack and MeDiPack](#codipack-and-medipack) are placed in the `externals/` folders.

The only required argument for `meson.py` is a name of a directory where it should store the configuration. You can have multiple configurations in different folders next to each other. To generate a basic configuration that will be stored in the folder `build` use

```
 ./meson.py build
```

Options can be passed to the script to enable or disable different features of SU2.  Below you find a list of project options and their default values:
 
| Option | Default value | Description |
|---| --- | --- |
| `-Denable-autodiff`  | `false`   |   enable AD (reverse) support (needed for discrete adjoint solver)  |
| `-Denable-directdiff` | `false`     |  enable AD (forward) support |
| `-Denable-pywrapper` | `false`      |    enable Python wrapper support|
| `-Dwith-mpi`       | `auto` |   Set dependency mode for MPI (`auto`,`enabled`,`disabled`)  |
| `-Dwith-omp`       | `false` |  enable MPI+Threads support (experimental) |
| `-Denable-cgns`     | `true`    |       enable CGNS support           |        
| `-Denable-tecio`    |  `true`       |    enable TECIO support         |
| `-Denable-mkl`      |  `false`      |    enable Intel MKL support     |
| `-Denable-openblas` |  `false`      |    enable OpenBLAS support      |
| `-Denable-pastix`   |  `false`      |    enable PaStiX support        |

For example to enable AD support pass the option to the `meson.py` script along with a value:
```
./meson.py build -Denable-autodiff=true
```
To set a installation directory for the binaries and python scripts, use the `--prefix` option, e.g.:

```
./meson.py build -Denable-autodiff=true --prefix=/home/username/SU2
```
If you are not interested in setting custom compiler flags and other options you can now go directly to the [Compilation](#compilation) section, otherwise continue reading the next section.

### Advanced Configuration ###
In general meson appends flags set with the environment variable `CXX_FLAGS`. It is however recommended to use 
mesons built-in options to set debug mode, warning levels and optimizations. All options can be found [here](https://mesonbuild.com/Builtin-options.html) or by using `./meson.py configure`. An already created configuration can be modified by using the `--reconfigure` flag, e.g.:
```
./meson.py build --reconfigure --buildtype=debug
```
Note that it is only possible to change one option at once.

#### Build Type ####

The debug mode can be enabled by using the `--buildtype=debug` option. This adds `-g` flag and disables all compiler optimizations. If you still want to have optimizations, use `--buildtype=debugoptimized`. The default build type is `release`.

#### Compiler optimizations ####

The optimization level can be set with `--optimization=level`, where `level` corresponds to a number between 0 (no optimization) and 3 (highest level of optimizations). The default level is 3.

#### Warning level ####

The warning level can be set with `--warnlevel=level`, where  `level` corresponds to a number between 0 (no warnings) and 3 (highest level of warning output). Level 1 corresponds to `-Wall`, level 2 to `-Wall -Wextra` and level 3 to `-Wall -Wextra -Wpedantic`. The default level is 0.

**Note:** The warning flags `-Wno-unused-parameter`, `-Wno-empty-body` and `-Wno-format-security` are always added by default.

#### Linear algebra options ####

Compiling with support for a BLAS library (`-Denable-mkl` or `-Denable-openblas`) is highly recommended if you use the high order finite element solver, or radial basis function (RBF) interpolation in fluid structure interaction problems.
To a lesser extent MKL 2019 is also used to accelerate (~5%) sparse linear algebra operations.
`-Denable-mkl` takes precedence over `-Denable-openblas`, the system tries to find MKL via [pkg-config](https://en.wikipedia.org/wiki/Pkg-config), if that fails it will then look for MKL in `/opt/intel/mkl`, this can be changed via option `-Dmkl_root`.
When OpenBLAS support is requested the build system uses pkg-config to search the system for package `openblas`, option `-Dblas-name`, if the library was built from source it may be necessary to set the environment variable PKG_CONFIG_PATH.

For large structural FEA problems on highly anisotropic grids iterative linear solvers might fail. Version 7 introduces experimental support for the direct sparse solver [PaStiX](https://gforge.inria.fr/projects/pastix/) (`-Denable-pastix`) see detailed instructions in `TestCases/pastix_support/readme.txt`.

If the use of BLAS is restricted to RBF interpolation, parallel versions of OpenBLAS can be used, the number of threads will then have to be controlled via the appropriate environment variable (consult the OpenBLAS documentation). Otherwise sequential BLAS should be used.

**Note:** The BLAS library needs to provide support for LAPACK functions.

### Compilation ###

Finally to compile and install SU2 use 
```
./ninja -C build install
```
where `build` is again a folder with a configuration created using a call to `meson.py` described in the previous section. By default ninja uses all available cores in your system for the compilation. You can set the number of cores manually by using the `-jN` flag, where `N` is the number of cores you want to use.


### Setting environment variables ###
Set the environment variables to use the executables from any directory without explicity specifying the path as described in the [installation section](/docs_v7/SU2-Linux-MacOS).

---

## Troubleshooting ##

### MPI installation is not found ###
Meson looks for an MPI installation using [pkg-config](https://en.wikipedia.org/wiki/Pkg-config). But if your MPI implementation does not provide them, it will search for the standard wrapper executables, `mpic`, `mpicxx`, `mpic++`. If these are not in your path, they can be specified by setting the standard environment variables `MPICC`, `MPICXX` during configuration.

### mpi4py library is not found ###
Meson imports the mpi4py module and searches for the include path. If it is installed in a custom location, make sure to add this path to the `PYTHONPATH` environment variable prior calling `meson.py`.

### Ninja compiles but fails to install ###
If building on a cluster that uses a NFS filesystem, ninja may finish the compilation but fail to install with an error such as:
```
OSError: [Errno 22] Invalid argument: 'SU2_CFD/src/SU2_CFD'
```
This is a known bug in earlier versions of Python 3. Try upgrading to Python >= 3.7 then rerun ninja.
