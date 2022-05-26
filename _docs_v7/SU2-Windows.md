---
title: SU2 on Windows
permalink: /docs_v7/SU2-Windows/
---

---

- [Installation](#installation)
  - [Download and unpack the archive](#download-and-unpack-the-archive)
  - [Add SU2 environment variables](#add-su2-environment-variables)
  - [Add SU2 to the system path](#add-su2-to-the-system-path)
  - [Optional: Install Microsoft MPI to enable parallel mode](#optional-install-microsoft-mpi-to-enable-parallel-mode)
- [Running SU2 in Windows](#running-su2-in-windows)

---

SU2 supports Windows platforms from Windows 7 and Windows 10 for x86 (64-bit). You have the option between a serial version and a parallel version. For the latter it is required that you install [Microsoft MPI](https://www.microsoft.com/en-us/download/details.aspx?id=100593) (the SDK is not required). 

## Installation 

### Download and unpack the archive
[Download](/docs_v7/Download/) the .zip for your operating system and unzip it where you want it to be installed. 

### Add SU2 environment variables
This is done through the Environment Variables control panel.  You can access these by typing "environ" in the search/run box of the start menu.  Start a New System variable.  Assign the Variable Name `SU2_RUN`, and assign the Variable Value to be the path to your SU2 Executables (the folder that contains `SU2_CFD.exe` for example). This variable will allow you to quickly navigate to the SU2 directory using `cd %SU2_RUN%`, and run the executables using `%SU2_RUN%\<executable>`.

**Note**: if the directory name contains white space, the executables may not work without appending ".exe", and the python scripts may not work. Additionally, when setting the enviornment variables and paths, quotes must be added, for example: `C:\Program Files\"Stanford ADL"\SU2\`

### Add SU2 to the system path
Access the system variables by typing "environ" in the search/run box of the start menu, select "edit the system environment variables", and then select "Environment Variables" from the System Properties menu. Edit the "Path" system variable (or select "New" if no "Path" system variable exists) and add the path to the SU2 executables. When there is more than one directory listed in "Path" they must be separated by semicolons. This will allow you to use the executables from any directory without explicitly specifying the path to the executable. 

### Optional: Install Microsoft MPI to enable parallel mode
As the well-known, freely-available, open-source implementations of MPI listed in the Install section may not support Windows, you may want to install Microsoft MPI. 

## Running SU2 in Windows

Running SU2 in Windows is identical to running in [Linux or Mac OS environments](/docs_v7/Execution/) and is run from the command line (whether cmd.exe or the freely-available Console2 for Windows). If your executable path contains white space you may need to add ".exe". Note, however, that you may need to use `mpiexec` instead of `mpirun`. 

