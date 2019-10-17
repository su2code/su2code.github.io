---
title: Governing Equations in SU2
permalink: /docs/Theory/
---

**This guide is for version 7 only**

This page contains a very brief summary of the different governing equation sets that are treated in each of the solvers within SU2. The reader will be referred to other references for the full detail of the numerical implementations, but we will also describe the approaches at a high level here.

---

## Content ##
- [Compressible Reynolds-averaged Navier-Stokes](#compressible-rans)
- [Compressible Laminar Navier-Stokes](#compressible-navier-stokes)
- [Compressible Euler](#compressible-euler)
- [Incompressible Reynolds-averaged Navier-Stokes](#compressible-rans)
- [Incompressible Laminar Navier-Stokes](#compressible-navier-stokes)
- [Incompressible Euler](#compressible-euler)
- [Elasticity](#elasticity)
- [Heat Conduction](#heat-conduction)
  
---

# Compressible Reynolds-averaged Navier-Stokes #

The compressible Navier-Stokes equations can be expressed in differential form as

$$ \mathcal{R}(U) = \frac{\partial U}{\partial t} + \nabla \cdot \bar{F}^{c}(U) - \nabla \cdot \bar{F}^{v}(U,\nabla U)  - S = 0 $$

where the conservative variables are given by 

$$U = \left \{  \rho, \rho \bar{v},  \rho E \right \}^\mathsf{T}$$ 

$$S$$ is a generic source term to be discussed later, and the convective and viscous fluxes are

$$\bar{F}^{c}   = \left \{ \begin{array}{c} \rho \bar{v}  \\ \rho \bar{v} \otimes  \bar{v} + \bar{\bar{I}} p \\ \rho E \bar{v} + p \bar{v}   \end{array} \right \}$$

and 

$$\bar{F}^{v} = \left \{ \begin{array}{c} \cdot \\ \bar{\bar{\tau}} \\ \bar{\bar{\tau}} \cdot \bar{v} + \kappa \nabla T  \end{array} \right  \}$$

where $$\rho$$ is the fluid density, $$\bar{v}=\left\lbrace u, v, w \right\rbrace^\mathsf{T}$$ $$\in$$ $$\mathbb{R}^3$$ is the flow speed in Cartesian system of reference, $$E$$ is the total energy per unit mass, $$p$$ is the static pressure, $$\bar{\bar{\tau}}$$ is the viscous stress tensor, $$T$$ is the temperature, $$\kappa$$ is the thermal conductivity, and $$\mu$$ is the viscosity. The viscous stress tensor can be expressed in vector notation as

$$\bar{\bar{\tau}}= \mu \left ( \nabla \bar{v} + \nabla \bar{v}^{T} \right ) - \mu \frac{2}{3} \bar{\bar I} \left ( \nabla \cdot \bar{v} \right )$$

Assuming a perfect gas with a ratio of specific heats $$\gamma$$ and gas constant $$R$$, one can close the system by determining pressure from $$p = (\gamma-1) \rho \left [ E - 0.5(\bar{v} \cdot \bar{v} ) \right ]$$ and temperature from the ideal gas equation of state $$T = p/(\rho R)$$. Conductivity can be a constant, or we assume a constant Prandtl number $Pr$ such that the conductivity varies with viscosity as $$\kappa = \mu c_p / Pr$$. 

It is also possible to model non-ideal fluids within SU2 using more advanced fluid models that are available, but this is not discussed here. Please see the tutorial on the topic.

For laminar flows, $$\mu$$ is simply the dynamic viscosity $$\mu_{d}$$, which can be constant or assumed to satisfy Sutherland's law as a function of temperature alone, and $$Pr$$ is the dynamic Prandtl number $$Pr_d$$. For turbulent flows, we solve the Reynolds-averaged Navier-Stokes (RANS) equations. In accord with the standard approach to turbulence modeling based upon the Boussinesq hypothesis, which states that the effect of turbulence can be represented as an increased viscosity, the viscosity is divided into dynamic and turbulent components, or  $$\mu_{d}$$ and $$\mu_{t}$$, respectively. Therefore, the effective viscosity in becomes

$$\mu =\mu_{d}+\mu_{t}$$.

Similarly, the thermal conductivity in the energy equation becomes an effective thermal conductivity written as

$$\kappa =\frac{\mu_{d} \, c_p}{Pr_{d}}+\frac{\mu_{t} \, c_p}{Pr_{t}}$$,

where we have introduced a turbulent Prandtl number $$Pr_t$$. The turbulent viscosity $$\mu_{t}$$ is obtained from a suitable turbulence model involving the mean flow state $U$ and a set of new variables for the turbulence. The Shear Stress Transport (SST) model of Menter and the Spalart-Allmaras (S-A) model are two of the most common and widely used turbulence models. The S-A and SST baseline models, along with several variants, are implemented in SU2.

# Compressible Euler #
# Incompressible Navier-Stokes #
# Incompressible Euler #
# Elasticity #
# Heat Conduction #
