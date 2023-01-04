---
title: Physical Definition
permalink: /docs_v7/Physical-Definition/
redirect_from: /docs/Physical-Definition/
---

The physical definition of a case includes the definition of the free-stream, the reference values and the non-dimensionalization. 
SU2 offers different ways of setting and computing this definition. This document gives a short overview on the config options and their physical relation.

---

- [Reference Values](#reference-values)
- [Free-Stream Definition (Compressible)](#free-stream-definition-compressible)
  - [Thermodynamic State](#thermodynamic-state)
  - [Mach Number and Velocity](#mach-number-and-velocity)
  - [Reynolds Number and Viscosity](#reynolds-number-and-viscosity)
  - [Non-Dimensionalization](#non-dimensionalization)
- [Free-Stream Definition (Thermochemical Nonequilibrium)](#free-stream-thermochemical-nonequilibrium)
  - [Chemical Composition and Mass Fractions](#chemical-composition-and-mass-fractions)
  - [Thermodynamic State](#thermodynamic-state)
  - [Mach Number and Velocity](#mach-number-and-velocity)
  - [Reynolds Number and Viscosity](#reynolds-number-and-viscosity)
  - [Non-Dimensionalization](#non-dimensionalization)
- [Flow Condition (Incompressible)](#flow-condition-incompressible)
  - [Thermodynamic and Gauge Pressure](#thermodynamic-and-gauge-pressure)
  - [Initial State and Non-Dimensionalization](#initial-state-and-non-dimensionalization)
- [Turbulence Models](#turbulence-models)
  - [Spalart-Allmaras (SA)](#spalart-allmaras-model)
  - [Shear Stress Transport (SST)](#shear-stress-transport)
- [Transition Models](#transition-models)

---

## Reference Values ##

| Solver | Version |
| --- | --- |
| `EULER`, `NAVIER_STOKES`, `RANS`, `INC_EULER`, `INC_NAVIER_STOKES`, `INC_RANS`, `FEM_EULER`, `FEM_NAVIER_STOKES` | 7.0.0 |

The following table depicts the reference values used by most of the solvers in SU2. The highlighted variables vary depending on the actual solver and the user input.


| Variable | Unit | Reference |
|---|---|---|
| Length | $$m$$ | $$l_{ref} = 1$$ |
| **Density** | $$\frac{kg}{m^3}$$ | $$\rho_{ref}$$ (based on user input) |
| **Velocity** | $$\frac{m}{s}$$ | $$v_{ref}$$ (based on user input)|
| **Temperature** | $$K$$ | $$T_{ref}$$ (based on user input) |
| **Pressure** | $$Pa$$ | $$p_{ref}$$ (based on user input) |
| Viscosity | $$\frac{kg}{ms}$$ | $$\mu_{ref} = \rho_{ref}v_{ref}l_{ref}$$ |
| Time | $$s$$ | $$t_{ref} = \frac{l_{ref}}{v_{ref}}$$ |
| Heatflux | $$\frac{W}{m^2}$$ | $$Q_{ref} = \rho_{ref}v^3_{ref} $$ |
| Gas Constant | $$\frac{m^2}{s^2 K}$$ | $$R_{ref} = \frac{v^2_{ref}}{T_{ref}}$$|
| Conductivity | $$\frac{W}{mK}$$ | $$k_{ref} = \mu_{ref}R_{ref}$$ |
| Force | $$N$$ | $$ F_{ref} = \rho_{ref}v^2_{ref}l^2_{ref} $$ |


## Free-Stream Definition (Compressible) ##

| Solver | Version |
| --- | --- |
| `EULER`, `NAVIER_STOKES`, `RANS`,`FEM_EULER`, `FEM_NAVIER_STOKES` | 7.0.0 |

The physical definition for the compressible solvers in SU2 based around the definition of the free-stream. The free-stream values are not only used as boundary conditions for the `MARKER_FAR` option, but also for initialization and non-dimensionalization. That means even if you don't have any farfield BCs in your problem, it might be important to prescribe physically meaningful values for the options.

### Thermodynamic State ###

The thermodynamic state of the free-stream is defined by the pressure $$p_{\infty}$$, the density $$\rho_{\infty}$$ and the temperature $$T_{\infty}$$. Since these quantities are not independent, only two of these values have to be described and the third one can be computed by an equation of state, depending on the fluid model used. There are two possible ways implemented that can be set using `FREESTREAM_OPTION`:

- `TEMPERATURE_FS` (default): Density $$\rho_{\infty}$$ is computed using the specified pressure $$p_{\infty}$$ (`FREESTREAM_PRESSURE`) and temperature $$T_{\infty}$$ (`FREESTREAM_TEMPERATURE`).
- `DENSITY_FS`: Temperature $$T_{\infty}$$ is computed using the specified pressure $$p_{\infty}$$ (`FREESTREAM_PRESSURE`) and density $$\rho_{\infty}$$ (`FREESTREAM_DENSITY`). 

### Mach Number and Velocity ###

The free-stream velocity $$v_{\infty}$$ is always computed from the specified Mach number $$Ma_{\infty}$$ (`MACH_NUMBER`) and the computed thermodynamic state. The flow direction is based on the angle of attack (`AOA`) and the side-slip angle (`SIDESLIP_ANGLE`, for 3D).

### Reynolds Number and Viscosity ###

If it is a viscous computation, by default the pressure $$p_{\infty}$$ will be recomputed from a density $$\rho_{\infty}$$ that is found from the specified Reynolds number $$Re$$ (`REYNOLDS_NUMBER`). Note that for an ideal gas this does not change the Mach number $$Ma_{\infty}$$ as it is only a function of the temperature $$T_{\infty}$$. If you still want to use the thermodynamic state for the free-stream definition, set the option `INIT_OPTION` to `TD_CONDITIONS` (default: `REYNOLDS`). In both cases, the viscosity is computed from the dimensional version of Sutherland's law or the constant viscosity (`FREESTREAM_VISCOSITY`), depending on the `VISCOSITY_MODEL` option.

### Non-Dimensionalization ###

For all schemes, as reference values for the density and temperature the free-stream values are used, i.e. $$ \rho_{ref} = \rho_{\infty}, T_{ref} = T_{\infty}$$. The reference velocity is based on the speed of sound defined by the reference state: $$v_{ref} = \sqrt{\frac{p_{ref}}{\rho_{ref}}}$$. The dimensionalization scheme can be set using the option `REF_DIMENSIONALIZATION` and defines how the reference pressure $$p_{ref}$$ is computed:

- `DIMENSIONAL`: All reference values are set to `1.0`, i.e. the computation is dimensional.
- `FREESTREAM_PRESS_EQ_ONE`: Reference pressure equals free-stream pressure, $$p_{ref} = p_{\infty}$$.
- `FREESTREAM_VEL_EQ_MACH`: Reference pressure is chosen such that the non-dimensional free-stream velocity equals the Mach number: $$p_{ref} = \gamma p_{\infty}$$.
- `FREESTREAM_VEL_EQ_ONE`: Reference pressure is chosen such that the non-dimensional free-stream velocity equals `1.0`: $$p_{ref} = Ma^2_{\infty} \gamma p_{\infty}$$.

## Free-Stream Definition (Thermochemical Nonequilibrium) ##

| Solver | Version |
| --- | --- |
| `EULER`, `NAVIER_STOKES`, `RANS`,`FEM_EULER`, `FEM_NAVIER_STOKES` | 7.0.0 |

The physical definition for the compressible solvers in SU2 based around the definition of the free-stream. The free-stream values are not only used as boundary conditions for the `MARKER_FAR` option, but also for initialization and non-dimensionalization. That means even if you don't have any farfield BCs in your problem, it might be important to prescribe physically meaningful values for the options.

### Thermodynamic State ###

The thermodynamic state of the free-stream is defined by the pressure $$p_{\infty}$$, the density $$\rho_{\infty}$$ and the temperature $$T_{\infty}$$. Since these quantities are not independent, only two of these values have to be described and the third one can be computed by an equation of state, depending on the fluid model used. There are two possible ways implemented that can be set using `FREESTREAM_OPTION`:

- `TEMPERATURE_FS` (default): Density $$\rho_{\infty}$$ is computed using the specified pressure $$p_{\infty}$$ (`FREESTREAM_PRESSURE`) and temperature $$T_{\infty}$$ (`FREESTREAM_TEMPERATURE`).
- `DENSITY_FS`: Temperature $$T_{\infty}$$ is computed using the specified pressure $$p_{\infty}$$ (`FREESTREAM_PRESSURE`) and density $$\rho_{\infty}$$ (`FREESTREAM_DENSITY`). 

### Mach Number and Velocity ###

The free-stream velocity $$v_{\infty}$$ is always computed from the specified Mach number $$Ma_{\infty}$$ (`MACH_NUMBER`) and the computed thermodynamic state. The flow direction is based on the angle of attack (`AOA`) and the side-slip angle (`SIDESLIP_ANGLE`, for 3D).

### Reynolds Number and Viscosity ###

If it is a viscous computation, by default the pressure $$p_{\infty}$$ will be recomputed from a density $$\rho_{\infty}$$ that is found from the specified Reynolds number $$Re$$ (`REYNOLDS_NUMBER`). Note that for an ideal gas this does not change the Mach number $$Ma_{\infty}$$ as it is only a function of the temperature $$T_{\infty}$$. If you still want to use the thermodynamic state for the free-stream definition, set the option `INIT_OPTION` to `TD_CONDITIONS` (default: `REYNOLDS`). In both cases, the viscosity is computed from the dimensional version of Sutherland's law or the constant viscosity (`FREESTREAM_VISCOSITY`), depending on the `VISCOSITY_MODEL` option.

### Non-Dimensionalization ###

For all schemes, as reference values for the density and temperature the free-stream values are used, i.e. $$ \rho_{ref} = \rho_{\infty}, T_{ref} = T_{\infty}$$. The reference velocity is based on the speed of sound defined by the reference state: $$v_{ref} = \sqrt{\frac{p_{ref}}{\rho_{ref}}}$$. The dimensionalization scheme can be set using the option `REF_DIMENSIONALIZATION` and defines how the reference pressure $$p_{ref}$$ is computed:

- `DIMENSIONAL`: All reference values are set to `1.0`, i.e. the computation is dimensional.
- `FREESTREAM_PRESS_EQ_ONE`: Reference pressure equals free-stream pressure, $$p_{ref} = p_{\infty}$$.
- `FREESTREAM_VEL_EQ_MACH`: Reference pressure is chosen such that the non-dimensional free-stream velocity equals the Mach number: $$p_{ref} = \gamma p_{\infty}$$.
- `FREESTREAM_VEL_EQ_ONE`: Reference pressure is chosen such that the non-dimensional free-stream velocity equals `1.0`: $$p_{ref} = Ma^2_{\infty} \gamma p_{\infty}$$.

## Flow Condition (Incompressible) ##

| Solver | Version |
| --- | --- |
| `INC_EULER`, `INC_NAVIER_STOKES`, `INC_RANS` | 7.0.0 |

The physical definition of the incompressible solvers is accomplished by setting an appropriate flow condition for initialization and non-dimensionalization. SU2 solves the [incompressible Navier-Stokes equations](/docs_v7/Theory/#incompressible-navier-stokes) in a general form allowing for variable density due to heat transfer through the low-Mach approximation (or incompressible ideal gas formulation). 

### Thermodynamic and Gauge Pressure ###

In the incompressible problem the thermodynamic pressure is decoupled from the governing equations and density is therefore only a function of temperature variations. The absolute value of the pressure is not important and any reference to the pressure $$p$$ is considered as the gauge value, i.e. it is zero-referenced against ambient air pressure, so it is equal to absolute pressure minus (an arbitrary) atmospheric pressure.   

### Initial State and Non-Dimensionalization ###

The initial state, i.e. the initial values of density $$\rho_0$$, velocity vector $$\bar{v}_{0}$$ and temperature $$T_0$$ are set with `INC_DENSITY_INIT`, `INC_VELOCITY_INIT` and `INC_TEMPERATURE_INIT`, respectively. The initial pressure $$p_0$$ is always set to `0.0`.

The reference values $$\rho_{ref}, T_{ref}, v_{ref}$$ equal the initial state values by default (or if `INC_NONDIM= INITIAL_VALUES`). If `INC_NONDIM` is set to `REFERENCE_VALUES` you can define different values for them using the options `INC_DENSITY_REF`, `INC_VELOCITY_REF` and `INC_TEMPERATURE_REF`. The reference pressure is always computed by $$p_{ref} = \rho_{ref}v^2_{ref}$$.

**Note:** The initial state is also used as boundary conditions for `MARKER_FAR`.

## Turbulence Models ##

| Solver | Version |
| --- | --- |
| `*_RANS` | 7.4.0 |

This section describes how to setup turbulence models for RANS simulations. Turbulence is activated using the option `KIND_SOLVER= RANS`, or `KIND_SOLVER= INC_RANS`
A turbulence model can then be selected via the option `KIND_TURB_MODEL`
Different submodels and parameters are specified via the different options listed below.
The turbulent Prandtl number can be modified with the option `PRANDTL_TURB` (the default is 0.9).

### Spalart-Allmaras (SA) ###

SU2 implements several versions and corrections of the SA model.
The model is selected using `KIND_TURB_MODEL= SA` and the modifications via the `SA_OPTIONS` list. If this list is empty, then SU2 defaults to `SA-noft2`.
The freestream and inlet conditions are specified via the option `FREESTREAM_NU_FACTOR= 3` (ratio of SA variable to freestream kinematic viscosity).

The following modifications are allowed (refer to [NASA's TMR](https://turbmodels.larc.nasa.gov/spalart.html) for further info):
- Versions:
  - `NEGATIVE` - Negative SA model.
  - `EDWARDS` - Edwards modification.
  - `BCM` - BCM transitional model.
  - `WITHFT2` - SA model **with** ft2 term, note that by default we omit this term.
- Corrections:
  - `QCR2000` - Quadratic contitutive relation used in the stress tensor.
  - `COMPRESSIBILITY` - Mixing layer compressibility correction.
  - `ROTATION` - Dacles-Mariani et al. rotation correction.

All the modifications can be combined with each other expect `NEGATIVE` and `EDWARDS`.
For example, to specify `SA-neg-R-comp-QCR2000` use `SA_OPTIONS= NEGATIVE, WITHFT2, ROTATION, COMPRESSIBILITY, QCR2000`.
**However, some combinations are not considered standard**, e.g. `SA-neg` should have the ft2 term, whereas `SA-noft2-Edwards` and `SA-noft2-BCM` should not have the ft2 term, and they are usually not combined with other corrections (see TMR for more details). To use non-standard combinations it is necessary to add `EXPERIMENTAL` to the option list, e.g. `SA_OPTIONS= NEGATIVE, BCM, EXPERIMENTAL`.

The rough wall correction is implicitly turned on by specifying roughness values for wall markers via the `WALL_ROUGHNESS` option.

### Shear Stress Transport (SST) ###

SU2 implements the "Standard" (1994) and 2003 versions of the SST model along with several modifications.

**Note:** Currently all versions are "modified" i.e. the turbulence kinetic energy (TKE) is not included in the viscous stress tensor.

The main model is selected using `KIND_TURB_MODEL= SST` and the version and modifications via the `SST_OPTIONS` list. If this list is empty SU2 defaults to the baseline 1994 model, `V1994m` (see warning below). The options allow for a version and a set of modifiers to the version. 
The freestream and inlet conditions are specified via the options `FREESTREAM_TURBULENCEINTENSITY= 0.05` (5%) and `FREESTREAM_TURB2LAMVISCRATIO= 10` (ratio of turbulent to laminar viscosity).

**Note:** The default values for these options are suitable for internal flows but may be too high for external aerodynamics problems.

The following modifications are allowed:
- Versions:
  - `V1994m` - SSTm **WARNING:** Our implementation has a small [inconsistency with the literature](https://github.com/su2code/SU2/issues/1551), which will be resolved in the next major SU2 update (i.e. version 8).
  - `V2003m` - SST-2003m (no known inconsistencies).
- Production modifications:
  - `VORTICITY` - Uses vorticity to compute the source term instead of strain-rate magnitude.
  - `KATO_LAUNDER` - Uses the Kato-Launder modification (vorticity times strain-rate).
  - `UQ` - Production is computed using a modified stress tensor for [uncertainty quantification](https://su2code.github.io/tutorials/UQ_NACA0012/). **Note** with this modification TKE is always included in the stress tensor.
- Corrections:
  - `SUSTAINING` - SST with controlled decay.
  - Curvature corrections are currently not implemented.

Modifications from each of these three groups can be combined, for example `SST_OPTIONS= V2003m, VORTICITY, SUSTAINING`

## Transition Models ##

| Solver | Version |
| --- | --- |
| `*_RANS` | 7.5.0 |

This section describes how to setup transition models for RANS simulations. Transition is activated using the option `KIND_SOLVER= RANS`, or `KIND_SOLVER= INC_RANS` together with a choice of `KIND_TRANS_MODEL` (different from `NONE`).
Currently, the only valid option for `KIND_TRANS_MODEL` is `LM`, for Langtry-Menter transition models.
Different submodels and correlations are then specified via `LM_OPTIONS` (for example `LM_OPTIONS= LM2015, MENTER_LANGTRY`).

The following modifications are allowed:
- Versions:
  - `LM2015` - Correction to include stationary crossflow instabilities. It has to be used only in 3D problems. The RMS of roughness used in this model has to be set through the separate option `HROUGHNESS`.
- Correlations (only one can be specified):
  - `MALAN` - This is the default correlation when the LM model is coupled with the `SA` turbulence model.
  - `SULUKSNA` - This should be used only if the `SST` model is used. It should require a formulation of the Re_theta_t correlation that omits the pressure gradient parameter, however it is not clear. 
  - `KRAUSE` - This correlation should be used for hypersonic flows. Its implementation at the moment is unclear due to inconsistencies in the literature.
  - `KRAUSE_HYPER` - This correlation should be used for hypersonic flows. Its implementation at the moment is unclear due to inconsistencies in the literature.
  - `MEDIDA` - Designed for `SA` turbulence model. Has problems when dealing with separation induced transition.
  - `MEDIDA_BAEDER` - Designed for `SA` turbulence model. Has problems when dealing with separation induced transition.
  - `MENTER_LANGTRY` - This is the default correlation when the LM model is coupled with the `SST` turbulence model.
