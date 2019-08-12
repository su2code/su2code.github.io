---
title: Cygwin Build for Windows
permalink: /docs/Cygwin-Build-for-Windows/
---

### Overview
Cygwin provides a unix-like environment on a Windows machine, and emulates some of the functionality of a linux distribution. Downloads and more information on Cygwin is available at http://www.cygwin.com/. To compile and run SU2 in Cygwin on a Windows machine, you will need to configure Cygwin with the appropriate packages (listed below), and then continue from within Cygwin as though you were using a linux machine. 
In summary, the steps are:

1. Download Cygwin installer
2. Install Cygwin, selecting the packages necessary to compile the source code.
3. Download the source code into a directory within cygwin/
4. Install SU2 according to the directions for the linux installation. 

### Notes on installing Cygwin for first-time or beginner Cygwin users
* It is often recommended to install in  a directory rather than the default C:\ location.
* The Cygwin shell will only be able to access folders that are within the cygwin\ directory; you will need to install and run SU2 inside the cygwin directory.

### Cygwin packages
At the package selection step, search for the following terms and select the associated packages to install. This list is a work-in-progress, and further packages may be required or desired.

#### Basic
* g++, gcc compiler
* python: install the packages under the python sub-heading
* cpp: all debug, pre-processor, regular expression packages. 

### Example SU2 installation on WINDOWS 10 using 64-bit Cygwin

The CYGWIN `bash` shell is used for all steps on the command line. It is automatically available after the first installation step  (typically to be launched via the CYGWIN desktop icon).

