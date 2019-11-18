---
title: Build SU2 On Windows
permalink: /docs_v7/Build-SU2-Windows/
---

***This guide is for version 7 only.*** 
This document will guide you through the steps to compile SU2 on Windows using the [Minimalist GNU for Windows
](http://www.mingw.org/) development environment (MinGW) and [Microsoft MPI](https://docs.microsoft.com/en-us/message-passing-interface/microsoft-mpi).

Note that there are multiple other ways of compiling SU2 on Windows (for example using Cygwin, Visual Studio, the Linux Subsystem) and all of them should(!) work one way or the other,
however, we can only document (and support) a limited number of possibilities. 

---

- [Requirements](#requirements)
- [Installation of Dependencies](#installation-of-dependencies)
- [Configuration and Compilation](#configuration-and-compilation)
- [Running the executables](#running-the-executables)

---

## Requirements

- Windows 10<sup>*</sup>
- Python 3.7 (download [here](https://www.python.org/downloads/windows/) or from the Microsoft Store)
- MinGW version 8.1.0<sup>*</sup> (download [here](https://osdn.net/projects/mingw/releases/))
- Microsoft MPI v10.1.2<sup>*</sup> (download [here](https://www.microsoft.com/en-us/download/details.aspx?id=100593), you need the `msmpisetup.exe` and the `msmpisdk.msi`)
- SU2 v7.x.x (download [here](https://su2code.github.io/download) or clone using git)

<sup>*</sup>Other version might work, but this has not been verified yet.


## Installation of Dependencies

- Install Microsoft MPI by simply executing the installers `msmpisetup.exe` and the `msmpisdk.msi`.

- Install MinGW by executing the installer `mingw-w64-install.exe`. Choose Version `8.1.0` and Architecture `x86_64` on the Settings page.
Everything else can stay on their default values. On the next page set a destination folder and remember it! Click next until everything has been downloaded and installed.

## Configuration and Compilation

In the file browser go to the mingw installation directory and execute the file `mingw-w64`. This should open the command prompt. Navigate to the SU2 source code directory (in the command prompt you can change directories using `cd` and list directories using `dir`).
Now you can follow the steps in the [Linux/MacOS Configuration and Compilation section](docs_v7/Build-SU2-From-Source/#configuration-and-compilation). But make sure to use `python meson.py` and `ninja.exe` instead of `./meson.py` and `./ninja`, respectively.




## Running the executables
Add SU2 to the system path. This will allow you to use the executables from any directory without explicitly specifying the path to the executable. To do that access the system variables by typing “environ” in the search/run box of the start menu, select “edit the system environment variables”, and then select “Environment Variables” from the System Properties menu. Edit the “Path” system variable (or select “New” if no “Path” system variable exists) and add the path to the SU2 executables, i.e. the path that you have set with the `--prefix` option (if option was not given, the default is `C:\bin`). When there is more than one directory listed in “Path” they must be separated by semicolons.
Running SU2 in Windows is identical to running in [Linux or Mac OS environments](/_docs_v7/Execution.md) and is run from the command line (whether cmd.exe or the freely-available Console2 for Windows). However, you may have to use `mpiexec` instead of `mpirun` to execute the code in parallel.
