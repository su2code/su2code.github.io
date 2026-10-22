---
title: "Hybrid RANS/LES (DES)"
permalink: /docs_v7/Hybrid-RANS-LES/
---

Hybrid RANS/LES methods run a RANS model in attached boundary layers and a large-eddy simulation (LES) away from the walls. In LES, the mesh and the time step resolve the large turbulent eddies, and the model only handles the small ones. Detached eddy simulation (DES) and its variants are the hybrid methods in SU2. Use them for massively separated, unsteady flows where URANS is not accurate enough and a full LES is too expensive.

For a step-by-step case setup, see [Setup Guide: Unsteady Flows and DES](../Setup-Guide-Unsteady-DES/). For the SA model itself, see [Turbulence Models](../Turbulence-Models/).

---

- [How DES works in SU2](#how-des-works-in-su2)
- [How to select it](#how-to-select-it)
  - [DES variant](#des-variant)
  - [DES length scale options](#des-length-scale-options)
  - [Low-dissipation convective scheme](#low-dissipation-convective-scheme)
  - [Stochastic backscatter model](#stochastic-backscatter-model)
  - [Time averages](#time-averages)
- [What SU2 does differently from the literature](#what-su2-does-differently-from-the-literature)
- [Equations and references](#equations-and-references)
- [Recommended use](#recommended-use)
- [Output fields](#output-fields)
- [Verification and test cases](#verification-and-test-cases)
- [Known limits](#known-limits)
- [Links](#links)

---

## How DES works in SU2

In SU2, all DES variants modify the Spalart-Allmaras (SA) model. The SA model uses the wall distance in its destruction term. DES replaces this distance with a *DES length scale*:

- Near the wall, the length scale is the wall distance. The model acts as RANS.
- Far from the wall, the length scale is `DES_CONST` times a local cell size. The model then acts as a subgrid model for LES.

The variants differ in two points: how they protect attached boundary layers from switching to LES, and how they measure the cell size.

The DES length scale is computed only in the SA solver (`CTurbSASolver::SetDES_LengthScale`). The SST solver never reads `HYBRID_RANSLES`. So in SU2 develop, DES needs `KIND_TURB_MODEL= SA`. SST-based DES variants are in open pull requests.

DES works with the compressible (`RANS`) and the incompressible (`INC_RANS`) solvers. Both pass the DES length scale and the LES sensor to the output.

## How to select it

### DES variant

Set the turbulence model to SA and pick a variant with `HYBRID_RANSLES`:

```
SOLVER= RANS
KIND_TURB_MODEL= SA
HYBRID_RANSLES= SA_DDES
DES_CONST= 0.65
TIME_DOMAIN= YES
```

| `HYBRID_RANSLES` | Method | Cell size used in LES mode |
|---|---|---|
| `NONE` (default) | No DES. The SA model runs as RANS or URANS. | – |
| `SA_DES` | Original DES (Spalart et al. 1997). Switches to LES wherever `DES_CONST` times the cell size is smaller than the wall distance. | Longest edge from the node |
| `SA_DDES` | Delayed DES (Spalart et al. 2006). A *shielding function* f_d keeps attached boundary layers in RANS mode. | Longest edge from the node |
| `SA_ZDES` | DDES with the vorticity-based cell size of the zonal DES (Deck 2012). | Cell size seen across the vorticity vector |
| `SA_EDDES` | DDES with the shear-layer-adapted cell size of Shur et al. (2015). Meant to switch faster from RANS to LES in separated shear layers. | Shear-layer-adapted size |

### DES length scale options

| Option | Default | What it does |
|---|---|---|
| `DES_CONST` | `0.65` | The DES constant. The LES length scale is `DES_CONST` times the cell size. |
| `LES_FILTER_WIDTH` | `-1.0` | If positive, SU2 uses this value as the cell size at every node, for all variants. It replaces the local cell size. Give it in mesh length units. A negative value uses the local cell size. |
| `ENFORCE_LES` | `NO` | `YES` sets the length scale to `DES_CONST` times the cell size everywhere, also near walls. The whole domain then runs as LES with an SA-based subgrid model. SU2 stops with an error if `HYBRID_RANSLES= NONE`. |

`LES_FILTER_WIDTH` and `ENFORCE_LES` are mainly for LES test problems, such as decaying isotropic turbulence.

### Low-dissipation convective scheme

Upwind schemes add numerical dissipation. In LES regions, this dissipation damps the resolved eddies. `ROE_LOW_DISSIPATION` blends the upwind dissipation with a central flux: full upwind in RANS regions, little upwind in LES regions.

| `ROE_LOW_DISSIPATION` | Blending sensor |
|---|---|
| `NONE` (default) | No blending. |
| `FD` | Based on the DDES shielding function f_d. Full upwind where f_d = 0 (RANS), down to 5% upwind where f_d = 1. |
| `NTS` | The sensor of Travin et al. (2002), as written in Xiao et al. (2012). Uses `DES_CONST`, the cell size and the eddy viscosity. |
| `FD_DUCROS` | `FD` plus the Ducros shock sensor: full upwind near shocks. |
| `NTS_DUCROS` | `NTS` plus the Ducros shock sensor, combined as in Xiao et al. (2015). |

Facts from the code:

- The blending acts only with `CONV_NUM_METHOD_FLOW= ROE`, `SLAU` or `SLAU2`. With any other scheme, SU2 ignores the option without a warning.
- The sensor is computed in the compressible Navier-Stokes solver (`CNSSolver::SetRoe_Dissipation`). The incompressible solver does not use this option.
- The minimum upwind fraction is fixed at 0.05 in the code. The Ducros threshold for `FD_DUCROS` is fixed at 0.65.
- `FD` computes its own f_d from the wall distance and the eddy viscosity. It does not need `HYBRID_RANSLES`.
- With the option on, the volume output gets the field `ROE_DISSIPATION`.

For incompressible LES regions, SU2 has the centered scheme `CONV_NUM_METHOD_FLOW= LD2` (low dissipation, low dispersion). It works only with the incompressible solver and a constant-density fluid. The backscatter test case uses it.

### Stochastic backscatter model

In the "grey area" just after separation, a DES has neither modeled nor resolved turbulence: the RANS eddy viscosity is gone and the resolved eddies have not grown yet. The stochastic backscatter model (Kok 2017) adds random forcing in LES regions to speed up the growth of resolved eddies. *Backscatter* means energy that flows from the small, modeled scales back to the large, resolved ones.

SU2 adds a random stress to the momentum equations. The random field comes from three extra equations (Langevin equations) for a random vector, solved together with the SA equation.

| Option | Default | What it does |
|---|---|---|
| `STOCHASTIC_BACKSCATTER` | `NO` | Turns the model on. Needs `HYBRID_RANSLES` other than `NONE` and a 3D mesh, else SU2 stops with an error. |
| `SBS_INTENSITY_COEFF` | `1.0` | Strength of the random stress. Must not be negative. |
| `SBS_TIMESCALE_COEFF` | `0.05` | Time scale coefficient of the Langevin equations. If `0` or less, SU2 does not solve them. It then uses a new, uncorrelated random field at every time step. |
| `SBS_LENGTHSCALE_COEFF` | `0.02` | Strength of the spatial smoothing of the random source. The smoothing length grows with this coefficient times the squared cell size. |
| `SBS_MAX_ITER_SMOOTH` | `100` | Maximum iterations of the smoothing. `0` turns smoothing off. |
| `SBS_FD_LOWER_THRESHOLD` | `0.9` | The model acts only where the LES sensor is above this value. |
| `SBS_SOURCE_NU_EQUATION` | `YES` | Also adds a random source to the SA equation, so that modeled and resolved energy stay in balance. |
| `SBS_RELAXATION_FACTOR` | `0.0` | If positive, the intensity ramps up from zero at the start (or restart) of the run. The ramp time is this factor times `REYNOLDS_LENGTH` divided by the free-stream speed. |
| `SBS_IN_BOX` | `NO` | `YES` limits the model to a box. |
| `SBS_BOX_BOUNDS` | none | The box: `( x_min, x_max, y_min, y_max, z_min, z_max )`. It has no default, so always set it with `SBS_IN_BOX= YES`. |
| `SBS_SOURCE_DIAGNOSTICS` | `NO` | Prints statistics of the smoothed random source on screen. |

Facts from the code:

- The model is part of the SA solver. With `SBS_TIMESCALE_COEFF` positive, the SA solver has 4 variables instead of 1: ν̃ and the three components of the random vector. The history output then has `RMS_STOCH_VAR-X`, `-Y` and `-Z`.
- The random numbers come from a hash of the global node index, the direction and the time step. A run gives the same random field for any number of MPI ranks.
- The smoothing is an implicit Laplacian filter solved with successive over-relaxation at the first inner iteration of each time step. SU2 prints its residual on screen at every time step. After smoothing, SU2 rescales the field to keep its variance.
- The box is set at the first time step of the run. It does not follow mesh motion.
- With backscatter on, SU2 does not apply the SA under-relaxation (the `MAX_UPDATE_SA` limit on the update of ν̃).

### Time averages

A DES result is a time average. In a time-domain run, add `TIME_AVERAGE` to `VOLUME_OUTPUT`:

```
VOLUME_OUTPUT= ( COORDINATES, SOLUTION, PRIMITIVE, DDES, VORTEX_IDENTIFICATION, TIME_AVERAGE )
WINDOW_START_ITER= 2000
```

- SU2 averages density, velocity, pressure and skin friction (`MEAN_*`), and computes the resolved Reynolds stresses (`UUPRIME`, `VVPRIME`, `UVPRIME`, ...) and `PPRIME`.
- With a turbulence model, it also averages the modeled Reynolds stresses (`MODELED_REYNOLDS_STRESS_*`). With backscatter, it averages the random stresses (`STOCHASTIC_REYNOLDS_STRESS_*`).
- The average starts at `WINDOW_START_ITER` and gives every time step the same weight. `WINDOW_FUNCTION` does not apply to the volume averages.
- SU2 updates the averages at every time step, not only when it writes a file.
- The averages are not read back from a restart file. A restarted run starts a new average. This is why `WINDOW_START_ITER` defaults to `RESTART_ITER` and must not be smaller.

History averages (`TAVG_*`) and the windowed Cauchy criterion are explained in the [unsteady setup guide](../Setup-Guide-Unsteady-DES/#time-averages-and-convergence-in-time).

## What SU2 does differently from the literature

All facts below are from `SU2_CFD/src/solvers/CTurbSASolver.cpp` (`SetDES_LengthScale`) unless stated.

**Cell size.** The papers define the DES cell size on cells, for example the largest cell dimension Δmax = max(Δx, Δy, Δz). SU2 is vertex-based. It uses the longest edge from the node to any neighbor node (`CPhysicalGeometry::SetMaxLength`). On a hexahedral mesh this is close to the largest cell dimension. On a tetrahedral or prismatic mesh, it is the longest edge.

**No low-Reynolds-number correction.** DDES (Spalart et al. 2006) multiplies the LES length scale by a function Ψ. Ψ stops the SA damping terms from reducing the subgrid viscosity when the eddy viscosity is small. SU2 computes Ψ (the variable `psi_2`) but never uses it. The LES length scale is always `DES_CONST` times the cell size.

**`SA_DES` sensor.** The LES sensor is a switch: 0 where the wall distance is smaller than the LES length scale, 1 elsewhere.

**`SA_ZDES` is not the full zonal method.** Deck (2012) describes a zonal method with several modes that the user assigns to regions. SU2 has one automatic mode: DDES with the vorticity-based cell size. The cell size per direction is the largest distance to a neighbor node along x, y and z. SU2 switches back to the longest-edge cell size where f_d < 0.99. Deck's mode 2 uses its own threshold for this switch (to be reviewed).

**`SA_EDDES` cell size.** Shur et al. (2015) project the cell vertices onto the plane normal to the vorticity. SU2 uses the edges from the node to its neighbors instead. It takes the absolute value of each edge component before the cross product with the vorticity direction. The vortex tilting measure is averaged over the node and its neighbors. SU2 uses the longest-edge cell size where f_d < 0.999. The other constants (F_min = 0.1, F_max = 1, a1 = 0.15, a2 = 0.3) are those of the paper.

**Shielding function.** `SA_DDES`, `SA_ZDES` and `SA_EDDES` use the DDES shielding function f_d with the constants 8 and 3 of the paper. The LES sensor output is f_d where the LES length scale is smaller than the wall distance, and 0 elsewhere.

**Roughness.** With DES on, the SA source term uses the DES length scale and ignores `WALL_ROUGHNESS`. The rough-wall boundary condition and the eddy viscosity still use it. See [Wall Treatment](../Wall-Treatment/#roughness-with-sa).

**Backscatter inside the SA equation.** Where the backscatter model is active (LES sensor above `SBS_FD_LOWER_THRESHOLD`), the SA source term uses fv1 = 1, fv2 = 0 and fw = 0 (`SU2_CFD/include/numerics/turbulent/turb_sources.hpp`). With fw = 0, the SA destruction term is switched off there. The random source added to the SA equation is limited to 5 times the production term.

**Backscatter energy estimate.** The random stress scales with an estimate of the subgrid kinetic energy, (eddy viscosity / DES length scale)². In the momentum equations, SU2 uses the dynamic eddy viscosity μt for this estimate (`SU2_CFD/src/numerics/flow/flow_diffusion.cpp`). In the SA equation and in the averaged output, it uses the kinematic eddy viscosity νt (to be reviewed).

## Equations and references

This page does not repeat the model equations. See the original papers:

- DES: P. R. Spalart, W.-H. Jou, M. Strelets, S. R. Allmaras, "Comments on the feasibility of LES for wings, and on a hybrid RANS/LES approach", *Advances in DNS/LES*, Greyden Press, 1997.
- DDES: P. R. Spalart et al., "A new version of detached-eddy simulation, resistant to ambiguous grid densities", *Theor. Comput. Fluid Dyn.* 20, 181–195, 2006. [doi:10.1007/s00162-006-0015-0](https://doi.org/10.1007/s00162-006-0015-0)
- ZDES: S. Deck, "Recent improvements in the Zonal Detached Eddy Simulation (ZDES) formulation", *Theor. Comput. Fluid Dyn.* 26, 523–550, 2012. [doi:10.1007/s00162-011-0240-z](https://doi.org/10.1007/s00162-011-0240-z)
- EDDES: M. L. Shur et al., "An enhanced version of DES with rapid transition from RANS to LES in separated flows", *Flow Turbul. Combust.* 95, 709–737, 2015. [doi:10.1007/s10494-015-9618-0](https://doi.org/10.1007/s10494-015-9618-0)
- NTS blending: A. Travin et al., "Physical and numerical upgrades in the detached-eddy simulation of complex turbulent flows", *Advances in LES of Complex Flows*, 239–254, 2002. [doi:10.1007/0-306-48383-1_16](https://doi.org/10.1007/0-306-48383-1_16)
- NTS form used in SU2: Z. Xiao et al., "Numerical dissipation effects on massive separation around tandem cylinders", *AIAA J.* 50(5), 1119–1136, 2012. [doi:10.2514/1.J051299](https://doi.org/10.2514/1.J051299)
- NTS with Ducros sensor: Z. Xiao et al., *Int. J. Heat Fluid Flow* 51, 138–150, 2015. [doi:10.1016/j.ijheatfluidflow.2014.10.007](https://doi.org/10.1016/j.ijheatfluidflow.2014.10.007)
- Stochastic backscatter: J. C. Kok, "A stochastic backscatter model for grey-area mitigation in detached eddy simulations", *Flow Turbul. Combust.* 99, 119–150, 2017. [doi:10.1007/s10494-017-9809-y](https://doi.org/10.1007/s10494-017-9809-y)
- SA model: [NASA Turbulence Modeling Resource, SA page](https://tmbwg.github.io/turbmodels/spalart.html).

## Recommended use

All advice in this section is general practice, not checked in SU2 (to be reviewed).

- **Variant.** Prefer `SA_DDES` or `SA_EDDES` over `SA_DES`. Plain DES can switch to LES inside an attached boundary layer if the mesh is fine along the wall. The flow can then separate because of the mesh (to be reviewed).
- **Mesh.** Run DES in 3D. Resolve the boundary layer as for RANS (y+ about 1, no wall functions). In the separated region, use nearly cubic cells: the cell size sets the LES filter. In the spanwise direction, the domain must be large enough to hold the largest eddies (to be reviewed).
- **Time step.** Choose a time step so that the convective CFL number, based on the local cell size and velocity, is about 1 or less in the LES region (to be reviewed).
- **Time marching.** Use `TIME_MARCHING= DUAL_TIME_STEPPING-2ND_ORDER`, as in the test cases. Converge the inner iterations by 2 to 3 orders per time step (to be reviewed).
- **Convective scheme.** Use a second-order scheme (`MUSCL_FLOW= YES`) without a slope limiter where there are no shocks. With `ROE`, `SLAU` or `SLAU2`, try `ROE_LOW_DISSIPATION= FD` or `NTS`. Add a `_DUCROS` variant if there are shocks (to be reviewed).
- **Statistics.** Run the start-up transient first. Then set `WINDOW_START_ITER` and average over many flow-through times. Check that the averages no longer change (to be reviewed).
- **Check the switch.** Plot `LES_SENSOR` and `DES_LENGTHSCALE`. Attached boundary layers should stay at sensor 0 (RANS). Separated regions should show sensor near 1 (LES).

## Output fields

| Group | Fields | When |
|---|---|---|
| `DDES` | `DES_LENGTHSCALE`, `WALL_DISTANCE`, `LES_SENSOR` | `HYBRID_RANSLES` is not `NONE` |
| `BACKSCATTER` | `STOCHSOURCE_X/Y/Z`, `ENERGY_BACKSCATTER_RATIO` | Backscatter on |
| `SOLUTION`, `RESIDUAL` | `STOCHVAR_X/Y/Z`, `RES_STOCHVAR_X/Y/Z` | Backscatter on with `SBS_TIMESCALE_COEFF` > 0 |
| `ROE_DISSIPATION` | `ROE_DISSIPATION` | Compressible solver with `ROE_LOW_DISSIPATION` set |
| `TIME_AVERAGE` | `MEAN_*`, `RMS_*`, `*PRIME`, `MODELED_REYNOLDS_STRESS_*`, `STOCHASTIC_REYNOLDS_STRESS_*` | Time-domain run |

Note: the `RMS_U`, `RMS_V`, ... fields hold the mean of the squared value (for example the mean of u²), not the root mean square. The fluctuations are in `UUPRIME`, `VVPRIME`, and so on.

The full list is in the [Output Fields Reference](../Output-Fields-Reference/).

## Verification and test cases

There is no verification case for DES in the [V&V section](/vandv/home/). The regression tests only check that the options run:

- [`TestCases/ddes/flatplate/ddes_flatplate.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/ddes/flatplate/ddes_flatplate.cfg): `SA_EDDES` on a 2D flat plate, compressible, `SLAU2`. A 2D flat plate is not a real DES case.
- [`TestCases/backscatter/backward_step/backwardStep.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/backscatter/backward_step/backwardStep.cfg): `SA_DDES` with stochastic backscatter in a box, incompressible, `LD2` scheme, periodic in the spanwise direction. It shows all `SBS_*` options and the `TIME_AVERAGE` output.

Background: [An Overview of DDES in SU2: Implementation and Recent Results](/documents/dev_meeting_2017/su2_dev_molina.pdf) (2017 developers meeting).

## Known limits

- **DES with SST runs as URANS, without a warning.** SU2 accepts `HYBRID_RANSLES` with `KIND_TURB_MODEL= SST`. The SST solver ignores it, and the run is plain URANS. The screen still prints the DES variant, and `DES_LENGTHSCALE` and `LES_SENSOR` are written as zero.
- **No check for steady runs.** SU2 does not stop if `HYBRID_RANSLES` is set with `TIME_DOMAIN= NO`. A steady DES has no physical meaning.
- **`ROE_LOW_DISSIPATION` is ignored** with schemes other than `ROE`, `SLAU` and `SLAU2`, and in the incompressible solver, without a warning.
- **Backscatter is 3D only** and needs the SA model.
- **Wall roughness is only partly used with DES** (see [Roughness](#what-su2-does-differently-from-the-literature)).
- **Time averages restart from zero** after a restart.

## Links

- [Setup Guide: Unsteady Flows and DES](../Setup-Guide-Unsteady-DES/)
- [Setup Guide: RANS External Aerodynamics](../Setup-Guide-RANS-External-Aero/)
- [Turbulence Models](../Turbulence-Models/)
- [Wall Treatment: Wall Functions and Roughness](../Wall-Treatment/)
- [Option Reference](../Option-Reference/)
- [Output Fields Reference](../Output-Fields-Reference/)
- [Markers and Boundary Conditions](../Markers-and-BC/)

---

Last checked against SU2 develop `11c177b904`.
