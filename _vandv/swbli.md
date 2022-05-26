---
title: Shock-Wave Boundary-Layer Interaction
permalink: /vandv/swbli/
---

| Solver | Version | Author |
| --- | --- | --- |
| `RANS` | 7.4.0 | P. Gomes |

The details of the Mach 5 SWBLI validation case are taken from [NASA](https://www.grc.nasa.gov/www/wind/valid/m5swbli/m5swbli.html).

<p align="center">
<img src="/vandv_files/swbli/mach.png" alt="Mach number contours (SST-2003m)" />
</p>
**Figure 1** - Mach number contours (SST-2003m).

We validate our implementation of the SA and SST models by comparing the SU2 numerical results on a sequence of grids against experimental results.

## Problem Setup

The geometry and flow conditions are according to the [main reference](https://www.grc.nasa.gov/www/wind/valid/m5swbli/m5swbli.html).
The SU2 configuration files used in this study are [available here](https://github.com/su2code/SU2/blob/develop/TestCases/vandv/rans/swbli/).
Mean flow convective fluxes were computed with Roe's scheme and a limited MUSCL reconstruction (Green-Gauss gradients and Venkatakrishnan's limiter).
The SA-neg and SST-2003m turbulence models were used with first order advection.
SU2 was run with "freestream equal Mach" non-dimensionalization for all configurations.

## Mesh Description

Quad-dominant meshes of increasing density were used to perform a grid convergence study.
The meshes were generated using GMSH by defining a refinement factor for all sizes and counts.
Particular attention was given to the y+ on the bottom plate (smaller than 1 on the coarsest level), the main shock, and the separation region.
The GMSH script can be downloaded from the [SU2 V&V GitHub repository](https://github.com/su2code/VandV/tree/master/rans/swbli).
The mesh designations and approximate sizes are: 

- L1 "coarse" (2 x "fine") - 37k quadrilaterals
- L2 "medium" (1.41 x "fine") - 76k quadrilaterals
- L3 "fine" - 146k quadrilaterals

## Results

Given the focus of this validation case (interaction between a shock and a boundary layer) it is of particular interest to analyze how well CFD predicts the 

### Grid convergence

The main configuration studied here is the Roe scheme, with MUSCL reconstruction using Green-Gauss gradients, and limited using the van Albada edge-based limiter.
The only possible tunning parameter of this configuration is the entropy fix coefficient, which was fixed at 1e-5.
We compare this configuration with the JST scheme on three grid levels (with 2nd and 4th order coefficient values of 0.5 and 0.01, respectively).
For completeness, we also test the effect of the limiter on the "fine" level by using the Venkatakrishnan limiter with coefficient 0.05.

We observe second order convergence of the lift and drag coefficients, and good agreement between Roe + van Albada, JST, [FaSTAR results](https://jaxa.repo.nii.ac.jp/?action=pages_view_main&active_action=repository_view_main_item_detail&item_id=2921&item_no=1&page_id=13&block_id=21), and [Cflow results](https://jaxa.repo.nii.ac.jp/?action=pages_view_main&active_action=repository_view_main_item_detail&item_id=2923&item_no=1&page_id=13&block_id=21).
The Roe + Venkatakrishnan configuration predicts lower values, which were observed to be sensitive to the limiter coefficient. For example lowering it to 0.025 increases drag to the level obtained with the other two configurations.

<p align="left">
<img src="/vandv_files/30p30n/drag.png" alt="Drag coefficient at 5.5deg AoA" />
</p>
**Figure 2** - Drag coefficient at 5.5deg AoA.

<p align="left">
<img src="/vandv_files/30p30n/lift.png" alt="Lift coefficient at 5.5deg AoA" />
</p>
**Figure 3** - Lift coefficient at 5.5deg AoA.

### Maximum lift

Roe + van Albada and JST agree well on the maximum lift, and again match the results of other codes.
However JST predicts the flow to remain attached at significantly higher angle-of-attack than expected.

<p align="left">
<img src="/vandv_files/30p30n/max_lift.png" alt="Lift coefficient on the fine grid level" />
</p>
**Figure 4** - Lift coefficient on the fine grid level.

<p align="left">
<img src="/vandv_files/30p30n/max_drag.png" alt="Drag coefficient on the fine grid level" />
</p>
**Figure 5** - Drag coefficient on the fine grid level.

### Discussion

The pressure coefficient distributions at 5.5 degrees AoA computed by Roe + van Albada and JST are nearly identical.
However, JST predicts significantly higher skin friction coefficient (Cf) on the suction side which explains the higher angle-of-attack required for leading-edge separation to occur.
Away from this critical point the lift and drag characteristics are dominated by the pressure distribution and thus the two schemes agree well.
The only significant differences in Cf between the van Albada and Venkatakrishnan limiters are at the trailing-edges.

<p align="left">
<img src="/vandv_files/30p30n/cp.png" alt="Pressure coefficient distribution at 5.5deg AoA on fine grid level" />
</p>
**Figure 6** - Pressure coefficient distribution at 5.5deg AoA on fine grid level.

<p align="left">
<img src="/vandv_files/30p30n/cf.png" alt="Skin friction coefficient distribution at 5.5deg AoA on fine grid level" />
</p>
**Figure 7** - Skin friction coefficient distribution at 5.5deg AoA on fine grid level.

