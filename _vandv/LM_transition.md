---
title: Langtry and Menter transition model
permalink: /vandv/LM_transition/
---

| Solver | Version | Author |
| --- | --- | --- |
| `RANS` | 7.4.0 | S. Kang |

The details of the Langtry and Menter(LM) transition model validation cases are taken from the [AIAA Transition modeling workshop-I](https://transitionmodeling.larc.nasa.gov).
To validate the LM model, the simulation results of SU2 are compared with the results of Fluent19.0 with a similar numerical setting.

## Problem Setup


Flow conditions are the reference from : https://doi.org/10.2514/6.2022-3679 and [AIAA Transition modeling workshop-I](https://transitionmodeling.larc.nasa.gov).

| Case | T3A | T3B | T3Am | NLF0416|
| --- | --- | --- | --- | --- |
|Inlet Velocity (m/s)| 69.44 | 69.44 | 19.8 | 34.72 |
|Density (kg/m^3) | 0.053 | 0.053 | 1.2 | 2.13 |
|Viscosity (kg/ms) | 1.85E-5 | 1.85E-5 | 1.79E-5 | Sutherland's Law |
|Freestream Temperature (K) | 300 | 300 | 300 | 300 |
|Unit Reynolds number (1/m) | 2.0E5 | 2.0E5 | 1.328E6 | 4.0E6 | 
|Mach Number | 0.2 | 0.2 | 0.058 | 0.1 |
|AoA | 0.0 | 0.0 | 0.0 | 0.0 |
|Viscosity Ratio| 11.9 | 99.0 | 9.0 | 1.0 |
|Freestream Turbulence Intensity (%) | 5.855 | 7.216 | 1.0 | 0.15 |


## Mesh Description

The grids of T3A, T3B, and NLF cases are provided by [TMW](https://transitionmodeling.larc.nasa.gov/workshop_i/)(Transition Model Workshop). And, The grid of T3Am was made with reference to https://doi.org/10.2514/6.2022-3679.
If you want to run the above cases, you can use only the fine-level grid files available in the [SU2 V&V repository](https://github.com/su2code/Tutorials/tree/master/compressible_flow/Transitional_Flat_Plate/).


## Numerical Scheme 

| Flat plate | Fluent | SU2 |
| --- | --- | --- |
| Flux | Roe-FDS | L2ROE |
| Gradient | Least Squares Cell Based | WEIGHTED_LEAST_SQUARES |
| Spatial Discretization Flow | Third-order MUSCL | MUSCL_FLOW |
| Spatial Discretization Turbulence | Third-order MUSCL | MUSCL_YES |


| NLF0416 | Fluent | SU2 |
| --- | --- | --- |
| Flux | Roe-FDS | L2ROE |
| Gradient | Least Squares Cell Based | WEIGHTED_LEAST_SQUARES |
| Spatial Discretization Flow | second-order Upwind | MUSCL_FLOW |
| Spatial Discretization Turbulence | second-order Upwind | MUSCL_YES |

## Results

Present results of all grid resolutions and then plot the results of the fine-level grid separately. If you want to see other results of the gird level, you can see them at "vandv_files/LMmodel".
All of the flat plate results(= attached flow) are in good agreement with the Fluent results. But, the Airfoil results have the oscillation near the separation region both Fluent and SU2. 



### T3A 
The experiment data from [here](http://cfd.mace.manchester.ac.uk/ercoftac/)

C : Coarse

M : Medium

F : Fine

X : Extra fine



<p align="center">
<img src="/vandv_files/LM_model/T3A/All_Cf.png" alt="All result comparsion of Cf distribution on T3A" />
<img src="/vandv_files/LM_model/T3A/Fine_Cf.png" alt="Fine level result comparsion of Cf distribution on T3A" />

### T3B
The experiment data from [here](http://cfd.mace.manchester.ac.uk/ercoftac/)

C : Coarse

M : Medium

F : Fine

X : Extra fine


<p align="center">
<img src="/vandv_files/LM_model/T3B/All_Cf.png" alt="All result comparsion of Cf distribution on T3B" />
<img src="/vandv_files/LM_model/T3B/Fine_Cf.png" alt="Fine level result comparsion of Cf distribution on T3B" />


### T3Am
The experiment data from [here](http://cfd.mace.manchester.ac.uk/ercoftac/)

Mesh_1 : Tiny

Mesh_2 : Coarse

Mesh_3 : Medium

Mesh_4 : Fine

Mesh_5 : Extra Fine

Mesh_6 : Ultra Fine

<p align="center">
<img src="/vandv_files/LM_model/T3Am/All_Cf.png" alt="All result comparsion of Cf distribution on T3Am" />
<img src="/vandv_files/LM_model/T3Am/Mesh5_Cf.png" alt="Fine level result comparsion of Cf distribution on T3Am" />


### NLF0416
Fluent and SU2, the NLF-0416 airfoil results oscillate near the separation region. So, Here are shown only the fine-level grid results of every 1000 iterations and the instantaneous.

C : Coarse

M : Medium

F : Fine

Every 1000 iteration results : 

<p align="center">
<img src="/vandv_files/LM_model/NLF/Delta_1000_Fine_Cp.png" alt="Fine level result comparsion of Cp distribution on NLF-0416" />
<img src="/vandv_files/LM_model/NLF/Delta_1000_Fine_Cf.png" alt="Fine level result comparsion of Cf distribution on NLF-0416" />


Instantaneous result is :

<p align="center">
<img src="/vandv_files/LM_model/NLF/Inst_All_Cp.png" alt="Fine level result comparsion of Cp distribution on NLF-0416" />
<img src="/vandv_files/LM_model/NLF/Inst_All_Cf.png" alt="Fine level result comparsion of Cf distribution on NLF-0416" />
<img src="/vandv_files/LM_model/NLF/Inst_Fine_Cp.png" alt="Fine level result comparsion of Cp distribution on NLF-0416" />
<img src="/vandv_files/LM_model/NLF/Inst_Fine_Cf.png" alt="Fine level result comparsion of Cf distribution on NLF-0416" />
