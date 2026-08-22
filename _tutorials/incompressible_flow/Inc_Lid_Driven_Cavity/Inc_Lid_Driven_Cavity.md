---
title: "Incompressible, Lid Driven Cavity Flow"
permalink: "/tutorials/Inc_Lid_Driven_Cavity/"
written_by: Thijs Aalbers
for_version: 8.5.0
revised_by: ...
revision_date: ...
revised_version: ...
solver: INC_NAVIER_STOKES
requires: SU2_CFD
complexity: beginner
follows:
---

![LDC velocity contours](../../tutorials_files/incompressible_flow/Inc_Lid_Driven_Cavity/images/ldc_velocity.png)

## Goals

Upon completing this tutorial, the user will be familiar with performing a simulation of laminar, incompressible, lid-driven flow within a cavity. Consequently, the following capabilities of SU2 will be showcased in this tutorial:

- Steady, 2D, laminar, incompressible, Navier-Stokes equations 
- Upwind Difference Scheme (UDS) convective scheme in space (2nd-order, upwind)
- The pressure-correction solver for incompressible flow (PISO)

The intent of this tutorial is to demonstrate the pressure-correction solver (PISO) algorithm of the incompressible solver, by using a very simple test case.

## Resources

The resources for this tutorial can be found in the [Inc_Lid_Driven_Cavity](incompressible_flow/https://github.com/su2code/Tutorials/tree/master/incompressible_flow/Inc_Lid_Driven_Cavity) directory in the [tutorial repository](https://github.com/su2code/Tutorials). You will need the configuration file ([incomp_pb_liddrivencavity.cfg](https://github.com/su2code/Tutorials/tree/master/incompressible_flow/Inc_Lid_Driven_Cavity/incomp_pb_liddrivencavity.cfg)) and the mesh file ([mesh_cavity_65x65.su2](https://github.com/su2code/Tutorials/tree/master/incompressible_flow/Inc_Lid_Driven_Cavity/mesh_cavity_65x65.su2)).


## Tutorial

The following tutorial will walk you through the steps required when solving for the flow in the lid-driven cavity using the pressure-correction incompressible solver in SU2. It is assumed you have already obtained and compiled the SU2_CFD code for a serial computation. If you have yet to complete these requirements, please see the [Download](/docs_v7/Download/) and [Installation](/docs_v7/Installation/) pages.

### Background

The lid-driven cavity is a classic benchmark problem for testing incompressible flow solvers. It consists of a simple 2D square cavity, with a moving lid. This moving lid creates a driving force on the fluid in the cavity trough the viscosity of the fluid. As the fluid is contained by the cavity, this driving force results in several vortices forming inside the cavity, depending on the Reynolds number. 

### Problem Setup

### Mesh Description

The computational mesh for the cavity is composed of quadrilaterals with 65 uniformly spaced nodes in both the x- and y-directions. The 4 boundaries of the cavity are no-slip walls. The cavity is 1 m by 1 m.


### Configuration File Options


### Running SU2

#### In Serial


#### In Parallel



### Results
