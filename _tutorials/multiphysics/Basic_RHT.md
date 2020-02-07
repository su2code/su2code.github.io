---
title: Radiative Heat Transfer (RHT) in Laminar Buoyancy-Driven Cavity
permalink: /tutorials/Basic_RHT/
written_by: rsanfer
for_version: 7.0.2
revised_by: ransfer
revision_date: 2020-02-06
revised_version: 7.0.2
solver: INC_NAVIER_STOKES
requires: SU2_CFD
complexity: basic
follows: Inc_Laminar_Cavity
---

### Goals

This tutorial couples SU2's incompressible fluid solver with a one-equation Radiative Heat Transfer (RHT) model. Upon its completion, the user will be familiar with the following capabilities of SU2:
- Steady, 2D, laminar, incompressible, Navier-Stokes equations with an FDS convective scheme
- P1 model: 1-equation Radiative Heat Transfer model
- Two-way coupling of convective and radiative heat transfer

In this tutorial, we use a very similar problem definition as for the [Laminar Buoyancy-driven Cavity](../Inc_Laminar_Cavity) tutorial, a 1x1 m cavity in 2D with opposing hot and cold vertical walls and insulated horizontal walls. In this case, the media is participating, which means it absorbs part of the energy emitted by the hot and cold walls in form of radiation, and this absorption will have an impact on the overall behaviour of the flow. The properties of the test case are shown next:

![ProblemSetup1](../multiphysics/images/rht1.png)

### Resources

