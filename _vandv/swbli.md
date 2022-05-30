---
title: Shock-Wave Boundary-Layer Interaction
permalink: /vandv/swbli/
---

| Solver | Version | Author |
| --- | --- | --- |
| `RANS` | 7.4.0 | P. Gomes |

The details of the Mach 5 SWBLI validation case are taken from the [NPARC Alliance Validation Archive](https://www.grc.nasa.gov/www/wind/valid/m5swbli/m5swbli.html).

<p align="center">
<img src="/vandv_files/swbli/mach.png" alt="Mach number contours (SST-2003m)" />
</p>
**Figure 1** - Mach number contours (SST-2003m).

We validate our implementation of the SA and SST models by comparing the SU2 numerical results on a sequence of grids against experimental results.

## Problem Setup

The main geometry features and flow conditions are according to the [main reference](https://www.grc.nasa.gov/www/wind/valid/m5swbli/m5swbli.html). In this study, the inlet was extended 10mm to avoid the intersection of the supersonic inlet with a no-slip wall (that extension is modelled with a slip wall).
The SU2 configuration files used in this study are [available here](https://github.com/su2code/SU2/blob/develop/TestCases/vandv/rans/swbli/).
These are applicable to all grid levels, however note that simulations on finer grids were restarted from the results on the previous (coarser) level.
Mean flow convective fluxes were computed with Roe's scheme and a limited MUSCL reconstruction (Green-Gauss gradients and Venkatakrishnan's limiter).
The SA-neg and SST-2003m turbulence models were used with first order advection.
SU2 was run with "freestream equal Mach" non-dimensionalization for all configurations.

## Mesh Description

Quad-dominant meshes of increasing density were used to perform a grid convergence study.
The meshes were generated using GMSH where a refinement factor was applied for all sizes and counts.
Particular attention was given to the y+ on the bottom plate (smaller than 1 on the coarsest level), the main shock, and the separation region.
The GMSH script can be downloaded from the [SU2 V&V GitHub repository](https://github.com/su2code/VandV/tree/master/rans/swbli).
The mesh designations and approximate sizes are:

- L1 "coarse" (2 x "fine") - 37k quadrilaterals
- L2 "medium" (1.41 x "fine") - 76k quadrilaterals
- L3 "fine" - 146k quadrilaterals

## Results

Given the focus of this validation case (interaction between a shock wave and a boundary layer) it is of particular interest to analyze how well CFD predicts the skin friction coefficient on the bottom plate and the separation (caused by the shock wave) and re-attachment locations.
Figure 2 compares the skin friction coefficient for the two turbulence models and three mesh levels used, with the experimental values.

<p align="center">
<img src="/vandv_files/swbli/cf.png" alt="Comparison of skin friction coefficient." />
</p>
**Figure 2** - Comparison of skin friction coefficient.

The results do not change significantly between meshes L2 and L3, they were also not sensitive to other perturbations such as refining the mesh around the main shock, or global refinement (i.e. L4).
