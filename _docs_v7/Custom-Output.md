---
title: History and Solution Output
permalink: /docs_v7/Custom-Output/
redirect_from: /docs/Custom-Output/
---

With v7.0 we have introduced a new way of customizing the output on screen, in the history file and in the visualization files.
It is now possible to individually define what you want to have in your output. 

---

- [Restart and Visualization Files](#restart-and-visualization-files)
  - [Setting Output Fields](#setting-output-fields)
  - [Example](#example)
- [Customizing the Screen and History Output](#customizing-the-screen-and-history-output)
  - [Screen Output](#screen-output)
  - [History Output](#history-output)
  - [Example](#example-1)
  
---


Let's define some terminology first.

- **Screen output** : The convergence history printed on the console.
- **History output**: The convergence history written to a file.
- **Volume output** : Everything written to the visualization and restart files.
- **Output field**: A single scalar value for screen and history output or a vector of a scalar quantity at every node in the mesh for the volume output.
- **Output group**: A collection of output fields.


**Note**: You can print all available output fields and groups available for the current solver (set with the `SOLVER` option) by calling `SU2_CFD` with the `-d` flag, i.e.
```
SU2_CFD -d <your_config_file.cfg>
```


## Restart and Visualization Files ##

SU2 can output the solution in several file formats. You can specify what files you want to have by setting the option `OUTPUT_FILES` to a list of files. The valid options are described in the following table:

| Option value | Description |
|---|---|
| `RESTART` | Native SU2 binary restart format |
| `RESTART_ASCII` | ASCII CSV restart format |
| `CSV` | ASCII CSV restart format (identical to `RESTART_ASCII`) |
| `PARAVIEW` | Binary Paraview XML .vtu format |
| `PARAVIEW_LEGACY` | Binary Paraview .vtk format |
| `PARAVIEW_MULTIBLOCK` | Paraview XML Multiblock .vtm format |
| `PARAVIEW_ASCII` | ASCII Paraview .vtk format |
| `TECPLOT` | Binary Tecplot .szplt format |
| `TECPLOT_ASCII` | ASCII Tecplot .dat format |
| `SURFACE_CSV` | Surface values in CSV format (includes all markers set with `MARKER_PLOTTING`) |
| `SURFACE_PARAVIEW` | Surface values in binary Paraview .vtu format (includes all markers set with `MARKER_PLOTTING`)|
| `SURFACE_PARAVIEW_LEGACY` | Surface values in binary Paraview .vtk format (includes all markers set with `MARKER_PLOTTING`)|
| `SURFACE_PARAVIEW_ASCII` | Surface values in ASCII Paraview .vtk format (includes all markers set with `MARKER_PLOTTING`)|
| `SURFACE_TECPLOT` | Surface values in binary Tecplot .szplt format (includes all markers set with `MARKER_PLOTTING`)|
| `SURFACE_TECPLOT_ASCII` | Surface values in ASCII Tecplot .dat format (includes all markers set with `MARKER_PLOTTING`)|

The default value of `OUTPUT_FILES` is `(RESTART, PARAVIEW, SURFACE_PARAVIEW)`. The output frequency can be set by using the `OUTPUT_WRT_FREQ` option. If it is a time-dependent problem, the frequency is based on the time iterations, while for steady-state problems it is based on the outer or inner iterations, depending on whether it is a multi-zone or single-zone problem, respectively.

**Note:** If run SU2 in parallel you should always use binary output files to get the best performance.

### Setting Output Fields ###

The `VOLUME_OUTPUT` option can be used to set fields for the restart and visualization files. Here you have the option to specify either single fields and/or groups.

### Example ###

For the compressible Navier-Stokes solver (i.e. `SOLVER=NAVIER_STOKES`), a **non-exhaustive list** of possible fields/groups is the following:

| Field Name | Description  | Group Name  |  
|---|---|---|
|  `COORD-X` | x coordinate | `COORDINATES`   |
|  `COORD-Y` | y coordinate   | `COORDINATES`   |
|  `COORD-Z` | z coordinate   |  `COORDINATES`  |
| `DENSITY` | Density | `SOLUTION`   |
|  `MOMENTUM-X` | Momentum x-component | `SOLUTION`   |
|  `MOMENTUM-Y` | Momentum y-component  | `SOLUTION`   |
|  `MOMENTUM-Z` | Momentum z-component |  `SOLUTION`  |
|  `ENERGY` | Density times the specific total energy  |  `SOLUTION`  |
|  `RMS_` | Root-mean square residual of the solution  |  `RMS_RES`  |
|  `PRESSURE` | Pressure|  `PRIMITIVE`  |
|  `TEMPERATURE` | Temperature |  `PRIMITIVE`  |
|  `MACH` | Mach Number |  `PRIMITIVE`  |
|  `PRESSURE_COEFF` | Pressure Coefficient  |  `PRIMITIVE`  |
|  `LAMINAR_VISCOSITY` | Laminar viscosity  |  `PRIMITIVE`  |
|  `SKIN_FRICTION-X` | Skin friction coefficient x-component in local coordinates |  `PRIMITIVE`  |
|  `SKIN_FRICTION-Y` | Skin friction coefficient y-component in local coordinates |  `PRIMITIVE`  |
|  `SKIN_FRICTION-Z` | Skin friction coefficient z-component in local coordinates |  `PRIMITIVE`  |
|  `HEAT_FLUX` | Heat flux |  `PRIMITIVE`  |
|  `Y_PLUS` | Y-Plus |  `PRIMITIVE`  |
| `VORTICITY` | Vorticity | `VORTEX_IDENTIFICATION` |
| `Q_Criterion` | Q-Criterion | `VORTEX_IDENTIFICATION` |


## Customizing the Screen and History Output ##

### Screen Output ###
You can define the output fields you want to have on screen by using the config option `SCREEN_OUTPUT`. 
Fields available depend on the solver you are using. Fields available for **all solvers** are the following:

- `TIME_ITER`:  Time iteration index
- `OUTER_ITER`: Outer (coupling) iteration index (for multi-zone problems only)
- `INNER_ITER`: Inner iteration index (pseudo-time iteration)
- `CUR_TIME`:   Current physical time of your simulation
- `TIME_STEP`:  Current time step
- `WALL_TIME`:  Current average wall-clock time for one iteration



If you run a multizone problem, the convergence history of the individual zones (i.e. the convergence of the inner iteration) is disabled by default and only the convergence of the outer iteration is shown. That means `SCREEN_OUTPUT` in the sub-config files is ignored. You can still print fields from individual zones by using the field name and the zone index. For example in an Fluid-Structure interaction problem the drag in zone 0 and the von-Mises stress in zone 1 can be used as fields by adding `DRAG[0]` and/or `VMS[1]` to the screen output in the main config file. It is possible to force the output of the full inner convergence history per zone by setting `WRT_ZONE_CONV` to `YES`. 

You can also customize the frequency when the convergence history should be written to screen by using `SCREEN_WRT_FREQ_INNER`, `SCREEN_WRT_FREQ_OUTER` and `SCREEN_WRT_FREQ_TIME`.


### History Output ###

The history output can be customized in a similar fashion to the screen output by using the `HISTORY_OUTPUT` option. In fact, screen and history outputs share all fields which means that everything that can written to screen can be written also to the history file and vice versa. However, instead of specifying single output fields, for the history output it is **only possible** to specify output groups by using the group name.

If you run a multizone problem, in addition to the history files per zone, a file (default: `history_multizone.dat`) will be created where the convergence history of the outer iteration is stored. Groups for this output can be set by using the `HISTORY_OUTPUT` option in the main config file.

You can also customize the frequency when the convergence history should be written to the history file by using `HISTORY_WRT_FREQ_INNER`, `HISTORY_WRT_FREQ_OUTER` and `HISTORY_WRT_FREQ_TIME`.

### Example ###

For the compressible Navier-Stokes solver (i.e. `SOLVER=NAVIER_STOKES`), a **non-exhaustive list** of possible fields/groups is the following:

| Field Name (for screen output)  | Description  | Group Name (for history output)  |  
|---|---|---|
| `TIME_ITER` | Time iteration index | `ITER`   |
| `OUTER_ITER` | Outer (coupling) iteration index. | `ITER`   |
| `INNER_ITER` | Inner iteration index (pseudo-time iteration). | `ITER`   |
| `CUR_TIME` | Current physical time of your simulation. | `TIME_DOMAIN`   |
| `TIME_STEP` |  Current time step. | `TIME_DOMAIN`   |
| `WALL_TIME` | Current average wall-clock time for one iteration. | `WALL_TIME`   |
| `RMS_DENSITY` | Root-mean square residual of the density. | `RMS_RES`   |
|  `RMS_MOMENTUM-X` | Root-mean square residual of the momentum x-component. | `RMS_RES`   |
|  `RMS_MOMENTUM-Y` | Root-mean square residual of the momentum y-component.  | `RMS_RES`   |
|  `RMS_MOMENTUM-Z` | Root-mean square residual of the momentum z-component.  |  `RMS_RES`  |
|  `RMS_ENERGY` | Root-mean square residual of the energy.  |  `RMS_RES`  |
|  `DRAG` | Total Drag coefficient. |  `AERO_COEFF`  |
|  `LIFT` | Total Lift coefficient |  `AERO_COEFF`  |
|  `SIDEFORCE` | Total Sideforce coefficient.  |  `AERO_COEFF`  |
|  `MOMENT-X` | Total Moment around the x-axis.  |  `AERO_COEFF`  |
|  `MOMENT-Y` | Total Moment around the y-axis.  |  `AERO_COEFF`  |
|  `MOMENT-Z` | Total Moment around the z-axis. |  `AERO_COEFF`  |
|  `FORCE-X` | Total Force in x direction. |  `AERO_COEFF`  |
|  `FORCE-Y` | Total Force in y direction. |  `AERO_COEFF`  |
|  `FORCE-Z` | Total Force in z direction.|  `AERO_COEFF`  |
|  `EFFICIENCY` | Total Lift-to-drag ratio. |  `AERO_COEFF`  |

