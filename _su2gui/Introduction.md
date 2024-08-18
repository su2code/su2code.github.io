---
title: Introduction to SU2GUI
permalink: /su2gui/Introduction/
---

**SU2GUI** is a Graphical User Interface (GUI) for the SU2 open-source CFD software. It facilitates easier execution of SU2 tasks and provides visualization capabilities for the results.
Please note that SU2GUI is currently under development. We welcome feedback and contributions to improve the tool. SU2GUI is under active development by individuals all around the world on GitHub and is released under an open-source license.


## Overview of SU2GUI Workflow

Here is an overview of how SU2GUI works:

![overview_su2gui](../../su2gui_files/User_guide/workflow.png)


SU2GUI is designed to simplify and streamline the process of setting up, running, and analyzing simulations with SU2. It utilizes several Python libraries such as Pandas, VTK, JSON, Trame, and Vuetify to deliver its full functionality. These libraries handle data processing, visualization, and user interface components, making SU2GUI both powerful and versatile. Below is a typical workflow when using SU2GUI:

### 1. Launch SU2GUI
Start the application by running the `su2gui` command in your terminal. This opens the graphical user interface where all operations are conducted.

### 2. Load Your Case
Once SU2GUI is launched, use the interface to load your Case along with the necessary files such as mesh, configuration, and other relevant configurations. The GUI allows for easy management and organization of these files, ensuring that your simulation is properly set up.

### 3. Run Simulation
With everything loaded, you can set up and run your simulation directly from the GUI. SU2GUI provides a user-friendly environment to configure parameters, initialize conditions, and start the solver.

### 4. Visualize Results
As the simulation runs, you can visualize and analyze the results in real-time using the integrated visualization tools within SU2GUI. This allows for immediate feedback and adjustments to the simulation if needed.

### 5. Manage Cases
SU2GUI also offers robust case management features. You can easily delete, download, or load new or previous cases, providing you with greater control over your simulation projects and data.


For a more detailed understanding of how to use SU2GUI, refer to the [QuickStart page](./../quick-start).
