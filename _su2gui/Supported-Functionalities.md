---
title: Supported Functionalities
permalink: /su2gui/Supported-Functionalities/
---


In this section, we explore the various supported functionalities of the SU2 GUI. While the SU2 GUI currently doesn't support all the features of the SU2 suite, you can still make adjustments using traditional methods.

The supported properties are organized according to the nodes in the Side Menu:

### Physics

This node supports selecting Solver, Turbulence Model, Sub-Model, Energy Equation, and Wall Function.

For more details on models in SU2, refer to this [page](../../docs_v7/Physical-Definition/).

### Materials

This node supports selecting the type of fluid density, viscosity, heat capacity, and conductivity, and specifying the necessary properties.

### Numeric

This node supports selecting the type of Spatial Gradients, MUSCL Spatial Gradients, and CFL value.

### Boundaries

This node contains sub-nodes based on the user's mesh file. Each sub-node allows you to modify the properties of that boundary.

Currently supported Boundary Markers include:

`MARKER_ISOTHERMAL`, `MARKER_HEATFLUX`, `MARKER_HEATTRANSFER`, `MARKER_EULER`, `MARKER_WALL_FUNCTIONS`, `MARKER_OUTLET`, `INC_OUTLET_TYPE`, `MARKER_SYM`, `MARKER_FAR`, `MARKER_INLET`, `INC_INLET_TYPE`, `INLET_TYPE`, `MARKER_SUPERSONIC_INLET`, `MARKER_SUPERSONIC_OUTLET`.

### Initialization

This node provides options for initializing the simulation. Uniform initialization requires constant values, Patch Initialization requires constant values for two zones, and Restart File Initialization requires a restart file in .dat or .csv format.

For more details on initialization, refer to this [page](../Initialization/).

### FileIO

This node supports managing file input/output. It includes options to rename Restart, Volume Output, and History files, and select their writing frequency for the current case. Additionally, there are options to overwrite Restart and Volume files.

### Solver

This node allows you to adjust the residual convergence value and iteration count, with support currently limited to ITER. Using the solver button, you can start SU2_CFD, and visualization will begin as the restart file is created. Please note that result visualization is currently supported only for 2D simulations, not 3D.