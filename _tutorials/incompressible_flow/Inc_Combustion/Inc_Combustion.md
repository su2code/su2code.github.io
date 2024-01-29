---
title: Incompressible, Laminar Combustion Simulation
permalink: /tutorials/Inc_Combustion/
written_by: EvertBunschoten
for_version: 8.0.0
revised_by:  
revision_date:
revised_version:
solver: INC_NAVIER_STOKES
requires: SU2_CFD, mlpcpp
complexity: advanced
follows:
---


## Goals

Version 8.0.0 of SU2 supports the simulation of reduced-order combustion simulations. In particular, flamelet-generated manifold (FGM) simulations. The FGM solver in SU2 computes the transport of a set of controlling variables. These are used to interpolate a manifold of detailed-chemistry flamelet data to retrieve the thermo-chemical state of the mixture, and reaction source terms. This capability can be used to solve 2D and 3D, laminar, (partially) premixed, direct and adjoint simulations with heat loss and modeling of differential diffusion effects. The latter is relevant specifically lean hydrogen flames. This tutorial describes how to set up a premixed hydrogen combustion simulation case. Additionally, information is provided regarding the governing equations and preferential diffusion model. Finally, the relevant options in the configuration file regarding the SU2 FGM solver are discussed.

## Resources and Prerequisites

