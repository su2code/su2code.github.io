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


## Incompressible Flow ##

| Solver | Version | 
| --- | --- |
| `INC_EULER`, `INC_NAVIER_STOKES`, `INC_RANS` | 7.0.0 |


## Turbulence Equations ##

| Solver | Version | 
| --- | --- |
| `RANS`, `INC_RANS` | 7.0.0 |

Only one method is currently available: `SCALAR_UPWIND` which must be selected via option `CONV_NUM_METHOD_TURB`.
This method does not have any special parameters.

