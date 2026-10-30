---
title: Changes in Version 8
permalink: /docs_v7/Guide-to-v8/
---

SU2 version 8 ("Harrier") started with v8.0.0 in August 2023. Most v7 config files still run in v8. A few options were renamed or removed, some defaults changed, and several fixes change the results of turbulent cases. The Python wrapper and the build system also changed.

How to read this page:

- Read [Breaking changes](#breaking-changes) first. These can stop a v7 config from running or change its results.
- [New features](#new-features-by-area) lists what v8 adds, by area. Each item gives the release that added it.
- Use the [checklist](#migrating-a-v7-config) at the end to update a config.

When SU2 finds a removed option in a config file, it stops and names the option. For many options it also names the replacement. The full list of renamed and removed options is on [Renamed and Removed Options](../Renamed-Options/). The changes from v6 to v7 (`EXT_ITER`, `PHYSICAL_PROBLEM`, output options and so on) are on [Guide to Version v7](../Guide-to-v7/).

---

- [Breaking changes](#breaking-changes)
  - [Renamed and removed options](#renamed-and-removed-options)
  - [Changed defaults and behaviour](#changed-defaults-and-behaviour)
  - [Changes that affect results](#changes-that-affect-results)
  - [Python wrapper](#python-wrapper)
  - [Build and tools](#build-and-tools)
- [New features by area](#new-features-by-area)
- [Migrating a v7 config](#migrating-a-v7-config)

---

## Breaking changes

### Renamed and removed options

These are the most common ones. See [Renamed and Removed Options](../Renamed-Options/) for all of them.

| Old option | New option | Release |
| --- | --- | --- |
| `DYNAMIC_ANALYSIS` | `TIME_DOMAIN` | v8.0.0 |
| `DYN_TIMESTEP` | `TIME_STEP` | v8.0.0 |
| `DYN_TIME` | `MAX_TIME` | v8.0.0 |
| `SINGLEZONE_DRIVER` | Removed, no replacement | v8.0.0 |
| `SPECIES_USE_STRONG_BC= YES` | `MARKER_SPECIES_STRONG_BC= (marker1, ...)` | v8.0.0 |
| `DEAD_LOAD` | `GRAVITY_FORCE` or `BODY_FORCE` | v8.2.0 |
| `SMOOTH_GEOMETRY` | Removed (it had no effect) | v8.2.0 |
| `INC_INLET_USENORMAL` | `INLET_USE_NORMAL` (now works for all solvers) | v8.3.0 |
| `RAMP_OUTLET_PRESSURE`, `RAMP_OUTLET_PRESSURE_COEFF` | `RAMP_OUTLET`, `RAMP_OUTLET_COEFF` | v8.3.0 |
| `RAMP_ROTATING_FRAME`, `RAMP_ROTATING_FRAME_COEFF` | `RAMP_MOTION_FRAME`, `RAMP_MOTION_FRAME_COEFF` | v8.3.0 |
| `DATADRIVEN_INITIAL_DENSITY`, `DATADRIVEN_INITIAL_ENERGY` (added in v8.2.0) | Removed, no replacement | v8.5.0 |

The FEA solver now uses the same time options as the flow solver. A dynamic structural case needs `TIME_DOMAIN= YES`, `TIME_STEP` and `MAX_TIME`.

Removed option values (v8.0.0):

- `CONV_NUM_METHOD_FLOW= CUSP`. Use `JST` or an upwind scheme.
- `TIME_DISCRE_FEA= CD_EXPLICIT` and `GENERALIZED_ALPHA`. Only `NEWMARK_IMPLICIT` is left.
- `DV_KIND= FFD_TWIST_2D`. It was never implemented.
- `OBJECTIVE_FUNCTION= FLOW_ANGLE_OUT` and `MASS_FLOW_IN` (turbomachinery).

These turbulence settings changed in v7.4.0. The v7 guide does not cover them, and older v7 configs may still use them:

| Old setting | New setting |
| --- | --- |
| `KIND_TURB_MODEL= SA_NEG` | `KIND_TURB_MODEL= SA`, `SA_OPTIONS= NEGATIVE, WITHFT2` |
| `KIND_TURB_MODEL= SA_E` | `KIND_TURB_MODEL= SA`, `SA_OPTIONS= EDWARDS` |
| `KIND_TURB_MODEL= SA_COMP` | `KIND_TURB_MODEL= SA`, `SA_OPTIONS= COMPRESSIBILITY` |
| `KIND_TURB_MODEL= SA_E_COMP` | `KIND_TURB_MODEL= SA`, `SA_OPTIONS= EDWARDS, COMPRESSIBILITY, EXPERIMENTAL` |
| `KIND_TURB_MODEL= SST_SUST` | `KIND_TURB_MODEL= SST`, `SST_OPTIONS= SUSTAINING` |
| `KIND_TRANS_MODEL= BC` | `KIND_TURB_MODEL= SA`, `SA_OPTIONS= BCM` |

The `SA_NEG` row selects standard SA-neg, including ft2. To request negative SA without ft2, use
`SA_OPTIONS= NEGATIVE, EXPERIMENTAL`; this is a different formulation and can change the results.
Edwards with a compressibility correction also needs `EXPERIMENTAL`, because it is not a standard TMR
combination. See [Turbulence Models](../Turbulence-Models/#combinations-that-su2-accepts).

### Changed defaults and behaviour

| What | Before | Now | Release |
| --- | --- | --- | --- |
| SST version when `SST_OPTIONS` names none | SST-1994m | SST-2003m | v8.0.0 |
| `MUSCL_FLOW= YES` (or `MUSCL_ADJFLOW= YES`) with a centered scheme | Ignored | Error. Remove the line or set it to `NO`. | v8.0.0 |
| Restart files (`WRT_RESTART_COMPACT`, new option, default `YES`) | All volume output fields | Only the fields needed to restart | v8.2.0 |
| Default file names (`RESTART_FILENAME`, `SOLUTION_FILENAME`, ...) | `restart.dat`, `solution.dat`, ... | `restart`, `solution`, ... SU2 adds the extension. | v8.3.0 |
| `MGLEVEL` | Exact number of coarse levels | Maximum. Levels with fewer than `MG_MIN_MESHSIZE` (500) points are dropped. | v8.5.0 |
| `MG_PRE_SMOOTH`, `MG_POST_SMOOTH` | Fixed number of smoothing steps | Maximum. The smoother stops early (`MG_SMOOTH_EARLY_EXIT= YES`). | v8.5.0 |
| `MG_DAMP_RESTRICTION`, `MG_DAMP_PROLONGATION` | 0.75, fixed | 0.5, used as a start value and adapted during the run | v8.5.0 |

Notes:

- **SST.** To keep the old model, set `SST_OPTIONS= V1994m`. In v8.0.0 the 1994m model itself also changed to match the literature, so old SST-1994m results are not reproduced exactly.
- **Restart files.** With compact restarts, extra fields such as pressure or skin friction are no longer in the restart file. They are still in the visualization files. Set `WRT_RESTART_COMPACT= NO` if your scripts read these fields from the restart file. See [Restart File](../Restart-File/).
- **File names.** Give file names without an extension. If you give the expected extension, SU2 removes it. A different extension stays part of the name.
- **Multigrid.** `MG_SMOOTH_EARLY_EXIT= NO` gives fixed smoothing and fixed damping again. To also get the old damping values, set `MG_DAMP_RESTRICTION` and `MG_DAMP_PROLONGATION` to 0.75.

### Changes that affect results

Many fixes in v8 change the converged solution a little, mostly for turbulent flows. Do not expect v7 and v8 to give the same forces. The main ones:

- SST: the default changed to SST-2003m and SST-1994m was corrected (v8.0.0). SST-2003 had important fixes (v8.2.0). The cross-diffusion term has a new discretization (v8.3.0).
- SA: corrections to the SA and SA-neg models (v8.0.0, v8.1.0). The nonlinear diffusion term has a new discretization (v8.3.0).
- Symmetry planes: corrected (v8.1.0). Intersecting and curved symmetry planes and inviscid walls work better (v8.2.0).
- Multigrid: new smoothing and damping rules (v8.5.0), see above.

### Python wrapper

The Python wrapper was rewritten in v8.0.0. Scripts written for v7 need changes. Many methods have new names, for example:

| v7 | v8 |
| --- | --- |
| `Postprocessing()` | `Finalize()` |
| `GetNumberVertices(iMarker)` | `GetNumberMarkerNodes(iMarker)` |
| `SetVertexTemperature(...)` | `SetMarkerCustomTemperature(...)` |

Methods that set boundary conditions now start with `SetMarkerCustom`. The [Python wrapper test cases](https://github.com/su2code/SU2/tree/master/TestCases/py_wrapper) show the current interface.

### Build and tools

- The old autotools build (`configure`, `make`) was removed in v8.0.0. Build with meson. See [Build SU2 on Linux/MacOS](../Build-SU2-Linux-MacOS/).
- Some old Python scripts were removed in v8.0.0: `compute_multipoint.py`, `compute_stability.py`, `config_gui.py` and `convert_to_csv.py`.
- v8.5.0 uses PaStiX version 6 (`-Denable-pastix=true`) and CoolProp 7.2.0. The release binaries now include OpenMP, and the default compiler optimization is stronger.

---

## New features by area

Many bug fixes and small improvements are not listed. See the [GitHub release notes](https://github.com/su2code/SU2/releases) for all changes.

### Solvers and models

- **Combustion.** Flamelet model for premixed flames: `KIND_SCALAR_MODEL= FLAMELET` with `FLUID_MODEL= FLUID_FLAMELET` (v8.0.0). Preferential diffusion (`PREFERENTIAL_DIFFUSION`) and spark ignition (`FLAME_INIT_METHOD= SPARK`) (v8.1.0). See [Species Transport and Combustion](../Setup-Guide-Species-Combustion/) and the tutorials [Laminar Combustion](/tutorials/Inc_Combustion/) and [Counterflow Diffusion Flame](https://su2code.github.io/tutorials/Inc_Laminar_Diffusion_Flame/).
- **Data-driven fluid model.** `FLUID_MODEL= DATADRIVEN_FLUID` with look-up tables or neural networks (`INTERPOLATION_METHOD= LUT` or `MLP`) (v8.0.0). Physics-informed networks with `USE_PINN` (v8.2.0). See [NICFD](../Setup-Guide-NICFD/) and the tutorial [Physics-informed neural networks](/tutorials/NICFD_nozzle_datadriven/).
- **Species transport.** Custom wall conditions with `MARKER_WALL_SPECIES` (v8.4.0). Adaptive CFL now also covers species (v8.1.0).
- **NEMO.** Ionization for viscous flows (v8.0.0). See [Thermochemical Nonequilibrium](../Thermochemical-Nonequilibrium/).
- **SST.** Compressibility corrections `SST_OPTIONS= COMPRESSIBILITY-WILCOX` or `COMPRESSIBILITY-SARKAR` (v8.1.0). Lower limits relative to the free stream with `SST_OPTIONS= DIMENSIONLESS_LIMIT`, `LOWER_LIMIT_K_FACTOR` and `LOWER_LIMIT_OMEGA_FACTOR` (v8.1.0). Rough-wall models with `KIND_ROUGHSST_MODEL` and `WALL_ROUGHNESS` (v8.4.0).
- **SA.** Source terms for 2D axisymmetric flows (v8.1.0).
- **Hybrid RANS/LES.** Stochastic backscatter model (`STOCHASTIC_BACKSCATTER`), `ENFORCE_LES`, `LES_FILTER_WIDTH` and the low-dissipation scheme `LD2` (v8.5.0). See [Unsteady and DES](../Setup-Guide-Unsteady-DES/).
- **Compressible flow.** Conductivity models other than `CONSTANT_PRANDTL` (`CONDUCTIVITY_MODEL`) (v8.4.0).
- **Incompressible flow.** Temperature limits with `TEMPERATURE_LIMITS` (v8.4.0). Preconditioning for multicomponent flows (v8.4.0). See [Incompressible](../Setup-Guide-Incompressible/).
- **Boundary conditions.** SA inlet based on local conditions (v8.0.0). Supersonic inlet profiles (v8.1.0). `INLET_USE_NORMAL` for compressible inlets (v8.3.0).
- **Actuator disks and engines.** Blade element actuator disk, `ACTDISK_TYPE= BLADE_ELEMENT` (v8.0.1). Engine mass flow coupling for zero-thrust cases, `ENGINE_EXHAUST_TO_INLET` (v8.5.0).
- **Gusts.** Gust encounter for 3D meshes and free-flying elastic aircraft, `GUST_DIR= Z_DIR` (v8.0.0).
- **Turbomachinery.** New turbomachinery outputs (v8.0.1). New interfaces between rows and `TURBO_PERF_KIND` (v8.1.0). New ramps (v8.3.0, v8.4.0). See [Turbomachinery](../Setup-Guide-Turbomachinery/) and the tutorial [Aachen Turbine](/tutorials/Aachen_Turbine/).
- **Structural solver.** Thermal expansion (`MATERIAL_THERMAL_EXPANSION_COEFF`, `MATERIAL_REFERENCE_TEMPERATURE`) and centrifugal forces (`CENTRIFUGAL_FORCE`) (v8.2.0).
- **Stopping a run.** SIGTERM stops the run and writes the output files (v8.1.0).

### Numerics

- **Limiters.** Nishikawa limiters `NISHIKAWA_R3`, `NISHIKAWA_R4` and `NISHIKAWA_R5` (v8.0.0). See [Slope Limiters](../Slope-Limiters-and-Shock-Resolution/).
- **MUSCL.** Kappa scheme with `MUSCL_KAPPA_FLOW`, `MUSCL_KAPPA_TURB` and related options (v8.4.0). The default 0 keeps the previous scheme. MUSCL ramp with `RAMP_MUSCL` and `KIND_MUSCL_RAMP` (v8.4.0).
- **MSW scheme.** Uses a pressure sensor, set with `MSW_ALPHA` (v8.5.0). See [Convective Schemes](../Convective-Schemes/).
- **CFL.** `CFL_ADAPT_PARAM` takes a sixth value: the iteration where adaptation starts (v8.2.0).
- **Robustness.** Limits on the solution update: `MAX_UPDATE_FLOW`, `MAX_UPDATE_SA`, `MAX_UPDATE_SST`. Exact turbulence Jacobians with `USE_ACCURATE_TURB_JACOBIANS` (v8.3.0).
- **Linear solvers.** `LINEAR_SOLVER= FGCRODR` with `LINEAR_SOLVER_RESTART_DEFLATION` (v8.4.0). Nested preconditioning with `LINEAR_SOLVER_INNER` (v8.4.0). Newton-Krylov improvements (v8.4.0). Level scheduling for OpenMP ILU, `LINEAR_SOLVER_ILU_LEVEL_SCHEDULING` (v8.5.0). See [Linear Solvers and Preconditioners](../Linear-Solvers-and-Preconditioners/).
- **Multigrid.** New options `MG_MIN_MESHSIZE`, `MG_SMOOTH_EARLY_EXIT`, `MG_SMOOTH_RES_THRESHOLD` and `MG_SMOOTH_COEFF` (v8.5.0).
- **Mesh deformation and shape design.** RBF mesh deformation, `DEFORM_KIND= RBF` (v8.3.0). Camber line Hicks-Henne design variable, `DV_KIND= HICKS_HENNE_CAMBER` (v8.3.0). See [Shape Optimization](../Setup-Guide-Shape-Optimization/).

### Output

- Custom outputs (functions of other outputs) with `CUSTOM_OUTPUTS`, for all solvers (v8.0.0). See [Custom Output](../Custom-Output/).
- New volume fields: local time step and CFL, velocity for compressible flow, thermal conductivity, heat capacity and diffusivity (v8.0.0).
- `CUR_TIME` is in the default history output of unsteady runs (v8.0.1). `ITER_TIME` gives the wall time per iteration (v8.5.0).
- Compact restart files and `VOLUME_OUTPUT= COMPACT` (v8.2.0).
- Wall heat fluxes are reported as imposed by the wall boundary condition (v8.2.0).

### Adjoint and AD

- Faster hybrid parallel (MPI + OpenMP) discrete adjoint (v8.0.0, v8.0.1).
- Tape debug mode with `CHECK_TAPE_TYPE` and `CHECK_TAPE_VARIABLES` (v8.3.0).
- Discrete adjoint of thermoelastic problems (v8.5.0). The Newton-Krylov adjoint uses FGCRODR (v8.5.0).
- The FADO optimization framework is installed with SU2 (v8.2.0).

### Multizone and multiphysics

- Solid-to-solid heat transfer with contact resistance, `CHT_INTERFACE_CONTACT_RESISTANCE` (v8.1.0). See the tutorial [Contact Resistance CHT](/tutorials/SS_CR_CHT/).
- Coupled thermoelasticity (v8.2.0). `MARKER_CREATE_COPY` makes thermoelastic setups simpler (v8.5.0).
- See [Multizone](../Multizone/) and [Heat Transfer and CHT](../Setup-Guide-Heat-Transfer-CHT/).

### Performance

- FGMRES on GPUs with CUDA: build with `-Denable-cuda=true` and set `ENABLE_CUDA= YES` (v8.3.0).
- Better OpenMP performance: adaptive edge color group size (v8.0.1) and more parallel regions.
- Profiling with Tracy (v8.3.0) and gprof (`-Denable-gprof=true`, v8.1.0). See [Tracy Integration](../Tracy-Integration/).

### Python wrapper

- Rewritten in v8.0.0. Python scripts can deform the mesh in memory, read and set the solution and primitive variables in the volume and on markers, read all history outputs, set custom boundary conditions, set the angles of attack and sideslip, and choose the zone in multizone cases.
- Custom inlets (v8.1.0). Custom source terms for all solvers with `PYTHON_CUSTOM_SOURCE` (v8.3.0). Source terms for the heat solver (v8.4.0).
- See [Execution](../Execution/) and the tutorials [Dynamic FSI with Python](/tutorials/Dynamic_FSI_Python/) and [User Defined Combustion Model](/tutorials/TFC_python/).

---

## Migrating a v7 config

1. Run the config with v8. SU2 lists every unknown option and often the replacement. Fix them with the tables above and [Renamed and Removed Options](../Renamed-Options/).
2. For FEA dynamic cases, replace `DYNAMIC_ANALYSIS`, `DYN_TIMESTEP` and `DYN_TIME` with `TIME_DOMAIN`, `TIME_STEP` and `MAX_TIME`.
3. For SST cases, decide on the version. Add `SST_OPTIONS= V1994m` only if you must stay close to old results. Otherwise use the new default, SST-2003m.
4. Replace `KIND_TURB_MODEL` values like `SA_NEG` or `SST_SUST` with `SA_OPTIONS` or `SST_OPTIONS`.
5. Remove `MUSCL_FLOW= YES` from cases with a centered scheme (`JST`, `LAX-FRIEDRICH`). Replace `CUSP` with another scheme.
6. If you read fields other than the solution from restart files, set `WRT_RESTART_COMPACT= NO`.
7. Write file names without an extension.
8. With multigrid, check the number of levels SU2 prints at the start. Set `MG_SMOOTH_EARLY_EXIT= NO` if you need the old smoothing.
9. Update Python wrapper scripts to the new method names.
10. Build from source with meson, not autotools.
11. Compare the results with your v7 results. Small differences are expected for turbulent cases.

---

Last checked against SU2 release v8.5.0.
