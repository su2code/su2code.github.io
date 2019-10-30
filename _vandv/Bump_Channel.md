---
title: 2D Bump-in-Channel RANS Verification Case
permalink: /vandv/Bump_Channel/
---

<p align="center">
<img src="/vandv_files/Bump_Channel/images/bump_cf_0p75_gridconv_sst.png" alt="Skin Friction Grid Convergence SST x = 0.75" width="435"/>
</p>


The details of the 2D Bump-in-Channel Verification case are taken from the [NASA TMR website](https://turbmodels.larc.nasa.gov/bump.html). 

By comparing the SU2 results of the bump-in-channel case against CFL3D and FUN3D on a sequence of refined grids and seeing agreement of key quantities, we can build a high degree of confidence that the SA and SST models are implemented correctly. Therefore, the goal of this case is to verify the implementations of the SA and SST models in SU2.

## Problem Setup

The bump-in-channel case is low Mach test case (nearly incompressible) for a fully turbulent flow over a no-slip wall featuring an elevated bump on the surface. The primary difference between this case and the flat plate case is that pressure gradients are induced by the wall curvature of the bump, which makes this case more challenging for turbulence models.

This problem will solve the flow past the bump with these conditions:
- Freestream Temperature = 300 K
- Freestream Mach number = 0.2
- Reynolds number = 3.0E6
- Reynolds length = 1.0 m

The length of the section of wall with the bump is 1.5 meters, and it is represented by an adiabatic no-slip wall boundary condition. The lower boundaries of the domain upstream and downstream of the bump section are modeled as symmetry planes. Inlet and outlet boundary conditions are used on the left and right boundaries of the domain, and a symmetry boundary condition is used over the top region of the domain (the upper wall of the channel), which is located 5 meters away from the bump. All other fluid and boundary conditions are applied as prescribed on the NASA TMR website.

## Mesh Description

Structured meshes of increasing density are used to perform a grid convergence study. The meshes are identical to the 2D versions found on the [NASA TMR website](https://turbmodels.larc.nasa.gov/bump_grids.html) for this case after converting to 2D, unstructured CGNS format (ADF). These meshes are named according to the number of vertices in the x and y directions, respectively. The mesh sizes are: 

1. 89x41  - 3520 quadrilaterals
2. 177x81  - 14080 quadrilaterals
3. 353x161 - 56320 quadrilaterals
4. 705x321 - 225280 quadrilaterals
5. 1409x641 - 901120 quadrilaterals

![Turb Plate Mesh](/vandv_files/Bump_Channel/images/turb_plate_mesh_bcs.png)
Figure (1): Mesh with boundary conditions: inlet (red), outlet (blue), far-field (orange), symmetry (purple), wall (green).

If you would like to run the bump-in-channel problem for yourself, you can use the files available in the [SU2 V&V repository](https://github.com/su2code/VandV/tree/master/rans/bump_in_channel_2d). Configuration files for both the SA and SST cases, as well as all grids in CGNS format, are provided. A Python script is also distributed in order to easily recreate the figures seen below from the data. *Please note that the mesh files found in the repository have been gzipped to reduce storage requirements and should be unzipped before use.*

## Results

The results for the mesh refinement study are presented and compared to results from FUN3D and CFL3D, including results for both the SA and SST turbulence models.

We will compare the convergence of the lift and drag coefficient on the bump with grid refinement, as well as the value of the skin friction coefficient at 3 locations on the bump (x = 0.63, x = 0.75, x = 0.87). We also show the skin friction and pressure coefficients plotted along the length of the bump. For both turbulence models, we present profiles of the eddy viscosity and x-velocity at the x = 0.75 location (top of the bump). For the SST model, we show additional profiles for the turbulent kinetic energy and dissipation near the wall at the x = 0.75 location. All cases were converged until the density residual was reduced to 10<sup>-13</sup>, which is demonstrated by a figure containing residual convergence histories for each mesh.

Both the SA and SST models exhibit excellent agreement in the figures below. With grid refinement, we see that all quantities of interest asymptote very close to those of FUN3D and CFL3D (and additional codes not shown here but displayed on the NASA TMR), which builds high confidence in the implementations of these two turbulence models in SU2. The SU2 results for all profile comparisons are nearly indistinguishable from the CFL3D and FUN3D counterparts.

### SA Model

<p align="center">
<img src="/vandv_files/Bump_Channel/images/bump_cd_gridconv_sa.png" alt="Drag Grid Convergence SA" width="435"/>
<img src="/vandv_files/Bump_Channel/images/bump_cl_gridconv_sa.png" alt="Lift Grid Convergence SA" width="435"/>
<img src="/vandv_files/Bump_Channel/images/bump_cf_0p63_gridconv_sa.png" alt="Skin Friction Grid Convergence SA x = 0.63" width="435"/>
<img src="/vandv_files/Bump_Channel/images/bump_cf_0p75_gridconv_sa.png" alt="Skin Friction Grid Convergence SA x = 0.75" width="435"/>
<img src="/vandv_files/Bump_Channel/images/bump_cf_0p87_gridconv_sa.png" alt="Skin Friction Grid Convergence SA x = 0.87" width="435"/>
<img src="/vandv_files/Bump_Channel/images/bump_cf_profile_sa.png" alt="Skin Friction Profile SA" width="435"/>
<img src="/vandv_files/Bump_Channel/images/bump_cp_profile_sa.png" alt="Pressure Profile SA" width="435"/>
<img src="/vandv_files/Bump_Channel/images/bump_eddy_profile_sa.png" alt="Eddy Viscosity Profile SA" width="435"/>
<img src="/vandv_files/Bump_Channel/images/bump_vel_profile_sa.png" alt="Velocity Profile SA" width="435"/>
<img src="/vandv_files/Bump_Channel/images/bump_residual_convergence_sa.png" alt="Residual Convergence SA" width="435"/>
</p>

### SST Model

<p align="center">
<img src="/vandv_files/Bump_Channel/images/bump_cd_gridconv_sst.png" alt="Drag Grid Convergence SST" width="435"/>
<img src="/vandv_files/Bump_Channel/images/bump_cl_gridconv_sst.png" alt="Lift Grid Convergence SST" width="435"/>
<img src="/vandv_files/Bump_Channel/images/bump_cf_0p63_gridconv_sst.png" alt="Skin Friction Grid Convergence SST x = 0.63" width="435"/>
<img src="/vandv_files/Bump_Channel/images/bump_cf_0p75_gridconv_sst.png" alt="Skin Friction Grid Convergence SST x = 0.75" width="435"/>
<img src="/vandv_files/Bump_Channel/images/bump_cf_0p87_gridconv_sst.png" alt="Skin Friction Grid Convergence SST x = 0.87" width="435"/>
<img src="/vandv_files/Bump_Channel/images/bump_cf_profile_sst.png" alt="Skin Friction Profile SST" width="435"/>
<img src="/vandv_files/Bump_Channel/images/bump_cp_profile_sst.png" alt="Pressure Profile SST" width="435"/>
<img src="/vandv_files/Bump_Channel/images/bump_eddy_profile_sst.png" alt="Eddy Viscosity Profile SST" width="435"/>
<img src="/vandv_files/Bump_Channel/images/bump_vel_profile_sst.png" alt="Velocity Profile SST" width="435"/>
<img src="/vandv_files/Bump_Channel/images/bump_residual_convergence_sst.png" alt="Residual Convergence SST" width="435"/>
</p>

