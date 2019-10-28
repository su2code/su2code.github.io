---
title: Windows Demo
permalink: /docs_v7/Windows-Demo/
---

This tutorial is intended to demonstrate 1) How to set up system variable, 2) How to run SU2 on Windows.

## Set up system variable
1. Click Windows key
![System Variable Figure 1](../../docs_files/windows_system_variable_01.png)
2. Type "environ" in the search/run box of the start menu, select "edit the system environment variables"
![System Variable Figure 2](../../docs_files/windows_system_variable_02.png)
3. Click "Environment Variables..."
![System Variable Figure 3](../../docs_files/windows_system_variable_03.png)
4. Click "Path" system variable and then click "Edit" (or select "New" if "Path" system variable doesn't exist)
![System Variable Figure 4](../../docs_files/windows_system_variable_04.png)
![System Variable Figure 5](../../docs_files/windows_system_variable_05.png)
05. You need to add path to SU2 exectuables. In this example, we add  C:\SU2  in the Path variable. If you didn't use the default values from the installer, you should add the path where your executables exist  ex) "C:\Program Files (x86)\SU2"
![System Variable Figure 6](../../docs_files/windows_system_variable_06.png)
06. Don't forget to click "OK" 
![System Variable Figure 7](../../docs_files/windows_system_variable_07.png)

## Running SU2 on Windows
1. Click Windows key
![Windows Quickstart Figure 1](../../docs_files/windows_quick_start_01.png)
2. Type "cmd" in the search/run box of the start menu, select "Command Prompt"
![Windows Quickstart Figure 2](../../docs_files/windows_quick_start_02.png)
3. Move to the directory containing the config file and the mesh file
![Windows Quickstart Figure 3](../../docs_files/windows_quick_start_03.png)
4. Run the executable by entering "SU2_CFD inv_channel.cfg" at the command line. **If you didn't add the path to SU2 executables in system variable "Path", this command won't work**
![Windows Quickstart Figure 4](../../docs_files/windows_quick_start_04.png)
5. SU2 will print residual updates with each iteration of the flow solver, and the simulation will finish after reaching the specified convergence criteria
![Windows Quickstart Figure 6](../../docs_files/windows_quick_start_06.png)
6. Files containing the results will be written upon exiting SU2. The flow solution can be visualized in ParaView (.vtk) or Tecplot (.dat for ASCII). To visualize the flow solution in ParaView update the OUTPUT_FORMAT setting in the configuration file
