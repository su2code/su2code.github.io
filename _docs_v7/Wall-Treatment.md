---
title: "Wall Treatment: Wall Functions and Roughness"
permalink: /docs_v7/Wall-Treatment/
---

This page covers two ways to change what a turbulence model does at a viscous wall. *Wall functions* replace the resolved near-wall layer with an analytical law of the wall, so the first mesh point can be further from the wall. *Roughness models* change the wall boundary condition of the turbulence model so that it predicts the higher friction and heat transfer of a rough surface.

For the SA and SST models themselves, see [Turbulence Models](../Turbulence-Models/). For the basic wall boundary conditions, see [Markers and Boundary Conditions](../Markers-and-BC/).

---

- [Wall functions](#wall-functions)
  - [How to select them](#how-to-select-them)
  - [What SU2 does](#what-su2-does)
  - [LES wall models for the DG solver](#les-wall-models-for-the-dg-solver)
- [Wall roughness](#wall-roughness)
  - [How to select it](#how-to-select-it)
  - [Roughness with SA](#roughness-with-sa)
  - [Roughness with SST](#roughness-with-sst)
- [What SU2 does differently from the literature](#what-su2-does-differently-from-the-literature)
- [Equations and references](#equations-and-references)
- [Recommended use](#recommended-use)
- [Verification and test cases](#verification-and-test-cases)
- [Known limits](#known-limits)
- [Links](#links)

---

## Wall functions

### How to select them

List the wall markers and the wall function type in `MARKER_WALL_FUNCTIONS`:

```
SOLVER= RANS
KIND_TURB_MODEL= SST
MARKER_HEATFLUX= ( wall, 0.0 )
MARKER_WALL_FUNCTIONS= ( wall, STANDARD_WALL_FUNCTION )
```

The format is `( marker, type, marker, type, ... )`. Some types need extra values after the type (see [LES wall models](#les-wall-models-for-the-dg-solver)).

| Type | Status in SU2 develop |
|---|---|
| `NO_WALL_FUNCTION` | No wall function on this marker (the default for unlisted markers). |
| `STANDARD_WALL_FUNCTION` | The wall function of the finite-volume solvers. Only with `SOLVER= RANS` or `INC_RANS`, else SU2 stops with an error. Works with SA and SST. |
| `EQUILIBRIUM_WALL_MODEL` | LES wall model of the high-order DG solver. Not used by the finite-volume solvers. |
| `LOGARITHMIC_WALL_MODEL` | LES wall model of the high-order DG solver. Not used by the finite-volume solvers. |
| `ADAPTIVE_WALL_FUNCTION`, `SCALABLE_WALL_FUNCTION`, `NONEQUILIBRIUM_WALL_MODEL` | Not implemented. SU2 stops with an error. |

The `STANDARD_WALL_FUNCTION` has five expert options:

| Option | Default | What it does |
|---|---|---|
| `WALLMODEL_KAPPA` | `0.41` | Von Karman constant of the law of the wall. Also used by the SST wall function and by the `LIMITER_KNOPP` roughness model. |
| `WALLMODEL_B` | `5.5` | Additive constant B of the law of the wall. |
| `WALLMODEL_MINYPLUS` | `5.0` | The wall function acts only where y+ is at or above this value. |
| `WALLMODEL_MAXITER` | `200` | Maximum Newton iterations for the friction velocity (and for ν̃ in SA). |
| `WALLMODEL_RELFAC` | `0.5` | Relaxation factor of the Newton iterations. The SST wall function also uses it to relax the new k and ω values. |

### What SU2 does

The wall function follows Nichols and Nelson (2004). At each time step or iteration, for each wall node with a wall function:

1. SU2 takes the tangential velocity at the first interior node along the wall normal.
2. It solves Spalding's law of the wall for the friction velocity with a damped Newton method. The compressible solver uses the White–Christoph form, which includes compressibility and heat transfer. The incompressible solver uses the incompressible, adiabatic form.
3. In the compressible solver, on walls that are not isothermal, it updates the wall temperature with the Crocco–Busemann relation (frictional heating).
4. It stores the wall shear stress from the law. On the edges that connect the wall node to interior nodes, the viscous flux is scaled so that the wall shear stress equals this value. The velocity at the wall stays zero (no-slip).
5. The turbulence solver sets its variables at the first interior node:
   - **SA**: ν̃ is found from the eddy viscosity of the law of the wall (Newton method on the fv1 relation).
   - **SST**: ω is the blend of the viscous-sublayer and log-layer values of Nichols and Nelson. k follows from ω and the eddy viscosity of the law of the wall. Both are relaxed with `WALLMODEL_RELFAC`.

Where y+ is below `WALLMODEL_MINYPLUS`, the flow solver uses the normal no-slip wall. SU2 then prints how many points have a small y+. If the Newton method does not converge, SU2 prints a warning with the number of points.

The y+ in the output (`Y_PLUS`) is the y+ from the wall function on these markers.

The page [Markers and BC](../Markers-and-BC/#wall-functions) gives the original description, and [Theory](../Theory/#wall-functions) gives the summary.

### LES wall models for the DG solver

`EQUILIBRIUM_WALL_MODEL` and `LOGARITHMIC_WALL_MODEL` are used only by the high-order discontinuous Galerkin (DG) solver (`FEM_NAVIER_STOKES`, `FEM_LES`), on isothermal and heat flux walls. Each needs three values after the type:

```
MARKER_WALL_FUNCTIONS= ( wall, EQUILIBRIUM_WALL_MODEL, 0.05, 1.1, 30 )
```

The values are the height of the exchange point (where the model reads the outer flow), the stretching factor of the 1D wall-model grid, and its number of points. `LOGARITHMIC_WALL_MODEL` uses the Reichardt law for velocity and the Kader law for temperature. The values in the example are only placeholders (to be reviewed).

## Wall roughness

### How to select it

Give each rough marker its roughness height in `WALL_ROUGHNESS`:

```
MARKER_HEATFLUX= ( wall, 0.0 )
WALL_ROUGHNESS= ( wall, 400e-6 )
```

- The value is the *equivalent sand-grain roughness* k_s: the grain size of a sand-covered surface with the same friction. It is not the measured height of the real roughness. Conversion from real surfaces needs a correlation from the literature.
- Give k_s in the length unit of the mesh (metres for a mesh in metres).
- A marker with k_s = 0, or not listed, is smooth.
- The marker must be a viscous wall: `MARKER_HEATFLUX`, `MARKER_ISOTHERMAL`, `MARKER_HEATTRANSFER` or a CHT interface. Else SU2 stops with an error.
- At each node, SU2 uses the roughness of the nearest wall (found with the wall distance search).
- `WALL_ROUGHNESS` cannot be combined with `STANDARD_WALL_FUNCTION` on any marker. SU2 stops with an error.

There is no separate on/off switch. Setting a positive k_s turns on the rough-wall model of the active turbulence model.

`HROUGHNESS` is a different option: it is a roughness input of the LM transition model, not a wall roughness. See [Transition Models](../Transition-Models/).

### Roughness with SA

SU2 uses the rough-wall extension of Aupoix and Spalart (2003), in the form of the [NASA Turbulence Modeling Resource](https://tmbwg.github.io/turbmodels/spalart.html#sarough). No option selects it: it is always on for SA when k_s > 0.

- The wall distance in the SA model becomes d + 0.03 k_s.
- χ = ν̃/ν gets the extra term c_R1 k_s / d, with c_R1 = 0.5.
- The wall condition ν̃ = 0 is replaced by a gradient condition: dν̃/dn = ν̃ / (0.03 k_s). So ν̃ and the eddy viscosity are not zero at a rough wall.
- The skin friction on a rough wall uses the laminar plus the eddy viscosity at the wall.

### Roughness with SST

For SST, the roughness model only changes the wall values of k and ω. Choose the model with `KIND_ROUGHSST_MODEL`:

| `KIND_ROUGHSST_MODEL` | Wall values |
|---|---|
| `WILCOX1998` (default) | k = 0. ω from the roughness function S_R of Wilcox (1998). |
| `WILCOX2006` | k = 0. ω from the roughness function S_R of Wilcox (2006). |
| `LIMITER_KNOPP` | k > 0 and ω from Knopp et al. (2009). |
| `LIMITER_AUPOIX` | k ≥ 0 and ω from Aupoix (2015). |

All four use the roughness in wall units, k+ = u_τ k_s / ν, at the wall node. `KIND_ROUGHSST_MODEL` has no effect without a positive `WALL_ROUGHNESS`.

## What SU2 does differently from the literature

All facts below are from the SU2 code. Files: `SU2_CFD/src/solvers/CNSSolver.cpp`, `CIncNSSolver.cpp`, `CTurbSASolver.cpp`, `CTurbSSTSolver.cpp`, `SU2_CFD/include/numerics/turbulent/turb_sources.hpp`.

**Wall functions**

- **Vertex-based grid.** Nichols and Nelson use the first cell center. SU2 uses the first interior node along the wall normal. The wall node itself stays on the wall with zero velocity. The law sets the stress on the edges from the wall node, not a slip velocity.
- **Heat flux in the law.** In the compressible solver, the heat flux term of the White–Christoph law uses the `MARKER_HEATFLUX` value. On isothermal walls, SU2 sets this heat flux to zero inside the law and keeps the wall temperature fixed.
- **Incompressible solver.** The law has no compressibility or heat transfer terms. Wall functions on a CHT interface stop with an error in the incompressible solver.
- **Below `WALLMODEL_MINYPLUS`** the flow solver falls back to the no-slip wall. The turbulence solver then sets no wall condition at all at that node: ν̃ (SA) or k and ω (SST) at the wall are left free. A wall-resolved RANS sets ν̃ = 0, or k = 0 and a large ω, at the wall (to be reviewed).
- **Non-converged Newton method.** SU2 falls back to fixed values (y+ = 30, friction velocity 1, eddy viscosity 1) in the units of the run. Watch for the warning message.
- **SST ω and k.** ω follows Nichols and Nelson (eqs. 19–21). k = ω μt / ρ uses the density at the wall. The code comment notes that the paper uses ρ, not ρ_wall.

**SA roughness**

- The modified χ enters fv1 and ft2. fv2 uses the unmodified χ = ν̃/ν. The code comment says this keeps the modified vorticity unchanged, following the TMR page and the 2003 paper (to be reviewed).
- With DES (`HYBRID_RANSLES`), the SA source term uses the DES length scale and ignores the roughness. The rough-wall condition and the eddy viscosity still use it. See [Hybrid RANS/LES](../Hybrid-RANS-LES/).

**SST roughness**

- k+ uses the wall shear stress from the previous force evaluation, so it lags by one iteration.
- `LIMITER_KNOPP` limits ω at the wall to the smooth-wall value 60ν/(β1 d1²), where d1 is the distance to the nearest node. It uses `WALLMODEL_KAPPA` as the von Karman constant (to be reviewed).
- Roughness changes only the wall values. The SST source terms are unchanged.

## Equations and references

This page does not repeat the equations. See:

- Wall functions: R. H. Nichols, C. C. Nelson, "Wall function boundary conditions including heat transfer and compressibility", *AIAA J.* 42(6), 1107–1114, 2004. [doi:10.2514/1.3539](https://doi.org/10.2514/1.3539)
- Law of the wall: D. B. Spalding, "A single formula for the law of the wall", *J. Appl. Mech.* 28, 455–458, 1961. [doi:10.1115/1.3641728](https://doi.org/10.1115/1.3641728)
- SA roughness: B. Aupoix, P. R. Spalart, "Extensions of the Spalart–Allmaras turbulence model to account for wall roughness", *Int. J. Heat Fluid Flow* 24, 454–462, 2003. [doi:10.1016/S0142-727X(03)00043-2](https://doi.org/10.1016/S0142-727X(03)00043-2). Summary: [TMR, SA rough-wall extension](https://tmbwg.github.io/turbmodels/spalart.html#sarough).
- SST roughness, `WILCOX1998` and `WILCOX2006`: D. C. Wilcox, *Turbulence Modeling for CFD*, DCW Industries, 2nd edition 1998 and 3rd edition 2006.
- SST roughness, `LIMITER_KNOPP`: T. Knopp, B. Eisfeld, J. B. Calvo, "A new extension for k–ω turbulence models to account for wall roughness", *Int. J. Heat Fluid Flow* 30, 54–65, 2009. [doi:10.1016/j.ijheatfluidflow.2008.09.009](https://doi.org/10.1016/j.ijheatfluidflow.2008.09.009)
- SST roughness, `LIMITER_AUPOIX`: B. Aupoix, "Roughness corrections for the k–ω shear stress transport model: status and proposals", *J. Fluids Eng.* 137(2), 021202, 2015. [doi:10.1115/1.4028122](https://doi.org/10.1115/1.4028122)
- SA and SST models: [NASA Turbulence Modeling Resource](https://tmbwg.github.io/turbmodels/).

## Recommended use

All advice in this section is general practice, not checked in SU2 (to be reviewed).

**Wall functions**

- Aim for the first interior node in the log layer: y+ about 30 to 100. The upper limit grows with the Reynolds number. The [Markers and BC](../Markers-and-BC/#wall-functions) page gives 100 to 500 (to be reviewed).
- Avoid a first node in the buffer layer (y+ about 5 to 30) on large parts of the wall (to be reviewed).
- Wall functions assume an attached boundary layer in equilibrium. Expect lower accuracy near separation, reattachment and strong pressure gradients (to be reviewed).
- List every viscous wall in `MARKER_WALL_FUNCTIONS` (see [Known limits](#known-limits)).
- If the "did not converge" warning stays, increase `WALLMODEL_MAXITER` or decrease `WALLMODEL_RELFAC` (from the [Markers and BC](../Markers-and-BC/#wall-functions) page).
- Check the y+ field (`Y_PLUS`) on the walls after the run.

**Roughness**

- Resolve the wall as for a smooth wall: y+ about 1 at the first node (to be reviewed).
- `LIMITER_KNOPP` and `LIMITER_AUPOIX` were proposed to fix known weaknesses of the Wilcox wall values on fine meshes and at small roughness (to be reviewed).
- Check k+ against the range the chosen model was calibrated for (to be reviewed).

## Verification and test cases

There is no verification case for wall functions or roughness in the [V&V section](/vandv/home/). The regression tests check that the options run.

Wall functions (all on a flat plate, `STANDARD_WALL_FUNCTION`):

- [`wallfunctions/flatplate/compressible_SA/turb_SA_flatplate.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/wallfunctions/flatplate/compressible_SA/turb_SA_flatplate.cfg), and [`turb_SA_flatplate_restart.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/wallfunctions/flatplate/compressible_SA/turb_SA_flatplate_restart.cfg)
- [`wallfunctions/flatplate/compressible_SST/turb_SST_flatplate.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/wallfunctions/flatplate/compressible_SST/turb_SST_flatplate.cfg)
- [`wallfunctions/flatplate/incompressible_SA/turb_SA_flatplate.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/wallfunctions/flatplate/incompressible_SA/turb_SA_flatplate.cfg)
- [`wallfunctions/flatplate/incompressible_SST/turb_SST_flatplate.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/wallfunctions/flatplate/incompressible_SST/turb_SST_flatplate.cfg)

Roughness:

- SA, incompressible: [`incomp_rans/rough_flatplate/rough_flatplate_incomp.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/incomp_rans/rough_flatplate/rough_flatplate_incomp.cfg) and [`pb_rough_flatplate_incomp.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/incomp_rans/rough_flatplate/pb_rough_flatplate_incomp.cfg) (pressure-based solver).
- SST, compressible: [`WILCOX2006`](https://github.com/su2code/SU2/blob/develop/TestCases/rans/flatplate/roughness/bc_wilcox2006/turb_SST_flatplate_roughBCWilcox2006.cfg), [`LIMITER_KNOPP`](https://github.com/su2code/SU2/blob/develop/TestCases/rans/flatplate/roughness/bc_knopp/turb_SST_flatplate_roughBCKnopp.cfg), [`LIMITER_AUPOIX`](https://github.com/su2code/SU2/blob/develop/TestCases/rans/flatplate/roughness/bc_aupoix/turb_SST_flatplate_roughBCAupoix.cfg). No test uses the default `WILCOX1998`.
- No test uses SA roughness in the compressible solver.

Tutorials with wall functions:

- [Turbulent Bend with wall functions](/tutorials/Inc_Turbulent_Bend/): incompressible, SST, compared with measurements.
- [Aachen Turbine](/tutorials/Aachen_Turbine/): compressible turbomachinery, SA.

## Known limits

- **List all viscous walls.** The turbulence solvers check one global flag: "does any marker have a wall function?" If yes, they apply the wall-function condition on every heat flux and isothermal wall, also on walls not listed in `MARKER_WALL_FUNCTIONS`. The flow solver applies the law of the wall only on the listed markers. A mix of listed and unlisted walls is therefore inconsistent (code, `CTurbSASolver::BC_HeatFlux_Wall`, `CTurbSSTSolver::BC_HeatFlux_Wall`).
- **Small y+.** Below `WALLMODEL_MINYPLUS`, the turbulence variables at the wall get no boundary condition (see above). A mesh with y+ much below 5 should be run without wall functions (to be reviewed).
- **DG wall model types in RANS.** `EQUILIBRIUM_WALL_MODEL` passes the config check in a finite-volume RANS run, but the finite-volume flow solver ignores it. The turbulence solver still switches to its wall-function condition.
- **Wall functions and roughness** cannot be combined.
- **SA roughness and DES**: the roughness is only partly used.
- **Incompressible CHT interfaces** do not support wall functions.

## Links

- [Markers and Boundary Conditions](../Markers-and-BC/)
- [Turbulence Models](../Turbulence-Models/)
- [Hybrid RANS/LES (DES)](../Hybrid-RANS-LES/)
- [Setup Guide: RANS External Aerodynamics](../Setup-Guide-RANS-External-Aero/)
- [Setup Guide: Unsteady Flows and DES](../Setup-Guide-Unsteady-DES/)
- [Option Reference](../Option-Reference/)
- [Output Fields Reference](../Output-Fields-Reference/)

---

Last checked against SU2 develop `11c177b904`.
