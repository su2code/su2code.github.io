---
title: Solver Setup
permalink: /docs_v7/Solver-Setup/
---

This is a basic introduction on how to set up a simulation using SU2. We distinguish between single-zone computations and multi-zone computations. The following considers a single zone only. For an explanation on multi-zone problems, continue with [Basics of Multi-Zone Computations](/docs_v7/Multizone).

Three different types of mathematical problems can be solved in SU2. The type of problem to be solved is specified on the config file by the `MATH_PROBLEM` field. The three options are:
`DIRECT`: also refered to as primal, flow solver.?
`DISCRETE_ADJOINT`: a discrete adjoint methodology based on Automatic Differentiation.
`CONTINUOUS_ADJOINT`: a continuous adjoint methodology based on Automatic Differentiation.

See the [Software Components](/docs_v7/Software-Components/) documentation to determine which software module is required for each problem.

---

- [Defining the Problem](#defining-the-problem)
  - [Restarting the simulation](#restarting-the-simulation)
- [Controlling the simulation](#controlling-the-simulation)
  - [Time-dependent Simulation](#time-dependent-simulation)
  - [Steady-state Simulation](#steady-state-simulation)
  - [Setting convergence criteria](#setting-convergence-criteria)
    - [Residual](#residual)
    - [Coefficient](#coefficient)
  
---

# Defining the Problem #

| Solver | Version | 
| --- | --- |
| `ALL`| 7.2.0 |

## Direct ##

SU2 is capable of dealing with different kinds of physical problems. The kind of problem is defined by choosing a solver using the `SOLVER` option. The list of possible values and a description can be found in the following table:

| Option Value | Problem | Type |
|---|---|---|
|`EULER` | **Euler's equation** |Finite-Volume method |
|`NAVIER_STOKES` | **Navier-Stokes' equation** | Finite-Volume method |
|`RANS` | **Reynolds-averaged Navier-Stokes' equation** | Finite-Volume method|
|`INC_EULER` | **Incompressible Euler's equation** | Finite-Volume method |
|`INC_NAVIER_STOKES` | **Incompressible Navier-Stokes' equation** | Finite-Volume method|
|`INC_RANS` | **Incompressible Reynolds-averaged Navier-Stokes' equation** | Finite-Volume method|
|`HEAT_EQUATION_FVM` | **Heat equation** | Finite-Volume method |
|`ELASTICITY` | **Equations of elasticity** | Finite-Element method |
|`FEM_EULER` | **Euler's equation** | Discontinuous Galerkin FEM |
|`FEM_NAVIER_STOKES`| **Navier-Stokes' equation** | Discontinuous Galerkin FEM |
|`MULTIPHYSICS` | Multi-zone problem with different solvers in each zone | - |

### Turbulence modeling ###

The turbulence model to be used for RANS and INC_RANS is specified in the config file by the `KIND_TURB_MODEL` option. The current options are `SA` for the Spalart-Allmaras and `SST` for the Mentor Shear Stress Transport.

Different corrections or variations are implemented for each turbulence model which can be simultaneously used. These are specified in the `TURB_MODEL_CORRECTIONS` option. The default is `NONE` standing for the standalone version.

```
% ------------------------- Turbulence modeling -------------------------------%
%
% Turbulence model
KIND_TURB_MODEL= SA
%
% Turbulence model corrections (NONE, SA-EDW, SA-NOFT2, SA-COMP, SA-NEG, SA-QCR2000, SST-SUST)
TURB_MODEL_CORRECTIONS= SA-EDW, SA-NEG
```

#### Spalart-Allamaras ####
The single transported Spalart-Allmaras variable $\tilde{\nu}$ is initialized with the value at the farfield or inlet boundary. As suggested in the literature, the value there is computed as $\tilde{\nu}/\nu = \mathrm{turb2lam}$. In SU2 the free-stream Spalart-Allmaras variable to kinematic laminar viscosity ratio, $\mathrm{turb2lam}$, is controlled by the `FREESTREAM_NU_FACTOR` option. The default value is $\tilde{\nu}/\nu = 3.0$ avoiding laminar solutions.

In the following the implemented model versions in SU2 are listed:
`SA-EDW` refers to the so-called Edwards modification.
`SA-NOFT2` refers to the modification where the $f_{t2}$ term is set to zero, i.e., $c_{t3} = 0$.
`SA-COMP` refers to the Mixing Layer Compressibility modification.
`SA-NEG` refers to the negative Spalart-Allmaras modification.
`SA-QCR2000` refers to the Quadratic Constitutive Relation modification, 2000 version.

An extension of SU2 includes and hybrid turbulence model: the Spalart-Allmaras original model with Detached-Eddy Simulation (DES) modification. Refer to Eduardo Moina's thesis? Four different techniques are currently implemented:

`SA_DES` Detached-Eddy Simulation
`SA_DDES` Delayed Detached-Eddy Simulation
`SA_ZDES` Zonal Detached-Eddy Simulation
`SA_EDDES` Enhanced Detached-Eddy Simulation

In the config file the hybrid RANS/LES model is specified by the `HYBRID_RANSLES` field. The DES constant can be parametrized by the field `DES_CONST`, with 0.65 as default.

#### Menter’s k-omega SST Model ####
As initial conditions, the values of are initialized at all grid point with the farfield values. The farfield conditions for $k$ and $omega$ are
The freestream turbulence kinetic energy value is set by the `FREESTREAM_TURBULENCEINTENSITY` field. The default value 0.05 which corresponds to a 5%.

The freestream dissipation is set by the `FREESTREAM_TURB2LAMVISCRATIO` field. The same definition as for  `FREESTREAM_TURBULENCEINTENSITY` applies.

##### Limitations of k and omega #####
To increase robustness and prevent negative values, a hard-coded upper and lower limit are set for each turbulent variable:
```
// turbulence kinetic energy
lowerlimit = 1.0e-10;
upperlimit = 1.0e10;

// 
lowerlimit = 1.0e-4;
upperlimit = 1.0e15;
```
Further, by the model definition in the farfield region there is no production of $k$ nor $\omega$ while destruction still takes place. Consequently the turbulence quantities typically decay on their way from the farfield boundary to the airfoil. In order to prevent the non-physical decay <!--of the turbulence variables--> in SU2 there are implemented to two approaches:
- Sustaining terms: it consists on the introduction of additional source terms in the turbulence model equations compensating the destruction terms in the farfield flow. This approach is activated by using the modified version of the SST moodel, `SST-sust`.
- Floor values: this approach is equivalent to setting the lowerlimit to the farfield values in the upstream region of an airfoil. The floor values are implemented in the form of fixed values. This correction can be activated with the following parameters in the config file:
`TURB_FIXED_VALUES= YES`
`TURB_FIXED_VALUES_DOMAIN= -1.0`
To determine those grid points where the correction should be applied, we compare the dot product of the normalized freestream velocity vector and the grid point coordinates. For those points which dot product result is lower than the specified `TURB_FIXED_VALUES_DOMAIN` value, the turbulence quantities are just set to the farfield values there. Note that although the Spalart-Allmaras turbulence model does not suffer from a decaying turbulence variable, the floor values limitation can also be employed. <!--The implementation is analogous to the strong boundary conditions, setting the turbulent residual equal zero at those locations.-->

### Foward mode of AD ###
The forward mode of AD capability allows to compute the forward derivatives (see [Advanced AD Techniques](/docs_v7/Advanced-AD-Techniques)) of an specified function with respect to a registered variable/s. If multiple design variables are registered as input, the output will consist on the accumulation. The function to be differentiated can be any of the variables specified as `COEFFICIENT` in the `SetHistoryOutputFields` functions of the flow output classes. To get the derivative, one just needs to write D_< string group name > in the `HISTORY_OUTPUT` field from the config file. Addioiniallty, the field `DIRECT_DIFF` specifies the variable to be registered as an input. In SU2 it is possible to register almost any variable. Currently SU2 has implemented the following variables:

`D_MACH` Freestream Mach number
`D_AOA` angle of attack
`D_PRESSURE`  freestream pressure
`D_TEMPERATURE` freestream temperature
`D_DENSITY` freestream density
`D_TURB2LAM` freestream ratio of turbulent to laminar viscosity
`D_SIDESLIP` sideslip angle
`D_VISCOSITY` freestream laminar viscosity
`D_REYNOLDS` freestream Reynolds number
`D_DESIGN` design??
`D_YOUNG` Young's modulus
`D_POISSON` Poisson's ratio
`D_RHO` solid density (inertial)
`D_RHO_DL` density for dead loads
`D_EFIELD` electric field

The execution of this capability is done by the module `SU2_CFD_DIRECTDIFF`. See the [Software Components](/docs_v7/Software-Components/) for further details.

## Discrete adjoint ##

SU2 can compute the variation of an objective function with respect to the design surface shape control points. To get the list of objective functions available in SU2 we address to https://github.com/su2code/SU2/blob/master/Common/include/option_structure.hpp ENUM_OBJECTIVE and Objective_Map to see the proper nomenclature for the config file. DON'T KNOW HOW TO ADDRESS PROPERLY?

The objective function value can be scaled by a weighting factor. This value can be specified in the `OBJECTIVE_WEIGHT` field on the config file.

## Continuous adjoint ##

Same as the discrete adjoint but using the continuous adjoint approach :)

Every solver has its specific options and we refer to the tutorial cases for more information. However, the basic controls detailed in the remainder of this page are the same for all solvers and mathematical problems.

# Restarting the simulation #

| Solver | Version | 
| --- | --- |
| `ALL`| 7.2.0 |

A simulation can be restarted from a previous computation by setting `RESTART_SOL=YES`. If it is a time-dependent problem, additionally `RESTART_ITER` must be set to the time iteration index you want to restart from:

```
% ------------------------- Solver definition -------------------------------%
%
% Type of solver 
SOLVER= EULER
%
% Restart solution (NO, YES)
RESTART_SOL= NO
%
% Iteration number to begin unsteady restarts (used if RESTART_SOL= YES)
RESTART_ITER= 0
%
```

<!-- ## Direct and Adjoint ##
The option `MATH_PROBLEM` defines whether the direct problem (`DIRECT`, default) or the adjoint problem should be solved. For the latter you have the choice between the continuous adjoint solver (`CONTINUOUS_ADJOINT`) or the discrete adjoint solver (`DISCRETE_ADJOINT`). Note that the discrete adjoint solver requires the `*_AD` binaries (i.e. SU2 must be [compiled](/docs_v7/Build-SU2-From-Source) with the `-Denable-autodiff=true` flag). Not all problems have a corresponding adjoint solver (yet). See below for a compatibility list:

| `SOLVER` | Discrete Adjoint Solver available | Continuous Adjoint Solver available |
| --- | --- | --- |
| `EULER` | yes | yes |
| `NAVIER_STOKES`| yes | yes |
| `RANS`| yes | yes (using frozen viscosity) |
| `INC_EULER` | yes | yes |
| `INC_NAVIER_STOKES`| yes | yes |
| `INC_RANS`| yes | yes (using frozen viscosity) |
| `HEAT_EQUATION_FVM`| yes| no| 
| `ELASTICITY` | yes | no|
| `FEM_EULER`| no | no |
| `FEM_NAVIER_STOKES`| no | no | -->

---

# Controlling the simulation #

| Solver | Version | 
| --- | --- |
| `ALL`| 7.2.0 |

A simulation is controlled by setting the number of iterations the solver should run (or by setting a convergence critera). The picture below depicts the two types of iterations we consider.

![Types of Iteration](../../docs_files/unst_singlezone.png)


SU2 makes use of an outer time loop to march through the physical time, and of an inner loop which is usually a pseudo-time iteration or a (quasi-)Newton scheme. The actual method used depends again on the specific type of solver.

## Courant-Friedrichs-Lewy number ##

The Courant-Friedrichs-Lewy number is specified by the `CFL_NUMBER` parameter. It is possible to adapt locally its magnitude on each pseudo-iteration according to the solver residual convergence. To enable this capability, the `CFL_ADAPT` must be set to `YES`.

The option `CFL_ADAPT_PARAM` controls the adaptative CFL number, which parameters are: factor-down, factor-up, CFL min value, CFL max value and acceptable linear solver convergence.

If an adaptative CFL number is used, the initial CFL number for the finest grid is set to <CFL min value>. The local CFL number increases by <factor-up> until <CFL max value> if the solution rate of change is not limited, and acceptable linear convergence is achieved. It is reduced by <factor-down> if rate is limited, there is not enough linear convergence, or the nonlinear residuals are stagnant and oscillatory. It is reset back to <CFL min value> when linear solvers diverge, or if nonlinear residuals increase too much.

No idea about the acceptable <linear solver convergence> parameter?

## Time-dependent Simulation ##

| Solver | Version | 
| --- | --- |
| `ALL`| 7.2.0 |

To enable a time-dependent simulation set the option `TIME_DOMAIN` to `YES` (default is `NO`). There are different methods available for certain solvers which can be set using the `TIME_MARCHING` option. For example for any of the FVM-type solvers a first or second-order dual-time stepping (`DUAL_TIME_STEPPING-1ST_ORDER`/`DUAL_TIME_STEPPING-2ND_ORDER`) method or a conventional time-stepping method (`TIME_STEPPING`) can be used.

```
% ------------------------- Time-dependent Simulation -------------------------------%
%
TIME_DOMAIN= YES
%
% Time Step for dual time stepping simulations (s)
TIME_STEP= 1.0
%
% Total Physical Time for dual time stepping simulations (s)
MAX_TIME= 50.0
%
% Number of internal iterations 
INNER_ITER= 200
%
% Number of time steps
TIME_ITER= 200
%
```

The solver will stop either when it reaches the maximum time (`MAX_TIME`) or the maximum number of time steps (`TIME_ITER`), whichever event occurs first. Depending on the `TIME_MARCHING` option, the solver might use an inner iteration loop to converge each physical time step. The number of iterations within each time step is controlled using the `INNER_ITER` option.

## Steady-state Simulation ##

| Solver | Version | 
| --- | --- |
| `ALL`| 7.2.0 |

A steady-state simulation is defined by using `TIME_DOMAIN=NO`, which is the default value if the option is not present. In this case the number of iterations is controlled by the option `ITER`.

**Note:** To make it easier to switch between steady-state, time-dependent and multizone simulations, the option `INNER_ITER` can also be used to specify the number of iterations. If both options are present, `INNER_ITER` has precedence.

## Setting convergence criteria ##

| Solver | Version | 
| --- | --- |
| `ALL`| 7.2.0 |

Despite setting the maximum number of iterations, it is possible to use a convergence criterion so that the solver will stop when it reaches a certain value of a residual or if variations of a coefficient are below a certain threshold. To enable a convergence criterion use the option `CONV_FIELD` to set an output field that should be monitored. The list of possible fields depends on the solver. Take a look at [Custom Output](/docs_v7/Custom-Output/) to learn more about output fields. Depending on the type of field (residual or coefficient) there are two types of methods:

### Steady-state Residual ###
If the field set with `CONV_FIELD` is a residual, the solver will stop if it is smaller than the value set with 
`CONV_RESIDUAL_MINVAL` option. Example:

```
% ------------------- Residual-based Convergence Criteria -------------------------%
%
CONV_FIELD= RMS_DENSITY
%
%
% Min value of the residual (log10 of the residual)
CONV_RESIDUAL_MINVAL= -8
%
```

### Steady-state Coefficient ###
If the field set with `CONV_FIELD` is a coefficient, a Cauchy series approach is applied. A Cauchy element is defined as the relative difference of the coefficient between two consecutive iterations. The solver will stop if the average over a certain number of elements (set with `CONV_CAUCHY_ELEMS`) is smaller than the value set with `CONV_CAUCHY_EPS`. The current value of the Cauchy coefficient can be written to screen or history by adding the `CAUCHY` field to the `SCREEN_OUTPUT` or `HISTORY_OUTPUT` option (see [Custom Output](/docs_v7/Custom-Output/)). Example:

```
% ------------------ Coefficient-based Convergence Criteria -----------------------%
%
CONV_FIELD= DRAG
%
%
% Number of elements to apply the criteria
CONV_CAUCHY_ELEMS= 100
%
% Epsilon to control the series convergence
CONV_CAUCHY_EPS= 1E-10
%
```
For both methods the option `CONV_STARTITER` defines when the solver should start monitoring the criterion.

### Time-dependent Coefficient ###
In a time-dependend simulation we have two iterators, `INNER_ITER` and `TIME_ITER`. The convergence criterion for the `INNER_ITER` loop is the same as in the steady-state case. 
For the `TIME_ITER`, there are convergence options implemented for the case of a periodic flow. The convergence criterion uses the so-called windowing approach, (see [Custom Output](/docs_v7/Custom-Output/)). The convergence options are applicable  only for coefficients.
To enable time convergence, set `WINDOW_CAUCHY_CRIT=YES` (default is `NO`). The option `CONV_WINDOW_FIELD` determines the output-fields to be monitored. 
Typically, one is interested in monitoring time-averaged coefficients, e.g `TAVG_DRAG`.
 Analogously to the steady state case, 
the solver will stop, if the average over a certain number of elements (set with `CONV_WINDOW_CAUCHY_ELEMS`) is smaller than the value set with `CONV_WINDOW_CAUCHY_EPS`.
The current value of the Cauchy coefficient can be written to screen or history using the flag `CAUCHY` (see [Custom Output](/docs_v7/Custom-Output/)).
The option `CONV_WINDOW_STARTITER` determines the numer of iterations, the solver should wait to start moniotring, after `WINDOW_START_ITER` has passed. `WINDOW_START_ITER` determines the iteration, when the (time dependent) outputs are averaged, (see [Custom Output](/docs_v7/Custom-Output/)).
The window-weight-function used is determined by the option `WINDOW_FUNCTION`

```
% ------------------ Coefficient-based Windowed Time Convergence Criteria -----------------------%
%
% Activate the windowed cauchy criterion
WINDOW_CAUCHY_CRIT = YES
%
% Specify convergence field(s)
CONV_WINDOW_FIELD= (TAVG_DRAG, TAVG_LIFT)
%
% Number of elements to apply the criteria
CONV_WINDOW_CAUCHY_ELEMS= 100
%
% Epsilon to control the series convergence
CONV_WINDOW_CAUCHY_EPS= 1E-3
%
% Number of iterations to wait after the iteration specified in  WINDOW_START_ITER.
CONV_WINDOW_STARTITER = 10
%
% Iteration to start the windowed time average
WINDOW_START_ITER = 500
%
% Window-function to weight the time average. Options (SQUARE, HANN, HANN_SQUARE, BUMP), SQUARE is default.
WINDOW_FUNCTION = HANN_SQUARE
```

**Note:** The options `CONV_FIELD` and `CONV_WINDOW_FIELD` also accept a list of fields, e.g. `(DRAG, LIFT,...)`, to monitor. The solver will stop if all fields reach their respective stopping criterion (i.e. the minimum value for residuals or the cauchy series threshold for coefficients as mentioned above).
