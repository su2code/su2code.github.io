---
title: Windows Installation
permalink: /docs_v7/Windows-Installation/
---

As of release 4.1.1, SU2 supports Windows platforms from Windows 7 through Windows 10 in (x86) 32-bit and (x64) 64-bit architectures (see details and limitations below). Please note that the executables have been built to support any version of Windows but have only been tested on Windows 7 and Windows 10, x64 platform. The x86 versions are available for legacy support but are limited to smaller problems due to the 2 GB memory limit in x86 systems; a 64-bit architecture is recommended. Windows binaries are packaged as an Archive (.zip). If you encounter a problem installing or running in Windows please contact the support team for assistance. 

This version is built with CGNS 3.3.0 but no Tecplot binary support (Tecplot text format output is always available).   

## Installation 

1. **Download and unpack the archive**. Download the .zip for your operating system (Windows 7 or Windows 10) and unzip it where you want it to be installed. 

2. **Add SU2 environment variables**. This is done through the Environment Variables control panel.  You can access these by typing "environ" in the search/run box of the start menu.  Start a New System variable.  Assign the Variable Name "SU2_RUN", and assign the Variable Value to be the path to your SU2 Executables (the folder that contains SU2_CFD.exe for example).  If you used the default values from the installer, this could be "C:\SU2\".  This variable will allow you to quickly navigate to the SU2 directory using "cd %SU2_RUN%", and run the executables using "%SU2_RUN%\<executable>" if SU2\ has not been added to the system path.

*NOTE*: if the directory name contains white space, the executables may not work without appending ".exe", and the python scripts may not work. Additionally, when setting the enviornment variables and paths, quotes must be added, for example: "C:\Program Files\"Stanford ADL"\SU2\"

3. **Add SU2 to the system path**. Access the system variables by typing "environ" in the search/run box of the start menu, select "edit the system environment variables", and then select "Environment Variables" from the System Properties menu. Edit the "Path" system variable (or select "New" if no "Path" system variable exists) and add the path to the SU2 executables. When there is more than one directory listed in "Path" they must be separated by semicolons. This will allow you to use the executables from any directory without explicitly specifying the path to the executable. 

4. **Optional: Install Microsoft MPI to enable parallel mode**. As the well-known, freely-available, open-source implementations of MPI listed in the Install section may not support Windows, you may want to install Microsoft MPI. 

## Running SU2 in Windows

Running SU2 in Windows is identical to running in Linux or Mac OS environments and is run from the command line (whether cmd.exe or the freely-available Console2 for Windows). If your executable path contains white space you may need to add ".exe" . 

