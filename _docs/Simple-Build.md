---
title: Simple Build
permalink: /docs/Simple-Build/
---

SU2 uses the GNU automake tools to configure and build the software from source in Linux and Mac OS X environments (or with a terminal emulator on Windows). In keeping with our philosophy of simplifying the install process, a vanilla version of the code can be quickly installed without any dependencies. To compile the most basic version of SU2 (single-threaded with no optional features), execute the following commands in a terminal after extracting the source code: 
```
$ cd /path/to/your/SU2/
$ ./configure --prefix=/path/to/install/SU2
$ make
$ make install
```
The `--prefix` option defines the location that the executables will be installed (in a folder named bin/ within your chosen install location from --prefix). If the `--prefix` option is not specified, the code will be installed in `/usr/local/bin`, which may require admin access. You can also use the "-j N" option of the make command in order to compile SU2 in parallel using N cores, i.e., run
```
make -j 8 install
```
to compile using 8 cores. This can greatly reduce the compilation time if building on a multicore laptop, workstation, or cluster head node. 

Make sure to note the **SU2_RUN** and **SU2_HOME** environment variables displayed at the conclusion of configure. It is recommended that you add the **SU2_RUN** and **SU2_HOME** variables to your ~/.bashrc file and update your PATH variable to include the install location ($SU2_RUN, specified by `--prefix`).
