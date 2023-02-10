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
  - [User Defined Functions ](#user-defined-functions)
  
---


Let's define some terminology first.

- **Screen output** : The convergence history printed on the console.
- **History output**: The convergence history written to a file.
- **Volume output** : Everything written to the visualization and restart files.
- **Output field**: A single scalar value for screen and history output or a vector of a scalar quantity at every node in the mesh for the volume output.
- **Output group**: A collection of output fields.


**Note**: You can print all available output fields and groups available for the current solver (set with the `SOLVER` option) by calling `SU2_CFD` with the `-d` flag (dry-run mode), i.e.
```
SU2_CFD -d <your_config_file.cfg>
```


## Restart and Visualization Files ##

SU2 can output the solution in several file formats. You can specify what files you want to have by setting the option `OUTPUT_FILES` to a list of files. The valid options are described in the following table:

| Option value | Description |
|---|---|
| `RESTART` | Native SU2 binary restart format |
| `RESTART_ASCII` | Native SU2 ASCII CSV restart format |
| `STL_BINARY` | binary mesh in .stl format |
| `STL_ASCII` | ASCII mesh in .stl format |
| `MESH` | Native SU2 mesh in .su2 format |
| `CSV` | ASCII CSV restart format (identical to `RESTART_ASCII`) |
| `PARAVIEW_MULTIBLOCK` | Binary Paraview .vtm format |
| `PARAVIEW` | Binary Paraview .vtk format |
| `PARAVIEW_ASCII` | ASCII Paraview .vtk format |
| `TECPLOT` | Binary Tecplot .szplt format |
| `TECPLOT_ASCII` | ASCII Tecplot .dat format |
| `SURFACE_CSV` | Surface values in CSV format (includes all markers set with `MARKER_PLOTTING`) |
| `SURFACE_PARAVIEW` | Surface values in binary Paraview .vtk format (includes all markers set with `MARKER_PLOTTING`)|
| `SURFACE_PARAVIEW_ASCII` | Surface values in ASCII Paraview .vtk format (includes all markers set with `MARKER_PLOTTING`)|
| `SURFACE_TECPLOT` | Surface values in binary Tecplot .szplt format (includes all markers set with `MARKER_PLOTTING`)|
| `SURFACE_TECPLOT_ASCII` | Surface values in ASCII Tecplot .dat format (includes all markers set with `MARKER_PLOTTING`)|

The default value of `OUTPUT_FILES` is `(RESTART, PARAVIEW, SURFACE_PARAVIEW)`. The output frequencies can be set by using the `OUTPUT_WRT_FREQ` option. OUTPUT_WRT_FREQ accepts a list of integer values for each of the file types in `OUTPUT_FILES`. If a single value is given, this value will be used as the writing frequency for all output files. If 2 values are used, the first value is used for the first file type in OUTPUT_FILES, and the second value is used for the other file types in the list. For time-dependent problems, the frequency is based on the time iterations, while for steady-state problems it is based on the outer or inner iterations, depending on whether it is a multi-zone or single-zone problem, respectively.

**Note:** If you run SU2 in parallel you should always use binary output files to get the best performance.

### Setting Output Fields ###

The `VOLUME_OUTPUT` option can be used to set fields for the restart and visualization files. Here you have the option to specify either single fields and/or groups.

| Option value | Default value | Description | Data type |
|---|---|---|---|
| VOLUME_OUTPUT| COORDINATES,SOLUTION,PRIMITIVE| fields or groups that will be saved to file| list of keywords|


### Example ###

Groups and fields can be combined, e.g.:

`VOLUME_OUTPUT= SOLUTION, PRESSURE, DENSITY `

will save all field that are in the `SOLUTION` group. Pressure is in the `PRIMITIVE` group for the compressible solver and in the `SOLUTION` group for the incompressible solver. Density on the other hand is in the `SOLUTION` group for the compressible solver and in the `PRIMITIVE` group for the incompressible solver. They can be added individually as in the example above, or by simply adding the entire `PRIMITIVE` group to the list if file size is no issue. Note that keywords that are not valid for the current setup will simply be ignored. 

For the compressible Navier-Stokes solver (i.e. `SOLVER=NAVIER_STOKES`), a **non-exhaustive list** of possible fields/groups is the following:

| Field Name | Description  | Group Name  |  Remarks |
|---|---|---|
|  `COORD-X` | x coordinate | `COORDINATES`   | - |
|  `COORD-Y` | y coordinate   | `COORDINATES`   | - |
|  `COORD-Z` | z coordinate   |  `COORDINATES`  | 3D only |
|  `DENSITY` | Density | `SOLUTION`   | - |
|  `MOMENTUM-X` | Momentum x-component | `SOLUTION`   | - |
|  `MOMENTUM-Y` | Momentum y-component  | `SOLUTION`   | - |
|  `MOMENTUM-Z` | Momentum z-component |  `SOLUTION`  | 3D only |
|  `ENERGY` | Energy  |  `SOLUTION`  | - |
|  `PRESSURE` | Pressure|  `PRIMITIVE`  | - |
|  `TEMPERATURE` | Temperature |  `PRIMITIVE`  | - |
|  `MACH` | Mach Number |  `PRIMITIVE`  | - |
|  `PRESSURE_COEFF` | Pressure Coefficient  |  `PRIMITIVE`  | - |
|  `LAMINAR_VISCOSITY` | Laminar viscosity  |  `PRIMITIVE`  | - |
|  `SKIN_FRICTION-X` | Skin friction coefficient x-component |  `PRIMITIVE`  | - |
|  `SKIN_FRICTION-Y` | Skin friction coefficient y-component  |  `PRIMITIVE`  | - |
|  `SKIN_FRICTION-Z` | Skin friction coefficient z-component |  `PRIMITIVE`  | 3D only |
|  `HEAT_FLUX` | Heat flux |  `PRIMITIVE`  | - |
|  `Y_PLUS` | Y-Plus |  `PRIMITIVE`  | - |

Additionally, for every field in the SOLUTION group, the limiters (group name `LIMITER`) and residuals (group name RESIDUAL) can be saved by adding `RES_` or `LIMITER_` in front of the field name. 


For the incompressible Navier-Stokes solver (i.e. `SOLVER=INC_NAVIER_STOKES`), the solution group is different:

| Field Name | Description  | Group Name  |  Remarks |
|---|---|---|
|  `PRESSURE` | Pressure | `SOLUTION`   | - |
|  `VELOCITY-X` | Velocity x-component | `SOLUTION`   | - |
|  `VELOCITY-Y` | Velocity y-component  | `SOLUTION`   | - |
|  `VELOCITY-Z` | Velocity z-component |  `SOLUTION`  | 3D only |
|  `TEMPERATURE` | Static Temperature  |  `SOLUTION`  | `INC_ENERGY_EQUATION= YES` |
|  `DENSITY` | Density  |  `PRIMITIVE`  | - |


Turbulence quantities:

| Field Name | Description  | Group Name  |  Remarks |
|---|---|---|
|  `NU_TILDE` | Spalart Allmaras variable | `SOLUTION`   | SA models |
|  `TKE` | Turbulent kinetic energy k | `SOLUTION`   | SST models |
|  `DISSIPATION` | Turbulent dissipation rate omega   | `SOLUTION`   | SST models |
|  `EDDY_VISCOSITY` | Turbulent eddy viscosity  |  `PRIMITIVE`  | - |


To inspect the mesh quality we additionaly have:

| Field Name | Description  | Group Name  |  Remarks |
|---|---|---|
|  `ORTHOGONALITY` | Orthogonality angle |  `MESH_QUALITY`  | - |
|  `ASPECT_RATIO` | CV Aspect ratio |  `MESH_QUALITY`  | - |
|  `VOLUME_RATIO` | CV sub-volume ratio |  `MESH_QUALITY`  | - |

For moving grids:

| Field Name | Description  | Group Name  |  Remarks |
|---|---|---|
|  `GRID_VELOCITY-X` | X-component of grid velocity vector |  `GRID_VELOCITY`  | - |
|  `GRID_VELOCITY-Y` | Y-component of grid velocity vector |  `GRID_VELOCITY`  | - |
|  `GRID_VELOCITY-Z` | Z-component of grid velocity vector |  `GRID_VELOCITY`  | 3D only |


## Customizing the Screen and History Output ##

### Screen Output ###
You can define the output fields you want to have printed on screen by using the config option `SCREEN_OUTPUT`. 

| Option value | Default value | Description | Data type | Remark |
|---|---|---|---|---|
| SCREEN_OUTPUT| INNER_ITER, RMS_DENSITY, RMS_MOMENTUM-X,RMS_MOMENTUM-Y, RMS_ENERGY| field or group that will be printed to screen | list of keywords| compressible |
| SCREEN_OUTPUT| INNER_ITER, RMS_PRESSURE, VELOCITY-X,VELOCITY-Y| field or group that will be printed to screen | list of keywords| incompressible |


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

The history output can be customized in a similar fashion as the screen output by using the `HISTORY_OUTPUT` option. In fact, screen and history outputs share all fields which means that everything that can written to screen can be written also to the history file and vice versa. 

If you run a multizone problem, in addition to the history files per zone, a file (default: `history_multizone.dat`) will be created where the convergence history of the outer iteration is stored. Groups for this output can be set by using the `HISTORY_OUTPUT` option in the main config file.

You can also customize the frequency when the convergence history should be written to the history file by using `HISTORY_WRT_FREQ_INNER`, `HISTORY_WRT_FREQ_OUTER` and `HISTORY_WRT_FREQ_TIME`.

### Example ###

For the compressible Navier-Stokes solver (i.e. `SOLVER=NAVIER_STOKES`), a **non-exhaustive list** of possible fields/groups is the following:

| Field Name  | Description  | Group Name  |  
|---|---|---|
| `TIME_ITER` | Time iteration index | `ITER`   |
| `OUTER_ITER` | Outer (coupling) iteration index. | `ITER`   |
| `INNER_ITER` | Inner iteration index (pseudo-time iteration). | `ITER`   |
| `CUR_TIME` | Current physical time of your simulation. | `TIME_DOMAIN`   |
| `TIME_STEP` |  Current time step. | `TIME_DOMAIN`   |
| `WALL_TIME` | Current average wall-clock time for one iteration. | `WALL_TIME`   |
| `RMS_DENSITY` | Root-mean square residual of the density. | `RMS_RES`   |
| `RMS_MOMENTUM-X` | Root-mean square residual of the momentum x-component. | `RMS_RES`   |
| `RMS_MOMENTUM-Y` | Root-mean square residual of the momentum y-component.  | `RMS_RES`   |
| `RMS_MOMENTUM-Z` | Root-mean square residual of the momentum z-component.  |  `RMS_RES`  |
| `RMS_ENERGY` | Root-mean square residual of the energy.  |  `RMS_RES`  |
| `DRAG` | Total Drag coefficient. |  `AERO_COEFF`  |
| `LIFT` | Total Lift coefficient |  `AERO_COEFF`  |
| `SIDEFORCE` | Total Sideforce coefficient.  |  `AERO_COEFF`  |
| `MOMENT_X` | Total Moment around the x-axis.  |  `AERO_COEFF`  |
| `MOMENT_Y` | Total Moment around the y-axis.  |  `AERO_COEFF`  |
| `MOMENT_Z` | Total Moment around the z-axis. |  `AERO_COEFF`  |
| `FORCE_X` | Total Force in x direction. |  `AERO_COEFF`  |
| `FORCE_Y` | Total Force in y direction. |  `AERO_COEFF`  |
| `FORCE_Z` | Total Force in z direction.|  `AERO_COEFF`  |
| `EFFICIENCY` | Total Lift-to-drag ratio. |  `AERO_COEFF`  |

### User Defined Functions ###

From version 7.4.0 it is possible for users to create custom outputs via math expressions of solver variables and built-in outputs.
All custom outputs are specified via the config option `CUSTOM_OUTPUTS`, in general the syntax to define a custom output is `name : type{expression}[markers];` (note the use of ; to separate different outputs).
Where 'name' is the identifier that can be used to request output to screen or history file, and also to reference the output in other custom outputs (he group name for all custom outputs is `CUSTOM`).

The available types are:
- `Macro`: Introduces a new field that can only be used in other expressions, it is not an output by itself (note the "$" symbol to reference macros in the example below).
- `Function`: Introduces a new scalar output that is a function of other scalar outputs, it cannot reference fields (e.g. velocity).
- `AreaAvg` and `AreaInt`: Computes an area average or integral of a field (the expression) over the list of markers.
- `MassFlowAvg` and `MassFlowInt`: Computes a mass flow average or integral.
- `Probe`: Evaluates the expression using the values of the mesh point closest to the coordinates specified inside "[]", [x, y] or [x, y, z] (2 or 3D).

**Note:** Each custom output can only use one type, e.g. it is not possible to write `p_drop : AreaAvg{PRESSURE}[inlet] - AreaAvg{PRESSURE}[outlet]`. This would need to be separated into two `AreaAvg` outputs and one `Function` to compute their difference.

**Example:**
```
CUSTOM_OUTPUTS= 'velocity : Macro{sqrt(pow(VELOCITY_X, 2) + pow(VELOCITY_Y, 2) + pow(VELOCITY_Z, 2))};\
                 avg_vel : AreaAvg{$velocity}[z_minus, z_plus];\
                 var_vel : AreaAvg{pow($velocity - avg_vel, 2)}[z_minus, z_plus];\
                 dev_vel : Function{sqrt(var_vel) / avg_vel};\
                 probe1 : Probe{$velocity}[0.005, 0.005, 0.05]'
```

To obtain the list of solver variables that can be used, write an invalid expression (e.g. 'x : AreaAvg{INVALID}[]') and run SU2.

To use a custom output as the objective function of the discrete adjoint solver, use `OBJECTIVE_FUNCTION= CUSTOM_OBJFUNC` and set `CUSTOM_OBJFUNC` appropriately, for example:
```
CUSTOM_OBJFUNC= 'LIFT + dev_vel'
```

For more details see the [example test case](https://github.com/su2code/SU2/blob/master/TestCases/user_defined_functions/lam_flatplate.cfg).

