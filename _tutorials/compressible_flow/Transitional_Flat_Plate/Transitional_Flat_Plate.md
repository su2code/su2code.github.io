---
title: Transitional Flat Plate
permalink: /tutorials/Transitional_Flat_Plate/
written_by: sametcaka
for_version: 7.0.0
revised_by: talbring
revision_date: 2020-03-03
revised_version: 7.0.2
solver: RANS
requires: SU2_CFD
complexity: basic
follows: 
---

![lam_to_turb](../../tutorials_files/compressible_flow/Transitional_Flat_Plate/images/lam_to_turb.png)

## Goals

Upon completing this tutorial, the user will be familiar with performing an external, transitional flow over a flat plate. The flow over the flat plate will be laminar until it reaches a point where a transition correlation depending on local flow variables is activated. The results can be compared to the zero pressure gradient natural transition experiment of Schubauer & Klebanoff [1]. The following capabilities of SU2 will be showcased in this tutorial:

- Steady, 2D, incompressible RANS equations
- Spalart-Allmaras (S-A) turbulence model with Bas-Cakmakcioglu (B-C) transition model
- Roe convective scheme in space (2nd-order, upwind)
- Corrected average-of-gradients viscous scheme
- Euler implicit time integration
- Inlet, Outlet, Symmetry and No-Slip Wall boundary conditions

## Resources

