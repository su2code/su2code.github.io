---
title: Unsteady Conjugate Heat Transfer
permalink: /tutorials/Inc_Heated_Cylinders_Unsteady/
written_by: oleburghardt
for_version: 7.1.0
revised_by: TobiKattmann
revision_date: 2021-03-04
revised_version: 7.1.1
solver: INC_NAVIER_STOKES, HEAT_EQUATION
requires: SU2_CFD
complexity: advanced
follows: Static_CHT
userguide: Multizone
---

<br>
<iframe width="560" height="315" src="https://www.youtube.com/embed/MqN8GalSyzk" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Goals

This tutorial is a follow-up on the [heated cylinders with conjugate heat transfer tutorial](/tutorials/Inc_Heated_Cylinders/) where a steady CHT solution was computed for a problem involving multiple physical zones.
The following capabilities of SU2 will be showcased in this tutorial:

- Time domain and time-marching config file options (plus related ones) for unsteady simulations
- Use of time iterations, outer and inner iterations
- Paraview multiblock output

The intent of this tutorial is to demonstrate how a steady CHT simulation can be turned into an unsteady one.

## Resources

The resources for this tutorial can be found in the [Inc_Heated_Cylinders_Unsteady](https://github.com/su2code/Tutorials/tree/master/multiphysics/unsteady_cht) directory in the [tutorial repository](https://github.com/su2code/Tutorials). You will need the configuration files for all physical zones ([flow_cylinder.cfg](https://github.com/su2code/Tutorials/tree/master/multiphysics/unsteady_cht/flow_cylinder.cfg), [solid_cylinder1.cfg](https://github.com/su2code/Tutorials/tree/master/multiphysics/unsteady_cht/solid_cylinder1.cfg), [solid_cylinder2.cfg](https://github.com/su2code/Tutorials/tree/master/multiphysics/unsteady_cht/solid_cylinder2.cfg), [solid_cylinder3.cfg](https://github.com/su2code/Tutorials/tree/master/multiphysics/unsteady_cht/solid_cylinder3.cfg)), the cofiguration file to invoke a multiphysics simulation run ([cht_2d_3cylinders.cfg](https://github.com/su2code/Tutorials/tree/master/multiphysics/unsteady_cht/cht_2d_3cylinders.cfg)) and the mesh file ([mesh_cht_3cyl.su2](https://github.com/su2code/Tutorials/tree/master/multiphysics/unsteady_cht/mesh_cht_3cyl.su2)).

## Tutorial

The following tutorial will walk you through the steps required when solving for an unsteady coupled CHT solution. It is assumed you have already obtained and compiled the SU2_CFD code for a serial computation. If you have yet to complete these requirements, please see the [Download](/docs/Download/) and [Installation](/docs/Installation/) pages and that make sure you have completed the [heated cylinders with conjugate heat transfer tutorial](/tutorials/Inc_Heated_Cylinders/).

### Background

For unsteady flows around walls that are transferring heat from an adjacent (solid) zone, the coupling of temperature and heat flux distributions has to be resolved for each and every time step. Both will vary over time as they depend on the current flow field.

### Problem Setup

The problem setup is the same as in the [heated cylinders with conjugate heat transfer tutorial](/tutorials/Inc_Heated_Cylinders/) except for the density. It is increased in all zones by a factor of 100 so that for the flow we obtain a Reynolds number of 4000 which will make it unsteady. Thus we set
```
INC_DENSITY_INIT= 0.0210322
```
in [flow_cylinder.cfg](https://github.com/su2code/Tutorials/tree/master/multiphysics/unsteady_cht/flow_cylinder.cfg) and

```
MATERIAL_DENSITY= 0.0210322
```
in [solid_cylinder1.cfg](https://github.com/su2code/Tutorials/tree/master/multiphysics/unsteady_cht/solid_cylinder1.cfg), [solid_cylinder2.cfg](https://github.com/su2code/Tutorials/tree/master/multiphysics/unsteady_cht/solid_cylinder2.cfg) and [solid_cylinder3.cfg](https://github.com/su2code/Tutorials/tree/master/multiphysics/unsteady_cht/solid_cylinder3.cfg)

For simplicity we leave all other parameters unchanged.

### Mesh Description

The [mesh](https://github.com/su2code/Tutorials/tree/master/multiphysics/unsteady_cht/mesh_cht_3cyl.su2) is the same as in the [heated cylinders with conjugate heat transfer tutorial](/tutorials/Inc_Heated_Cylinders/).

### Configuration File Options

An unsteady simulation is set up by enabling the time domain and choosing a time marching algorithm in the [master config file](https://github.com/su2code/Tutorials/tree/master/multiphysics/unsteady_cht/cht_2d_3cylinders.cfg):

```
TIME_DOMAIN = YES
%
%
TIME_MARCHING= DUAL_TIME_STEPPING-2ND_ORDER
```

The time marching parameters have to match the flow physics that should be resolved. For a given inlet velocity of 3.40297 m/s at Re = 4000, the Strouhal number estimation for the most upstream cylinder is Sr = 0.21. This gives a frequency of f = Sr*v = 0.71Hz for the vortex shedding so that a time step of 0.05s is chosen in the [master config file](https://github.com/su2code/Tutorials/tree/master/multiphysics/unsteady_cht/cht_2d_3cylinders.cfg):

```
TIME_STEP= 0.05
```

In order to sufficiently resolve the coupling in each time step, we set the number of outer iterations to 200 in the [master config file](https://github.com/su2code/Tutorials/tree/master/multiphysics/unsteady_cht/cht_2d_3cylinders.cfg):

```
OUTER_ITER = 200
```

The number of inner (zone-internal) iterations is set to 1 by default. We do not have to touch any of the zone-specific config files for unsteady options.

### Running SU2

One time iteration will run rather quick and it is up to the user for how long the simulation should run or, equivalently, which physical time span should be covered. In the video above, 1000 time steps had been computed to generate a 50s realtime video. See the [heated cylinders with conjugate heat transfer tutorial](/tutorials/Inc_Heated_Cylinders/) how to execute SU2_CFD.