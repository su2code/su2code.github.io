---
title: Inviscid Hypersonic Wedge
permalink: /tutorials/Inviscid Hypersonic Wedge/
written_by: CatarinaGarbacz
for_version: 7.0.0
revised_by: jtneedels
revision_date: 2023-01-22
revised_version: 7.5.0
solver: NEMO_EULER
requires: SU2_CFD
complexity: basic
follows: 
---

## Goals

Upon completion of this tutorial, the user will be familar with performing a simulation of external, inviscid flow over a 2D geometry using the NEMO Euler solver. The specific geometry chosen for the tutorial is a 10 degree wedge. Consequently, the following capabilities of SU2 will be showcased in the tutorial:
- Steady, 2D thermochenical nonequilibrium Euler equations
- AUSM convective scheme in space (2nd-order, updwind)
- Euler implicit time integration
- Farfield, Outlet, and Euler Wall boundary conditions

The intent of this tutorial is to introduce the setup of a thermochemical nonequilibrium simulation using a simple 2D geometry.

## Resources

You can find the resources for this tutorial in the folder [nemo/Inviscid_Hypersonic_Wedge](https://github.com/su2code/Tutorials/blob/master/nemo/Inviscid_Hypersonic_Wedge/) in the [tutorial repository](https://github.com/su2code/Tutorials). You will need the mesh file [invwedge.su2](https://github.com/su2code/Tutorials/blob/master/nemo/Inviscid_Hypersonic_Wedge/invwedge.su2)
and the config file [invwedge.cfg](https://github.com/su2code/Tutorials/blob/master/nemo/Inviscid_Hypersonic_Wedge/invwedge_ausm.cfg).

## Tutorial

The following tutorial will walk you through the steps required when solving for the flow through the channel using SU2. It is assumed you have already obtained and compiled SU2_CFD. If you have yet to complete these requirements, please see the [Download](/docs_v7/Download/) and [Installation](/docs_v7/Installation/) pages.

## Background

This example uses a 2D wedge geometry, a canonical propblem in supersonic and hypersonic flows. It is meant to be a simple test in inviscid flow for the general setup of a thermochemical nonequilibrium flow simulation.

## Problem Setup

This tutorial will solve the for the flow through the channel with these conditions:
- Gas Model = AIR-5 (five species air model)
- Gas Composition, mass fraction (N2, O2, NO, N, O) = (0.77, 0.23, 0.00, 0.00, 0.00)
- Free-stream Static Temperature = 288.15 K
- Free-stream Static Temperature_ve = 288.15 K
- Free-stream Static Pressure = 101325.0 N/m2
- Free-stream Mach Number = 5.0
- Outlet Static Pressure = 10.0 N/m2

### Mesh Description

The mesh geometry features a 10 degree wedge, composed of quadrilaterals with 370 cells in the axial direction and 70 cells in the wall normal direction. The following figure contains a view of the mesh topology

![Wedge Mesh](../../tutorials_files/nemo/Inviscid_Hypersonic_Wedge/images/inwedge_mesh_bcs.png)
Figure (1): The computational mesh with boundary conditions highlighted.

The boundary conditions for the channel are also highlighted in the figure. Farfield, outlet, and Euler wall boundary conditions are used. The Euler wall boundary condition enforces both symmetry along the inlet and flow tangency on the surface of the wedge.

It should be noted the farfield boundary implementation for the NEMO solver is not a characteristic based farfield, but enforces the flow conditions on the boundary. This is appropriate for hypersonic flow, where there is no outgoing characteristic. The outlet boundary has a Mach switch, enforcing a supersonic outlet for supersonic flow and a characteristic based outlet for subsonic flow. The characteristic based outlet requires specification of a back pressure to fully specify the state at the exit.

### Configuration File Options

Several of the key configuration file options for this simulation are highlighted here. Here we explain details on free-stream composition.

```
% ------------- DIRECT, ADJOINT, AND LINEARIZED PROBLEM DEFINITION ------------%
%
SOLVER= NEMO_EULER
GAS_MODEL= AIR-5
GAS_COMPOSITION= (0.77, 0.23, 0.0, 0.0, 0.0)
MATH_PROBLEM= DIRECT
RESTART_SOL= NO

% ----------- COMPRESSIBLE AND INCOMPRESSIBLE FREE-STREAM DEFINITION ----------%
%
MACH_NUMBER= 5
AOA= 0.0
SIDESLIP_ANGLE= 0.0
FREESTREAM_PRESSURE= 101325.0
FREESTREAM_TEMPERATURE= 288.15
FREESTREAM_TEMPERATURE_VE= 288.15

% ---- NONEQUILIBRIUM GAS, IDEAL GAS, POLYTROPIC, VAN DER WAALS AND PENG ROBINSON CONSTANTS -------%
%
FLUID_MODEL= SU2_NONEQ
```

For thermochemical nonequilibrium Euler simulations, `NEMO_EULER` must be specified using the `SOLVER` config option. For NEMO simulations, a gas model and free-stream gas composition must also be specified. In this case, we choose a five species air model consisting of N2, O2, NO, N, and O with an initial composition of 77% N2 and 23% O2. Finally, for NEMO simulations it is also necessary to specify the thermochemical library using the `FLUID_MODEL` option. In this case we choose the SU2 built-in thermochemical library, `SU2_NONEQ`.

Here we explain some details on markers and boundary conditions:

```
% -------------------- BOUNDARY CONDITION DEFINITION --------------------------%
%
MARKER_EULER= ( Euler, Wall )
MARKER_OUTLET= ( Exit, 10 )
MARKER_FAR = ( Farfield, Inlet )
```

The 5 different boundary markers in the computational grid must have an accompanying string name. These marker names (Euler, Wall, Exit, and Outlet, and Inlet ) are each given a specific type of boundary condition in the config file. 

```
% ------------------------ SURFACES IDENTIFICATION ----------------------------%
%
MARKER_PLOTTING= (NONE )
MARKER_MONITORING= ( Wall )
```

Any boundary markers that are listed in the `MARKER_PLOTTING` option will be written into the surface solution vizualization file. Any surfaces on which an objective is to be calculated, such as forces or moments, must be included in the `MARKER_MONITORING` option.

Some basic options related to time integration:

```
% ------------- COMMON PARAMETERS DEFINING THE NUMERICAL METHOD ---------------%
%
NUM_METHOD_GRAD= WEIGHTED_LEAST_SQUARES
CFL_NUMBER= 3
ITER= 999
LINEAR_SOLVER= BCGSTAB
LINEAR_SOLVER_ERROR= 1E-6
LINEAR_SOLVER_ITER= 5

% -----------------------------------------------------------------------%
%
CONV_NUM_METHOD_FLOW= AUSM
MUSCL_FLOW= YES
SLOPE_LIMITER_FLOW= VENKATAKRISHNAN
VENKAT_LIMITER_COEFF= 0.05
TIME_DISCRE_FLOW= EULER_IMPLICIT
```

In general, users can choose from explicit or implicit time integration schemes.

Setting the convergence criteria:
```
% --------------------------- CONVERGENCE PARAMETERS --------------------------%
%
CONV_RESIDUAL_MINVAL= -10
CONV_STARTITER= 10
CONV_CAUCHY_ELEMS= 100
CONV_CAUCHY_EPS= 1E-10
```

There are three different types of criteria for terminating a simulation in SU2: running a specified number of iterations (`ITER` option), reducing the residual of a chosen equation by a specified order of magnitude (or reaching a specified lower limit), or by converging a particular output quantity, such as drag, to a certain tolerance. 


### Running SU2

To run this test case, follow these steps at a terminal command line:
 1. Move to the directory containing the config file ([invwedge_ausm.cfg](https://github.com/su2code/Tutorials/blob/master/nemo/Inviscid_Hypersonic_Wedge/invwedge_ausm.cfg)) and the mesh file ([invwedge.su2](https://github.com/su2code/Tutorials/blob/master/nemo/Inviscid_Hypersonic_Wedge/invwedge.su2)). Make sure that the SU2 tools were compiled, installed, and that their install location was added to your path.
 2. Run the executable by entering 
 
    ```
    $ SU2_CFD invwedge_ausm.cfg
    ```
     
     at the command line.
 3. SU2 will print residual updates with each iteration of the flow solver, and the simulation will finish after reaching the specified convergence criteria.
 4. Files containing the results will be written upon exiting SU2. The flow solution can be visualized in ParaView (.vtk) or Tecplot (.dat for ASCII). To visualize the flow solution in ParaView update the `OUTPUT_FORMAT` setting in the configuration file.

### Results

The following images show some SU2 results for the inviscid channel problem.

![Wedge Mach](../../tutorials_files/nemo/Inviscid_Hypersonic_Wedge/images/invwedge_mach.png)
Figure (2): Mach number contours for the 2D wedge.

![Wedge Pressure](../../tutorials_files/nemo/Inviscid_Hypersonic_Wedge/images/invwedge_pressure.png)
Figure (3): Pressure contours for the 2D wedge.
