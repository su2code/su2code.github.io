---
title: Guide to Version v7
permalink: /docs_v7/Guide-to-v7/
redirect_from: /docs/Guide-to-v7/
---

With v7.0 we have introduced a lot of updates and changes that affect how you interact with the code. This document gives an overview on the most important changes, so that you can quickly update your existing config files to be compatible with v7.0. 

---

- [Definition of the physical problem and solver](#definition-of-the-physical-problem-and-solver)
- [Definition of the incompressible solver](#definition-of-the-incompressible-solver)
- [Controlling the solver](#controlling-the-solver)
- [Output options](#output-options)
- [ASCII Restart format](#ascii-restart-format)
- [Grid/mesh movement](#gridmesh-movement)
- [Setting convergence criteria](#setting-convergence-criteria)

---


### Definition of the physical problem and solver ###

The option `PHYSICAL_PROBLEM` has been renamed to `SOLVER`. The rational behind this change is that we are going to have several different solvers in the future which essentially solve the same physical problems. You can find a list of current solvers in the new [Solver Setup](/docs_v7/Solver-Setup) section.

### Definition of the incompressible solver ###

The option `REGIME_TYPE` has been removed. In line with the change above, the incompressible solver is now specified using the `SOLVER` option by setting it to `INC_EULER`, `INC_NAVIER_STOKES` or `INC_RANS`.

### Controlling the solver ###

We have made the control of the different solvers more consistent. In particular setting the number of iterations. The option `EXT_ITER` has been removed and is replaced depending on the definition of the problem. Options for defining a time-dependent problem also changed. More details can be found in the table below and in section [Solver Setup](/docs_v7/Solver-Setup).

| Old option name | New option name | Note
| --- | --- | --- |
| `EXT_ITER` | `INNER_ITER`/`ITER` or `OUTER_ITER` or `TIME_ITER`|  Depending on the problem
| `UNSTEADY_SIMULATION` | `TIME_MARCHING` | Option values are the same as before |
| - | `TIME_DOMAIN` | Value `YES` enables the time-dependent mode (default is `NO`) |
| `UNST_TIMESTEP` | `TIME_STEP` | - |
| `UNST_TIME` | `MAX_TIME` | - |
| `UNST_TIME_ITER` | `INNER_ITER` | - |

### Output options ###

A lot of effort has been put into making the output more customizable. Below you find a list of options that have changed.

| Old option name | New option name | Note
| --- | --- | --- |
| `SOLUTION_FLOW_FILENAME` | `SOLUTION_FILENAME` | - |
| `RESTART_FLOW_FILENAME` | `RESTART_FILENAME` | - |
| `SURFACE_FLOW_FILENAME` | `SURFACE_FILENAME` | - |
| `VOLUME_FLOW_FILENAME` | `VOLUME_FILENAME` | - |
| `OUTPUT_FORMAT` | `TABULAR_FORMAT` | This option now defines **only** the format of tabular outputs like the history files (values are `CSV`, `TECPLOT`) |
| - | `OUTPUT_FILES` | Replaces the options `WRT_VOL_SOL`, `WRT_SRF_SOL`, `WRT_CSV_SOL`, `WRT_BINARY_RESTART`, by specifying a list of files to output (see [Custom Output](/docs_v7/Custom-Output))|
| `WRT_SOL_FREQ_DUALTIME`,  `WRT_SOL_FREQ` |  `OUTPUT_WRT_FREQ` | - |
| `WRT_CON_FREQ_DUALTIME`,  `WRT_CON_FREQ` |  `SCREEN_WRT_FREQ_INNER`, `SCREEN_WRT_FREQ_OUTER`, `SCREEN_WRT_FREQ_TIME` | Same options exist for history output (by replacing `SCREEN_*` with `HISTORY_*`) |
| `WRT_OUTPUT`|  - | Removed. Equivalent behavior can be achieved by setting `OUTPUT_FILES` to `NONE` |
| `WRT_RESIDUALS`, `WRT_LIMITERS` | `VOLUME_OUTPUT`| Add the corresponding fields to the new option | 
| `LOW_MEMORY_OUTPUT` | - | Removed. Equivalent behavior can be achieved by setting `VOLUME_OUTPUT` to `COORDINATES, SOLUTION`|

**Important note**: Visualization files are now also written when the code runs in parallel (if added to `OUTPUT_FILES`). 

### ASCII Restart format ###

The ASCII restart format has been changed to a `CSV` format. As a consequence **ASCII restart files** generated with a version before 7.0 are not compatible any more. However, in your installation directory you will find a python script called `convert_to_csv.py` that will convert old restart files to the new format. On your commandline use
```
convert_to_csv.py -i your_restart.dat
```
to run the script. This will create a file called `your_restart.csv` wich can be used as input if you disable reading binary files with `READ_BINARY_RESTART` set to `NO`.

### Grid/mesh movement ###

Mesh movement has been split into grid movement (motion is applied on the whole mesh, `GRID_MOVEMENT` option) and surface movement (motion is defined for a particular marker, `SURFACE_MOVEMENT` option).

| Option | Option values | Options to define the movement|
| --- | --- | --- |
|`GRID_MOVEMENT`| `RIGID_MOTION`, `ROTATING_FRAME`, `STEADY_TRANSLATION` | `MOTION_ORIGIN`, `TRANSLATION_RATE`, `ROTATION_RATE`, `PITCHING_OMEGA`, `PITCHING_AMPL`, `PITCHING_PHASE`, `PLUNGING_OMEGA`, `PLUNGING_AMPL`
| `SURFACE_MOVEMENT` | `DEFORMING`, `MOVING_WALL`, `EXTERNAL`, `EXTERNAL_ROTATION` | `SURFACE_MOTION_ORIGIN`, `SURFACE_TRANSLATION_RATE`, `SURFACE_ROTATION_RATE`, `SURFACE_PITCHING_OMEGA`, `SURFACE_PITCHING_AMPL`, `SURFACE_PITCHING_PHASE`, `SURFACE_PLUNGING_OMEGA`, `SURFACE_PLUNGING_AMPL`


### Setting convergence criteria ###
Below are the options that have changed or are removed:

| Old option name | New option name | Note
| --- | --- | --- |
| `RESIDUAL_MINVAL` | `CONV_RESIDUAL_MINVAL` | - |
| `CAUCHY_ELEMS` | `CONV_CAUCHY_ELEMS` | - |
| `CAUCHY_EPS` | `CONV_CAUCHY_EPS` | - |
| `CONV_CRITERIA` | `CONV_FIELD` | Accepts all fields available as output for the current solver (see [Solver Setup](/docs_v7/Solver-Setup#setting-convergence-critera))|
| `RESIDUAL_REDUCTION` | - | Removed. Equivalent behavior can be achieved by choosing a relative residual field for `CONV_FIELD` and setting `CONV_RESIDUAL_MINVAL` appropriately. 


