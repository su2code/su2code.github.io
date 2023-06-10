---
title: 2D Axisymmetric, Nonpremixed, Nonreacting, Variable Density, Turbulent Jet Flow
permalink: /vandv/SANDIA_jet/
---

| Solver | Version | Author |
| --- | --- | --- |
| `INC_RANS` | 7.5.0 | Sem Bosmans |
The details of the Zero Pressure Gradient Flat Plate case are taken from the [NASA TMR website](https://turbmodels.larc.nasa.gov/flatplate.html).

By comparing the SU2 results of the flat plate case against CFL3D and FUN3D on a sequence of refined grids and seeing agreement of key quantities, we can build a high degree of confidence that the SA and SST models are implemented correctly. Therefore, the goal of this case is to verify the implementations of the SA and SST models in SU2.

## Problem Setup

...

## Mesh Description

An inlet section with a length of 30D is included upstream of the jet exit, in order to achieve fully-developed turbulent pipe flow.

## Results

First, the results for the grid convergence study are presented. We will compare the convergence of the maximum value of the mixture fraction, as well as the mean axial velocity component at four locations with grid refinement. Additionally, a figure is included demonstrating the residual convergence histories for each mesh. 

Based on the grid convergence study, we can build confidence that the compared simulation results are coming from a mesh independent solution, using the grid containing 7649 quadrilaterals. 

The comparisons in the figures demonstrate good agreement with the experimental data and other codes, which builds high confidence in the implementation of the composition-dependent model in SU2 for the incompressible solver. 

---

### Grid Convergence

<p align="center">
<img src="/vandv_files/SANDIA_jet/images/Grid_convergence4.png" alt="Mixture Fraction Grid Convergence x/D=4" />
<img src="/vandv_files/SANDIA_jet/images/Grid_convergence15.png" alt="Mixture Fraction Grid Convergence x/D=15" />
<img src="/vandv_files/SANDIA_jet/images/Grid_convergence30.png" alt="Mixture Fraction Grid Convergence x/D=30" />
<img src="/vandv_files/SANDIA_jet/images/Grid_convergence50.png" alt="Mixture Fraction Grid Convergence x/D=50" />
<img src="/vandv_files/SANDIA_jet/images/Grid_convergenceU4.png" alt="Velocity Grid Convergence x/D=4" />
<img src="/vandv_files/SANDIA_jet/images/Grid_convergenceU15.png" alt="Velocity Grid Convergence x/D=15" />
<img src="/vandv_files/SANDIA_jet/images/Grid_convergenceU30.png" alt="Velocity Grid Convergence x/D=30" />
<img src="/vandv_files/SANDIA_jet/images/Grid_convergenceU50.png" alt="Velocity Grid Convergence x/D=50" />
</p>

---

### SST Model

The two main SST models, 1994m and 2003m, are compared against FUN3D and CFL3D. Note that for FUN3D and CFL3D, for this case only the 1994m results are available. 