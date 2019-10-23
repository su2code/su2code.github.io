---
title: Linear Solvers and Preconditioners
permalink: /docs/Linear-Solvers-and-Preconditioners/
---

Linear solvers (and preconditioners) are used in implicit (pseudo)time integration schemes (any option with "IMPLICIT" or "DUAL-TIME" in the name).
This page lists the available options and provides guidance on how to setup the linear solvers for best results.
As the numerical properties of the linear systems vary significantly with application, and even with application-specific options, a "one size fits all" default setting is not available.

---

## Content ##

- [Option List](#option-list)
  - [Linear Solvers](#linear-solvers)
  - [Linear Preconditioners](#linear-preconditioners)
  - [External Solvers](#external-solvers)
- [Setup Advice](#setup-advice)
  - [Fluid Simulations](#fluid-simulations)
  - [Structural Simulations](#structural-simulations)
  - [Mesh Deformation](#mesh-deformation)
  - [Discrete Adjoint](#discrete-adjoint)

---

## Option List ##

### Linear Solvers ###

The following options accept a type of linear solver:
- `LINEAR_SOLVER`: Main option for direct/primal and continuous adjoint problems. The linear solver used by all physics solvers of the zone associated with the configuration file.
- `DISCADJ_LIN_SOLVER`: Main option for discrete adjoint problems.
- `DEFORM_LINEAR_SOLVER`: Linear solver for elasticity-based mesh deformation.

In most applications the linear solver tolerance is defined by option `LINEAR_SOLVER_ERROR`, and the maximum number of iterations by `LINEAR_SOLVER_ITER`.
Heat applications use `LINEAR_SOLVER_ERROR_HEAT` and `LINEAR_SOLVER_ITER_HEAT` instead.
Similarly mesh deformation uses `DEFORM_LINEAR_SOLVER_ERROR` and `DEFORM_LINEAR_SOLVER_ITER`.

The available types of (iterative) linear solver are:

| Type | Description | Notes |
| --- | --- | --- |
| `FGMRES` | Flexible Generalized Minimum Residual | This is the default option. |
| `RESTARTED_FGMRES` | Restarted `FGMRES` (reduces memory footprint) | Restart frequency controlled by `LINEAR_SOLVER_RESTART_FREQUENCY`. |
| `BCGSTAB` | Bi-Conjugate Gradient Stabilized | See setup advice. |
| `CONJUGATE_GRADIENT` | Conjugate Gradient | Use it only for elasticy, or mesh deformation problems (i.e. symmetric/self-adjoint). |
| `SMOOTHER` | Iterative smoothing with the selected preconditioner. | Relaxation factor controlled by `LINEAR_SOLVER_SMOOTHER_RELAXATION` |

**Note**: The `SMOOTHER` option is not available for mesh deformation applications (as it stands little chance of doing any smoothing).

### Linear Preconditioners ###

Analogously to the above options, the following accept a type of linear preconditioner:
- `LINEAR_SOLVER_PREC`
- `DISCADJ_LIN_PREC`
- `DEFORM_LINEAR_SOLVER_PREC`

The available types of preconditioner are:

| Type | Description | Notes |
| --- | --- | --- |
| `JACOBI` | Block Jacobi preconditioner. | Lowest computational cost and effectiveness. |
| `LU_SGS` | Lower-Upper Symmetric Gauss-Seidel. | Lowest memory footprint, intermediate cost and effectiveness. |
| `ILU` | Incomplete Lower Upper factorization with connectivity-based sparse pattern. | Highest cost and effectiveness, fill-in is controlled by ``. |
| `LINELET` | Line-implicit Jacobi preconditioner. | Tridiagonal systems solved along grid lines normal to walls, Jacobi elsewhere. |

**Note**: Only `JACOBI` and `ILU` are compatible with discrete adjoint solvers.

### External Solvers ###

Version 7 introduces experimental support for the direct sparse solver [PaStiX](https://gforge.inria.fr/projects/pastix/) see detailed options in `TestCases/pastix_support/readme.txt`

## Setup Advice ##

For tiny problems with ~10k nodes almost any solver will do, these settings are more important for medium-large problems.

**Disclaimer**: Your own experience is more important that this advice, but if you have yet to gain some this should help.

### Fluid Simulations ###

Fastest overall convergence is usually obtained by using the highest CFL number for which the flow solver is stable, and the linear systems still reasonably economic to solve.
For example central schemes like JST allow very high CFL values, however at some point (100-400 for RANS grids) the linear systems become too expensive to solve and performance starts decreasing.
Upwind schemes are less plagued by this as stability considerations usually put a lower limit on CFL, and the linear systems are better conditioned to begin with.
Opposite to CFL, the linear solver tolerance should be the lowest possible for which the flow solver is still stable, usually in the 0.05-0.001 range, having to go lower is often a sign of poor mesh quality resulting in localized high residuals.
The maximum number of iterations should allow the linear solver to converge, however the memory footprint of `FGMRES` (which should be your default solver) is proportional to that number, if that becomes a problem you can switch to `RESTARTED_FGMRES` or `BCGSTAB`, the latter may perform better for stiff systems like those resulting from central schemes at high CFL.
High CFL cases will usually require the `ILU` preconditioner, while low CFL cases may run better with `LU_SGS` as even if more linear iterations are required `LU_SGS` does not have a setup cost.
The concept of high/low CFL is somewhat case dependent, for RANS meshes (stretched close to walls) and upwind schemes high is greater than 100 and low less than 20, central schemes move the limits down, time domain and less stretched meshes (e.g. for Euler or Navier-Stokes) move the limits up.

### Structural Simulations ###

At scale these become the most difficult systems to solve in SU2 due to their elliptical nature, they are easier for time-domain problems nonetheless always start with the `ILU` preconditioner.
A much larger number of linear iterations is required `RESTARTED_FGMRES` or `CONJUGATE_GRADIENT` should be used.
For linear elasticity an error of at most 1e-8 should be targeted, for nonlinear elasticity 1e-6 may suffice as multiple iterations are performed.
If the solution becomes challenging, and the problem is 2D or you have RAM to spare, consider using the external direct solvers.

### Mesh Deformation ###

For elasticity-based mesh deformation the advice is the same as for structural simulations.

### Discrete Adjoint ###

Discrete adjoint applications respond well to high CFL values the advice is generally the same as for the primal counterpart (fluid or structural).
The `ILU` preconditioner should be used as `JACOBI` will only give an advantage for very low CFL values.

