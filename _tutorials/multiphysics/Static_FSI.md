---
title: Static Fluid-Structure Interaction (FSI)
permalink: /tutorials/Static_FSI/
written_by: rsanfer
for_version: 7.0.2
revised_by: rsanfer
revision_date: 2020-02-05
revised_version: 7.0.2
solver: Multiphysics
requires: SU2_CFD
complexity: intermediate
follows: Nonlinear_Elasticity
follows2: Inc_Inviscid_Hydrofoil
userguide: Multizone
---

### Goals

This tutorial combines SU2's fluid and structural capabilities to solver a steady-state Fluid-Structure Interaction problem. This document will cover:
- Setting up a multiphysics problem in SU2
- Nonlinear structural mechanics and incompressible Navier-Stokes flow
- Coupling boundary conditions on primary config file
- Changes required to the config files of each subproblem

In this tutorial, we use the same problem definition as for most structural tutorials, a vertical, slender cantilever, clamped in its base, but in this case it is immersed in a horizontal flow in a channel. This is shown next:

![ProblemSetup](../multiphysics/images/fsi1.png)

### Resources

You can find the resources for this tutorial in the folder [fsi/steady_state](https://github.com/su2code/Tutorials/blob/master/fsi/steady_state) of the [Tutorials repository](https://github.com/su2code/Tutorials). There is a [FSI config file](https://github.com/su2code/Tutorials/blob/master/fsi/steady_state/config_fsi_steady.cfg) and two sub-config files for the [flow](https://github.com/su2code/Tutorials/blob/master/fsi/steady_state/config_channel.cfg) and [structural](https://github.com/su2code/Tutorials/blob/master/fsi/steady_state/config_cantilever.cfg) subproblems.

Moreover, you will need two mesh files for the [flow domain](https://github.com/su2code/Tutorials/blob/master/fsi/steady_state/mesh_channel.su2) and the [cantilever](https://github.com/su2code/Tutorials/blob/master/fsi/steady_state/mesh_cantilever.su2).

### Background 

_The equations presented here are a summary of the approach to FSI in SU2 that is further described in R. Sanchez PhD thesis$$^1$$. Please refer to this document for more information._

SU2 adopts a partitioned approach for Fluid-Structure Interaction that requires imposing compatibility and continuity conditions at the FSI interface $$\Gamma = \Omega_f \cap \Omega_s$$. Continuity of displacements is defined as 

$$ 
	\mathbf{u}_\Gamma = \mathbf{z}_\Gamma,
$$

while the equilibrium of tractions over the interface requires that

$$ 	
	\boldsymbol{\lambda}_f + \boldsymbol{\lambda}_s = 0, 
$$

where $$\boldsymbol{\lambda}_f$$ and $$\boldsymbol{\lambda}_s$$ are, respectively, the tractions over the fluid and structural sides of $$\Gamma$$. They may be defined as

$$
\begin{cases}
  \begin{array}{ll}
  \boldsymbol{\lambda}_{f} = -p\mathbf{n}_{f}+\boldsymbol{\tau}_{f} \mathbf{n}_{f}  &\text{on  } \Gamma_{f},  \\
  \boldsymbol{\lambda}_{s} = \mathbf{\sigma}_{s} \mathbf{n}_{s} &\text{on  } \Gamma_{s},  \\  
  \end{array}
\end{cases}
$$

where $$\mathbf{n}_{f}$$ and $$\mathbf{n}_{s}$$ are the dimensional, outward normals to the fluid and structural sides of $$\Gamma$$ (including area information). 

We define the structural, fluid mesh and fluid problems respectively as $$\mathscr{S}$$, $$\mathscr{M}$$ and $$\mathscr{F}$$. We can write the governing equations of the coupled FSI problem as a function of the problem state variables, $$\mathbf{u}$$, $$\mathbf{w}$$ and $$\mathbf{z}$$, which are respectively the structural displacements, the flow conservative variables and the flow mesh displacements, as

$$\mathscr{G}(\mathbf{u}, \mathbf{w}, \mathbf{z}) = 
\begin{cases}
\renewcommand\arraystretch{1.4}
      \mathscr{S}(\mathbf{u}, \mathbf{w}, \mathbf{z}) = \mathbf{T}(\mathbf{u}) - \mathbf{F}_b - \mathbf{F}_{\Gamma}(\mathbf{u}, \mathbf{w}, \mathbf{z}) + \rho_s \mathbf{\ddot{u}} = \mathbf{0},  \\
      \mathscr{F}(\mathbf{w}, \mathbf{z}) = \mathbf{\dot{w}} + \nabla \cdot \mathbf{F^{c}}(\mathbf{w}, \mathbf{z}, \mathbf{\dot{z}}) - \nabla \cdot \mathbf{F^{v}}(\mathbf{w}, \mathbf{z})  = \mathbf{0}, \\
      \mathscr{M}(\mathbf{u}, \mathbf{z}) = \mathbf{\tilde{K}}_{\mathscr{M}}\mathbf{z} - \mathbf{\tilde{f}}(\mathbf{u}) = \mathbf{0}.  
\end{cases}
$$

Due to the non-linear nature of the coupled problem, one can apply Newton-Raphson methods to obtain the coupled solution $$^2$$. The problem may be linearised within a time step writing it in the form of a Newton iteration

$$
\left\{
\begin{array}{ccc}
       \frac{\partial \mathscr{S}}{\partial \mathbf{u}} 
     & \frac{\partial \mathscr{S}}{\partial \mathbf{w}}
     & \frac{\partial \mathscr{S}}{\partial \mathbf{z}} \\         
       \mathbf{0} 
     & \frac{\partial \mathscr{F}}{\partial \mathbf{w}}
     & \frac{\partial \mathscr{F}}{\partial \mathbf{z}} \\            
       \frac{\partial \mathscr{M}}{\partial \mathbf{u}} 
     & \mathbf{0}
     & \frac{\partial \mathscr{M}}{\partial \mathbf{z}} \\
     \end{array}
\right\}     
\normalsize
\left\{
\begin{array}{cc|cc}
       \Delta \mathbf{u} \\                                                         
       \Delta \mathbf{w} \\
       \Delta \mathbf{z} \\
\end{array}
\right\}
=
- \left\{
\begin{array}{cc|cc}
       \mathscr{S}(\mathbf{u}, \mathbf{w}, \mathbf{z})  \\
       \mathscr{F}(\mathbf{w}, \mathbf{z})  \\  
       \mathscr{M}(\mathbf{u}, \mathbf{z})  \\                
     \end{array}
\right\}
.
$$

However, the construction of the previous Jacobian of the problem is complex. In SU2, we avoid it by adopting a Block-Gauss-Seidel (BGS) strategy, which allows the sequential solution of the three problems within each FSI iteration,

$$
\left\{
\begin{array} {ccc}
\frac{\partial \mathscr{S}}{\partial \mathbf{u}} & 0 & 0 \\
0 & \frac{\partial \mathscr{F}}{\partial \mathbf{w}} & 0 \\
\frac{\partial \mathscr{M}}{\partial \mathbf{u}} & 0 & \frac{\partial \mathscr{M}}{\partial \mathbf{z}}
\end{array} 
\right\}
\left\{
\begin{array}{c}
\Delta \mathbf{u} \\ \Delta \mathbf{w} \\ \Delta \mathbf{z}
\end{array} 
\right\}
= - 
\left\{
\begin{array}{c}  
\mathscr{S}(\mathbf{u},\mathbf{w},\mathbf{z}) \\
\mathscr{F}(\mathbf{w},\mathbf{z}) \\
\mathscr{M}(\mathbf{u},\mathbf{z})
\end{array} 
\right\}
$$

The linearized problem in BGS form is solved iteratively until convergence.

#### Mesh Description

The cantilever is discretized using 1000 4-node quad elements with linear interpolation. The fluid domain is discretized using a finite volume mesh with 7912 nodes and 15292 triangular volumes. The wet interface is matching between the fluid and structural domains.

#### Configuration File Options

We start the tutorial by definining the problem as a multiphysics case,

```
SOLVER = MULTIPHYSICS
```

We set the config files for each sub-problem using the command ```CONFIG_LIST```, and state that each sub-problem will use a different mesh file:

```
CONFIG_LIST = (config_channel.cfg, config_cantilever.cfg)
MULTIZONE_MESH = NO
```

Now, we define the outer iteration strategy to solve the FSI problem. We use a Block Gauss-Seidel iteration as defined in the background section with a maximum of 40 outer iterations

```
MULTIZONE_SOLVER = BLOCK_GAUSS_SEIDEL
OUTER_ITER = 40
```

Then, the convergence criteria is set to evaluate the averaged residual of the flow state vector (zone 0) (```AVG_BGS_RES[0]```) and the structural state vector (zone 1) (```AVG_BGS_RES[1]```) in two consecutive outer iterations, $$\mathbf{w}^{n+1}-\mathbf{w}^{n}$$ and $$\mathbf{u}^{n+1}-\mathbf{u}^{n}$$ respectively.

```
CONV_FIELD = AVG_BGS_RES[0], AVG_BGS_RES[1]
CONV_RESIDUAL_MINVAL = -9
```

Finally, we define the coupling conditions. In this case, the interface between the marker ```flowbound``` in the flow field, and ```feabound``` in the structural field, is defined as

```
MARKER_ZONE_INTERFACE = (flowbound, feabound)
```

The last step is defining our desired output. In this tutorial, we will use the following configuration for the screen output

```
SCREEN_OUTPUT = (OUTER_ITER, AVG_BGS_RES[0], AVG_BGS_RES[1], DEFORM_MIN_VOLUME[0], DEFORM_ITER[0])
WRT_ZONE_CONV = NO
```

where the convergence magnitudes are plotted alongside the minimum volume obtained in the deformed mesh, and the number of iterations required by the linear solver that updates the mesh deformation. For clarity, the command ```WRT_ZONE_CONV``` limits the output to the outer iterations, while the convergence of the flow and structural sub-problems is not written to screen.

The convergence output will be set using

```
HISTORY_OUTPUT = ITER, BGS_RES[0], AERO_COEFF[0], BGS_RES[1]

WRT_ZONE_HIST = NO
CONV_FILENAME= history
```

where the individual components of the flow and structural outer-iteration residuals will be written, together with the convergence of the aerodynamic coefficients for the flow domain. In terms of result output, we use 

```
OUTPUT_FILES = (RESTART, PARAVIEW)
RESTART_FILENAME = restart_fsi_steady
VOLUME_FILENAME = fsi_steady
```

where the volume files ```fsi_steady_*.vtu``` and restart files ```restart_fsi_steady_*.vtu``` will be appended the zone number.

#### Applying coupling conditions to the individual domains

Minor modifications are required for the flow and structural config files to be used in Fluid-Structure Interaction, as compared to a single-zone problem. As it is understood that the user will have a basic knowledge of the flow and structural solvers of SU2 before attempting this tutorial, only the specific commands for FSI will be discussed here.

On the fluid domain (zone 0), it is necessary to indicate SU2 what is the boundary for which the flow loads will need to be computed and later applied to the structural domain, in [config_channel.cfg](https://github.com/su2code/Tutorials/blob/master/fsi/steady_state/config_channel.cfg). This is done using

```
MARKER_FLUID_LOAD = ( flowbound )
```

Next, given that we are using an Arbitrary Lagrangian-Eulerian (ALE) formulation for the flow domain, the conditions for mesh deformation need to be set. We start by defining

```
DEFORM_MESH = YES
MARKER_DEFORM_MESH = ( flowbound )
```

where the deforming boundary is set to ```flowbound```. Next, the mesh problem defined in the background section is set. We define the stiffness of the flow mesh as a function of the distance to the deformable wall, where volumes that are farther away from the boundary will be more flexible (thus, more prone to deform largely)

```
DEFORM_STIFFNESS_TYPE = WALL_DISTANCE
```

Next, we set the properties of the linear solver. This is a pseudo-linear-elastic problem and, therefore, the properties of the linear elastic solver will be similar as those used on the [Linear Elasticity Tutorial](../Linear_Elasticity/). As a result, for this case we use
```
DEFORM_LINEAR_SOLVER = CONJUGATE_GRADIENT
DEFORM_LINEAR_SOLVER_PREC = ILU
DEFORM_LINEAR_SOLVER_ERROR = 1E-8
DEFORM_LINEAR_SOLVER_ITER = 1000
DEFORM_CONSOLE_OUTPUT = NO
```

As the structural side uses a Lagrangian formulation, and therefore no mesh deformation is carried out, only the wet boundary that receives the flow loads needs to be specified in [config_cantilever.cfg](https://github.com/su2code/Tutorials/blob/master/fsi/steady_state/config_cantilever.cfg)

```
MARKER_FLUID_LOAD = ( feabound )
```

### Running SU2

Follow the links provided to download the [FSI config file](https://github.com/su2code/Tutorials/blob/master/fsi/steady_state/config_fsi_steady.cfg) and the [flow](https://github.com/su2code/Tutorials/blob/master/fsi/steady_state/config_channel.cfg) and [structural](https://github.com/su2code/Tutorials/blob/master/fsi/steady_state/config_cantilever.cfg) sub-config files.

Also, you will need two files for the [channel mesh](https://github.com/su2code/Tutorials/blob/master/fsi/steady_state/mesh_channel.su2) and the [cantilever mesh](https://github.com/su2code/Tutorials/blob/master/fsi/steady_state/mesh_cantilever.su2). Please note that the latter is different from the structural mechanics tutorial due to a different definition of the boundary conditions.

Execute the code with the standard command and using the multi-zone config file

```
$ SU2_CFD config_fsi_steady.cfg
```

which will show the following convergence history:

```
+----------------------------------------------------------------+
|                        Multizone Summary                       |
+----------------------------------------------------------------+
|  Outer_Iter| avg[bgs][0]| avg[bgs][1]|MinVolume[0]|DeformIter[0|
+----------------------------------------------------------------+
|           0|   -0.298306|   -2.057930|  8.8212e-10|           0|
|           1|   -1.233707|   -2.461095|  8.7251e-10|          44|
|           2|   -1.873187|   -2.756673|  8.7582e-10|          44|
|           3|   -2.318032|   -3.063910|  8.7469e-10|          44|
|           4|   -2.779761|   -3.367198|  8.7509e-10|          44|
|           5|   -3.234473|   -3.671810|  8.7495e-10|          44|
|           6|   -3.691477|   -3.975951|  8.7500e-10|          44|
|           7|   -4.147655|   -4.280253|  8.7498e-10|          44|
|           8|   -4.604089|   -4.584496|  8.7498e-10|          44|
|           9|   -5.060508|   -4.888768|  8.7498e-10|          44|
|          10|   -5.516800|   -5.193024|  8.7498e-10|          44|
|          11|   -5.972522|   -5.497350|  8.7498e-10|          44|
|          12|   -6.430557|   -5.802173|  8.7498e-10|          44|
|          13|   -6.887166|   -6.107626|  8.7498e-10|          44|
|          14|   -7.332413|   -6.412442|  8.7498e-10|          44|
|          15|   -7.786647|   -6.715388|  8.7498e-10|          44|
|          16|   -8.241665|   -7.018034|  8.7498e-10|          44|
|          17|   -8.696447|   -7.320767|  8.7498e-10|          44|
|          18|   -9.150914|   -7.623596|  8.7498e-10|          44|
|          19|   -9.605232|   -7.926468|  8.7498e-10|          44|
|          20|  -10.059523|   -8.229348|  8.7498e-10|          44|
|          21|  -10.513823|   -8.532227|  8.7498e-10|          44|
|          22|  -10.968128|   -8.835097|  8.7498e-10|          44|
|          23|  -11.422397|   -9.137915|  8.7498e-10|          44|
```

The code is stopped as soon as the values of ```avg[bgs][0]``` and ```avg[bgs][1]``` are below the convergence criteria set in the config file. 

The displacement field on the structural domain and the velocity field on the flow domain obtained in ```fsi_steady_1.vtu```_and ```fsi_steady_0.vtu``` respectively are shown below:

![FSI Results1](../multiphysics/images/fsi2.png)

![FSI Results2](../multiphysics/images/fsi3.png)

#### Relaxing the computation

In order to increase the speed of convergence, it is normally a good option to apply a relaxation 


to the sub-iterations of the FSI problem. This is done by adding the following commands

```
BGS_RELAXATION= FIXED_PARAMETER
STAT_RELAX_PARAMETER= 0.8
```

to the FSI master config file. Running SU2 now would result in the following convergence history

```
+----------------------------------------------------------------+
|                        Multizone Summary                       |
+----------------------------------------------------------------+
|  Outer_Iter| avg[bgs][0]| avg[bgs][1]|MinVolume[0]|DeformIter[0|
+----------------------------------------------------------------+
|           0|   -0.298306|   -2.057930|  8.8212e-10|           0|
|           1|   -1.328468|   -2.545969|  8.4294e-10|          44|
|           2|   -2.534408|   -3.682943|  8.6847e-10|          44|
|           3|   -3.191063|   -4.589793|  8.7367e-10|          44|
|           4|   -3.914158|   -5.005570|  8.7472e-10|          44|
|           5|   -4.607760|   -5.801215|  8.7493e-10|          44|
|           6|   -5.312537|   -6.111128|  8.7497e-10|          44|
|           7|   -6.011509|   -6.646911|  8.7498e-10|          44|
|           8|   -6.713854|   -7.336080|  8.7498e-10|          44|
|           9|   -7.420407|   -7.562424|  8.7498e-10|          44|
|          10|   -8.120180|   -8.055230|  8.7498e-10|          44|
|          11|   -8.821508|   -8.532547|  8.7498e-10|          44|
|          12|   -9.521912|   -9.019092|  8.7498e-10|          44|

```

where the -9 convergence parameter is reached in almost half the iterations as per the non-relaxed case.

#### Printing the inner convergence

Sometimes, especially when things don't work as expected, it's interesting to visualize the convergence of each of the subproblems. This can be achieved enabling

```
WRT_ZONE_CONV = YES
``` 

in the main config file of the multizone problem, ```config_fsi_steady.cfg```. In most cases we will not be interested on every single inner iteration of the fluid domain; we can use

```
SCREEN_WRT_FREQ_INNER = 10
```

in ```config_channel.cfg``` to limit the printout to every 10 iterations. The resulting screen output is the following:


```
+----------------------------------------------------------------+
|                     Zone 0 (Incomp. Fluid)                     |
+----------------------------------------------------------------+
|  Outer_Iter|  Inner_Iter|      rms[P]|      rms[U]|      rms[V]|
+----------------------------------------------------------------+
|           0|           0|   -4.799717|  -19.870540|  -32.000000|
|           0|          10|   -5.421646|   -4.859176|   -5.558343|
|           0|          20|   -6.200459|   -5.584293|   -6.120761|
|           0|          30|   -6.852188|   -6.205093|   -6.958953|
|           0|          40|   -7.502751|   -6.854100|   -8.034484|
|           0|          50|   -8.316190|   -7.662838|   -8.492639|
|           0|          60|   -9.153994|   -8.509430|   -9.696622|
|           0|          70|  -10.119472|   -9.498203|  -10.117162|
|           0|          80|  -11.035958|  -10.448171|  -11.143732|
|           0|          90|  -11.613994|  -10.982943|  -11.842820|
|           0|         100|  -12.264740|  -11.616077|  -12.556728|
|           0|         104|  -12.684964|  -12.046580|  -12.778620|
+-----------------------------------------------------------------------------+
|                              Zone 1 (Structure)                             |
+-----------------------------------------------------------------------------+
|  Outer_Iter|  Inner_Iter|      rms[U]|      rms[R]|      rms[E]|    VonMises|
+-----------------------------------------------------------------------------+
|           0|           0|   -1.172239|   -2.720505|   -4.519976|  2.0796e+03|
|           0|           1|   -1.818490|    1.181466|   -1.921389|  2.0398e+03|
|           0|           2|   -2.637505|    0.417532|   -3.589310|  2.1346e+03|
|           0|           3|   -2.582883|   -1.193130|   -5.577934|  1.9673e+03|
|           0|           4|   -3.571091|   -1.385185|   -7.138344|  1.9576e+03|
|           0|           5|   -3.760354|   -2.702330|   -9.178542|  1.9592e+03|
|           0|           6|   -4.723581|   -3.572916|  -11.185106|  1.9596e+03|
|           0|           7|   -6.588695|   -5.625140|  -15.057476|  1.9596e+03|
|           0|           8|  -10.508431|   -9.374250|  -22.787668|  1.9596e+03|
|           0|           9|  -16.135784|  -11.615447|  -28.539041|  1.9596e+03|
+----------------------------------------------------------------+
|                        Multizone Summary                       |
+----------------------------------------------------------------+
|  Outer_Iter| avg[bgs][0]| avg[bgs][1]|MinVolume[0]|DeformIter[0|
+----------------------------------------------------------------+
|           0|   -0.298306|   -2.057930|  8.8212e-10|           0|

...

+----------------------------------------------------------------+
|                     Zone 0 (Incomp. Fluid)                     |
+----------------------------------------------------------------+
|  Outer_Iter|  Inner_Iter|      rms[P]|      rms[U]|      rms[V]|
+----------------------------------------------------------------+
|          23|           0|  -16.031295|  -15.634452|  -15.943223|
|          23|          10|  -16.975566|  -16.340396|  -17.434490|
+-----------------------------------------------------------------------------+
|                              Zone 1 (Structure)                             |
+-----------------------------------------------------------------------------+
|  Outer_Iter|  Inner_Iter|      rms[U]|      rms[R]|      rms[E]|    VonMises|
+-----------------------------------------------------------------------------+
|          23|           0|  -11.932854|  -11.641052|  -26.043863|  1.7015e+03|
|          23|           1|  -15.380609|  -11.613595|  -28.521836|  1.7015e+03|
|          23|           2|  -15.998092|  -11.631016|  -28.517418|  1.7015e+03|
|          23|           3|  -15.999487|  -11.665152|  -28.602409|  1.7015e+03|
|          23|           4|  -15.833821|  -11.653692|  -28.591287|  1.7015e+03|
|          23|           5|  -15.421288|  -11.637929|  -28.570815|  1.7015e+03|
+----------------------------------------------------------------+
|                        Multizone Summary                       |
+----------------------------------------------------------------+
|  Outer_Iter| avg[bgs][0]| avg[bgs][1]|MinVolume[0]|DeformIter[0|
+----------------------------------------------------------------+
|          23|  -11.422397|   -9.137915|  8.7498e-10|          44|
```

where it can be observed that the multizone summary corresponds to the non-relaxed case presented first, and each of the subproblems are converged to a very high accuracy level.

### References
$$^1$$ Sanchez, R. (2018), A coupled adjoint method for optimal design in fluid-structure interaction problems with large displacements, _PhD thesis, Imperial College London_, DOI: [10.25560/58882](https://doi.org/10.25560/58882)

$$^2$$ Matthies H. G. and  Steindorf J. (2002), Partitioned but strongly coupled iteration schemes fornonlinear fluid–structure interaction, _Computers & Structures, 80(27–30):199–1999_.

### Attribution

If you are using this content for your research, please kindly cite the following reference in your derived works:

Sanchez, R. _et al._ (2018), [Coupled Adjoint-Based Sensitivities in Large-Displacement Fluid-Structure Interaction using Algorithmic Differentiation](https://spiral.imperial.ac.uk/handle/10044/1/51023), _Int J Numer Meth Engng, Vol 111, Issue 7, pp 1081-1107_. DOI: [10.1002/nme.5700](https://doi.org/10.1002/nme.5700)

<dl>
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>
<br />
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
</dl>

