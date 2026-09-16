---
title: Build SU2 on Windows
permalink: /docs_v7/Build-SU2-Windows/
---

This document will guide you through the steps to compile SU2 natively on Windows. Two toolchains are described:

- the Microsoft Visual C++ compiler (MSVC) from Visual Studio, with [Microsoft MPI](https://docs.microsoft.com/en-us/message-passing-interface/microsoft-mpi) for parallel runs,
- the [Minimalist GNU for Windows](http://www.mingw.org/) development environment (MinGW).

Note that there are multiple other ways of compiling SU2 on Windows (for example using Cygwin or the Windows Subsystem for Linux, where the [Linux/MacOS instructions](/docs_v7/Build-SU2-Linux-MacOS/) apply) and all of them should(!) work one way or the other,
however, we can only document (and support) a limited number of possibilities.

---

- [Building with Visual Studio (MSVC)](#building-with-visual-studio-msvc)
  - [Requirements](#requirements)
  - [Installation of Dependencies](#installation-of-dependencies)
  - [Configuration and Compilation](#configuration-and-compilation)
  - [Known Limitations](#known-limitations)
- [Building with MinGW](#building-with-mingw)
- [Running the executables](#running-the-executables)

---

## Building with Visual Studio (MSVC)

### Requirements

- Windows 10 or 11 (64-bit)
- Python 3 (download [here](https://www.python.org/downloads/windows/) or from the Microsoft Store)
- [Visual Studio 2022](https://visualstudio.microsoft.com/downloads/) or the Build Tools for Visual Studio 2022, with the "Desktop development with C++" workload
- Git, if you clone the source code (download [here](https://git-scm.com/download/win))
- Optional, for parallel runs: Microsoft MPI (download [here](https://www.microsoft.com/en-us/download/details.aspx?id=100593), you need the `msmpisetup.exe` and the `msmpisdk.msi`)

These instructions were tested on Windows 11 with Python 3.10, MSVC 19.44 (Visual Studio 2022 Build Tools) and Microsoft MPI 10.1.

### Installation of Dependencies

- Install Visual Studio or the Build Tools and select the "Desktop development with C++" workload.
- If you want to run SU2 in parallel, install Microsoft MPI by executing both `msmpisetup.exe` and `msmpisdk.msi`. The SDK installer sets the environment variables `MSMPI_INC` and `MSMPI_LIB64` that are used to find MPI when SU2 is configured. Command prompts that were already open do not see these variables, so open a new one after installing.

Meson and Ninja do not have to be installed, SU2 downloads its own copies during configuration.

### Configuration and Compilation

All commands have to be run from the **x64 Native Tools Command Prompt for VS 2022**, which you can find in the start menu. The regular command prompt does not have the compiler in its path, and the x86 prompt builds 32-bit executables.

Navigate to the SU2 source code directory and configure the build:

```
python meson.py setup build -Denable-cgns=false --prefix=C:\SU2
```

Then compile and install:

```
ninja.exe -C build install
```

The executables and the Python scripts are installed to the `bin` folder of the prefix, `C:\SU2\bin` in this example.

If Microsoft MPI is installed, the configuration summary contains `Run-time dependency MPI for c found: YES` and SU2 is built with MPI support. Do **not** pass `-Dwith-mpi=enabled`: Meson only detects Microsoft MPI for C, which is all SU2 needs, but forcing MPI also requires the C++ detection, which fails. The line `Run-time dependency MPI for cpp found: NO` is therefore expected.

The remaining options are the same as on Linux and MacOS, see the [Linux/MacOS Configuration and Compilation section](/docs_v7/Build-SU2-Linux-MacOS/#configuration-and-compilation).

### Known Limitations

- CGNS support has to be disabled with `-Denable-cgns=false`, because the HDF5 library that is bundled with CGNS does not compile with MSVC. Meshes in the native SU2 format can be used without restrictions.
- MSVC prints warnings such as `Command line warning D9002 : ignoring unknown option`, these do not affect the build.
- At run time SU2 may print `WARNING: SU2 was not compiled for an AVX-capable architecture`. This only concerns performance.

## Building with MinGW

These instructions were written for SU2 v7 and have not been verified with more recent versions.

Requirements:

- Windows 10<sup>*</sup>
- Python 3.7 (download [here](https://www.python.org/downloads/windows/) or from the Microsoft Store)
- MinGW-w64 version 8.1.0<sup>*</sup> (download [here](https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/installer/mingw-w64-install.exe/download))
- Microsoft MPI v10.1.2<sup>*</sup> (download [here](https://www.microsoft.com/en-us/download/details.aspx?id=100593), you need the `msmpisetup.exe` and the `msmpisdk.msi`)
- SU2 v7.x.x (download [here](https://su2code.github.io/download) or clone using git)

<sup>*</sup>Other version might work, but this has not been verified yet.

Installation of dependencies:

- Install Microsoft MPI by simply executing the installers `msmpisetup.exe` and the `msmpisdk.msi`.

- Install MinGW by executing the installer `mingw-w64-install.exe`. Choose Version `8.1.0` and Architecture `x86_64` on the Settings page.
Everything else can stay on their default values. On the next page set a destination folder and remember it! Click next until everything has been downloaded and installed.

Configuration and compilation:

In the file browser go to the mingw installation directory and execute the file `mingw-w64`. This should open the command prompt. Navigate to the SU2 source code directory (in the command prompt you can change directories using `cd` and list directories using `dir`).
Now you can follow the steps in the [Linux/MacOS Configuration and Compilation section](/docs_v7/Build-SU2-Linux-MacOS/#configuration-and-compilation). But make sure to use `python meson.py` and `ninja.exe` instead of `./meson.py` and `./ninja`, respectively.

Note that the older MinGW distribution from mingw.org (GCC 6) cannot compile current versions of SU2, use MinGW-w64.

## Running the executables

Add the `bin` folder of the installation to your `PATH` and set `SU2_RUN` to the same folder, as described in the [installation guide](/docs_v7/SU2-Windows/). SU2 is then started with

```
SU2_CFD.exe config.cfg
```

for a serial run, or with

```
mpiexec -n 4 SU2_CFD.exe config.cfg
```

for a parallel run on 4 processes.
