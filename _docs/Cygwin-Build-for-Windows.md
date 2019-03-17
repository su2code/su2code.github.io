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

#### Example SU2 installation on WINDOWS 10 using 64-bit Cygwin
The shell used for all command line steps is the the default Cygwin bash shell.
                                                                                               
1) Install CYGWIN (64-bit version)                                                             
   a) Download and run https://www.cygwin.com/setup-x86_64.exe                                 
   b) Install development tools (also 64-bit versions):                                        
     i) gcc, gfortran, python3.7, openmpi, automake, libtools, autoconf, etc.                  
     ii) python-configobj needs to be installed for the same python version                    
         (Python module for handling config files)                                             
         often there are installation problems (not yet figured out when and why)              
         after installation it should reside in the folder /usr/bin as shown below                
     iii) folder /usr/bin as it should be for python3.7 and python-config                      
         lrwxrwxrwx 1 Andreas None   14 17. Mrz 19:29 /usr/bin/python3.7 -> python3.7m.exe     
         -rwxr-xr-x 1 Andreas None 3,3K 17. Mrz 19:46 /usr/bin/python3.7-config                
         -rwxr-xr-x 1 Andreas None 9,1K 15. Feb 10:05 /usr/bin/python3.7m.exe                  
         -rwxr-xr-x 1 Andreas None 3,3K 17. Mrz 19:46 /usr/bin/python3.7m-config

2) Set Python version for the installation process                                                       
   export PYTHON=/usr/bin/python3.7                                                                      
                                                                                                         
3) Goto folder where the SU2 source distribtution has been unzipped                                      
   a) download the SU2 source installation file for version 6.2.0                                                               
      https://github.com/su2code/SU2/archive/v6.2.0.tar.gz                                               
   b) unzip and untar                                                                                    
   c) change into the folder where files were untarred                                                    
      NOTE: this is later (see step 7) the folder where the SU2_HOME variable points to                  
                                                                                                         
4) Launch following configure command:                                                                   
   NOTE: didn't get tecio working, therefore disabled with --disable-tecio                               
   NOTE: "--enable-mpi-cxx" instead of "--enable-mpi"                                                    
   (see http://cygwin.1069669.n5.nabble.com/libmpi-cxx-dll-a-missing-td142324.html)                      
                                                                                                         
  ./configure --prefix=path_where_you_want_the_Executables --disable-tecio --enable-mpi-cxx CXXFLAGS=-O3 
                                                                                                         
5) Compile and link using:                                                                               
   make                                                                                                  
                                                                                                         
6) Not really needed (if a setup like in 7 is used)                                                      
   make install                                                                                          
                                                                                                         
7) Add the $SU2_HOME and $SU2_RUN environment variables to ~/.bashrc (and "source ~/.bashrc")
                                                                                                                 
   export SU2_RUN="path_where_you_want_the_Executables" (use same folder here as in the configure command above) 
   export SU2_HOME="/d/software/CFD/SU2/SU2-6.2.0"  <-- UPDATE THIS folder to your environment                   
   export PATH=$PATH:$SU2_RUN                                                                                    
   export PYTHONPATH=$PYTHONPATH:$SU2_RUN                                                                        
                                                                                                                 
8) cd to the QuickStart folder and try serial and parallel versions                                              
                                                                                                                 
   SERIAL command:                                                                                               
                                                                                                                 
   SU2_CFD.exe inv_NACA0012.cfg                                                                                  
                                                                                                                 
   PARALLEL command:                                                                                             
   (mpirun and mpiexec should be the same; mpiexec recommended as standard command)                              
   (-oversubscribe allows more processes than cores)                                                             
   (although I have 8 cores, even with "-n 6" I had to use the option)                                           
   (otherwise I got: There are not enough slots available in the system ...)                                     
                                                                                                                 
   mpiexec -n 6 -oversubscribe SU2_CFD.exe inv_NACA0012.cfg

