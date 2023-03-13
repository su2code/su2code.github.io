---
title: Governing Equations in SU2
permalink: /docs_v7/Theory/
---

This page contains a very brief summary of the different governing equation sets that are treated in each of the solvers within SU2. The reader will be referred to other references in some instances for the full detail of the numerical implementations, but the approaches are also described at a high level here.

---

- [Compressible Navier-Stokes](#compressible-navier-stokes)
- [Compressible Euler](#compressible-euler)
- [Thermochemical Nonequilibrium Navier-Stokes](#thermochemical-nonequilibrium-navier-stokes)
- [Thermochemical Nonequilibrium Euler](#thermochemical-nonequilibrium-euler)
- [Incompressible Navier-Stokes](#incompressible-navier-stokes)
- [Incompressible Euler](#incompressible-euler)
- [Turbulence Modeling](#turbulence-modeling)
- [Species Transport](#species-transport)
- [Flamelet Combustion Modeling](#flamelet-combustion-modeling)
- [Elasticity](#elasticity)
- [Heat Conduction](#heat-conduction)
  
---

# Compressible Navier-Stokes #

| Solver | Version | 
| --- | --- |
| `NAVIER_STOKES`, `RANS`, `FEM_NAVIER_STOKES` | 7.0.0 |


SU2 solves the compressible Navier-Stokes equations expressed in differential form as

$$ \mathcal{R}(U) = \frac{\partial U}{\partial t} + \nabla \cdot \bar{F}^{c}(U) - \nabla \cdot \bar{F}^{v}(U,\nabla U)  - S = 0 $$

where the conservative variables are the working variables and given by 

$$U = \left \{  \rho, \rho \bar{v},  \rho E \right \}^\mathsf{T}$$ 

$$S$$ is a generic source term, and the convective and viscous fluxes are

$$\bar{F}^{c}   = \left \{ \begin{array}{c} \rho \bar{v}  \\ \rho \bar{v} \otimes  \bar{v} + \bar{\bar{I}} p \\ \rho E \bar{v} + p \bar{v}   \end{array} \right \}$$

and 

$$\bar{F}^{v} = \left \{ \begin{array}{c} \cdot \\ \bar{\bar{\tau}} \\ \bar{\bar{\tau}} \cdot \bar{v} + \kappa \nabla T  \end{array} \right  \}$$

where $$\rho$$ is the fluid density, $$\bar{v}=\left\lbrace u, v, w \right\rbrace^\mathsf{T}$$ $$\in$$ $$\mathbb{R}^3$$ is the flow speed in Cartesian system of reference, $$E$$ is the total energy per unit mass, $$p$$ is the static pressure, $$\bar{\bar{\tau}}$$ is the viscous stress tensor, $$T$$ is the temperature, $$\kappa$$ is the thermal conductivity, and $$\mu$$ is the viscosity. The viscous stress tensor can be expressed in vector notation as

$$\bar{\bar{\tau}}= \mu \left ( \nabla \bar{v} + \nabla \bar{v}^{T} \right ) - \mu \frac{2}{3} \bar{\bar I} \left ( \nabla \cdot \bar{v} \right )$$

Assuming a perfect gas with a ratio of specific heats $$\gamma$$ and specific gas constant $$R$$, one can close the system by determining pressure from $$p = (\gamma-1) \rho \left [ E - 0.5(\bar{v} \cdot \bar{v} ) \right ]$$ and temperature from the ideal gas equation of state $$T = p/(\rho R)$$. Conductivity can be a constant, or we assume a constant Prandtl number $$Pr$$ such that the conductivity varies with viscosity as $$\kappa = \mu c_p / Pr$$. 

It is also possible to model non-ideal fluids within SU2 using more advanced fluid models that are available, but this is not discussed here. Please see the tutorial on the topic.

For laminar flows, $$\mu$$ is simply the dynamic viscosity $$\mu_{d}$$, which can be constant or assumed to satisfy Sutherland's law as a function of temperature alone, and $$Pr$$ is the dynamic Prandtl number $$Pr_d$$. For turbulent flows, we solve the Reynolds-averaged Navier-Stokes (RANS) equations. In accord with the standard approach to turbulence modeling based upon the Boussinesq hypothesis, which states that the effect of turbulence can be represented as an increased viscosity, the viscosity is divided into dynamic and turbulent components, or  $$\mu_{d}$$ and $$\mu_{t}$$, respectively. Therefore, the effective viscosity in becomes

$$\mu =\mu_{d}+\mu_{t}$$

Similarly, the thermal conductivity in the energy equation becomes an effective thermal conductivity written as

$$\kappa =\frac{\mu_{d} \, c_p}{Pr_{d}}+\frac{\mu_{t} \, c_p}{Pr_{t}}$$

where we have introduced a turbulent Prandtl number $$Pr_t$$. The turbulent viscosity $$\mu_{t}$$ is obtained from a suitable turbulence model involving the mean flow state $$U$$ and a set of new variables for the turbulence. 

Within the `NAVIER_STOKES` and `RANS` solvers, we discretize the equations in space using a finite volume method (FVM) with a standard edge-based data structure on a dual grid with vertex-based schemes. The convective and viscous fluxes are evaluated at the midpoint of an edge. In the `FEM_NAVIER_STOKES` solver, we discretize the equations in space with a nodal Discontinuous Galerkin (DG) finite element method (FEM) with high-order (> 2nd-order) capability.

---

# Compressible Euler #

| Solver | Version | 
| --- | --- |
| `EULER`, `FEM_EULER` | 7.0.0 |

SU2 solves the compressible Euler equations, which can be obtained as a simplification of the compressible Navier-Stokes equations in the absence of viscosity and thermal conductivity. They can be expressed in differential form as

 $$ \mathcal{R}(U) = \frac{\partial U}{\partial t} + \nabla \cdot \bar{F}^{c}(U) - S = 0 $$

where the conservative variables are the working variables and are given by 

$$U = \left \{  \rho, \rho \bar{v},  \rho E \right \}^\mathsf{T}$$ 

$$S$$ is a generic source term, and the convective flux is

$$\bar{F}^{c}   = \left \{ \begin{array}{c} \rho \bar{v}  \\ \rho \bar{v} \otimes  \bar{v} + \bar{\bar{I}} p \\ \rho E \bar{v} + p \bar{v}   \end{array} \right \}$$

where $$\rho$$ is the fluid density, $$\bar{v}=\left\lbrace u, v, w \right\rbrace^\mathsf{T}$$ $$\in$$ $$\mathbb{R}^3$$ is the flow speed in Cartesian system of reference, $$E$$ is the total energy per unit mass, $$p$$ is the static pressure, and $$T$$ is the temperature. Assuming a perfect gas with a ratio of specific heats $$\gamma$$ and gas constant $$R$$, one can close the system by determining pressure from $$p = (\gamma-1) \rho \left [ E - 0.5(\bar{v} \cdot \bar{v} ) \right ]$$ and temperature from the ideal gas equation of state $$T = p/(\rho R)$$.

Within the `EULER` solvers, we discretize the equations in space using a finite volume method (FVM) with a standard edge-based data structure on a dual grid with vertex-based schemes. The convective and viscous fluxes are evaluated at the midpoint of an edge. In the `FEM_EULER` solver, we discretize the equations in space with a nodal Discontinuous Galerkin (DG) finite element method (FEM) with high-order (> 2nd-order) capability.

---

# Thermochemical Nonequilibrium Navier-Stokes #

| Solver | Version | 
| --- | --- |
| `NEMO_NAVIER_STOKES` | 7.0.0 |


To simulate hypersonic flows in thermochemical nonequilibrium, SU2-NEMO solves the Navier-Stokes equations for reacting flows, expressed in differential form as

$$ \mathcal{R}(U) = \frac{\partial U}{\partial t} + \nabla \cdot \bar{F}^{c}(U) - \nabla \cdot \bar{F}^{v}(U,\nabla U)  - S = 0 $$

where the conservative variables are the working variables and given by 

$$U = \left \{  \rho_{1}, \dots, \rho_{n_s}, \rho \bar{v},  \rho E, \rho E_{ve} \right \}^\mathsf{T}$$ 

$$S$$ is a source term composed of

$$S = \left \{  \dot{w}_{1}, \dots, \dot{w}_{n_s}, \mathbf{0},  0, \dot{\theta}_{tr:ve} + \sum_s \dot{w}_s E_{ve,s} \right \}^\mathsf{T}$$  

and the convective and viscous fluxes are

$$\bar{F}^{c}   = \left \{ \begin{array}{c} \rho_{1} \bar{v} \\ \vdots \\ \rho_{n_s} \bar{v}  \\ \rho \bar{v} \otimes  \bar{v} + \bar{\bar{I}} p \\ \rho E \bar{v} + p \bar{v} \\  \rho E_{ve} \bar{v}  \end{array} \right \}$$

and 

$$\bar{F}^{v} = \left \{ \begin{array}{c} \\- \bar{J}_1 \\ \vdots \\ - \bar{J}_{n_s}  \\ \bar{\bar{\tau}} \\ \bar{\bar{\tau}} \cdot \bar{v} + \sum_k \kappa_k \nabla T_k - \sum_s \bar{J}_s h_s \\ \kappa_{ve} \nabla T_{ve} - \sum_s \bar{J}_s E_{ve}  \end{array} \right  \}$$

In the equations above, the notation is is largely the same as for the compressible Navier-Stokes equations. An individual mass conservation equation is introduced for each chemical species, indexed by $$s \in \{1,\dots,n_s\}$$. Each conservation equation has an associated source term, $$\dot{w}_{s}$$ associated with the volumetric production rate of species $$s$$ due to chemical reactions occuring within the flow.

Chemical production rates are given by $$ \dot{w}_s = M_s \sum_r (\beta_{s,r} - \alpha_{s,r})(R_{r}^{f} - R_{r}^{b})  $$

where the forward and backward reaction rates are computed using an Arrhenius formulation.

A two-temperature thermodynamic model is employed to model nonequilibrium between the translational-rotational and vibrational-electronic energy modes. As such, a separate energy equation is used to model vibrational-electronic energy transport. A source term associated with the relaxation of vibrational-electronic energy modes is modeled using a Landau-Teller formulation $$ \dot{\theta}_{tr:ve} = \sum _s \rho_s \frac{dE_{ve,s}}{dt} = \sum _s \rho_s \frac{E_{ve*,s} - E_{ve,s}}{\tau_s}. $$

Transport properties for the multi-component mixture are evaluated using a Wilkes-Blottner-Eucken formulation.

---

# Thermochemical Nonequilibrium Euler #

| Solver | Version | 
| --- | --- |
| `NEMO_EULER` | 7.0.0 |


To simulate inviscid hypersonic flows in thermochemical nonequilibrium, SU2-NEMO solves the Euler equations for reacting flows which can be obtained as a simplification of the thermochemical nonequilibrium Navier-Stokes equations in the absence of viscous effects. They can be expressed in differential form as

$$ \mathcal{R}(U) = \frac{\partial U}{\partial t} + \nabla \cdot \bar{F}^{c}(U) - S = 0 $$

where the conservative variables are the working variables and given by 

$$U = \left \{  \rho_{1}, \dots, \rho_{n_s}, \rho \bar{v},  \rho E, \rho E_{ve} \right \}^\mathsf{T}$$ 

$$S$$ is a source term composed of

$$S = \left \{  \dot{w}_{1}, \dots, \dot{w}_{n_s}, \mathbf{0},  0, \dot{\theta}_{tr:ve} + \sum_s \dot{w}_s E_{ve,s} \right \}^\mathsf{T}$$  

and the convective and viscous fluxes are

$$\bar{F}^{c}   = \left \{ \begin{array}{c} \rho_{1} \bar{v} \\ \vdots \\ \rho_{n_s} \bar{v}  \\ \rho \bar{v} \otimes  \bar{v} + \bar{\bar{I}} p \\ \rho E \bar{v} + p \bar{v} \\  \rho E_{ve} \bar{v}  \end{array} \right \}$$

# Incompressible Navier-Stokes #

| Solver | Version | 
| --- | --- |
| `INC_NAVIER_STOKES`, `INC_RANS` | 7.0.0 |


SU2 solves the incompressible Navier-Stokes equations in a general form allowing for variable density due to heat transfer through the low-Mach approximation (or incompressible ideal gas formulation).
The reader is referred to [this paper](https://arc.aiaa.org/doi/10.2514/1.J058222) for extended details on the incompressible Navier-Stokes and Euler solvers in SU2.
The equations can be expressed in differential form as

$$ \mathcal{R}(V) = \frac{\partial V}{\partial t} + \nabla \cdot \bar{F}^{c}(V) - \nabla \cdot \bar{F}^{v}(V,\nabla V)  - S = 0 $$

where the conservative variables are given by 

$$U=\left\lbrace \rho, \rho\bar{v},\rho c_{p} T \right\rbrace ^\mathsf{T}$$

but the working variables within the solver are the primitives given by

$$V = \left \{  p, \bar{v}, T \right \}^\mathsf{T}$$ 

$$S$$ is a generic source term, and the convective and viscous fluxes are

$$\bar{F}^{c}(V) = \left\{\begin{array}{c} \rho \bar{v} \\ \rho \bar{v} \otimes \bar{v} + \bar{\bar{I}} p \\ \rho c_{p} \, T \bar{v} \end{array} \right\}$$

$$\bar{F}^{v}(V,\nabla V) = \left\{\begin{array}{c} \cdot \\ \bar{\bar{\tau}} \\  \kappa \nabla T \end{array} \right\} $$

where $$\rho$$ is the fluid density, $$\bar{v}=\left\lbrace u, v, w \right\rbrace^\mathsf{T}$$ $$\in$$ $$\mathbb{R}^3$$ is the flow speed in Cartesian system of reference, $$p$$ is the pressure, $$\bar{\bar{\tau}}$$ is the viscous stress tensor, $$T$$ is the temperature, $$\kappa$$ is the thermal conductivity, and $$\mu$$ is the viscosity. The viscous stress tensor can be expressed in vector notation as

$$\bar{\bar{\tau}}= \mu \left ( \nabla \bar{v} + \nabla \bar{v}^{T} \right ) - \mu \frac{2}{3} \bar{\bar I} \left ( \nabla \cdot \bar{v} \right )$$

In the low-Mach form of the equations, the pressure is decomposed into thermodynamic and dynamic components. $$p$$ is interpreted as the dynamic pressure in the governing equations, and $$p_o$$ is the thermodynamic (operating) pressure, which is constant in space. The system is now closed with an equation of state for the density that is a function of temperature alone $$\rho  = \rho(T)$$. Assuming an ideal gas with a specific gas constant $$R$$, one can determine the density from $$\rho = \frac{p_o}{R T}$$. 

Conductivity can be a constant, or we assume a constant Prandtl number $$Pr$$ such that the conductivity varies with viscosity as $$\kappa = \mu c_p / Pr$$. For laminar flows, $$\mu$$ is simply the dynamic viscosity $$\mu_{d}$$, which can be constant or assumed to satisfy Sutherland's law as a function of temperature alone, and $$Pr$$ is the dynamic Prandtl number $$Pr_d$$. For turbulent flows, we solve the incompressible Reynolds-averaged Navier-Stokes (RANS) equations. In accord with the standard approach to turbulence modeling based upon the Boussinesq hypothesis, which states that the effect of turbulence can be represented as an increased viscosity, the viscosity is divided into dynamic and turbulent components, or  $$\mu_{d}$$ and $$\mu_{t}$$, respectively. Therefore, the effective viscosity in becomes

$$\mu =\mu_{d}+\mu_{t}$$

Similarly, the thermal conductivity in the energy equation becomes an effective thermal conductivity written as

$$\kappa =\frac{\mu_{d} \, c_p}{Pr_{d}}+\frac{\mu_{t} \, c_p}{Pr_{t}}$$

where we have introduced a turbulent Prandtl number $$Pr_t$$. The turbulent viscosity $$\mu_{t}$$ is obtained from a suitable turbulence model involving the mean flow state $$U$$ and a set of new variables for the turbulence. 

The governing equation set in the general form above is very flexible for handling a number of variations in the modeling assumptions, from constant density inviscid flows up to variable density turbulent flows with a two-way coupled energy equation and temperature-dependent transport coefficients. Natural convection and 2D axisymmetric problems can be treated in a straightforward manner with the addition of source terms.

Within the `INC_NAVIER_STOKES` and `INC_RANS` solvers, we discretize the equations in space using a finite volume method (FVM) with a standard edge-based data structure on a dual grid with vertex-based schemes. The convective and viscous fluxes are evaluated at the midpoint of an edge. We apply a density-based scheme that is a generalization of artificial compressibility in order to achieve pressure-velocity coupling and solve the incompressible equations in a fully coupled manner.

---

# Incompressible Euler #

| Solver | Version | 
| --- | --- |
| `INC_EULER` | 7.0.0 |

SU2 solves the incompressible Euler equations as a simplification of the low-Mach formulation above in the absence of viscosity and thermal conductivity (no energy equation is required). The equations can be expressed in differential form as

$$ \mathcal{R}(V) = \frac{\partial V}{\partial t} + \nabla \cdot \bar{F}^{c}(V) - S = 0 $$

where the conservative variables are given by 

$$U=\left\lbrace \rho, \rho\bar{v} \right\rbrace ^\mathsf{T}$$

but the working variables within the solver are the primitives given by

$$V = \left \{  p, \bar{v} \right \}^\mathsf{T}$$ 

$$S$$ is a generic source term, and the convective flux is

$$\bar{F}^{c}(V) = \left\{\begin{array}{c} \rho \bar{v} \\ \rho \bar{v} \otimes \bar{v} + \bar{\bar{I}} p \end{array} \right\}$$

where $$\rho$$ is a fluid density (constant), $$\bar{v}=\left\lbrace u, v, w \right\rbrace^\mathsf{T}$$ $$\in$$ $$\mathbb{R}^3$$ is the flow speed in Cartesian system of reference, and $$p$$ is the dynamic pressure.

Within the `INC_EULER` solver, we discretize the equations in space using a finite volume method (FVM) with a standard edge-based data structure on a dual grid with vertex-based schemes. The convective and viscous fluxes are evaluated at the midpoint of an edge. We apply a density-based scheme that is a generalization of artificial compressibility in order to achieve pressure-velocity coupling and solve the incompressible equations in a fully coupled manner.

---

# Turbulence Modeling #

Available for `RANS`, `INC_RANS`.

SU2 implements several variants of the SST and SA turbulence models, for specifics of the models please see the [NASA Turbulence Modeling Resource](https://turbmodels.larc.nasa.gov/index.html) (TMR).
For information on how to use turbulence models in SU2 see the [users guide](https://su2code.github.io/docs_v7/Physical-Definition/).

The edge-based finite volume discretization of flow solvers is also used in turbulence solvers. Convective fluxes are evaluated using a scalar upwind scheme (1st or 2nd order).

## Wall functions

Available for `RANS`, `INC_RANS`.

The wall function model of Nichols and Nelson (2004) has been implemented in the compressible and the incompressible solver, for the SA as well as the SST models. For the compressible solver, the wall function model takes into account the frictional heating of the wall according to the Crocco-Busemann relation when the wall boundary conditions is not isothermal. When the wall model is active, the value of the dimensional distance of the first node from the wall can be $$ y^+ > 5$$. When the wall model is not active, $$y^+ < 5 $$ and in addition a fine mesh is necessary close to the wall to resolve the near wall boundary layer.

---

# Species Transport #

Compatible with `NAVIER_STOKES`, `RANS`, `INC_NAVIER_STOKES`, `INC_RANS`.

$$ \mathcal{R}(U) = \frac{\partial U}{\partial t} + \nabla \cdot \bar{F}^{c}(U) - \nabla \cdot \bar{F}^{v}(U,\nabla U)  - S = 0 $$

where the conservative variables (which are also the working variables) are given by 

$$U=\left\lbrace \rho Y_1, ..., \rho Y_{N-1} \right\rbrace ^\mathsf{T}$$

with $$Y_i$$ $$[-]$$ being the species mass fraction. And 

$$\sum_{i=0}^N Y_i = 1 \Rightarrow Y_N = 1 - \sum_{i=0}^{N-1} Y_i$$
  
$$S$$ is a generic source term, and the convective and viscous fluxes are

$$\bar{F}^{c}(V) = \left\{\begin{array}{c} \rho Y_1 \bar{v} \\ ... \\\rho Y_{N-1} \, \bar{v} \end{array} \right\}$$

$$\bar{F}^{v}(V,\nabla V) = \left\{\begin{array}{c} D \nabla Y_{1} \\ ... \\  D \nabla Y_{N-1} \end{array} \right\} $$

with $$D$$ $$[m^2/s]$$ being the mass diffusion. 

$$D = D_{lam} + \frac{\mu_T}{Sc_{T}}$$

where $$\mu_T$$ is the eddy viscosity and $$Sc_{T}$$ $$[-]$$ the turbulent Schmidt number.

---

# Flamelet Combustion Modeling #

| Solver | Version | 
| --- | --- |
| `INC_NAVIER_STOKES` | 8.0.0 |

The Flamelet combustion model (also called Flamelet Generated Manifold (FGM)) for laminar premixed flames has been implemented in the incompressible solver. The flamelet method is a tabulated chemistry approach. Two additional transport equations are solved for the progress variable $$C$$ and the total enthalpy $$h_t$$, which is here the sensible + the chemical enthalpy. Thermo-chemical properties (viscosity, temperature, reaction source terms,...) are retrieved from a lookup table, which is constructed from 1D detailed chemistry simulations (e.g. Cantera, FlameMaster, Chem1d). For a detailed introduction to flamelet modeling see the work of van Oijen et al. https://www.sciencedirect.com/science/article/pii/S0360128515300137

---

# Elasticity #

| Solver | Version | 
| --- | --- |
| `ELASTICITY` | 7.0.0 |

For structural analysis of solids in SU2, we solve the elasticity equations in a form allowing for geometric non-linearities expressed as

$$ \rho_s \frac{\partial^2 \mathbf{u}}{\partial t^2} = \nabla (\mathbf{F} \cdot \mathbf{S}) + \rho_s \mathbf{f} $$

where $$\rho_s$$ is the structural density, $$\mathbf{u}$$ are the displacements of the solid, $$\mathbf{F}$$ is the material deformation gradient, $$\mathbf{S}$$ is the second Piola-Kirchhoff stress tensor, and $$\mathbf{f}$$ is the volume forces on the structural domain. 

In the `ELASTICITY` solver, we discretize the equations in space with a nodal finite element method (FEM).

---

# Heat Conduction #

| Solver | Version | 
| --- | --- |
| `HEAT_EQUATION_FVM` | 7.0.0 |

The governing equation for heat conduction through a solid material can be expressed in differential form as the following:

$$ R(U) = \frac{\partial U}{\partial t} - \nabla \cdot \bar{F}^{v}(U,\nabla U) - S = 0 $$

where the conservative variable is $$U=\left\lbrace \rho_s c_{p_s} T\right\rbrace$$, $$\rho_s$$ is the solid density, $$c_{p_s}$$ is the specific heat of the solid, and $$T$$ is the temperature. The viscous flux can be written as 

$$ \bar{F}^{v}(U,\nabla U) = \kappa_s \nabla T $$

where $$\kappa_s$$ is the thermal conductivity of the solid. The material properties of the solid are considered constant.

Within the `HEAT_EQUATION_FVM` solver, we discretize the equations in space using a finite volume method (FVM) with a standard edge-based data structure on a dual grid with vertex-based schemes. The viscous flux is evaluated at the midpoint of an edge.
