---
title: Non-ideal compressible flow in a supersonic nozzle using data-driven fluid modeling
permalink: /tutorials/NICFD_nozzle_datadriven/
written_by: EvertBunschoten
for_version: 8.1.0
solver: RANS
requires: SU2_CFD, SU2_DataMiner 
complexity: advanced
follows: 
---

![NICFD nozzle Mach](../../tutorials_files/compressible_flow/NICFD_nozzle/images/mach_isolines.png)

## Goals

This tutorial explains how to use the data-driven fluid model in SU2 in order to model the fluid properties of siloxane MM using physics-informed machine learning. In addition, this tutorial explains how to use [SU2 DataMiner](https://github.com/EvertBunschoten/SU2_DataMiner.git) to generate fluid data and train a multi-layer perceptron which can be used by SU2 for NICFD simulations. The data-driven fluid model is demonstrated by simulating the supersonic expansion of siloxane MM through a converging-diverging nozzle. 

The fluid considered in this tutorial is siloxane MM, but the methods presented in this tutorial can be used to generate multi-layer perceptrons for any fluid available in the CoolProp library.

## Resources

The resources for this tutorial can be found in [compressible_flow/NICFD_nozzle/PhysicsInformed](https://github.com/su2code/Tutorials/tree/master/compressible_flow/NICFD_nozzle/PhysicsInformed) in the [tutorial repository](https://github.com/su2code/Tutorials). In addition, [SU2 DataMiner](https://github.com/EvertBunschoten/SU2_DataMiner.git) is required for the generation of fluid data and the multi-layer perceptron for the data-driven fluid model in SU2. SU2 DataMiner is a python-based software suite that can be used for preparing data-driven fluid simulations in SU2 for laminar combustion and NICFD. 

In order to utilize the data-driven fluid model for this tutorial, SU2 should be compiled with the following flags:
```
-Denable-mlpcpp=true -Denable-pywrapper=true
```
Please visit the [Download](/docs_v7/Download/) and [Installation](/docs_v7/Installation/) pages for more information.

Finally, the mesh in this tutorial is generated with the python module for [gmsh](https://gmsh.info/). 

## Tutorial

In the first part of this tutorial, SU2 DataMiner is used to generate fluid data and train a multi-layer perceptron through physics-informed machine learning to model the thermodynamic state of siloxane MM. After that, the NICFD simulation is run by using the SU2 python wrapper.

### Step 1: SU2 DataMiner configuration

SU2 DataMiner uses a configuration class from which all parameters describing the fluid, training data, and network training parameters are retrieved. The configuration used in this tutorial can be generated with [this file](https://github.com/su2code/Tutorials/tree/feature_PINN/compressible_flow/NICFD_nozzle/PhysicsInformed/0:generate_config.py). The fluid thermodynamic data for siloxane MM that are used in this tutorial are generated with the python module for CoolProp using the Helmoltz equation of state. The fluid name and equation of state are therefore defined as "MM" and "HEOS".
```
fluid_name = "MM"
EoS_type = "HEOS"

Config = Config_NICFD()
Config.SetFluid(fluid_name)
Config.SetEquationOfState(EoS_type)
```
The fluid data are generated on a grid of density and internal energy. The density-based fluid data grid is enabled by disabling the option for a pressure-temperature data grid.
```
# Fluid data are generated on a density-energy grid rather than pressure-temperature.
Config.UsePTGrid(False)
```
All other options in the SU2 DataMiner configuration can be kept as default. Finally, the configuration is given a name, its contents diplayed in the terminal and the configuration is saved as a binary in the current working directory.
```
# Display configuration settings and save config object.
Config.SetConfigName("SU2DataMiner_MM")
Config.PrintBanner()
Config.SaveConfig()
```

### Step 2: Fluid data generation

The next step is to generate the fluid thermodynamic data that are used to train the multi-layer perceptron. At the moment, the data-driven fluid model in SU2 is compatible with single-phase fluids only. Therefore, SU2 DataMiner generates fluid data in the gas and supercritical gas phases only. In this tutorial, the ranges for density and internal energy within which fluid data are computed are automatically determined based on the triple point of the fluid and the maximum pressure and temperature for which fluid data are available in the CoolProp module. 

The fluid data generation process is outlined in [the following script](https://github.com/su2code/Tutorials/tree/feature_PINN/compressible_flow/NICFD_nozzle/PhysicsInformed/1:generate_fluid_data.py). 

### Step 3: Multi-layer perceptron definition 

### Step 4: Mesh generation and NICFD simulation

