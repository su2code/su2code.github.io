---
title: "Hybrid RANS/LES (DES)"
permalink: /docs_v7/Hybrid-RANS-LES/
---

This page explains the model and its SU2 implementation. For numerical setup choices, see the [setup guide](../Setup-Guide-Unsteady-DES/); use its tutorial and V&V links for worked examples and comparisons.

Hybrid RANS/LES methods run a RANS model in attached boundary layers and a large-eddy simulation (LES) away from the walls. In LES, the mesh and the time step resolve the large turbulent eddies, and the model only handles the small ones. Detached eddy simulation (DES) and its variants are the hybrid methods in SU2. Use them for massively separated, unsteady flows where URANS is not accurate enough and a full LES is too expensive.

For a step-by-step case setup, see [Setup Guide: Unsteady Flows and DES](../Setup-Guide-Unsteady-DES/). For the SA and SST models themselves, see [Turbulence Models](../Turbulence-Models/).

**Note:** the SST variants and the new `SA_EDDES` length scale come with [PR #2150](https://github.com/su2code/SU2/pull/2150). They are in develop once that PR is merged.

---

- [How DES works in SU2](#how-des-works-in-su2)
- [How to select it](#how-to-select-it)
  - [DES variant](#des-variant)
  - [DES length scale options](#des-length-scale-options)
  - [Low-dissipation convective scheme](#low-dissipation-convective-scheme)
  - [Stochastic backscatter model](#stochastic-backscatter-model)
  - [Time averages](#time-averages)
- [What SU2 does differently from the literature](#what-su2-does-differently-from-the-literature)
  - [SA variants](#sa-variants)
  - [SST variants](#sst-variants)
  - [Shear-layer-adapted cell size](#shear-layer-adapted-cell-size)
- [Equations and references](#equations-and-references)
- [Recommended use](#recommended-use)
- [Output fields](#output-fields)
- [Verification and test cases](#verification-and-test-cases)
- [Known limits](#known-limits)
- [Links](#links)

---

## How DES works in SU2

A RANS model has a destruction term, which removes turbulence. A length scale sets the size of this term. DES replaces the RANS length with a shorter *DES length scale* away from the walls. There, destruction grows, the eddy viscosity drops, and the model acts as an LES subgrid model.

- **SA variants.** The RANS length is the wall distance d. In original DES, the length scale is min(d, C_DES Δ), with the local grid measure Δ. In the delayed variants it is d − f_d·max(0, d − C_DES Δ).
- **SST variants.** The RANS length is l_RANS = √k / (β* ω), with β* = 0.09. The destruction term of the k equation, β* ρ k ω, becomes ρ k^{3/2} / l_DES. With l_DES = l_RANS this is the RANS term again. The ω equation does not change.
- The delayed variants use a *shielding function* f_d. Where f_d is near zero, the model keeps the RANS length. Where f_d is near one, it uses the DES limit.
- With a suitable mesh and time step, the shortened scale lets the model act as an LES subgrid model. Distance from the wall alone does not select the mode.

The variants differ in two points: how they protect attached boundary layers from switching to LES, and how they measure the cell size.

SU2 computes the DES length scale at the start of every iteration, in the turbulence solver: `CTurbSASolver::SetDES_LengthScale` for SA and `CTurbSSTSolver::SetDES_LengthScale` for SST. Both are called from `Preprocessing`.

SU2 checks two things before the run (`CConfig::SetPostprocessing`). It stops with an error if:

- `HYBRID_RANSLES` is set and `TIME_DOMAIN= NO`. A steady DES has no physical meaning.
- The variant does not match the turbulence model. The `SA_*` variants need `KIND_TURB_MODEL= SA`, the `SST_*` variants need `KIND_TURB_MODEL= SST`. This also stops a run with `KIND_TURB_MODEL= NONE`.

DES works with the compressible (`RANS`) and the incompressible (`INC_RANS`) solvers. Both pass the DES length scale and the LES sensor to the output. The regression tests of the SST variants use only the compressible solver.

## How to select it

### DES variant

Set the turbulence model and pick a matching variant with `HYBRID_RANSLES`:

```
SOLVER= RANS
KIND_TURB_MODEL= SA
HYBRID_RANSLES= SA_DDES
DES_CONST= 0.65
TIME_DOMAIN= YES
```

For SST, set `KIND_TURB_MODEL= SST` and an `SST_*` variant, for example `HYBRID_RANSLES= SST_DDES`.

| `HYBRID_RANSLES` | Model | Method | Cell size used in LES mode |
|---|---|---|---|
| `NONE` (default) | – | No DES. The turbulence model runs as RANS or URANS. | – |
| `SA_DES` | SA | Original DES (Spalart et al. 1997). Switches to LES wherever `DES_CONST` times the cell size is smaller than the wall distance. | Longest edge from the node |
| `SA_DDES` | SA | Delayed DES (Spalart et al. 2006). The shielding function f_d keeps attached boundary layers in RANS mode. | Longest edge from the node |
| `SA_ZDES` | SA | DDES with the vorticity-based cell size of the zonal DES (Deck 2012). | Cell size seen across the vorticity vector |
| `SA_EDDES` | SA | DDES with the shear-layer-adapted cell size of Shur et al. (2015). Meant to switch faster from RANS to LES in separated shear layers. | Shear-layer-adapted size |
| `SST_DDES` | SST | DDES for SST (Gritskevich et al. 2012, Appendix 1). | Longest edge from the node |
| `SST_IDDES` | SST | Improved DDES (IDDES) for SST (Gritskevich et al. 2012, Appendix 2). IDDES adds a wall-modelled LES branch: when resolved turbulence reaches an attached boundary layer and the mesh is fine enough, only a thin layer next to the wall stays in RANS mode. | A size that depends on the wall distance (see [SST variants](#sst-variants)) |
| `SST_SIDDES` | SST | Simplified IDDES: IDDES without the elevating function f_e (Gritskevich et al. 2012, Eq. 12). | Same as `SST_IDDES` |
| `SST_EDDES` | SST | `SST_DDES` with the shear-layer-adapted cell size of `SA_EDDES`. | Shear-layer-adapted size |

### DES length scale options

These options act only on the `SA_*` variants. The `SST_*` variants ignore them, without a warning.

| Option | Default | What it does |
|---|---|---|
| `DES_CONST` | `0.65` | The DES constant. The LES length scale is `DES_CONST` times the cell size. The SST variants use their own constant (see [SST variants](#sst-variants)). |
| `LES_FILTER_WIDTH` | `-1.0` | If positive, SU2 uses this value as the cell size at every node, for all SA variants. It replaces the local cell size. Give it in mesh length units. A negative value uses the local cell size. |
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
- `FD` computes its own f_d from the wall distance and the eddy viscosity. It does not need `HYBRID_RANSLES`. It always uses the SA form of f_d (constant 8), also with an SST variant.
- `NTS` always reads `DES_CONST`, also with an SST variant.
- With the option on, the volume output gets the field `ROE_DISSIPATION`.

For incompressible LES regions, SU2 has the centered scheme `CONV_NUM_METHOD_FLOW= LD2` (low dissipation, low dispersion). It works only with the incompressible solver and a constant-density fluid. The backscatter test case uses it.

### Stochastic backscatter model

In the "grey area" just after separation, a DES has neither modeled nor resolved turbulence: the RANS eddy viscosity is gone and the resolved eddies have not grown yet. The stochastic backscatter model (Kok 2017) adds random forcing in LES regions to speed up the growth of resolved eddies. *Backscatter* means energy that flows from the small, modeled scales back to the large, resolved ones.

SU2 adds a random stress to the momentum equations. The random field comes from three extra equations (Langevin equations) for a random vector, solved together with the SA equation. The model works only with the `SA_*` variants (see [Known limits](#known-limits)).

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

### SA variants

All facts below are from `SU2_CFD/src/solvers/CTurbSASolver.cpp` (`SetDES_LengthScale`) unless stated.

**Cell size.** The papers define the DES cell size on cells, for example the largest cell dimension Δmax = max(Δx, Δy, Δz). SU2 is vertex-based. It uses the longest edge from the node to any neighbor node (`CPhysicalGeometry::SetMaxLength`). On a hexahedral mesh this is close to the largest cell dimension. On a tetrahedral or prismatic mesh, it is the longest edge.

**No low-Reynolds-number correction.** DDES (Spalart et al. 2006) multiplies the LES length scale by a function Ψ. Ψ stops the SA damping terms from reducing the subgrid viscosity when the eddy viscosity is small. SU2 computes Ψ (the variable `psi_2`) but never uses it. The LES length scale is always `DES_CONST` times the cell size.

**`SA_DES` sensor.** The LES sensor is a switch: 0 where the wall distance is smaller than the LES length scale, 1 elsewhere.

**`SA_ZDES` is not the full zonal method.** Deck (2012) describes a zonal method with several modes that the user assigns to regions. SU2 has one automatic mode: DDES with the vorticity-based cell size. The cell size per direction is the largest distance to a neighbor node along x, y and z. SU2 switches back to the longest-edge cell size where f_d < 0.99. Deck's mode 2 uses its own threshold for this switch (to be reviewed).

**`SA_EDDES` cell size.** It uses the shear-layer-adapted cell size described [below](#shear-layer-adapted-cell-size), shared with `SST_EDDES`.

**Shielding function.** `SA_DDES`, `SA_ZDES` and `SA_EDDES` use the DDES shielding function f_d with the constants 8 and 3 of the paper. The LES sensor output is f_d where the LES length scale is smaller than the wall distance, and 0 elsewhere.

**Roughness.** With DES on, the SA source term uses the DES length scale and ignores `WALL_ROUGHNESS`. The rough-wall boundary condition and the eddy viscosity still use it. See [Wall Treatment](../Wall-Treatment/#roughness-with-sa).

**Backscatter inside the SA equation.** Where the backscatter model is active (LES sensor above `SBS_FD_LOWER_THRESHOLD`), the SA source term uses fv1 = 1, fv2 = 0 and fw = 0 (`SU2_CFD/include/numerics/turbulent/turb_sources.hpp`). With fw = 0, the SA destruction term is switched off there. The random source added to the SA equation is limited to 5 times the production term.

**Backscatter energy estimate.** The random stress scales with an estimate of the subgrid kinetic energy, (eddy viscosity / DES length scale)². In the momentum equations, SU2 uses the dynamic eddy viscosity μt for this estimate (`SU2_CFD/src/numerics/flow/flow_diffusion.cpp`). In the SA equation and in the averaged output, it uses the kinematic eddy viscosity νt (to be reviewed).

### SST variants

The length scale is computed in `CTurbSSTSolver::SetDES_LengthScale` (`SU2_CFD/src/solvers/CTurbSSTSolver.cpp`). The source term is in `CSourcePieceWise_TurbSST::ComputeResidual` (`SU2_CFD/include/numerics/turbulent/turb_sources.hpp`). The formulas and constants are those of Gritskevich et al. (2012), Appendices 1 and 2.

**Common parts.**

- l_RANS = √k / (β* ω), with β* = 0.09.
- The DES constant is blended with the SST function F1: C_DES = 0.78·F1 + 0.61·(1 − F1). SU2 does not read `DES_CONST` here.
- h_max is the longest edge from the node, as for SA. The paper uses the longest edge of the cell.
- The shielding functions use r_d = (ν_t + ν) / (κ² d² √(0.5 (S² + Ω²))), with κ = 0.41, the strain rate magnitude S and the vorticity magnitude Ω. To avoid a division by zero, SU2 keeps S and Ω above 1e-12 and the denominator of r_d above 1e-10.

**`SST_DDES`.** l_DES = l_RANS − f_d·max(0, l_RANS − C_DES h_max), with f_d = 1 − tanh((20 r_d)³).

**`SST_IDDES`.** The length scale is l_DES = f̃\_d (1 + f_e) l_RANS + (1 − f̃\_d) C_DES Δ, with:

- Δ = min(0.15·max(d, h_max), h_max). Near the wall, Δ depends on the wall distance d.
- f̃\_d = max(1 − f_dt, f_B). The function f_dt has the form of f_d, but r_dt uses only ν_t. The constants are C_dt1 = 20 and C_dt2 = 3.
- f_B = min(2 exp(−9α²), 1), with α = 0.25 − d / h_max.
- The elevating function f_e raises the RANS part near the interface between the RANS and LES layers. Its constants are C_t = 1.87 and C_l = 5.
- SU2 uses the constants of Appendix 2 (Eq. 13). Section 5 of the paper also mentions C_dt1 = 8; SU2 does not use that value.

**`SST_SIDDES`.** The same as `SST_IDDES`, with f_e = 0 (Eq. 12).

**`SST_EDDES`.** The same as `SST_DDES`, with h_max replaced by the [shear-layer-adapted cell size](#shear-layer-adapted-cell-size). The paper of Shur et al. (2015) uses SA. The code comment cites Guseva et al. (2017) and Xiao et al. (2020) for the use with SST.

**Source term.**

- In every SST variant, the k destruction is ρ k^{3/2} / l_DES. The ω equation does not change.
- The production limiter keeps its RANS form, based on ω, as in the paper (Eq. 3). Its constant is 20 with `V1994m` and 10 with `V2003m`, as in RANS.
- The implicit Jacobian of the k destruction keeps its RANS form, β* ω. This affects only how the inner iterations converge, not the converged solution.

**`SST_OPTIONS`.** SU2 accepts every `SST_OPTIONS` value with a hybrid variant. The regression tests use the default, `V2003m`. Points to know:

- `COMPRESSIBILITY-WILCOX` and `COMPRESSIBILITY-SARKAR`: in hybrid mode, the k destruction loses the compressibility factor (1 + ζ F(Mt)). The ω destruction and the Sarkar dilatation term keep their corrections.
- `SUSTAINING`: the sustaining source of k keeps its RANS form: β* ρ k ω, with the free-stream values of k and ω.
- With the LM transition model, SU2 multiplies the hybrid k destruction by the effective intermittency (limited to between 0.1 and 1), as in RANS.

### Shear-layer-adapted cell size

`SA_EDDES` and `SST_EDDES` use the shear-layer-adapted (SLA) cell size of Shur et al. (2015), Eqs. 1–6. The function is `CTurbSolver::ShearLayerAdaptedLengthScale` (`SU2_CFD/src/solvers/CTurbSolver.cpp`). It returns Δ_SLA = Δ̃\_ω · F_KH(⟨VTM⟩).

**Δ̃\_ω, the cell size seen along the vorticity (Eq. 1).** The paper projects the cell vertices onto the plane normal to the vorticity. It takes the largest distance between two projected points and divides it by √3. SU2 is vertex-based: the control volume of a node is its median-dual cell. SU2 uses the vertices of this cell:

- the node itself,
- the midpoints of its edges,
- the centroids of the faces that contain the node,
- the centroids of the elements that contain the node.

This works on any element type. On a hexahedral mesh aligned with the axes, the result is the box of the grid spacings.

**Vortex tilting measure (VTM, Eqs. 2 and 5).** The VTM measures how much the strain tilts the vorticity vector. It is near 0 in nearly 2D shear layers and near 1 in developed 3D turbulence. SU2 computes it in `CTurbVariable::SetVortex_Tilting`:

- The denominator uses 3 tr(S²) − tr(S)², where tr(S²) is the sum of the squares of all components of the strain tensor S.
- The factor max(1, 0.2 ν / ν_t) of Eq. 5 is included.
- Where the denominator is zero (no vorticity or no strain anisotropy), SU2 sets VTM = 1. F_KH is then 1.
- ⟨VTM⟩ is the plain mean of the VTM over the node and its neighbor nodes.

**F_KH (Eq. 4).** The constants are those of the paper: F_min = 0.1, F_max = 1, a1 = 0.15, a2 = 0.3.

**Shielding (Eq. 6).** Where f_d < 0.99 (ε = 0.01), SU2 sets F_KH = 1, so Δ = Δ̃\_ω. `SA_EDDES` uses the SA f_d, `SST_EDDES` the SST f_d.

**Zero vorticity.** Where |ω| < 1e-12, the vorticity direction is not defined. SU2 then uses h_max, as in standard DDES.

**Change from develop.** Before PR #2150, `SA_EDDES` used the edges from the node, with the absolute value of each component, instead of the median-dual cell. It used only the diagonal of the strain tensor in the VTM. Where f_d < 0.999, it used h_max. The reference values of the `ddes_flatplate` test changed with this fix.

## Equations and references

This page does not repeat the model equations. See the original papers:

- DES: P. R. Spalart, W.-H. Jou, M. Strelets, S. R. Allmaras, "Comments on the feasibility of LES for wings, and on a hybrid RANS/LES approach", *Advances in DNS/LES*, Greyden Press, 1997.
- DDES: P. R. Spalart et al., "A new version of detached-eddy simulation, resistant to ambiguous grid densities", *Theor. Comput. Fluid Dyn.* 20, 181–195, 2006. [doi:10.1007/s00162-006-0015-0](https://doi.org/10.1007/s00162-006-0015-0)
- ZDES: S. Deck, "Recent improvements in the Zonal Detached Eddy Simulation (ZDES) formulation", *Theor. Comput. Fluid Dyn.* 26, 523–550, 2012. [doi:10.1007/s00162-011-0240-z](https://doi.org/10.1007/s00162-011-0240-z)
- EDDES and the SLA cell size: M. L. Shur et al., "An enhanced version of DES with rapid transition from RANS to LES in separated flows", *Flow Turbul. Combust.* 95, 709–737, 2015. [doi:10.1007/s10494-015-9618-0](https://doi.org/10.1007/s10494-015-9618-0)
- SST DDES and IDDES: M. S. Gritskevich, A. V. Garbaruk, J. Schütze, F. R. Menter, "Development of DDES and IDDES formulations for the k-ω shear stress transport model", *Flow Turbul. Combust.* 88, 431–449, 2012. [doi:10.1007/s10494-011-9378-4](https://doi.org/10.1007/s10494-011-9378-4)
- SLA with SST, as cited in the code: Guseva et al., *Flow Turbul. Combust.* 98, 2017; Xiao et al., *Int. J. Heat Fluid Flow* 85, 2020.
- NTS blending: A. Travin et al., "Physical and numerical upgrades in the detached-eddy simulation of complex turbulent flows", *Advances in LES of Complex Flows*, 239–254, 2002. [doi:10.1007/0-306-48383-1_16](https://doi.org/10.1007/0-306-48383-1_16)
- NTS form used in SU2: Z. Xiao et al., "Numerical dissipation effects on massive separation around tandem cylinders", *AIAA J.* 50(5), 1119–1136, 2012. [doi:10.2514/1.J051299](https://doi.org/10.2514/1.J051299)
- NTS with Ducros sensor: Z. Xiao et al., *Int. J. Heat Fluid Flow* 51, 138–150, 2015. [doi:10.1016/j.ijheatfluidflow.2014.10.007](https://doi.org/10.1016/j.ijheatfluidflow.2014.10.007)
- Stochastic backscatter: J. C. Kok, "A stochastic backscatter model for grey-area mitigation in detached eddy simulations", *Flow Turbul. Combust.* 99, 119–150, 2017. [doi:10.1007/s10494-017-9809-y](https://doi.org/10.1007/s10494-017-9809-y)
- LES index of quality: I. B. Celik, Z. N. Cehreli, I. Yavuz, "Index of resolution quality for large eddy simulations", *J. Fluids Eng.* 127(5), 949–958, 2005.
- SA model: [NASA Turbulence Modeling Resource, SA page](https://tmbwg.github.io/turbmodels/spalart.html).
- SST model: [NASA Turbulence Modeling Resource, SST page](https://tmbwg.github.io/turbmodels/sst.html).

## Recommended use

All advice in this section is general practice, not checked in SU2 (to be reviewed).

- **Variant.** Prefer a delayed variant (`SA_DDES`, `SA_EDDES`, `SST_DDES`, `SST_EDDES`, ...) over `SA_DES`. Plain DES can switch to LES inside an attached boundary layer if the mesh is fine along the wall. The flow can then separate because of the mesh (to be reviewed). The [NACA 0021 V&V page](/vandv/NACA0021_DDES/) compares four variants on one case.
- **Mesh.** Run DES in 3D. Resolve the boundary layer as for RANS (y+ about 1, no wall functions). In the separated region, use nearly cubic cells: the cell size sets the LES filter. In the spanwise direction, the domain must be large enough to hold the largest eddies (to be reviewed).
- **Time step.** Choose a time step so that the convective CFL number, based on the local cell size and velocity, is about 1 or less in the LES region (to be reviewed).
- **Time marching.** Use `TIME_MARCHING= DUAL_TIME_STEPPING-2ND_ORDER`, as in the flat plate and backscatter tests. Converge the inner iterations by 2 to 3 orders per time step (to be reviewed).
- **Convective scheme.** Use a second-order scheme (`MUSCL_FLOW= YES`) without a slope limiter where there are no shocks. With `ROE`, `SLAU` or `SLAU2`, try `ROE_LOW_DISSIPATION= FD` or `NTS`. Add a `_DUCROS` variant if there are shocks (to be reviewed).
- **Statistics.** Exclude the start-up transient with `WINDOW_START_ITER`, then sample over many characteristic times. Compare separate sampling blocks and extend the interval; a flat cumulative average or passing Cauchy criterion alone does not establish statistical convergence (advice, to be reviewed).
- **Check the switch (SA).** Plot `LES_SENSOR` and `DES_LENGTHSCALE`. Attached boundary layers should stay at sensor 0 (RANS). Separated regions should show sensor near 1 (LES).
- **Check the switch (SST).** `LES_SENSOR` is zero for the SST variants. Instead, divide `DES_LENGTHSCALE` by 10 × `SRS_GRID_SIZE`, which is l_RANS. For `SST_DDES` and `SST_EDDES`, the ratio is 1 in RANS mode and smaller in LES mode.

## Output fields

| Group | Fields | When |
|---|---|---|
| `DDES` | `DES_LENGTHSCALE`, `WALL_DISTANCE`, `LESIQ`, `LES_SENSOR` | `HYBRID_RANSLES` is not `NONE` |
| `DDES` | `SRS_GRID_SIZE` | An `SST_*` variant |
| `BACKSCATTER` | `STOCHSOURCE_X/Y/Z`, `ENERGY_BACKSCATTER_RATIO` | Backscatter on |
| `SOLUTION`, `RESIDUAL` | `STOCHVAR_X/Y/Z`, `RES_STOCHVAR_X/Y/Z` | Backscatter on with `SBS_TIMESCALE_COEFF` > 0 |
| `ROE_DISSIPATION` | `ROE_DISSIPATION` | Compressible solver with `ROE_LOW_DISSIPATION` set |
| `TIME_AVERAGE` | `MEAN_*`, `RMS_*`, `*PRIME`, `MODELED_REYNOLDS_STRESS_*`, `STOCHASTIC_REYNOLDS_STRESS_*` | Time-domain run |
| `VELOCITY_GRADIENT` | `GRAD_VEL_XX`, `GRAD_VEL_XY`, `GRAD_VEL_YX`, `GRAD_VEL_YY`, and in 3D the `_XZ`, `_YZ`, `_ZX`, `_ZY`, `_ZZ` fields | Any viscous run |
| `SST_QUANTITIES` | `CDkw`, `F1`, `F2` | Any viscous run with SST |
| `DEBUG` | `WALL_DISTANCE` | Viscous run with `HYBRID_RANSLES= NONE` |

The fields that are new with PR #2150 (`CFlowOutput.cpp`):

- `DES_LENGTHSCALE` holds the hybrid length. For SA it is the length that replaces the wall distance in the destruction term. For SST it is l_DES in the k destruction; in RANS mode it equals l_RANS.
- `LES_SENSOR` comes from the SA solver. For the SST variants, SU2 writes 0 everywhere.
- `LESIQ` = 1 / (1 + 0.05 ((μ_t + μ)/μ)^0.53). This is the viscosity-based LES index of quality of Celik et al. (2005). It is near 1 where the eddy viscosity is small compared with the laminar viscosity.
- `SRS_GRID_SIZE` = 0.1 · √k / (0.09 ω), one tenth of l_RANS. It suggests a cell size for a scale-resolving simulation. The factor 0.1 is fixed in the code.
- `GRAD_VEL_` fields hold the velocity gradient: the first letter is the velocity component, the second the direction. For example, `GRAD_VEL_XY` is ∂u/∂y.
- `CDkw` is the SST cross-diffusion term. `F1` and `F2` are the SST blending functions.

Note: the `RMS_U`, `RMS_V`, ... fields hold the mean of the squared value (for example the mean of u²), not the root mean square. The fluctuations are in `UUPRIME`, `VVPRIME`, and so on.

The full list is in the [Output Fields Reference](../Output-Fields-Reference/).

## Verification and test cases

The V&V page [NACA 0021 Beyond Stall: Hybrid RANS/LES](/vandv/NACA0021_DDES/) compares `SA_DDES`, `SA_EDDES`, `SST_DDES` and `SST_EDDES` on a NACA 0021 airfoil at 60° angle of attack.

The regression tests only check that the options run and that the results do not change:

- [`TestCases/ddes/flatplate/ddes_flatplate.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/ddes/flatplate/ddes_flatplate.cfg): `SA_EDDES` on a 2D flat plate, compressible, `SLAU2`. A 2D flat plate is not a real DES case.
- [`TestCases/backscatter/backward_step/backwardStep.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/backscatter/backward_step/backwardStep.cfg): `SA_DDES` with stochastic backscatter in a box, incompressible, `LD2` scheme, periodic in the spanwise direction. It shows all `SBS_*` options and the `TIME_AVERAGE` output.
- `TestCases/ddes/oneram6/ddes_oneram6_*.cfg` (PR #2150), one per model: [`sst_ddes`](https://github.com/su2code/SU2/blob/e9e85686ad3b53fb76eb912d1e8be3b521372838/TestCases/ddes/oneram6/ddes_oneram6_sst_ddes.cfg), [`sst_iddes`](https://github.com/su2code/SU2/blob/e9e85686ad3b53fb76eb912d1e8be3b521372838/TestCases/ddes/oneram6/ddes_oneram6_sst_iddes.cfg), [`sst_siddes`](https://github.com/su2code/SU2/blob/e9e85686ad3b53fb76eb912d1e8be3b521372838/TestCases/ddes/oneram6/ddes_oneram6_sst_siddes.cfg), [`sst_eddes`](https://github.com/su2code/SU2/blob/e9e85686ad3b53fb76eb912d1e8be3b521372838/TestCases/ddes/oneram6/ddes_oneram6_sst_eddes.cfg) and [`sa_eddes`](https://github.com/su2code/SU2/blob/e9e85686ad3b53fb76eb912d1e8be3b521372838/TestCases/ddes/oneram6/ddes_oneram6_sa_eddes.cfg). They use the ONERA M6 wing on a hexahedral mesh, compressible, `ROE`. Each one restarts from an SA or SST RANS solution, so that the LES branch of the length scale is active, and runs a few short time steps. They are in the serial, parallel and hybrid regression scripts. They are not a setup example.

Background: [An Overview of DDES in SU2: Implementation and Recent Results](/documents/dev_meeting_2017/su2_dev_molina.pdf) (2017 developers meeting).

## Known limits

- **`ROE_LOW_DISSIPATION` is ignored** with schemes other than `ROE`, `SLAU` and `SLAU2`, and in the incompressible solver, without a warning.
- **Backscatter is 3D only and needs an `SA_*` variant.** SU2 does not stop if you turn it on with an `SST_*` variant. The SST solver has no random field, so the flow solver reads other turbulence variables in its place. Do not use this combination.
- **The SST variants ignore `DES_CONST`, `LES_FILTER_WIDTH` and `ENFORCE_LES`**, without a warning. With `ENFORCE_LES= YES`, the screen still says that LES is enforced everywhere.
- **No LES sensor for SST.** `LES_SENSOR` is zero for the SST variants (see [Recommended use](#recommended-use) for another check).
- **SST compressibility corrections.** In hybrid mode, the k destruction has no compressibility factor (see [SST variants](#sst-variants)).
- **Discrete adjoint with SST variants.** The SST source term does not declare the DES length scale as an input of the algorithmic differentiation (AD) preaccumulation (`turb_sources.hpp`). Derivatives that pass through the length scale can be missing (to be reviewed).
- **Wall roughness is only partly used with SA DES** (see [Roughness](#sa-variants)).
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

Source review: 23 October 2026, against [SU2 PR #2150 at `e9e85686ad`](https://github.com/su2code/SU2/tree/e9e85686ad3b53fb76eb912d1e8be3b521372838). See the [review scope and outstanding validation](../Documentation-Status/#guide-and-model-review). Setup recommendations remain draft where indicated.