1. Install CYGWIN (64-bit version) and development packages
   * Download and run:
   
     [setup-x86_64.exe](https://www.cygwin.com/setup-x86_64.exe)
     
     Inside the Cygwin Setup GUI use `C:\cygwin64` for both `Root Directory` and `Local Package Directory`. `Chose a Download Site` close to you (also http mirrors often work better). Continue to complete the bare minimum installation. This will end with a desktop icon named `Cygwin64 Terminal`. Double-click this to open the shell and launch further commands from there.
     
     For detailed informations on how to install CYGWIN and selected packages see [CYGWIN Installation](https://cygwin.com/install.html).

   * Install development tools (dependencies on these packages will be automatically selected by CYGWIN)
     
     > NOTE: A single command installing all required packages in one is given below this list
   
     1. General build environment tools
        * autoconf
        * autoconf2.5
        * autogen
        * automake
        * automake1.15
        * libtool
        * make
     1. Compilers 
        * gcc-g++
        * mingw64-x86_64-gcc-core
        * mingw64-x86_64-gcc-g++
     1. Python
        * python37
        * python37-devel
        * python3-configobj
     1. OpenMPI
        * libopenmpi-devel
        * openmpi
     1. Miscellaneous
        * vim (or any other editor in order to be able to edit files)
        * rsh
        * wget (to be able to download from the command line)
        * zlib-devel
    
   * All-in-one installation of packages (after the initial minimum installation):
   
   > NOTE: Prepend path to `setup-x86_64.exe` (depending where it has been downloaded)
     
     ```bash
     setup-x86_64.exe -q -P autoconf,autoconf2.5,autogen,automake,automake1.15,libtool,make,gcc-g++,mingw64-x86_64-gcc-core,mingw64-x86_64-gcc-g++,python37,python37-devel,python3-configobj,libopenmpi-devel,openmpi,vim,rsh,wget,zlib-devel
     ```
   
1. Configure CYGWINs default mount point (optional, but following steps use a syntax relying on this)
   
   ```bash
   mount -c / -o binary,noacl,posix=0
   mount -m > /etc/fstab
   ```

1. Configure OpenMPI

   Because in OpenMPI the C++ interface was removed, the option `-lmpi_cxx` has to be removed from the linker defaults. We need to check if this option is contained in the wrapper control file. This depends on the installed OpenMPI libraries.
   
   Assuming the 64-bit CYGWIN is installed in `C:\cygwin64` and `/etc/fstab` has been modified as in the previous step:

   ```bash
   cat /c/cygwin64/usr/share/openmpi/mpic++-wrapper-data.txt | grep lmpi_cxx
   ```
   
   If the option is set, then the following lines would be the result of the above  `grep`command:

       libs=-lmpi_cxx -lmpi                                        
       libs_static=-lmpi_cxx -lmpi -lopen-rte -lopen-pal -lm -lgdi3

   > NOTE: If `-lmpi_cxx` was not found, skip the next step

   If this is the case, edit `mpic++-wrapper-data.txt` and remove the `-lmpi_cxx` options so that the respective lines look like this:

       libs=-lmpi                                        
       libs_static=-lmpi -lopen-rte -lopen-pal -lm -lgdi3

1. Set the Python version for the installation process (for permanent setting add this line to `~/.profile`)
   
   ```bash
   export PYTHON=/usr/bin/python3.7
   ```

1. Get the SU2 source code:

   * Download following file for SU2 version 6.2.0
   
      ```bash
      wget https://github.com/su2code/SU2/archive/v6.2.0.tar.gz
      ```
      
   * Extract files and change into the folder where the files were extracted to:

      ```bash
      tar -xzvf v6.2.0.tar.gz
      cd SU2-6.2.0
      ```
   
      > NOTE: This is later the folder where the SU2_HOME variable points to

1. Run the utility for autoconf/automake toolchain setup:
  
   ```bash
   ./bootstrap
   ```

1. Create Makefiles:

   > NOTE: didn't yet get `tecio` working, therefore disabled with `--disable-tecio`<br>
   > NOTE: Removed `-DHAVE_EXECINFO_H` from metis cppflags (potentially could be solved via [gnulib](https://www.gnu.org/software/gnulib/manual/html_node/execinfo_002eh.html))
  
   ```bash
   ./configure --prefix=/home/Andreas/SU2-6.2.0 -enable-mpi --with-cc=/usr/bin/mpicc --with-cxx=/usr/bin/mpicxx --disable-tecio --with-metis-cppflags="-D_FILE_OFFSET_BITS=64 -DNDEBUG -DNDEBUG2 -DHAVE_GETLINE" 
   ```

1. Compile and link using:

   ```bash
   make
   ```

1. Distribute executables, etc. to their intended locations:

   ```bash
   make install
   ```

1. Reduce size of executables significantly (strip symbols, see also [CYGWIN FAQ 6.3](https://www.cygwin.com/faq.html). The SU2_CFD.exe is reduced from approx. 600MB to 15MB. Can be omitted if compiled with the -s option to gcc.

   ```bash
   make install-strip
   ```

1. Add the `$SU2_HOME` and `$SU2_RUN` environment variables to `~/.bashrc` (and `source ~/.bashrc`)

   ```bash
   export SU2_RUN="path_where_you_want_the_Executables" (use same folder here as in the configure command above)
   export SU2_HOME="/d/software/CFD/SU2/SU2-6.2.0"  <-- UPDATE THIS folder according to your environment
   export PATH=$PATH:$SU2_RUN                                                            
   export PYTHONPATH=$PYTHONPATH:$SU2_RUN                                                
   ```

1. Test serial and parallel versions:

   ```bash
   cd $SU2_HOME/QuickStart
   ```

   SERIAL command (due to the previous step `SU2_CFD.exe` should now be available in the path):

   ```bash
   SU2_CFD.exe inv_NACA0012.cfg
   ```

   PARALLEL command:
   Both `mpirun` and `mpiexec` do the same; `mpiexec` is recommended as the standard command.
   
   ```bash
   mpiexec -n 4 SU2_CFD.exe inv_NACA0012.cfg
   ```
   
   If more processes are requested than cores are available an error will be thrown:
  
   > There are not enough slots available in the system.
   
   On WINDOWS this can be if hyperthreading is active. A system physically having 4 CPUs (cores), would show 8 CPUs in case of hyperthreading. Oversubscribe allows more processes than cores (which not necessarily is faster).
   
   ```bash
   mpiexec -n 8 -oversubscribe SU2_CFD.exe inv_NACA0012.cfg
   ```
