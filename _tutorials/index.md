---
title: The SU2 Tutorial Collection
permalink: /tutorials/home/
redirect_from: /tutorials/index.html
disable_comments: true
disable_header: true
written_by: economon
for_version: 6.0.0
revised_by: talbring
revision_date: 2019-11-27
revised_version: 7.0.0
---

## Getting started with SU2

Rather than writing a long manual on all available (and constantly evolving) configuration options available in SU2, the approach has been taken to teach the various aspects of the SU2 code through a range of tutorials. If you would like to see all of the available config options, we keep a configuration file template in the root directory of the source distribution (see [config_template.cfg](https://github.com/su2code/SU2/blob/master/config_template.cfg)).

The tutorials are numbered roughly in order of their complexity and how experienced with the code the user may need to be, noting that the more advanced tutorials may assume the user has already worked through the earlier ones. Each tutorial attempts to present new features of SU2 and contains explanations for the key configuration file options. More information on the exact learning goals of a tutorial can be seen at the beginning of each.

You can get all the mesh and config files either by cloning or downloading the [tutorial repository](https://github.com/su2code/Tutorials) or by downloading them separately using the provided links on each tutorial page.

**Note:** Before beginning with the tutorials, please make sure to check out the information on how to [download](/docs_v7/Download/) and [install](/docs_v7/Installation/).

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
* [Transitional Flat Plate(BC transition model)](/tutorials/Transitional_Flat_Plate/)    
Simulation of external, transitional flow over a flat plate (transitional latminar-turbulent case).
* [Transitional Flat Plate(LM transition model)](/tutorials/Transitional_Flat_Plate_T3A/)    
Simulation of external, transitional flow over a flat plate(T3A & T3A-) (transitional latminar-turbulent case).
* [Turbulent ONERAM6](/tutorials/Turbulent_ONERAM6/)     
Simulation of external, viscous flow around a 3D geometry (isolated wing) using a turbulence model.
* [Unsteady NACA0012](/tutorials/Unsteady_NACA0012/)     
Simulation of unsteady, external, viscous flow around an airfoil.
* [Epistemic Uncertainty Quantification of RANS predictions of NACA 0012 airfoil](/tutorials/UQ_NACA0012/)    
Perform uncertainty quantification of errors arising due to assumptions inherent in turbulence models.
* [Non-ideal compressible flow in a supersonic nozzle](/tutorials/NICFD_nozzle/)    
Simulation of compressible flow in a nozzle using non-ideal thermodynamic models.
* [Data-driven equation of state for non-ideal compressible fluids](/tutorials/NICFD_nozzle_datadriven/)    
Demonstration of data-driven equation of state using a physics-informed neural network.
* [Turbomachinery: Aachen Turbine stage with mixing plane](/tutorials/Aachen_Turbine/)    
Simulation of compressible flow of the Aachen turbine demonstrating turbomachinery application.

#### Incompressible Flow

* [Inviscid Hydrofoil](/tutorials/Inc_Inviscid_Hydrofoil/)   
A simulation of internal, inviscid, incompressible flow around a NACA 0012 hydrofoil.
* [Laminar Flat Plate with Heat Transfer](/tutorials/Inc_Laminar_Flat_Plate/)    
Simulation of external, laminar, incompressible flow over a flat plate (classical Navier-Stokes case).
* [Turbulent Flat Plate](/tutorials/Inc_Turbulent_Flat_Plate/)    
Simulation of external, turbulent incompressible flow over a flat plate (classical RANS case).
* [Turbulent NACA 0012](/tutorials/Inc_Turbulent_NACA0012/)    
Simulation of external, viscous, incompressible flow around the NACA 0012 using a turbulence model.
* [Laminar Backward-facing Step](/tutorials/Inc_Laminar_Step/)    
Simulation of internal, laminar, incompressible flow over a backward-facing step with an inlet velocity profile input from file.
* [Laminar Buoyancy-driven Cavity](/tutorials/Inc_Laminar_Cavity/)    
Simulation of internal, laminar, incompressible flow in a differentially-heated cavity under the influence of gravity (classical natural convection case).
* [Streamwise Periodicity](/tutorials/Inc_Streamwise_Periodic/)    
Simulation of internal, turbulent, incompressible flow in a unit cell of a 2D pin-fin heat exchanger.
* [Species Transport](/tutorials/Inc_Species_Transport/)    
Simulation of internal, turbulent, incompressible flow through a mixing channel.
* [Species Transport Composition Dependent Model](/tutorials/Inc_Species_Transport_Composition_Dependent_Model/)    
Simulation of internal, turbulent, 3D incompressible flow through a Kenics static mixer.
* [Vortex Shedding](/tutorials/Inc_Von_Karman/)    
Simulation of unsteady laminar vortex shedding behind a circular cylinder.
* [Turbulent Bend](/tutorials/Inc_Turbulent_Bend/)    
Simulation of turbulent flow in a 90 degree pipe bend using wall functions.

#### Structural Mechanics

* [Linear Elasticity](/tutorials/Linear_Elasticity/)  
Simulation of an elasticity problem with small deformations
* [Linear Dynamics](/tutorials/Linear_Dynamics/)  
Simulation of a dynamic structural problem with small deformations
* [Non-linear Elasticity](/tutorials/Nonlinear_Elasticity/)  
Simulation of a non-linear structural problem with large deformations
* [Multiple Materials](/tutorials/Multiple_Material/)  
Simulation of a non-linear problem with multiple material definitions

#### Multiphysics

* [Static Fluid-Structure Interaction](/tutorials/Static_FSI/)  
Non-linear structural mechanics coupled with incompressible Navier-Stokes flow
* [Dynamic Fluid-Structure Interaction with the Python wrapper](/tutorials/Dynamic_FSI_Python/)    
Linear Nastran-like model coupled with compressible unsteady RANS equations using the Python wrapper.
* [Static Conjugate Heat Transfer](/tutorials/Static_CHT/)    
Simulation of multiple heated cylinders in incompressible fluid flow.
* [Unsteady Conjugate Heat Transfer](/tutorials/Inc_Heated_Cylinders_Unsteady/)    
Simulation of an unsteady coupled CHT problem incorporating multiple physical zones.
* [Conjugate Heat Transfer between Solid Domains](/tutorials/SS_CR_CHT/) 
Simulation of CHT between solid domains with contact resistance.
* [Pre-mixed Hydrogen Combustion](/tutorials/Inc_Combustion/) 
Simulation of a laminar, pre-mixed hydrogen flame on a cooled burner plate.
* [Python wrapper for User Defined Functionality](/tutorials/TFC_python/) 
Use the Python wrapper to setup user defined source terms, initial conditions and boundary conditions for combustion.

#### Shape Design Features

* [Unconstrained shape design of an transonic inviscid airfoil at a cte. AoA](/tutorials/Inviscid_2D_Unconstrained_NACA0012/)    
Get a basic introduction to the SU2 design capabilities by performing an optimal shape design of a 2D geometry (isolated airfoil) without constraints.
* [Constrained shape design of a transonic turbulent airfoil at a cte. C<sub>L</sub>](/tutorials/Turbulent_2D_Constrained_RAE2822/)    
Perform an optimal shape design of a 2D geometry (isolated airfoil at turbulent regime) with flow and geometrical constraints.
* [Constrained shape design of a transonic inviscid wing at a cte. C<sub>L</sub>](/tutorials/Inviscid_3D_Constrained_ONERAM6/)    
Learn the basis of 3D design by performing an optimal shape design of an isolated wing with geometrical constraints.
* [Multi-Objective Shape Design of an Inviscid Supersonic Ramp](/tutorials/Multi_Objective_Shape_Design/)    
Perform an optimal shape design with multiple objectives and a penalty function
* [Unsteady Shape Optimization](/tutorials/Unsteady_Shape_Opt_NACA0012/)  
Shape optimization of an 2D airfoil in unsteady flow conditions.
* [Species Transport](/tutorials/Species_Transport/)    
Optimization of internal, turbulent, incompressible flow through a mixing channel.
* [Optimizing pressure drop of a pipe bend](/tutorials/Inc_Turbulent_Bend_Opt/)    
Optimization of the pressure drop (also known as head loss), of a pipe bend. 