The resources for this tutorial can be found in the [incompressible_flow/Inc_Combustion](https://github.com/su2code/Tutorials/tree/master/incompressible_flow/Inc_Combustion) directory in the [tutorial repository](https://github.com/su2code/Tutorials). You will need the following files:
1. *Configuration file*: The configuration file for this case is named [hydrogen_configuration.cfg](https://github.com/su2code/Tutorials/tree/master/incompressible_flow/Inc_Combustion/hydrogen_configuration.cfg).
2. *Mesh file*: The geometry for this test case is a simple, 2D burner geometry with a cooled burner plate ([H2_Burner.su2](https://github.com/su2code/Tutorials/tree/master/incompressible_flow/Inc_Combustion/H2_Burner.su2)).
3. *Manifold files*: The working principle of the FGM method is the manifold containing the flamelet data. From this manifold, thermo-chemical and reaction source term information is retrieved during the simulation. SU2 supports the use of 2D and 3D look-up tables (LUT), as well as multi-layer perceptrons (MLP). In the current tutorial, MLP's will be utilized. These files have the `.mlp` extension. Evaluating MLP's in SU2 is done through the `MLPCpp` sub-module. Make sure you configure SU2 with the flag `-Denable-mlpcpp=true` to clone this submodule.

The mesh is created using [gmsh](https://gmsh.info/) and a respective `.geo` script is available to recreate/modify the mesh [H2_Burner.geo](https://github.com/su2code/Tutorials/tree/master/incompressible_flow/Inc_Combustion/H2_Burner.geo). The mesh is unstructured (i.e. only contains triangular elements) with 70495 elements and 35926 points. This mesh is quite large, but a high resolution is required in order to resolve the flame front.

![Mesh with boundary conditions](../../../tutorials_files/incompressible_flow/Inc_Combustion/mesh.png)
Figure (1): Computational mesh with color indication of the used boundary conditions.

The MLP files describe five architectures. These are used to predict the thermo-chemical state, preferential diffusion scalars, and reaction source terms. 
![MLP architecture used for prediction of temperature, diffusion coefficient, and dynamic viscosity](../../../tutorials_files/incompressible_flow/Inc_Combustion/MLP_Group1.png)

## Prerequisites

The following tutorial assumes you already compiled `SU2_CFD` in serial or parallel, please see the [Download](/docs_v8/Download/) and [Installation](/docs_v8/Installation/) if that is not done yet. Additionally it is advised to perform an entry level incompressible tutorial first, as this tutorial only goes over species transport with combustion.

## Background

The test case represents a simplified version of a two-dimensional, pre-mixed hydrogen burner with a heat exchanger suspended in the hot exhaust. The purpose of this test case is to demonstrate the capabilities of the SU2 FGM solver (differential diffusion, heat loss), not a solution for a realistic hydrogen combustion problem.

## Problem Setup

In order to run a FGM simulation in SU2, an additional set-up step apart from defining the mesh and configuration file is required. This step involves the definition of a flamelet data manifold which includes the necessary data required by SU2 to include the relevant phenomena. This section describes the two manifold formats supported by SU2 for FGM simulations, as well as an example of the set-up of the manifold used in the current tutorial. One of the key features in accurately modeling (lean) hydrogen combustion is the modeling of the effects of preferential diffusion. The preferential diffusion model currently implemented in SU2 is the model formulated by Nithin et al (TODO: reference to efimov paper). This section briefly summarizes this model and how to enable it in SU2 FGM simulations. Finally, this section describes the boundary and initial condition of the current test case, as well as the methodologies available to ignite the mixture. 

### Manifold set-up 

During FGM simulations, thermo-chemical, as well as reaction data is interpolated from a manifold of detailed-chemistry flamelet data based on a set of controlling variables. In SU2, two types of manifold are supported: two or three-dimensional look-up tables (LUT) and feed-forward, dense, multi-layer perceptrons (MLP). 

Variables required to be included in manifold:

Controlling variables: 
1. Progress variable [-]
2. Total enthalpy [J kg^-1]
3. optional: mixture fraction [-]

In the current example, the following progress variable definition is used:

$$
\begin{equation}
\mathcal{Y} = -7.36Y_{H_2}-23.01Y_H-2.04Y_{O_2}-4.8Y_O+1.83Y_{H_2O}-15.31Y_{OH}-57.02Y_{H_2O_2}+24.55Y_{HO_2}
\end{equation}
$$

Thermo-chemical data: 
1. Temperature (`Temperature`)[K] 
2. Specific heat (Cp)[J kg^-1 K^-1] 
3. Dynamic viscosity (ViscosityDyn)[]
4. Thermal conductivity (Conductivity)[W m^-1 K^-1]
5. Diffusivity (DiffusionCoefficient) []
6. Density (Density) [kg m^-3] or mixture molar weight (MolarWeightMix) [kg mol^-1]

Source term data:
1. Progress variable source term [kg m^-3 s^-1]

LUT:
The look-up table format supported in SU2 is based around the two-dimensional, trapezoidal map approach. The table file format should be in the dragon file format. For pre-mixed problems without differential diffusion (e.g. pre-mixed methane problems), a two-dimensional table is sufficient. An example of such a table can be found in the [methane combustion test case](https://github.com/su2code/TestCases/flamelet/01_laminar_premixed_ch4_flame_cfd/fgm_ch4.drg). The two table dimensions should span the progress variable and total enthalpy dimension.

For partially- or non-premixed problems or pre-mixed problems with preferential diffusion, a three-dimensional table is required. SU2 supports a quasi-3D table format, consisting of two-dimensonal trapezoidal maps stacked in the third dimension. An example of this can be found in the [partially premixed methane combustion test case](https://github.com/su2code/TestCases/flamelet/06_laminar_partial_premixed_ch4_flame_cfd/LUT_methane_3D.drg). The first two dimensions should span the progress variable and total enthalpy dimension, while the third dimension should be mixture fraction.

MLP:
A more memory efficient option in terms of manifold format comes as one or multiple multi-layer perceptrons. Dense, feed-forward multi-layer perceptrons to be specific. SU2 uses the [MLPCpp module](https://github.com/EvertBunschoten/MLPCpp.git) to evaluate MLP's during simulations. Information on how to translate networks trained through TensorFlow to the `.mlp` format supported in SU2, see the [MLPCpp repository](https://github.com/EvertBunschoten/MLPCpp.git). In the current tutorial, a set of MLP's will be used as the manifold for the FGM solver. Here, two MLP's are used to extract the thermo-chemical state of the mixture:


### Preferential diffusion model

Pre-mixed combustion of reactants with high hydrogen content at lean conditions undergo a phenomenon called preferential diffusion. Here, the hydrogen diffuses differently from the other species in the mixture, causing local variations in mixture fraction and inherent instabilities in the flame front, even during laminar flow. Accurately modeling preferential diffusion is therefore crucial to capturing the behavior of pre-mixed hydrogen flames. The modeling of preferential diffusion is supported in SU2 through the Efimov model TODO: reference to Efimov paper. When solving hydrogen FGM problems, SU2 solves the following transport equations for the controlling variables:

$$
\begin{equation}
    \frac{\partial \rho \mathcal{Y}}{\partial t} + \nabla\cdot(\rho\vec{u}\mathcal{Y}) - \nabla\cdot\left(D\nabla\beta_\mathcal{Y}\right) = \rho\dot{\omega}_\mathcal{Y}
\end{equation}
$$
$$
\begin{equation}
    \frac{\partial \rho h}{\partial t} + \nabla\cdot(\rho\vec{u} h) - \nabla\cdot\left(\beta_{h,1}\nabla T + D\nabla\beta_{h,2}\right) = 0
\end{equation}
$$
$$
\begin{equation}
    \frac{\partial \rho Z}{\partial t} + \nabla\cdot(\rho\vec{u}Z) - \nabla\cdot\left(D\nabla\beta_Z\right) = 0
\end{equation}
$$

Here, $\mathcal{Y},h$ and $Z$ are the progress variable, total enthalpy, and mixture fraction respectively. Preferential diffusion is modeled through the $\beta$-terms in the third term on the left hand side of equations 2-4. See TODO:reference to Efimov paper for details on the definitions of these scalars. The preferential diffusion model is automatically switched on when the $\beta$-terms are included in the manifold. In order to be detected, they should be named as follows:

1. $\beta_\mathcal{Y}$ : `Beta_ProgVar`
2. $\beta_{h,1}$ : `Beta_Enth_Thermal`
3. $\beta_{h,2}$ : `Beta_Enth`
4. $\beta_Z$ : `Beta_MixFrac`

If not all the $\beta$- terms are detected, the preferential diffusion model will not be used during the simulation. During the initialization of the fluid model, a message will be displayed in the terminal indicating whether the preferential diffusion model is enabled.

### Boundary conditions and ignition method

The material properties of the incompressible mean flow represent air:
- Density (constant) = 1.1766 kg/m^3
- Viscosity (constant) = 1.716e-5 kg/(m-s)
- Inlet Velocities (constant) = 1 m/s in normal direction
- Outlet Pressure (constant) = 0 Pa

The SST turbulence model is used with the default settings of freestream turbulence intensity of 5% and a turbulent-to-laminar viscosity ratio of 10.

The material properties specific to the species transport equations are:
- Mass Diffusivity (constant) = 1e-3 m^2/s
- Mass fractions at the eastern inlet: 0.5, 0.5
- Mass fractions at the northern inlet: 0.6, 0.0

## Configuration File Options

All available options concerning species transport are listed below as they occur in the [config_template.cfg](https://github.com/su2code/SU2/blob/master/config_template.cfg).

The options as of now are fairly limited. Species transport is switched on by setting `KIND_SCALAR_MODEL= SPECIES_TRANSPORT`. The `DIFFUSIVITY_MODEL= CONSTANT_DIFFUSIVITY` is currently the only available therefore the only additional choice the value of `DIFFUSIVITY_CONSTANT`. For the `SCHMIDT_NUMBER_TURBULENT` please consult [the respective theory](/docs_v7/Theory/#species-transport).

The number of species transport equations is not set individually but deduced from the number of values given in the respective lists for species options. SU2 checks whether the same amount of values is given in each option and solves the appropriate amount of equations. `MARKER_INLET_SPECIES` is one of these options and has to be used alongside a usual `MARKER_INLET`. For outlets, symmetries or walls this is not necessary. 

The option `SPECIES_USE_STRONG_BC` should be left to `NO` and is an experimental option where a switch to strongly enforced boundary conditions can be made.

For `CONV_NUM_METHOD_SPECIES= SCALAR_UPWIND` a second order MUSCL reconstruction and multiple limiters are available.

The `TIME_DISCRE_SPECIES` can be either an implicit or explicit euler and a CFL reduction coefficient `CFL_REDUCTION_SPECIES` compared to the regular `CFL_NUMBER` is available.

The inital species mass fractions are given by the list `SPECIES_INIT= 1.0, ...`.

`SPECIES_CLIPPING= YES` with the respective lists for min and max enforces a strict lower and upper limit for the mass fraction solution used by the solver.

```
% --------------------- SPECIES TRANSPORT SIMULATION --------------------------%
%
% Specify scalar transport model (NONE, SPECIES_TRANSPORT)
KIND_SCALAR_MODEL= SPECIES_TRANSPORT
%
% Mass diffusivity model (CONSTANT_DIFFUSIVITY)
DIFFUSIVITY_MODEL= CONSTANT_DIFFUSIVITY
%
% Mass diffusivity if DIFFUSIVITY_MODEL= CONSTANT_DIFFUSIVITY is chosen. D_air ~= 0.001
DIFFUSIVITY_CONSTANT= 0.001
%
% Turbulent Schmidt number of mass diffusion
SCHMIDT_NUMBER_TURBULENT= 0.7
%
% Inlet Species boundary marker(s) with the following format:
% (inlet_marker, Species1, Species2, ..., SpeciesN-1, inlet_marker2, Species1, Species2, ...)
MARKER_INLET_SPECIES= (inlet, 0.5, ..., inlet2, 0.6, ...)
%
% Use strong inlet and outlet BC in the species solver
SPECIES_USE_STRONG_BC= NO
%
% Convective numerical method for species transport (SCALAR_UPWIND)
CONV_NUM_METHOD_SPECIES= SCALAR_UPWIND
%
% Monotonic Upwind Scheme for Conservation Laws (TVD) in the species equations.
% Required for 2nd order upwind schemes (NO, YES)
MUSCL_SPECIES= NO
%
% Slope limiter for species equations (NONE, VENKATAKRISHNAN, VENKATAKRISHNAN_WANG, BARTH_JESPERSEN, VAN_ALBADA_EDGE)
SLOPE_LIMITER_SPECIES = NONE
%
% Time discretization for species equations (EULER_IMPLICIT, EULER_EXPLICIT)
TIME_DISCRE_SPECIES= EULER_IMPLICIT
%
% Reduction factor of the CFL coefficient in the species problem
CFL_REDUCTION_SPECIES= 1.0
%
% Initial values for scalar transport
SPECIES_INIT= 1.0, ...
%
% Activate clipping for scalar transport equations
SPECIES_CLIPPING= NO
%
% Maximum values for scalar clipping
SPECIES_CLIPPING_MAX= 1.0, ...
%
% Minimum values for scalar clipping
SPECIES_CLIPPING_MIN= 0.0, ...
```

For the screen, history and volume output multiple straight forward options were included. Whenever a number is used at the end of the keyword, one for each species (starting at zero) can be added.
```
SCREEN_OUTPUT= RMS_SPECIES_0, ..., MAX_SPECIES_0, ..., BGS_SPECIES_0, ..., \
               LINSOL_ITER_SPECIES, LINSOL_RESIDUAL_SPECIES, \
               SURFACE_SPECIES_0, ..., SURFACE_SPECIES_VARIANCE
```

For `HISTORY_OUTPUT` the residuals are included in `RMS_RES` and the linear solver quantities in `LINSOL`. The surface outputs can be included with `SPECIES_COEFF` or `SPECIES_COEFF_SURF` for each surface individually.

For `VOLUME_OUTPUT` no extra output field has the be set. The mass fractions are included in `SOLUTION` and the volume residuals in `RESIDUAL`.

All available output can be printed to screen using the `dry-run` feature of SU2:
```
$ SU2_CFD -d <config-filename>.cfg
```

## Running SU2

The simulation can be run in serial using the following command:
```
$ SU2_CFD species3_primitiveVenturi.cfg
```
or in parallel with your preferred number of cores (for this small case not more than 4 cores should be used):
```
$ mpirun -n <#cores> SU2_CFD species3_primitiveVenturi.cfg
```

## Results

The case converges nicely as expected on such a simple case and mesh.

![Residual plot](../../tutorials_files/incompressible_flow/Inc_Species_Transport/images/residuals_specMix.png)
Figure (2): Residual plot (Incompressible mean flow, SST turbulence model, species transport).

Note that there is still some unphysical mass fraction fluctuation for Species_0 at the junction corner. This becomes much less apparent by using `MUSCL_SPECIES = YES` but does not fully disappear.

![Species Mass Fractions](../../tutorials_files/incompressible_flow/Inc_Species_Transport/images/speciesMassFractions.jpg)
Figure (3): Volume mass fractions for both species. Species_1 is mirrored for better comparison.

Velocity magnitude field along which the species are transported. For a much less homogenous mixture at the outlet one could decrease the `DIFFUSIVITY_CONSTANT` which makes for a more interesting optimization problem.

![Velocity Magnitude](../../tutorials_files/incompressible_flow/Inc_Species_Transport/images/VelocityMag.jpg)
Figure (4): Velocity Magnitude in the domain.

## Additional remarks

An in depth optimization of this case with addition of the FFD-box, gradient validation and some more steps can found [here](/tutorials/Species_Transport/).