You can find the resources for this tutorial in the folder [multiphysics/radiation](https://github.com/su2code/Tutorials/blob/feature_radiation/multiphysics/radiation) of the [Tutorials repository](https://github.com/su2code/Tutorials). Please download the [config file](https://github.com/su2code/Tutorials/blob/feature_radiation/multiphysics/radiation/config_radiation.cfg) and the [mesh file](https://github.com/su2code/Tutorials/blob/feature_radiation/multiphysics/radiation/mesh_radiation.su2).

### Background 

SU2 adopts a P1 model for the simulation of Radiative Heat Transfer. The P1 model focuses on the integral magnitudes of the infinite-dimensional RTE equation, and works under the assumption that the energy distribution is linearly isotropic$$^1$$. In residual form, the P1 equation computes the radiative energy $$E$$ as

$$ 
	\mathscr{R}(E) = \nabla \cdot \mathbf{F}^{r}(E) + \kappa (E - \langle I_b \rangle) = 0,
$$

where the radiative flux is 

$$ 	
	\mathbf{F}^{r}(E) =  \left( \frac{-1}{3(\kappa + \sigma_s)} \nabla E \right),
$$

$$\kappa$$ and $$\sigma_s$$ are, respectively, the absorption and scattering coefficient, and $$\langle I_b \rangle$$ is the first moment of the blackbody intensity in an absorbing and emitting gray medium$$^2$$.

#### Mesh Description

The cavity is discretized with an structured mesh using 50 nodes in the horizontal and vertical boundaries, for a total of 2500 rectangular elements. The nodes are concentrated towards the boundary regions to adequately capture the boundary layer. The boundary conditions are as follows: 

![ProblemSetup2](../multiphysics/images/rht2.png)

#### Configuration File Options

We start the tutorial by definining the problem as an incompressible, Navier Stokes simulation

```
SOLVER = INC_NAVIER_STOKES
```

and we set the properties for the flow as defined in the goals section of this tutorial. More detail can be found in the [Laminar Buoyancy-driven Cavity](../Inc_Laminar_Cavity) tutorial.

```
INC_DENSITY_MODEL= VARIABLE
INC_ENERGY_EQUATION = YES
INC_DENSITY_INIT= 0.00597782417156  
INC_VELOCITY_INIT= ( 1.0, 0.0, 0.0 )
INC_TEMPERATURE_INIT= 288.15
INC_NONDIM = DIMENSIONAL

FLUID_MODEL= INC_IDEAL_GAS
SPECIFIC_HEAT_CP= 1004.703
MOLECULAR_WEIGHT= 28.96

VISCOSITY_MODEL= CONSTANT_VISCOSITY
MU_CONSTANT= 1.716e-5

CONDUCTIVITY_MODEL= CONSTANT_CONDUCTIVITY
KT_CONSTANT= 0.0246295028571

BODY_FORCE= YES
BODY_FORCE_VECTOR= ( 0.0, -9.81, 0.0 )

MARKER_HEATFLUX= ( upper, 0.0, lower, 0.0 )
MARKER_ISOTHERMAL= ( left, 461.04, right, 115.26 )
```

This tutorial focuses on the incorporation of Radiative effects to the incompressible Navier-Stokes solver in SU2. We first need to define the radiative model of choice. At the time of writing, the only available model is the P1 1-equation model, but the structure of SU2 has been defined to facilitate the implementation of new models.

```
RADIATION_MODEL = P1
```

Then, the properties of the model are set. For this example, there is no scattering defined, while the absorption coefficient is 0.1

```
ABSORPTION_COEFF = 0.1
SCATTERING_COEFF = 0.0
```

Next, we set the emissivity of the boundaries, where only the vertical walls have been considered to be emissive:

```
MARKER_EMISSIVITY = ( left, 1.0, right, 1.0 )
```

The last step is defining the maximum CFL for the diffussive P1 equation, which does not necessarily have to be the same as for the flow equations. In this case, the P1 equation is stable for a CFL = 1E5

```
CFL_NUMBER_RAD = 1E5
```

It only remains to set the solution method for the flow equations, where the CFL number is limited to 100 for stability

```
NUM_METHOD_GRAD= WEIGHTED_LEAST_SQUARES
CONV_NUM_METHOD_FLOW= FDS
MUSCL_FLOW= YES
SLOPE_LIMITER_FLOW= NONE
TIME_DISCRE_FLOW= EULER_IMPLICIT
CFL_NUMBER= 100
```

The convergence of the problem is controlled using

```
INNER_ITER= 2000

CONV_CRITERIA = RESIDUAL
CONV_FIELD = RMS_PRESSURE, RMS_VELOCITY-X, RMS_TEMPERATURE
CONV_RESIDUAL_MINVAL = -8
```

And, finally, the output of the problem is set. We can also output the convergence of the P1 equation using the keyword ```RMS_RAD_ENERGY```

```
SCREEN_OUTPUT = (INNER_ITER, RMS_PRESSURE, RMS_VELOCITY-X, RMS_TEMPERATURE, RMS_RAD_ENERGY)

OUTPUT_FILES = (RESTART, PARAVIEW)
SOLUTION_FILENAME = solution_rad
RESTART_FILENAME = restart_rad
VOLUME_FILENAME = radiation_tutorial

TABULAR_FORMAT = CSV
CONV_FILENAME= history
```

### Running SU2

Follow the links provided to download the [config](https://github.com/su2code/Tutorials/blob/feature_radiation/multiphysics/radiation/config_radiation.cfg) and [mesh](https://github.com/su2code/Tutorials/blob/feature_radiation/multiphysics/radiation/mesh_radiation.su2) files.

Execute the code with the standard command

```
SU2_CFD config_radiation.cfg
```

which will show the following convergence history:

```
Simulation Run using the Single-zone Driver
+----------------------------------------------------------------+
|  Inner_Iter|      rms[P]|      rms[U]|      rms[T]|  rms[E_Rad]|
+----------------------------------------------------------------+
|           0|   -4.566528|  -19.960693|    0.498633|    1.150738|
|           1|   -4.802575|   -4.203141|    0.590760|    0.916037|
|           2|   -4.802134|   -4.671948|    0.371239|    0.841595|
|           3|   -4.860542|   -5.097286|    0.290456|    0.766761|
|           4|   -5.125438|   -5.076119|    0.212441|    0.717057|
|           5|   -5.414242|   -5.426825|    0.115330|    0.682917|
|           6|   -5.644717|   -5.533804|   -0.188125|    0.655063|
|           7|   -5.591365|   -5.450852|   -0.476124|    0.634548|
|           8|   -5.659326|   -5.447890|   -0.654348|    0.617676|
|           9|   -5.808779|   -5.522011|   -0.809558|    0.605703|
|          10|   -5.913957|   -5.579328|   -0.984125|    0.594388|

...
|        1176|  -13.565946|  -13.985971|   -7.947333|   -5.654825|
|        1177|  -13.571295|  -13.991320|   -7.952680|   -5.660154|
|        1178|  -13.576645|  -13.996671|   -7.958032|   -5.665530|
|        1179|  -13.581994|  -14.002019|   -7.963378|   -5.670843|
|        1180|  -13.587344|  -14.007371|   -7.968731|   -5.676236|
|        1181|  -13.592692|  -14.012719|   -7.974075|   -5.681530|
|        1182|  -13.598042|  -14.018070|   -7.979430|   -5.686941|
|        1183|  -13.603390|  -14.023418|   -7.984772|   -5.692217|
|        1184|  -13.608740|  -14.028770|   -7.990128|   -5.697647|
|        1185|  -13.614087|  -14.034116|   -7.995468|   -5.702903|
|        1186|  -13.619438|  -14.039469|   -8.000826|   -5.708353|

```

The code is stopped as soon as the values of ```rms[P]```, ```rms[U]``` and ```rms[T]``` are below the convergence criteria set in the config file. 

```
All convergence criteria satisfied.
+-----------------------------------------------------------------------+
|      Convergence Field     |     Value    |   Criterion  |  Converged |
+-----------------------------------------------------------------------+
|                      rms[P]|      -13.6194|          < -8|         Yes|
|                      rms[U]|      -14.0395|          < -8|         Yes|
|                      rms[T]|      -8.00083|          < -8|         Yes|
```

From the convergence, it can be observed that the convective part of the problem converges quickly, however the energy equation is more stiff due to the quartic dependence of the radiative energy on the flow temperature. The resultant radiative energy field is shown next

![FSI Results](../multiphysics/images/rht3.png)

#### Assessing the radiation effects

We can easily turn off the radiation model to assess the effects of incorporating the RHT effects to the calculation. It is only necessary to select ```NONE``` as the radiation model

```
RADIATION_MODEL = NONE
```

Running the case now, the convergence to the required level is faster

```
+---------------------------------------------------+
|  Inner_Iter|      rms[P]|      rms[U]|      rms[T]|
+---------------------------------------------------+
|           0|   -4.566528|  -19.960693|    0.498633|
|           1|   -4.802575|   -4.203141|    0.590593|
|           2|   -4.802249|   -4.671488|    0.370967|
|           3|   -4.860553|   -5.096879|    0.291130|
|           4|   -5.129303|   -5.068037|    0.205752|
|           5|   -5.423720|   -5.416774|    0.099057|
|           6|   -5.623784|   -5.512461|   -0.198612|
|           7|   -5.475529|   -5.390245|   -0.456552|
|           8|   -5.502776|   -5.326692|   -0.630527|
|           9|   -5.665078|   -5.403656|   -0.805833|
|          10|   -5.772144|   -5.469751|   -0.987757|

...

|         747|  -13.526578|  -14.055709|   -7.916489|
|         748|  -13.535008|  -14.064139|   -7.924919|
|         749|  -13.543438|  -14.072569|   -7.933349|
|         750|  -13.551869|  -14.080999|   -7.941779|
|         751|  -13.560299|  -14.089429|   -7.950209|
|         752|  -13.568729|  -14.097859|   -7.958640|
|         753|  -13.577160|  -14.106289|   -7.967070|
|         754|  -13.585590|  -14.114719|   -7.975500|
|         755|  -13.594020|  -14.123149|   -7.983930|
|         756|  -13.602450|  -14.131579|   -7.992360|
|         757|  -13.610881|  -14.140010|   -8.000790|

```

We can compare the temperature field in the case with radiation (left) versus the case without radiation (right). The latter corresponds to the [Laminar Buoyancy-driven Cavity](../Inc_Laminar_Cavity) for ```Ra = 1.0E06```. It can be observed how the radiated case has an average temperature which is notably higher that in the non-absorbing case.

![RHT Results2](../multiphysics/images/rht4.png)

The temperature field has also an impact in the velocity fields, which are compared next for the cases with (left) and without radiation (right). 

![RHT Results3](../multiphysics/images/rht5.png)

### References
$$^1$$ Frank,  M., _et al._ (2006), Partial moment entropy approximation to radiative heat transfer. _Journal of Computational Physics 218(1),  1–18._ DOI: [10.1016/j.jcp.2006.01.038](https://doi.org/10.1016/j.jcp.2006.01.038)

$$^2$$ Jensen, K., _et al._ (2007), On various modeling approachesto radiative heat transfer in pool fires. _Combustion and Flame 148(4), 263–279._ DOI: [10.1016/j.combustflame.2006.09.008](https://doi.org/10.1016/j.combustflame.2006.09.008)

### Attribution

If you are using this content for your research, please kindly cite the following reference in your derived works:

Sanchez, R. _et al._ (2020), Adjoint-based sensitivity analysis in high-temperaturefluid flows with participating media, _(Submitted to) Modeling, Simulation and Optimization in the Health- and Energy-Sector, SEMA SIMAI SPRINGER SERIES_

<dl>
This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>
<br />
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
</dl>