The resources for this tutorial can be found in the [compressible_flow/Transitional_Flat_Plate](https://github.com/su2code/Tutorials/tree/master/compressible_flow/Transitional_Flat_Plate) directory in the [tutorial repository](https://github.com/su2code/Tutorials). You will need the configuration file ([transitional_BC_model_ConfigFile.cfg](https://github.com/su2code/Tutorials/tree/master/compressible_flow/Transitional_Flat_Plate/transitional_BC_model_ConfigFile.cfg)) and the mesh file ([grid.su2](https://github.com/su2code/Tutorials/tree/master/compressible_flow/Transitional_Flat_Plate/grid.su2)).
Additionally, experimental skin friction data corresponding to this test case is provided in the TestCases repository (All_ZeroPresGrad_FlatPlateExperiments.dat).

## Tutorial

The following tutorial will walk you through the steps required when solving for the transitional flow over a flat plate using SU2. It is assumed you have already obtained and compiled the SU2_CFD code for a serial or parallel computation. If you have yet to complete these requirements, please see the [Download](/docs_v7/Download/) and [Installation](/docs_v7/Installation/) pages.

### Background

Practically, most CFD analyses are carried out using fully turbulent fields that do not account for boundary layer transition. Given that the flow is everywhere turbulent, no separation bubbles or other complex flow phenomena evolve. A transition model can be introduced, however, such that the flow begins as laminar by damping the production term of the turbulence model until a point where a transition correlation is activated. Currently, the Bas-Cakmakcioglu (B-C) transition model [2] that uses Spalart-Allmaras (S-A) as the baseline turbulence model is implemented in SU2.

For verification, we will be comparing SU2 results against the results of natural transition flat plate experiment of Schubauer & Klebanoff. The experimental data include skin friction coefficient distribution versus the local Reynolds number over the flat plate.

### Problem Setup

The length of the flat plate is 1.5 meters, and it is represented by an adiabatic no-slip wall boundary condition. There is a symmetry plane located before the leading edge of the flat plate. Inlet boundary condition is used on the left boundary of the domain, and outlet boundary condition is applied to the top and right boundaries of the domain. The freestream velocity, density, viscosity and turbulence intensity (%) is specified as 50.1 m/s, 1.2 kg/m^3, 1.8e-05 and 0.18% (u'/U=0.0018), respectively. Since the Mach number is about 0.15, compressibility effects are negligible; therefore, the incompressible flow solver can be employed.

### Mesh Description

The mesh used for this tutorial, which consists of 41,412 quadrilaterals, is shown below.

![Flat Plate](../../tutorials_files/compressible_flow/Transitional_Flat_Plate/images/FlatPMesh.png)

Figure (1): Mesh with boundary conditions (red: inlet, blue:outlet, orange:symmetry, green:wall)

### Configuration File Options

Several of the key configuration file options for this simulation are highlighted here.

```
% Physical governing equations (EULER, NAVIER_STOKES,
%                               WAVE_EQUATION, HEAT_EQUATION, 
%                               LINEAR_ELASTICITY, POISSON_EQUATION)
SOLVER= INC_RANS
%
% Specify turbulent model (NONE, SA, SST)
KIND_TURB_MODEL= SA
%
% Specify transition model
SA_OPTIONS= BCM
%
% Specify Turbulence Intensity (u'/U)
FREESTREAM_TURBULENCEINTENSITY = 0.0018
```

The governing equations are RANS with the Spalart-Allmaras (`SA`) turbulence model. By entering `SA_OPTIONS= BCM`, the Bas-Cakmakcioglu Algebraic Transition Model is activated. This model requires freestream turbulence intensity that is to be used in the transition correlation, thus the `FREESTREAM_TURBULENCEINTENSITY` option is also used. The BC model achieves its purpose by modifying the production term of the 1-equation SA turbulence model. The production term of the SA model is damped until a considerable amount of turbulent viscosity is generated, and after that point, the damping effect on the transition model is disabled. Thus, a transition from laminar to turbulent flow is obtained.

The incompressible freestream properties are specified as follows. (Please see "Notes" for freestream properties of other transitional flat plate test cases).

```
% Initial density for incompressible flows (1.2886 kg/m^3 by default)
INC_DENSITY_INIT= 1.2
%
% Initial velocity for incompressible flows (1.0,0,0 m/s by default)
INC_VELOCITY_INIT= ( 50.1, 0.0, 0.0 )
%
% Viscosity model (SUTHERLAND, CONSTANT_VISCOSITY).
VISCOSITY_MODEL= CONSTANT_VISCOSITY
%
% Molecular Viscosity that would be constant (1.716E-5 by default)
MU_CONSTANT= 1.8e-05
```

The Reynolds number for the Schubauer & Klebanoff test case is 3.34e6 for 1 meter long flat plate and `REF_AREA= 1.5` are specified.

### Running SU2

To run this test case, follow these steps at a terminal command line:

1.	Copy the config file ([transitional_BC_model_ConfigFile.cfg](https://github.com/su2code/Tutorials/tree/master/compressible_flow/Transitional_Flat_Plate/transitional_BC_model_ConfigFile.cfg)) and the mesh file ([grid.su2](https://github.com/su2code/Tutorials/tree/master/compressible_flow/Transitional_Flat_Plate/grid.su2)) so that they are in the same directory. Move to the directory containing the config file and the mesh file. Make sure that the SU2 tools were compiled, installed, and that their install location was added to your path.

2.	Run the executable by entering 

    ```
    $ SU2_CFD transitional_BC_model_ConfigFile.cfg
    ``` 

    at the command line.

3.	SU2 will print residual updates for each iteration of the flow solver, and the simulation will finish upon reaching the specified convergence criteria.

4.	Files containing the results will be written upon exiting SU2. The flow solution can be visualized in Tecplot.

### Results

The figure below compares the skin friction results obtained by the B-C transition model to the experimental data. 

![SK_Cf_Rex](../../tutorials_files/compressible_flow/Transitional_Flat_Plate/images/Cf_Rex_SK.png)

Figure (2): Comparison of the skin friction coefficients for the Schubauer & Klebanoff case.

## Notes

By changing the freestream velocity and turbulence intensity options in the config file with the values given in the table below, you may also simulate other very popular zero pressure gradient transitional flat plate test cases. You may use the same grid file for these test cases.

![other_cases_table](../../tutorials_files/compressible_flow/Transitional_Flat_Plate/images/other_transition_cases.png)

## References

[1] Schubauer, G. B., and Klebanoff, P. S., 1955, "Contribution on the Mechanics of Boundary Layer Transition," NACA Technical Note No. TN-3489.

[2] Cakmakcioglu, S. C., Bas, O., and Kaynak, U., “A Correlation-Based Algebraic Transition Model,” Proceedings of the Institution of Mechanical Engineers, Part C: Journal of Mechanical Engineering Science, Accepted on 10/30/2017, https://doi.org/10.1177/0954406217743537
