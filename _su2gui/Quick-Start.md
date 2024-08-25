---
title: Quick Start
permalink: /su2gui/Quick-Start/
---

Welcome to the Quick Start Tutorial for the SU2 software suite. This tutorial introduces key features of SU2's analysis and design tools in an easily accessible format, taking only a few minutes to complete. If you haven’t done so already, please visit the [SU2](../../docs_v7/Installation/) and [SU2_GUI](./../Installation) download pages to obtain the latest stable releases and installation details. This tutorial mirrors the [SU2 Quick Start](../../docs_v7/Quick-Start/) guide and requires both the SU2_CFD and SU2_GUI tools.

This guide will help you:

- [Set up SU2GUI](#setup-su2gui)
- [Start a new case](#start-a-new-case)
- [Load mesh file](#load-mesh-file)
- [Load Configurations](#load-configurations)
- [Run simulation](#run-simulation)
- [Download case](#download-case)
- [Analyze results](#analyze-results)

### Setup SU2GUI

If you haven’t installed SU2_GUI, run the following command:

    pip install su2gui

To start the GUI, enter the following in your terminal:

    SU2_GUI

### Start a New Case

1. In the pop-up window, enter a new case name (e.g., `inv_naca0012`).
2. Press the Create button.

![](../../su2gui_files/Quick_Start/new-case.png)

### Load Mesh File

We will load the mesh file from [SU2/mesh_NACA0012_inv.su2](https://github.com/su2code/SU2/blob/master/QuickStart/mesh_NACA0012_inv.su2):

1. Click on "Load Mesh File" from the top pane.
2. In the pop-up window, select the mesh file, and it will be loaded.

![](../../su2gui_files/User_guide/Mesh/button-mesh-file.png)

### Load Configurations

Next, load the configuration file from [SU2/QuickStart/inv_NACA0012.cfg](https://github.com/su2code/SU2/blob/master/QuickStart/inv_NACA0012.cfg):

1. Click on "Load Config File" from the top pane.
2. In the pop-up window, choose the configuration file. You can also make other configuration changes through the GUI.

![](../../su2gui_files/Quick_Start/load-config.png)

### Run Simulation

1. Navigate to the Solver node from the Menu.
2. Set the desired number of iterations (default may be 250).
3. Press the Start Solver button to begin the simulation.

![](../../su2gui_files/Quick_Start/start-solver.png)

### Download Case

1. From the top pane, click on the Case button.
2. Select your current case (`inv_naca0012`) from the Cases dropdown menu.
3. Click the Download button to download the case.

![](../../su2gui_files/Quick_Start/download-case.png)

### Analyze Results

1. In the top pane, select "Mach" from the Color By dropdown menu.
2. Turn off the mesh preview using the indicated button.
3. Zoom in on the mesh for a better view and analyze the results.

![](../../su2gui_files/Quick_Start/analyze-results.png)

## Next Steps

- Further analyze the results in Paraview.
- Explore the [SU2 QuickStart](../../docs_v7/Quick-Start/) guide for more details.
