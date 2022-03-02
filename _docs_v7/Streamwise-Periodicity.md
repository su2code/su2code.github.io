---
title: Streamwise Periodicity
permalink: /docs_v7/Streamwise-Periodicity/
---

| Solver | Version | 
| --- | --- |
| `INC_NAVIER_STOKES`, `INC_RANS` | 7.2.0 |


This page contains an overview of the theory behind streamwise periodic flow and builds upon [Incompressible Navier-Stokes](/docs_v7/Theory/#incompressible-navier-stokes). A tutorial for [Streamwise Periodic Flow](/tutorials/Inc_Streamwise_Periodic/) is available.

---

- [Limitations](#limitations)
- [Introduction](#introduction)
- [Pressure and Velocity Periodiciy](#pandv-periodiciy)
    - [Massflow prescription](#massflow)
- [Temperature Periodiciy](#T-periodiciy)
    - [Fake temperature periodicity via outlet heat sink](#fake-temperature-periodicity-via-outlet-heat-sink)
- [References](#references)

---

## Limitations
- can only be used with the incompressible solver, namely `INC_NAVIER_STOKES` and `INC_RANS`
- temperature dependent fluid properties (e.g. $$c_p, \mu_{lam}$$) cannot be used with real streamwise periodic flow

## Introduction

A flow can be modeled as streamwise periodic if the following statements hold true:

$$\begin{align}
\bar{v}\left( \bar{x} \right) &= \bar{v} \left( \bar{x}+\bar{t} \right), \\
p\left( \bar{x} \right) &= p \left( \bar{x}+\bar{t} \right) + \Delta p_0, \\
T\left( \bar{x} \right) &= T \left( \bar{x}+\bar{t} \right) - \Delta T_0.
\end{align}$$

With $$\bar{t}$$ being the translation vector between periodic interfaces and $$\Delta p_0, \Delta T_0$$ the constant pressure or temperature drop between the periodic interfaces.

## Pressure and Velocity Periodicity

The continuous relation between physical pressure $$p$$ and periodic/reduced pressure $$\tilde{p}$$ in space is:

$$p\left( \bar{x} \right) = \tilde p \left( \bar{x} \right) - \frac{\Delta p_0}{\left\lVert\bar{t}\right\rVert_2}t_p, \quad t_p =\frac{1}{\left\lVert\bar{t}\right\rVert_2} \left| \left( \bar{x} - \bar{x}^\star \right) \cdot \bar{t} \right|.$$

This separation into two parts can be interpreted as a "constant" and a "linear" (along the domain) contribution. 
This relation is used to compute the recovered pressure for postprocessing. 
Inserting this pressure formulation into the momentum equation of the incompressible Navier-Stokes equation (see [here](/docs_v7/Theory/#incompressible-navier-stokes)) results in:

$$\frac{\partial \bar{v}}{\partial t} + \nabla\cdot\left( \rho \bar{v} \otimes \bar{v} + \bar{\bar{I}}\tilde{p} - \bar{\bar \tau}  \right) - \frac{\Delta p_0}{\left\lVert\bar{t}\right\rVert_2^2}\bar{t} = 0,$$

where two things changed:
1. Working variable of the pressure $$p$$ changed to the periodic pressure $$\tilde{p}$$.
2. A constant source term is added to the formulation of the momentum equation.

The source term is now the force that drives the flow and scales with the prescribed pressure drop $$\Delta p_0$$.

This substitution of the pressure variable has to be done in every place it appears. For pressure there is nothing further to do e.g. for the boundary conditions, which will be different for the derivation of periodic temperature.

### Massflow prescription

In applications often the massflux  $$\dot{m}_0^2$$  is known and the pressure drop is the observable. If a massflow is prescribed the pressure drop $$\Delta p_0$$ in the source term is adapted with each iteration to match the current massflow $$\dot{m}^2$$ with the prescribed massflow:


$$\Delta p_0^{n+1} - \Delta p_0^{n} = \Delta \left( \Delta p_0 \right) = \frac{\frac{1}{2} \rho \left( \dot{m}_0^2 - \dot{m}^2 \right)}{\left( \rho A \right)^2}.$$

$$\rho$$ is the density and $$A$$ the flowed through inlet Area. For the pressure drop update a relaxation factor $$\phi$$ is used:

$$\Delta p_0^{n+1} = \Delta p_0^{n} + \phi \Delta \left( \Delta p_0 \right).$$

## Temperature Periodicity

The here presented approach for periodicity in temperature is only possible if only heatflux or symmetry boundary conditions are used, isothermal walls in particular are not allowed. In that case use the [method described below](#fake-temperature-periodicity-via-outlet-heat-sink) is used:

Similar to the pressure term for the momentum equation the Temperature can be split in a periodic and a linear part:

$$T\left( \bar{x} \right) = \tilde T \left( \bar{x} \right) + \frac{\Delta T_0}{\left\lVert\bar{t}\right\rVert_2}t_p, \quad t_p =\frac{1}{\left\lVert\bar{t}\right\rVert_2} \left| \left( \bar{x} - \bar{x}^\star \right) \cdot \bar{t} \right|$$

Just as with the pressure term, this relation is used to compute the recovered temperature for postprocessing. 
Inserting the temperature formulation into the energy equation results in:

$$\frac{\partial \left( \rho c_p \tilde{T} \right)}{\partial t} + \nabla\cdot\left( \rho c_p \tilde{T} \bar{v} - \kappa\nabla \tilde{T} \right) + \frac{Q \rho }{ \dot{m}\left\lVert\bar{t}\right\rVert_2^2} \left[ \bar{t} \cdot \bar{v} \right] = 0$$

With $$Q$$ being the integrated heatflux across the domain boundaries in Watts. In contrast to the derivation for pressure periodicity in the momentum equations the boundary conditions have to adapted for the energy equation. The heatflux (Neumann) wall contribution for the energy equation becomes:

$$- \int_{\partial\Omega} \left( \kappa\nabla T \right) \cdot \bar{n} dS + \int_{\partial\Omega}  \kappa\frac{Q}{\dot{m} c_p \left\lVert\bar{t}\right\rVert_2^2} \left[ \bar{t} \cdot \bar{n} \right] dS = 0 $$

### Temperature periodicity via outlet heat sink

In cases where the above requirements cannot be held (e.g. isothermal walls, CHT interfaces) a simple massflow averaged outlet heat sink is implemented. In these cases pressure is still periodic but temperature is solved in its non-periodic form. Energy is extracted from the domain just at the outlet such that the temperature profile via the periodic interface is approximately retained. This of course is a major simplification that enables the use of an approximated temperature profile over the periodic interface. Solution interpretation, especially if it involves surface temperature integrals near the periodic faces, should be done with the necessary care.

The residual contributions are in twofold. Firstly an either user provided or computed heat is extracted at the outlet with massflow averaged weighting which proved to be better than area averaged weighting:

$$Res -= \frac{\dot m_{local}}{\dot m_{global}} Q_{integrated}$$

The second term is adaptive and scales with the difference between the initial temperature `INC_TEMPERATURE_INIT` and the actual area averaged temperature on the inlet:

$$Res += \frac{1}{2} |\dot m| c_p \left( T_{inlet} - \frac{T_{init}}{T_{ref}} \right)$$

This allows to set the general temperature level in the domain and thereby also allows for the use of temperature material parameters, or isothermal walls and CHT interfaces.

## References

$$^1$$ S.V. Patankar, C.H. Liu, and E.M. Sparrow. Fully developed flow and heat transfer in ducts having streamwise-periodic variations of cross-sectional area. *Journal of Heat Transfer*, 99(2):180–186, 1977. doi: [https://doi.org/10.1115/1.3450666](https://doi.org/10.1115/1.3450666)

$$^2$$ Steven B. Beale. On the implementation of stream-wise periodic boundary conditions. In *ASME 2005  Summer  Heat  Transfer  Conference  collocated  with  the  ASME  2005  Pacific  Rim  Technical  Conference  and  Exhibition  on  Integration  and  Packaging  of  MEMS,  NEMS,  and  ElectronicSystems*, pages 771–777. American Society of Mechanical Engineers, 2005. doi: [https://doi.org/10.1115/HT2005-72271](https://doi.org/10.1115/HT2005-72271)