---
title: Convective Schemes
permalink: /docs_v7/Convective-Schemes/
---

This page lists the convective schemes available in SU2 and their associated options, it is not meant as a detailed theory guide but some application guidance is given nonetheless.
The options listed here do not apply to the high order DG solver.

---

## Content ##

- [Introduction](#intro)
- [Compressible Flow](#compressible-flow)
  - [Central schemes](#compressible-central)
  - [Upwind schemes](#compressible-upwind)
- [Incompressible Flow](#incomp-flow)
  - [Central schemes](#incomp-central)
  - [Upwind schemes](#incomp-upwind)
- [Turbulence Equations](#turbulence)

---

## Introduction ##

Convective schemes are used in the FVM discretization of convective fluxes through the faces of the dual-grid control volumes.
They are selected via option `CONV_NUM_METHOD_FLOW` and fall under the two broad categories of central and upwind.
Central schemes tend to be more robust whereas second order upwind schemes can be more accurate (i.e. less dissipative).
To achieve second order upwind schemes need to be used with MUSCL reconstruction (`MUSCL_FLOW = YES`), see the "gradients and limiters" page for the MUSCL-related options.

## Compressible Flow ##

| Solver | Version | 
| --- | --- |
| `EULER`, `NAVIER_STOKES`, `RANS` | 7.0.0 |

### Central Schemes ###

- `JST`: Jameson-Schmidt-Turkel scheme with scalar dissipation defined by the second and fourth order dissipation coefficients in option `JST_SENSOR_COEFF = (2nd, 4th)` the default values are 0.5 and 0.02 respectively;
- `JST-KE`: Equivalent to `JST` with 0 fourth order coefficient (computational effort is reduced as solution Laplacians no longer need to be computed);
- `LAX-FRIEDRICH`: The simplest of central schemes with a first order dissipation term specified via `LAX_SENSOR_COEFF` (the default is 0.15), this scheme is the most stable and least accurate due to its very dissipative nature.

Option `CENTRAL_JACOBIAN_FIX_FACTOR` (default value 4.0) affects all central schemes, in implicit time marching it improves the numerical properties of the Jacobian matrix so that higher CFL values can be used.

### Upwind Schemes ###

The following table lists the available upwind schemes for compressible flow and what secondary options apply to each one.

| Scheme \ Option                                 | `ROE_KAPPA` | `ENTROPY_FIX_COEFF` | `ROE_LOW_DISSIPATION` | `USE_ACCURATE_FLUX_JACOBIANS` | `MIN/MAX_ROE_TURKEL_PREC` |
| --- | --- | --- | --- | --- | --- |
| `ROE` - Classic Roe scheme                      |      X      |          X          |           X           |                               |                           |
| `L2ROE` - Low dissipation Low Mach Roe          |      X      |          X          |                       |                               |                           |
| `LMROE` - Rieper's Low Mach Roe scheme          |      X      |          X          |                       |                               |                           |
| `TURKEL_PREC` - Row with Turkel preconditioning |             |                     |                       |                               |             X             |
| `AUSM`                                          |             |                     |                       |                               |                           |
| `AUSMPLUSUP` - AUSM+up                          |             |                     |                       |               X               |                           |
| `AUSMPLUSUP2` - AUSM+up2                        |             |                     |                       |               X               |                           |
| `SLAU`                                          |             |                     |           X           |               X               |                           |
| `SLAU2`                                         |             |                     |           X           |               X               |                           |
| `HLLC`                                          |      X      |                     |                       |                               |                           |
| `CUSP`                                          |             |          X          |                       |                               |                           |
| `MSW` - Modified Steger-Warming scheme          |             |                     |                       |                               |                           |

- `ROE_KAPPA`, default 0.5, constant that multiplies the left and right state averages;
- `ENTROPY_FIX_COEFF`, default 0.001, puts a lower bound on dissipation by limiting the minimum convective Eigenvalue to a fraction of the speed of sound;
- `ROE_LOW_DISSIPATION`, default `NONE`, methods to reduce dissipation where certain conditions are verified, `FD` (wall distance based), `NTS` (Travin and Shur), `FD_DUCROS` and `NTS_DUCROS` as before plus Ducros' shock sensor;
- `USE_ACCURATE_FLUX_JACOBIANS`, default `NO`, if set to `YES` accurate flux Jacobians are used instead of Roe approximates, slower on a per iteration basis but in some cases allows much higher CFL values to be used;
- `MIN/MAX_ROE_TURKEL_PREC`, defaults 0.01 and 0.2, reference Mach numbers for Turkel preconditioning.

## Incompressible Flow ##

| Solver | Version | 
| --- | --- |
| `INC_EULER`, `INC_NAVIER_STOKES`, `INC_RANS` | 7.0.0 |

### Central Schemes ###



### Upwind Schemes ###



## Turbulence Equations ##

| Solver | Version | 
| --- | --- |
| `RANS`, `INC_RANS` | 7.0.0 |

Only one method is currently available: `SCALAR_UPWIND` which must be selected via option `CONV_NUM_METHOD_TURB`.
This method does not have any special parameters.

