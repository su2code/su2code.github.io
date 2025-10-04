---
title: 2D Axisymmetric, Nonpremixed, Nonreacting, Variable Density, Turbulent Jet Flow
permalink: /vandv/SANDIA_jet/
---

| Solver | Version | Author |
| --- | --- | --- |
| `INC_RANS` | 7.5.0 | Sem Bosmans |


The details of the 2D Axisymmetric, Nonpremixed, Nonreacting, Variable Density, Turbulent Jet Flow are taken from [Sandia National Laboratories database](https://tnfworkshop.org/data-archives/simplejet/propanejet) <sup>[1](#ref1),[2](#ref2)/<sup>.

By comparing the results of SU2 simulations case against the experimental data, as well as OpenFOAM simulation results <sup>[3](#ref3)/<sup> (and MFSim <sup>[4](#ref4)/<sup>), we can build a high degree of confidence that the composition-dependent model is implemented correctly in combination with the SST turbulence model. Therefore, the goal of this case is to validate the implementation of the  composition-dependent model in SU2.

## Problem Setup
The problem consists of a turbulent propane jet mixing into coflowing air. The schematic overview of this problem is given in the figure below:

<p align="center">
<img src="/vandv_files/SANDIA_jet/images/VV_SETUP.png" alt="Schematic overview of the problem setup" />
</p>

The flow conditions are based on the Sandia experiment $$^{1}$$:

- Temperature = 294 [K]
- Thermodynamic pressure = 101325 [Pa]
- Jet inner diameter = 5.26 [mm]
- Jet outer diameter = 9.0 [mm]

The inlet conditions are given below:

Gas inlet:

- Bulk jet velocity = 53 [m/s]	
- Turbulence intensity = 4%
- Eddy viscosity ratio = 5.0
- Reynolds number = 68000

Air inlet:

- Velocity = 9.2 [m/s]
- Turbulence intensity = 0.4%
- Eddy viscosity ratio = 0.1 

The thermochemical properties for the propane and air are presented below:
* Propane:
    - Molecular Weight = 44.097 [g / mol]
    - Viscosity: 8.04E-06 [kg /(m s)]
    - Heat capacity at constant pressure: 1680.0 [J/(kg K)]
    - Thermal Conductivity: 0.0179 [W /(m K)]
* Air: 
    - Molecular Weight = 28.960 [g / mol]
    - Viscosity: 1.8551E-05 [kg /(m s)]
    - Heat capacity at constant pressure: 1009.39 [J/(kg K)]
    - Thermal Conductivity: 0.0258 [W /(m K)]

## Mesh Description

Structured meshes of increasing density have been used to perform a grid convergence study. The following four meshes have been used:

- 65x60 - 3556 quadrilaterals
- 80x74 - 5442 quadrilaterals
- 94x88 - 7649 quadrilaterals
- 108x102 - 10267 quadrilaterals

The length of the domain in streamwise direction is 80D. the width is 20D. Additionally, an inlet section with a length of 30D is included upstream of the jet exit, in order to achieve fully-developed turbulent pipe flow.

If you would like to run the problem for yourself, you can use the files available in the [SU2 V&V repository](https://github.com/su2code/VandV/tree/master/rans/SANDIA_jet). The configuration file, as well as the grids in GEO format, are provided. 

## Results

First, the results for the grid convergence study are presented. We will compare the convergence of the maximum value of the mixture fraction, as well as the mean axial velocity component at four locations with grid refinement. Additionally, a figure is included demonstrating the residual convergence histories for each mesh. 

Based on the grid convergence study, we can build confidence that the compared simulation results are coming from a mesh independent solution, using the grid containing 7649 quadrilaterals. 

The comparisons in the figures demonstrate good agreement with the experimental data and other codes, which builds high confidence in the implementation of the composition-dependent model in SU2 for the incompressible solver. 

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
<img src="/vandv_files/SANDIA_jet/images/Residual_convergence.png" alt="Residual Convergence for the Turbulent Jet Mixing" />
</p>

---

### Mixture Fraction

<p align="center">
<img src="/vandv_files/SANDIA_jet/images/YD0_f.png" alt="Mixture Fraction along Jet Centerline" />
<img src="/vandv_files/SANDIA_jet/images/XD04_f.png" alt="Mixture Fraction at x/D=4" />
<img src="/vandv_files/SANDIA_jet/images/XD15_f.png" alt="Mixture Fraction at x/D=15" />
<img src="/vandv_files/SANDIA_jet/images/XD30_f.png" alt="Mixture Fraction at x/D=30" />
<img src="/vandv_files/SANDIA_jet/images/XD50_f.png" alt="Mixture Fraction at x/D=50" />
</p>

### Mean Axial Velocity

<p align="center">
<img src="/vandv_files/SANDIA_jet/images/YD0_U_norm.png" alt="Normalized Mean Velocity Decay along Jet Centerline" />
<img src="/vandv_files/SANDIA_jet/images/YD0_U.png" alt="Mean Velocity Decay along Jet Centerline" />
<img src="/vandv_files/SANDIA_jet/images/XD04_U.png" alt="Mean Axial Velocity at x/D=4" />
<img src="/vandv_files/SANDIA_jet/images/XD15_U.png" alt="Mean Axial Velocity at x/D=15" />
<img src="/vandv_files/SANDIA_jet/images/XD30_U.png" alt="Mean Axial Velocity at x/D=30" />
<img src="/vandv_files/SANDIA_jet/images/XD50_U.png" alt="Mean Axial Velocity at x/D=50" />
</p>

### Mean Radial Velocity

<p align="center">
<img src="/vandv_files/SANDIA_jet/images/YD0_V.png" alt="Mean Radial Velocity along Jet Centerline" />
<img src="/vandv_files/SANDIA_jet/images/XD04_V.png" alt="Mean Radial Velocity at x/D=4" />
<img src="/vandv_files/SANDIA_jet/images/XD15_V.png" alt="Mean Radial Velocity at x/D=15" />
<img src="/vandv_files/SANDIA_jet/images/XD30_V.png" alt="Mean Radial Velocity at x/D=30" />
<img src="/vandv_files/SANDIA_jet/images/XD50_V.png" alt="Mean Radial Velocity at x/D=50" />
</p>

### Turbulent Kinetic Energy

<p align="center">
<img src="/vandv_files/SANDIA_jet/images/YD0_TKE.png" alt="TKE along Jet Centerline" />
<img src="/vandv_files/SANDIA_jet/images/XD04_TKE.png" alt="TKE Velocity at x/D=4" />
<img src="/vandv_files/SANDIA_jet/images/XD15_TKE.png" alt="TKE Velocity at x/D=15" />
<img src="/vandv_files/SANDIA_jet/images/XD30_TKE.png" alt="TKE Velocity at x/D=30" />
<img src="/vandv_files/SANDIA_jet/images/XD50_TKE.png" alt="TKE Velocity at x/D=50" />
</p>

### Density

<p align="center">
<img src="/vandv_files/SANDIA_jet/images/YD0_rho.png" alt="Mean density along Jet Centerline" />
</p>

The experimental results for the mean density are given in Sandia’s database, but these are directly computed from the mixture fraction by making use of the ratio between the density of propane and air. The ratio that is being used for this purpose is 1.6 <sup>[2](#ref2)/<sup>, whereas the expected ratio is lower. The higher density ratio used in the post-processing of the experimental data results in a wider density range across the domain, which can partly explain the differences between the experimental data and the numerical results on the density along the jet centerline. Note that the spreading rate of a jet is independent of the initial density ratio <sup>[2](#ref2)/<sup>.

<p align="center">
<img src="/vandv_files/SANDIA_jet/images/Residuals_convergence.png" alt="Residuals Convergence for the Turbulent Jet Mixing" />
</p>

---

### References
<a id="ref1">[1]</a> R.W. Schefer, "Data Base for a Turbulent, Nonpremixed, Nonreacting, Propane-Jet Flow", tech. rep., Sandia National Laboratories, Livermore, CA, 2001.

<a id="ref2">[2]</a> R.W. Schefer, F.C. Gouldin, S.C. Johnson and W. Kollmann, "Nonreacting Turbulent Mixing Flows", tech. rep., Sandia National Laboratories, Livermore, CA, 1986.

<a id="ref3">[3]</a> A. Aghajanpour and S. Khatibi, "Numerical Simulation of Velocity and Mixture Fraction Fiels in a Turbulent Non-reacting Propane Jet Flow Issuing into Parallel Co-Flowing Air in Isothermal Condition through OpenFOAM", 2023.

<a id="ref4">[4]</a> V. Goncalves, G.M. Magalhaes and J.M. Vedovetto, "Urans Simulation of Turbulent Non-Premixed and Non-Reacting Propane Jet Flow", Associacao Brasileira de Engenharia e Ciencias Mecanicas - ABCM, 2021.
