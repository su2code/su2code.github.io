---
title: Static Fluid-Structure Interaction (FSI) Adjoint via Python-wrapper
permalink: /tutorials/Adjoint_FSI_Python/
written_by: rsanfer
for_version: 7.0.3
revised_by: rsanfer
revision_date: 2020-03-04
revised_version: 7.0.3
solver: Multiphysics
requires: pysu2ad library
complexity: advanced
follows: Static_FSI
follows2: Static_FSI_Python
userguide: Build-SU2-Linux-MacOS
---

This tutorial uses SU2's python wrapper and its native adjoint solvers for incompressible flow and solid mechanics to solve a steady-state, **adjoint** Fluid-Structure Interaction problem. This document will cover:
- Operating with the AD version of the pysu2 library
- Extracting the adjoints of the flow loads and structural displacements from two different python instances of SU2
- Exchanging adjoint information between the two instances

In this tutorial, we will solve the adjoint of the problem presented in the [Static FSI with Python](../Static_FSI_Python/) tutorial, which is a pre-requisite in order to be able to run this tutorial.

### Resources

You can find the resources for this tutorial in the folder [python_fsi](https://github.com/su2code/Tutorials/tree/feature_python_fsi/multiphysics/python_fsi) of the [Tutorials repository](https://github.com/su2code/Tutorials). There is a [python script](https://github.com/su2code/Tutorials/tree/feature_python_fsi/multiphysics/python_fsi/run_fsi_adjoint.py) and two sub-config files for the [flow AD subproblem](https://github.com/su2code/Tutorials/tree/feature_python_fsi/multiphysics/python_fsi/config_channel_ad.cfg) and [structural AD subproblem](https://github.com/su2code/Tutorials/tree/feature_python_fsi/multiphysics/python_fsi/config_cantilever_ad.cfg).

Moreover, you will need to reuse the two mesh files from the  [Static FSI with Python](../Static_FSI_Python/) tutorial and the solution files generated when running it.

### Background 

For this tutorial, you will need to use advanced features of SU2, in particular the python-wrapped version of the AD code, which needs to be built from source. 

This tutorial has been tested on a linux system with the following specs

```
Linux kernel 5.3.18-1-MANJARO
GCC compilers version 9.2.0
Open MPI version 4.0.2
Python version 3.8.1
SWIG version 4.0.1
CoDiPack version 1.8
```

compiling the code from source using the following meson settings

```
./meson.py build -Dwith-mpi=enabled -Denable-autodiff=true -Denable-pywrapper=true
```

It requires an adequate setup of the system and a correct linkage of both the ```mpi4py``` and ```swig``` libraries. For questions, updates, or notes on the usability of this tutorials on different systems or configurations, please use the comment section below.

#### Mesh Description

The cantilever is discretized using 1000 4-node quad elements with linear interpolation. The fluid domain is discretized using a finite volume mesh with 7912 nodes and 15292 triangular volumes. The wet interface is matching between the fluid and structural domains.

#### Configuration File Options

We reuse the [flow](https://github.com/su2code/Tutorials/tree/feature_python_fsi/multiphysics/python_fsi/config_channel_ad.cfg) and [structural](https://github.com/su2code/Tutorials/tree/feature_python_fsi/multiphysics/python_fsi/config_cantilever_ad.cfg) config files from the [Static FSI with Python](../Static_FSI_Python/) tutorial. However, it is necessary to add some changes to run the discrete adjoint solver. 

First, we need to enable adjoint mode on the flow config file

```
MATH_PROBLEM = DISCRETE_ADJOINT
OBJECTIVE_FUNCTION = DRAG
```

and the structural config file

```
MATH_PROBLEM = DISCRETE_ADJOINT
```

where the drag coefficient is defined as the functional for which we want to compute the adjoint. 

Next, and same as for the primal tutorial, SU2 will see each instance as a single-zone problem. Therefore, it is necessary to set the output appropriately in order to prevent overwriting files. For the flow AD config

```
OUTPUT_FILES = (RESTART, PARAVIEW)
SOLUTION_FILENAME = solution_fsi_steady_0
RESTART_FILENAME = restart_fsi_steady_0

SOLUTION_ADJ_FILENAME = solution_ad_fsi_steady_0
RESTART_ADJ_FILENAME = restart_ad_fsi_steady_0
VOLUME_ADJ_FILENAME = fsi_ad_steady_0
```

and for the structural config

```
OUTPUT_FILES = (RESTART, PARAVIEW)
SOLUTION_FILENAME = solution_fsi_steady_1
RESTART_FILENAME = restart_fsi_steady_1

SOLUTION_ADJ_FILENAME = solution_ad_fsi_steady_1
RESTART_ADJ_FILENAME = restart_ad_fsi_steady_1
VOLUME_ADJ_FILENAME = fsi_ad_steady_1
```

Next, we choose the output for the history files. In this tutorial, we are interested on the derivative of the drag coefficient with respect to the Young's modulus of the cantilever, and therefore for the flow simulation it is enough to retrieve the residuals on the history file

```
HISTORY_OUTPUT = ITER, RMS_RES
CONV_FILENAME= history_ad_0
```

while for the structural config we need to request the sensitivities as well

```
HISTORY_OUTPUT = ITER, RMS_RES, SENSITIVITY
CONV_FILENAME= history_ad_1
```

Also, we monitor in this case adjoint quantities for the flow simulation

```
CONV_FIELD = RMS_ADJ_PRESSURE, RMS_ADJ_VELOCITY-X, RMS_ADJ_VELOCITY-Y
CONV_RESIDUAL_MINVAL = -12
```

and the structural simulation

```
CONV_FIELD = ADJOINT_DISP_X, ADJOINT_DISP_Y
CONV_STARTITER = 2
CONV_RESIDUAL_MINVAL = -7
```

Finally, and the same as for the primal case, it is necessary to indicate to the structural solver that the boundary solution will be used to update a fluid field. This is done by setting the config options

```
MARKER_FLUID_LOAD = ( feabound )
MARKER_DEFORM_MESH = ( feabound )
```

on the structural config file.

#### Applying coupling conditions to the individual domains

As usual for adjoint problems, the first step is to rename the restart files from the primal run as solution files, ```restart_fsi_steady_0.dat``` &rarr; ```solution_fsi_steady_0.dat``` and ```restart_fsi_steady_1.dat``` &rarr; ```solution_fsi_steady_1.dat```.

The key part of this tutorial is the [python script](https://github.com/su2code/Tutorials/tree/feature_python_fsi/multiphysics/python_fsi/run_fsi_adjoint.py) to run the adjoint FSI problem. Please take a moment to evaluate its contents, as we will go through some of its most important aspects.

First, we will need to import the SU2 adjoint library along with mpi4py, using

```
import pysu2ad as pysu2
from mpi4py import MPI
```

We define the names of the config files required by SU2 using

```
flow_filename = "config_channel_ad.cfg"
fea_filename = "config_cantilever_ad.cfg"
```

We will exemplify the initialization of SU2 using the flow domain. First, we create a single-zone adjoint driver object using

```
FlowDriver = pysu2.CDiscAdjSinglezoneDriver(flow_filename, 1, comm);
```

which is analogous to the SU2 driver in the C++ executable. We use a ```comm``` that is imported from ```mpi4py```

```
comm = MPI.COMM_WORLD
```

and the ```flow_filename``` variable previously defined. Next, identifyin the FSI boundary is analogous to the primal script and will not be repeated here.

Now, the major differences with respect to the primal case are presented. First, we need to initialize the cross dependency that is applied as a source term into the flow domain to 0, using

```
fea_sens=[]
for j in range(nVertex_Marker_Flow):
  fea_sens.append([0.0, 0.0, 0.0])
```

We start the FSI loop and limit it to 15 iterations

```
for i in range(15):
```

and the source term corresponding to the flow load adjoint is applied to the fluid domain. In the first iteration, this will be a zero-vector, but that will not be the case for subsequent iterations.

```
  FlowDriver.SetFlowLoad_Adjoint(FlowMarkerID,0,fea_sens[1][0],fea_sens[1][1],0)
  FlowDriver.SetFlowLoad_Adjoint(FlowMarkerID,1,fea_sens[0][0],fea_sens[0][1],0)     
  for j in range(2, nVertex_Marker_Flow):
    FlowDriver.SetFlowLoad_Adjoint(FlowMarkerID,j,fea_sens[j][0],fea_sens[j][1],0)
```

The flow adjoint iteration is run now using

```
  FlowDriver.ResetConvergence()
  FlowDriver.Preprocess(0)
  FlowDriver.Run()
  FlowDriver.Postprocess() 
  FlowDriver.Update()
  stopCalc = FlowDriver.Monitor(0)
```

We need to recover the flow loads and apply them to the structural simulation in order to run the primal iteration for the recording,

```
  flow_loads=[]
  for j in range(nVertex_Marker_Flow):
    vertexLoad = FlowDriver.GetFlowLoad(FlowMarkerID, j)
    flow_loads.append(vertexLoad)
    
  FEADriver.SetFEA_Loads(FEAMarkerID, 0, flow_loads[1][0], flow_loads[1][1], 0)
  FEADriver.SetFEA_Loads(FEAMarkerID, 1, flow_loads[0][0], flow_loads[0][1], 0)
  for j in range(2, nVertex_Marker_FEA):
    FEADriver.SetFEA_Loads(FEAMarkerID, j, flow_loads[j][0], flow_loads[j][1], 0)
```

and also, we need to extract the cross dependency on the mesh displacements

```
  flow_sens=[]
  for iVertex in range(nVertex_Marker_Flow):
    sensX, sensY, sensZ = FlowDriver.GetMeshDisp_Sensitivity(FlowMarkerID, iVertex)
    flow_sens.append([sensX, sensY, sensZ])
```

that will be used as a source term into the structural domain

```
  FEADriver.SetSourceTerm_DispAdjoint(FEAMarkerID,0,flow_sens[1][0],flow_sens[1][1],0)
  FEADriver.SetSourceTerm_DispAdjoint(FEAMarkerID,1,flow_sens[0][0],flow_sens[0][1],0)
  for j in range(nVertex_Marker_FEA):
    FEADriver.SetSourceTerm_DispAdjoint(FEAMarkerID,j,flow_sens[j][0],flow_sens[j][1],0)
```
      
Next, the structural adjoint simulation is run with

```
  FEADriver.ResetConvergence()
  FEADriver.Preprocess(0)  
  FEADriver.Run()
  FEADriver.Postprocess() 
  FEADriver.Update()
  stopCalc = FEADriver.Monitor(0)
```

and the crossed sensitivities with respect to the flow load are retrieved using

```
  fea_sens=[]
  for j in range(nVertex_Marker_FEA):
    sensX, sensY, sensZ = FEADriver.GetFlowLoad_Sensitivity(FEAMarkerID, j)
    fea_sens.append([sensX, sensY, sensZ])
```

Finally, these boundary displacements are imposed to the flow domain in the next iteration. Once the loop is completed, it only remains to write the solution of each domain to file using

```
FlowDriver.Output(0)
FEADriver.Output(0)
```

### Running SU2

Follow the links provided to download the [python script](https://github.com/su2code/Tutorials/tree/feature_python_fsi/multiphysics/python_fsi/run_fsi_adjoint.py) and the two sub-config files for the [flow](https://github.com/su2code/Tutorials/tree/feature_python_fsi/multiphysics/python_fsi/config_channel_ad.cfg) and [structural](https://github.com/su2code/Tutorials/tree/feature_python_fsi/multiphysics/python_fsi/config_cantilever_ad.cfg) subproblems.

Also, you will need the two mesh files for the [flow domain](https://github.com/su2code/Tutorials/tree/feature_python_fsi/multiphysics/python_fsi/mesh_channel.su2) and the [cantilever](https://github.com/su2code/Tutorials/tree/feature_python_fsi/multiphysics/python_fsi/mesh_cantilever.su2).

Execute the code using Python

```
$ python run_fsi_adjoint.py
```

The convergence history of each individual domain will be printed to screen, starting with the flow adjoint simulation

```
-------------------------------------------------------------------------
Direct iteration to store the primal computational graph.
Compute residuals to check the convergence of the direct problem.
log10[U(0)]: -16.7835, log10[U(1)]: -16.1388, log10[U(2)]: -17.2225.
log10[U(3)]: -32.
-------------------------------------------------------------------------

+---------------------------------------------------+
|  Inner_Iter|    rms[A_P]|    rms[A_U]|    Sens_Geo|
+---------------------------------------------------+
|           0|   -2.613161|   -1.287093|  0.0000e+00|
|          10|   -3.599787|   -2.867742|  0.0000e+00|
|          20|   -4.291071|   -3.771486|  0.0000e+00|
|          30|   -5.000513|   -4.533287|  0.0000e+00|
|          40|   -5.721670|   -5.350516|  0.0000e+00|
|          50|   -6.457920|   -5.924181|  0.0000e+00|
|          60|   -7.217678|   -6.566948|  0.0000e+00|
|          70|   -7.978391|   -7.212931|  0.0000e+00|
|          80|   -8.738623|   -7.908635|  0.0000e+00|
|          90|   -9.463444|   -8.636672|  0.0000e+00|
|         100|  -10.163400|   -9.400965|  0.0000e+00|
|         110|  -10.847301|  -10.206336|  0.0000e+00|
|         120|  -11.539210|  -11.037515|  0.0000e+00|
|         130|  -12.246150|  -11.854391|  0.0000e+00|
|         137|  -12.812627|  -12.143415|  0.0000e+00|

Recording the computational graph with respect to the secondary variables.
```

followed by the structural domain

```
-------------------------------------------------------------------------
Direct iteration to store the primal computational graph.
Compute residuals to check the convergence of the direct problem.
UTOL-A: -14.5125, RTOL-A: -11.6402, ETOL-A: -28.601.
-------------------------------------------------------------------------

+----------------------------------------------------------------+
|  Inner_Iter| rms[Ux_adj]| rms[Uy_adj]|     Sens[E]|    Sens[Nu]|
+----------------------------------------------------------------+
|           0|    1.608195|    2.017211|  1.4163e-05|  6.1467e-01|
|           1|   -7.838855|   -7.470968|  1.4163e-05|  6.1467e-01|
|           2|   -7.472256|   -7.061584|  1.4163e-05|  6.1467e-01|
```

We observe that, in both cases, the direct iteration recovers converged residuals for the primal problem.

After 15 iterations, both the flow and structural adjoint fields are successfully converged,

```
+---------------------------------------------------+
|  Inner_Iter|    rms[A_P]|    rms[A_U]|    Sens_Geo|
+---------------------------------------------------+
|           0|  -11.703018|  -10.364366|  5.3425e+02|
|          10|  -12.847050|  -12.112670|  5.3425e+02|

+----------------------------------------------------------------+
|  Inner_Iter| rms[Ux_adj]| rms[Uy_adj]|     Sens[E]|    Sens[Nu]|
+----------------------------------------------------------------+
|           0|   -8.235703|   -8.050333|  1.1606e-05|  5.0401e-01|
|           1|   -7.792824|   -7.398341|  1.1606e-05|  5.0401e-01|
|           2|   -7.994688|   -7.626300|  1.1606e-05|  5.0401e-01|
```

with a gradient of the drag with respect to the Young's modulus, E, of 1.1606E-05. The convergence of the Young's modulus sensitivity is as follows:

![FSI Results2](../multiphysics/images/fsipyadj1.png)

#### Sensitivity verification

In order to verify the Young's modulus sensitivity, we access the file ```history_ad_1.csv```, which stores the value with 10 significant figures. We obtain

```
Sens[E] = 1.160565822e-05
```

Now, we run central differences to test the accuracy of this value. We compute the drag coefficient for the incremented and decremented value of the Young's modulus

| Young's Modulus $$E$$ | Drag coefficient $$C_D$$  |
|---|---|
| 4.995E+04 | 3.122565491 |
| 5.000E+04 | 3.123146337 |
| 5.005E+04 | 3.123726058 |

which yields a $$\mathrm{d}C_D / \mathrm{d} E$$ computed with central differences of 1.160567E-05, which has an excellent agreement with the value computed via the adjoint.

### Attribution

If you are using this content for your research, please kindly cite the following reference in your derived works:

Sanchez, R. _et al._ (2018), [Coupled Adjoint-Based Sensitivities in Large-Displacement Fluid-Structure Interaction using Algorithmic Differentiation](https://spiral.imperial.ac.uk/handle/10044/1/51023), _Int J Numer Meth Engng, Vol 111, Issue 7, pp 1081-1107_. DOI: [10.1002/nme.5700](https://doi.org/10.1002/nme.5700)

<dl>
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>
<br />
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
</dl>

