---
title: SU2 on Linux/MacOS
permalink: /docs_v7/SU2-Linux-MacOS/
---

---

- [Installation](#installation)
  - [Download and unpack the archive](#download-and-unpack-the-archive)
  - [Setting Environment variables](#setting-environment-variables)
  - [Optional: Install MPICH for parallel mode](#optional-install-mpich-for-parallel-mode)

---

## Installation 

### Download and unpack the archive
[Download](/download/) the .zip for your operating system and unzip it where you want it to be installed. 

### Setting Environment variables

In order to use the executables from any directory without explicitely specifying the path to the executable you should set some environment variables. Either put the following lines to your `~/.bashrc` or `~/.bash_profile` to be permanent, or type the commands into the terminal for temporary use:
```
export SU2_RUN=<install_path>
export PATH=$SU2_RUN:$PATH
export PYTHONPATH=$SU2_RUN:$PYTHONPATH
```

where `<install_path>` is the path to the SU2 binaries (i.e. the folder that contains `SU2_CFD` etc.). If you have build [SU2 from source](/docs_v7/Build-SU2-Linux-MacOS/), it will be the path that you specified with the `--prefix` option (default: `/usr/bin`). The `export` commands are also printed after a successful configuration using `meson.py`.


### Optional: Install MPICH for parallel mode

If you want to run SU2 in parallel (and you have downloaded the `MPI` version), you need an installation of [MPICH](https://www.mpich.org/downloads/) on your machine. 
