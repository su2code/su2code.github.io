---
title: Convective Schemes
permalink: /docs_v7/Convective-Schemes/
---

This page lists the convective schemes available in SU2 and their associated options, it is not meant as a detailed theory guide but some application guidance is given nonetheless.
The options listed here do not apply to the high order DG solver.

---

- [Introduction](#introduction)
- [Compressible Flow](#compressible-flow)
  - [Central Schemes](#central-schemes)
  - [Upwind Schemes](#upwind-schemes)
- [Incompressible Flow](#incompressible-flow)
  - [Central Schemes](#central-schemes-1)
  - [Upwind Schemes](#upwind-schemes-1)
- [Turbulence Equations](#turbulence-equations)

---

## Introduction ##

Convective schemes are used in the FVM discretization of convective fluxes through the faces of the dual-grid control volumes.
They are selected via option `CONV_NUM_METHOD_FLOW` and fall under the two broad categories of central and upwind.
Central schemes tend to be more robust whereas second order upwind schemes can be more accurate (i.e. less dissipative).
To achieve second-order in space, upwind schemes need to be used with MUSCL reconstruction (`MUSCL_FLOW = YES`), see the [Slope Limiters and Shock Resolution](/docs_v7/Slope-Limiters-and-Shock-Resolution) page for the MUSCL-related options.

**Note:** MUSCL options have no effect on central schemes or on coarse multigrid levels in general.

## Compressible Flow ##

| Solver | Version | 
| --- | --- |
| `EULER`, `NAVIER_STOKES`, `RANS` | 7.0.0 |

### Central Schemes ###

- `JST` - Jameson-Schmidt-Turkel scheme with scalar dissipation defined by the second and fourth order dissipation coefficients in option `JST_SENSOR_COEFF = (2nd, 4th)` the default values are 0.5 and 0.02 respectively. This scheme offers a good compromise between accuracy and robustness but it will over predict viscous drag contributions in low-Re meshes.
- `JST_KE` - Equivalent to `JST` with 0 fourth order coefficient (the computational effort is slightly reduced as solution Laplacians no longer need to be computed);
- `JST_MAT` - Jameson-Schmidt-Turkel scheme with matrix dissipation, the classical dissipation term is scaled by the flux Jacobian with the minimum Eigenvalue limited by `ENTROPY_FIX_COEFF` (0.05-0.2 is recommended, larger means more numerical dissipation). This scheme gives better viscous drag predictions on low-Re meshes than `JST`.
- `LAX-FRIEDRICH` - The simplest of central schemes with a first order dissipation term specified via `LAX_SENSOR_COEFF` (the default is 0.15), this scheme is the most stable and least accurate due to its very dissipative nature.

The option `CENTRAL_JACOBIAN_FIX_FACTOR` (default value 4.0) affects all central schemes.
In implicit time marching it improves the numerical properties of the Jacobian matrix so that higher CFL values can be used.
To maintain CFL at lower-than-default values of dissipation coefficients, a higher factor should be used.
`JST_MAT` benefits from higher values (~8.0).

All compressible central schemes support vectorization (`USE_VECTORIZATION= YES`) with no robustness downsides, see the build instructions for how to tune the compilation for maximum vectorization performance.

**Note:** The Lax-Friedrich scheme is always used on coarse multigrid levels when any central scheme is selected.

### Upwind Schemes ###

- `ROE` - Classic Roe scheme;
- `L2ROE` - Low dissipation Low Mach Roe (L^2 Roe);
- `LMROE` - Rieper's Low Mach Roe;
- `TURKEL_PREC` - Roe scheme with Turkel preconditioning;
- `AUSM` - Advection Upstream Splitting Method;
- `AUSMPLUSUP` - AUSM+up, revised Mach and pressure splittings;
- `AUSMPLUSUP2` - AUSM+up2, uses an alternative pressure flux formulation;
- `SLAU` - Simple Low dissipation AUSM scheme;
- `SLAU2` - SLAU with the alternative pressure flux formulation;
- `HLLC` - Harten-Lax-van Leer-Contact;
- `CUSP` - Convective Upwind Split Pressure;
- `MSW` - Modified Steger-Warming.

Some of the schemes above have tunning parameters or accept extra options, the following table lists those options and indicates to which schemes they apply (if a scheme does not appear on the table, no options apply to it).

| Option \ Scheme                   | `ROE` | `L2ROE` | `TURKEL_PREC` | `AUSMPLUSUP[2]` | `SLAU[2]` | `HLLC` | `CUSP` |
| --------------------------------- | ----- | ------- | ------------- | --------------- | --------- | ------ | ------ |
| **`ROE_KAPPA`**                   |   X   |    X    |       X       |                 |           |   X    |        |
| **`ENTROPY_FIX_COEFF`**           |   X   |    X    |       X       |                 |           |        |    X   |
| **`ROE_LOW_DISSIPATION`**         |   X   |         |               |                 |     X     |        |        |
| **`USE_ACCURATE_FLUX_JACOBIANS`** |       |         |               |        X        |     X     |        |        |
| **`MIN/MAX_ROE_TURKEL_PREC`**     |       |         |       X       |                 |           |        |        |
| **`USE_VECTORIZATION`**           |   X   |         |               |                 |           |        |        |

- `ROE_KAPPA`, default 0.5, constant that multiplies the left and right state sum;
- `ENTROPY_FIX_COEFF`, default 0.001, puts a lower bound on dissipation by limiting the minimum convective Eigenvalue to a fraction of the speed of sound. Increasing it may help overcome convergence issues, at the expense of making the solution sensitive to this parameter.
- `ROE_LOW_DISSIPATION`, default `NONE`, methods to reduce dissipation in regions where certain conditions are verified, `FD` (wall distance based), `NTS` (Travin and Shur), `FD_DUCROS` and `NTS_DUCROS` as before plus Ducros' shock sensor;
- `USE_ACCURATE_FLUX_JACOBIANS`, default `NO`, if set to `YES` accurate flux Jacobians are used instead of Roe approximates, slower on a per iteration basis but in some cases allows much higher CFL values to be used and therefore faster overall convergence;
- `MIN_ROE_TURKEL_PREC` and `MAX_ROE_TURKEL_PREC`, defaults 0.01 and 0.2 respectively, reference Mach numbers for Turkel preconditioning;
- `USE_VECTORIZATION`, default `NO`, if `YES` use the vectorized (SSE, AVX, or AVX512) implementation which is faster but may be less robust against initial solution transients.

**Note:** Some schemes are not compatible with all other features of SU2, the AUSM family and CUSP are not compatible with unsteady simulations of moving grids, non-ideal gases are only compatible with the standard Roe and HLLC schemes.

## Incompressible Flow ##

| Solver | Version | 
| --- | --- |
| `INC_EULER`, `INC_NAVIER_STOKES`, `INC_RANS` | 7.0.0 |

### Central Schemes ###

`JST` and `LAX-FRIEDRICH` are available with low speed preconditioning, the afforementioned 1st, 2nd, and 4th order dissipation coefficients apply to these schemes but the `CENTRAL_JACOBIAN_FIX_FACTOR` option does not.

### Upwind Schemes ###

`FDS` - Flux Difference Splitting with low speed preconditioning, this scheme does not have tuning parameters.

## Turbulence Equations ##

| Solver | Version | 
| --- | --- |
| `RANS`, `INC_RANS` | 7.0.0 |

Only one method is currently available: `SCALAR_UPWIND` which must be selected via option `CONV_NUM_METHOD_TURB`.
This method does not have any special parameters.

