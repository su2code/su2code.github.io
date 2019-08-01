---
title: Build SU2 From Source
permalink: /docs/Build-SU2-From-Source
---

## Quick Compilation Guide ##

This is a quick guide to compile and install a basic version of SU2. For more information on the requirements and a more detailed description of the build system continue reading the rest of this page.

Short summary of the minimal requirements:

- C/C++ compiler
- Python 3

If you have these tools installed, you can create a configuration using the `meson.py` found in the root source code folder:
```
 ./meson.py build
```
Use `ninja` to compile and install the code

```
./ninja -C build install
```



## Requirements ##

### Compilers ###
Installing SU2 from source requires a C++ compiler. The GNU compilers (gcc/g++) are open-source, widely used, and reliable for building SU2. The Intel compiler set has been optimized to run on Intel hardware and has also been used successfully by the development team to build the source code, though it is commercially licensed. The Apple LLVM compiler (Clang) is also commonly used by the developers.

- GNU gcc / g++ 
- Intel icc / icpc 
- Apple LLVM (clang)
  
> **Note**: SU2 uses some C++11 features, that means at least GCC >= v4.7, Clang >= v3.0 or Intel C++ >= v12.0 is necessary.

### MPI ###
In order to build SU2 with parallel support, you need a suitable MPI installation on your machine. During the configuration the build tool does a check and enables MPI support. If no installation is found, a serial version of SU2 will be compiled.

### Python ###

SU2 requires Python 3 for compilation and for running the python scripts. Make sure that you have properly set up the `python3` executables in your environment. 

### Optional: swig and mpi4py ###
If you want to use the python wrapper capabilities, also `swig` and `mpi4py` are required. On **Linux** `swig` should be available in the package manager of your distribution and `mpi4py` can be installed using [pip](https://pip.pypa.io/en/stable/).

On **Mac OS X**, you can use the [Homebrew](http://brew.sh/) package manager. Once it is installed on your system, you can install Swig by running:

    $ sudo brew install swig

Install mpi4py with Python pip using easy install:

    $ sudo easy_install pip
    $ sudo pip install mpi4py
    
## Automatically installed dependencies ##

The following dependencies are added as submodules in the `git` repository and are automatically cloned during the [configuration](#configuration-and-compilation). If you downloaded the SU2 sources directly *without* `git clone`, a fallback method using `wget` is used. When even that fails, steps to download the dependencies manually will printed on screen.

### Meson and Ninja ###
The build system of SU2 is based on a combination of [meson](http://mesonbuild.com/) (as the front-end) and [ninja](https://ninja-build.org/) (as the back-end). Meson is an open source build system meant to be both extremely fast, and, even more importantly, as user friendly as possible. Ninja is a small low-level build system with a focus on speed. 

### CoDiPack and MeDiPack ###
In order to use the discrete adjoint solver the compilation requires two additional (header-only) libraries. [CoDi](https://github.com/SciCompKL/CoDiPack) provides the AD datatype and [MeDi](https://github.com/SciCompKL/MeDiPack) provides the infrastructure for the MPI communication when the reverse mode of AD is used. 

## Configuration and Compilation ##

Like mentioned above, SU2 uses meson and ninja for configuration and compilation, respectively. A configuration using meson is generated first and then an invocation of ninja is used to compile SU2 with this configuration. 


### Basic Configuration ###
In the root folder of the sources you will find a python script called `meson.py`. This script generates a configuration. Like mentioned above, it will also check whether all dependencies are found and downloads some of them if necessary see [previous section](#automatically-installed-dependencies). 

> **Note**: For the following steps you can also use preinstalled versions of `meson` and `ninja` available on your machine. Just replace the `./meson.py` and `./ninja` calls with the binaries of the respective installations. However, this way you have to manually make sure that the correct versions of [CoDiPack and MeDiPack](#codipack-and-medipack) are placed in the `externals/` folders.

The only required argument for `meson.py` is a name of a directory where it should store the configuration. You can have multiple configurations in different folders next to each other. To generate a basic configuration that will be stored in the folder `build` use

```
 ./meson.py build
```

Options can be passed to the script to enable or disable different features of SU2.  Below you find a list of project options and their default values:
 
| Option | Default value | Description |
|---| --- | --- |
| `-Denable-autodiff`  | `false`   |   enable AD (reverse) support (needed for discrete adjoint solver)  |
| `-Denable-directdiff` | `false`     |  enable AD (forward) support |
| `-Denable-mpi`       | `true` (depends on whether a MPI installation can be found) |   enable MPI support           |
| `-Denable-pywrapper` | `false`      |    enable Python wrapper support|
| `-Denable-cgns`     | `true`    |       enable CGNS support           |        
| `-Denable-tecio`    |  `true`       |    enable TECIO support         |

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
./meson.py build --reconfigure --debug
```
Note that it is only possible to change one option at once.

#### Build Type ####

The debug mode can be enabled by using the `--buildtype=debug` option or `--debug`. This adds `-g` flag and disables all compiler optimizations. If you still want to have optimizations, use `--buildtype=debugoptimized`. The default build type is `release`.

#### Compiler optimizations ####

The optimization level can be set with `--optimization=level`, where `level` corresponds to a number between 0 (no optimization) and 3 (highest level of optimizations). The default level is 3.

#### Warning level ####

The warning level can be set with `--warnlevel=level`, where  `level` corresponds to a number between 0 (no warnings) and 3 (highest level of warning output). Level 1 corresponds to `-Wall`, level 2 to `-Wall -Wextra` and level 3 to `-Wall -Wextra -Wpedantic`. The default level is 0.

> **Note:** The warning flags `-Wno-unused-parameter`, `-Wno-empty-body` and `-Wno-format-security` are always added by default.

### Compilation ###

Finally to compile and install SU2 use 
```
./ninja -C build install
```
where `build` is again a folder with a configuration created using a call to `meson.py` described in the previous section. By default ninja uses all available cores in your system for the compilation. You can set the number of cores manually by using the `-jN` flag, where `N` is the number of cores you want to use.
