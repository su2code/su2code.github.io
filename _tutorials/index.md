---
title: The SU2 Tutorial Collection
permalink: /tutorials/home/
redirect_from: /tutorials/index.html
---

## Getting started with SU2

Rather than writing a long manual on all available (and constantly evolving) configuration options available in SU2, the approach has been taken to teach the various aspects of the SU2 code through a range of tutorials. If you would like to see all of the available config options, we keep a configuration file template in the root directory of the source distribution (see [config_template.cfg](https://github.com/su2code/SU2/blob/master/config_template.cfg)).

The tutorials are numbered roughly in order of their complexity and how experienced with the code the user may need to be, noting that the more advanced tutorials may assume the user has already worked through the earlier ones. Each tutorial attempts to present new features of SU2 and contains explanations for the key configuration file options. More information on the exact learning goals of a tutorial can be seen at the beginning of each.

You can get all the mesh and config files either by cloning or downloading the [project website repository](https://github.com/su2code/su2code.github.io) or by downloading them separately using the provided links on each tutorial page.

**Note:** Before beginning with the tutorials, please make sure to check out the information on how to [download](/docs/Download/) and [install](/docs/Installation/).

## Summary of tutorials
------

#### Compressible Flow

* [Inviscid Bump in a Channel](/tutorials/Inviscid_Bump/)   
A simulation of internal, inviscid flow through a 2D geometry.
* [Inviscid Supersonic Wedge](/tutorials/Inviscid_Wedge/)    
Get familiar with a basic supersonic flows with analytical solution.
* [Inviscid ONERAM6](/tutorials/Inviscid_ONERAM6/)    
Simulation of external, inviscid flow around a 3D geometry (isolated wing).
* [Laminar Flat Plate](/tutorials/Laminar_Flat_Plate/)   
Simulation of external, laminar flow over a flat plate (classical Navier-Stokes validation).
* [Laminar Cylinder](/tutorials/Laminar_Cylinder/)    
Simulation of external, laminar flow around a 2D cylinder.
* [Turbulent Flat Plate](/tutorials/Turbulent_Flat_Plate/)    
Simulation of external, turbulent flow over a flat plate (classical RANS validation).
* [Transitional Flat Plate](/tutorials/Transitional_Flat_Plate/)    
Simulation of external, transitional flow over a flat plate (transitional latminar-turbulent case)
* [Turbulent ONERAM6](/tutorials/Turbulent_ONERAM6/)    
Simulation of external, viscous flow around a 3D geometry (isolated wing) using a turbulence model.
* [Epistemic Uncertainty Quantification of RANS predictions of NACA 0012 airfoil](/tutorials/UQ_NACA0012/)
Perform uncertainty quantification of errors arising due to assumptions inherent in turbulence models

#### Incompressible Flow

* [Inviscid Hydrofoil](/tutorials/Inc_Inviscid_Hydrofoil/)   
A simulation of internal, inviscid, incompressible flow around a NACA 0012 hydrofoil.
* [Laminar Flat Plate with Heat Transfer](/tutorials/Inc_Laminar_Flat_Plate/)    
Simulation of external, laminar, incompressible flow over a flat plate (classical Navier-Stokes case).
* [Turbulent Flat Plate](/tutorials/Inc_Turbulent_Flat_Plate/)    
Simulation of external, turbulentm incompressible flow over a flat plate (classical RANS case).
* [Turbulent NACA 0012](/tutorials/Inc_Turbulent_NACA0012/)    
Simulation of external, viscous, incompressible flow around the NACA 0012 using a turbulence model.
* [Laminar Backward-facing Step](/tutorials/Inc_Laminar_Step/)    
Simulation of internal, laminar, incompressible flow over a backward-facing step with an inlet velocity profile input from file.
* [Laminar Buoyancy-driven Cavity](/tutorials/Inc_Laminar_Cavity/)    
Simulation of internal, laminar, incompressible flow in a differentially-heated cavity under the influence of gravity (classical natural convection case).

#### Shape Design Features

* [Unconstrained shape design of an transonic inviscid airfoil at a cte. AoA](/tutorials/Inviscid_2D_Unconstrained_NACA0012/)
Get a basic introduction to the SU2 design capabilities by performing an optimal shape design of a 2D geometry (isolated airfoil) without constraints.
* [Constrained shape design of a transonic turbulent airfoil at a cte. C<sub>L</sub>](/tutorials/Turbulent_2D_Constrained_RAE2822/)    
Perform an optimal shape design of a 2D geometry (isolated airfoil at turbulent regime) with flow and geometrical constraints.
* [Constrained shape design of a transonic inviscid wing at a cte. C<sub>L</sub>](/tutorials/Inviscid_3D_Constrained_ONERAM6/)    
Learn the basis of 3D design by performing an optimal shape design of an isolated wing with geometrical constraints.
* [Multi-Objective Shape Design of an Inviscid Supersonic Ramp](/tutorials/Multi_Objective_Shape_Design/)    
 Perform an optimal shape design with multiple objectives and a penalty function
