---
title: "Setup Guide: Unsteady Flows and DES"
permalink: /docs_v7/Setup-Guide-Unsteady-DES/
---

{% include setup-guide-intro.md %}

---

- [When to use this guide](#when-to-use-this-guide)
- [Start from](#start-from)
- [Settings that matter](#settings-that-matter)
- [Check convergence and results](#check-convergence-and-results)
- [Common problems](#common-problems)
- [Related tutorials and test cases](#related-tutorials-and-test-cases)

---

## When to use this guide

Use this guide when the flow changes in time and you want to follow that change. Typical cases are:

- vortex shedding behind a bluff body or a stalled airfoil,
- buffet, large separated regions, wakes,
- bodies that move, such as a pitching airfoil.

The guide covers two approaches:

- **URANS** (unsteady RANS): the RANS equations solved in time. The turbulence model still models all turbulent eddies. URANS captures large, regular unsteadiness such as vortex shedding (advice).
- **DES** (detached eddy simulation), a hybrid RANS/LES method: RANS near the walls, large-eddy simulation (LES) in separated regions. In LES, the mesh and the time step resolve the large turbulent eddies and the model handles only the small ones (advice).

A steady RANS run that does not converge can be a sign that the flow is unsteady (advice). For steady settings, see [Setup Guide: Steady RANS for External Aerodynamics](../Setup-Guide-RANS-External-Aero/).

## Start from

### URANS

This config comes from the unsteady NACA0012 tutorial: `compressible_flow/Unsteady_NACA0012/unsteady_naca0012.cfg` in the [Tutorials repository](https://github.com/su2code/Tutorials/blob/develop/compressible_flow/Unsteady_NACA0012/unsteady_naca0012.cfg).
We changed `RESTART_SOL` to `NO` and removed `RESTART_ITER`, so the run starts from the free stream. The tutorial restarts at time step 499 to skip the start-up phase. We also removed the adjoint and file name options. All other values are unchanged.

```
% ------------- Problem ------------------------------------------------%
SOLVER= RANS
KIND_TURB_MODEL= SA
REF_DIMENSIONALIZATION= DIMENSIONAL
MATH_PROBLEM= DIRECT
RESTART_SOL= NO
%
% ------------- Free stream --------------------------------------------%
MACH_NUMBER= 0.3
AOA= 17.0
FREESTREAM_TEMPERATURE= 293.0
FREESTREAM_PRESSURE= 101325.0
REYNOLDS_NUMBER= 1000.0
REYNOLDS_LENGTH= 1.0
REF_ORIGIN_MOMENT_X= 0.25
REF_ORIGIN_MOMENT_Y= 0.00
REF_ORIGIN_MOMENT_Z= 0.00
REF_LENGTH= 1.0
REF_AREA= 1.0
%
% ------------- Boundary conditions ------------------------------------%
MARKER_HEATFLUX= ( airfoil, 0.0 )
MARKER_FAR= ( farfield )
MARKER_PLOTTING= ( airfoil )
MARKER_MONITORING= ( airfoil )
%
% ------------- Time integration (dual time stepping) ------------------%
TIME_DOMAIN= YES
TIME_MARCHING= DUAL_TIME_STEPPING-2ND_ORDER
TIME_STEP= 5e-4
TIME_ITER= 2000
INNER_ITER= 10
%
% ------------- Numerics -----------------------------------------------%
NUM_METHOD_GRAD= WEIGHTED_LEAST_SQUARES
CONV_NUM_METHOD_FLOW= JST
JST_SENSOR_COEFF= ( 0.5, 0.005 )
CONV_NUM_METHOD_TURB= SCALAR_UPWIND
MUSCL_TURB= NO
TIME_DISCRE_FLOW= EULER_IMPLICIT
TIME_DISCRE_TURB= EULER_IMPLICIT
CFL_NUMBER= 1e12
CFL_ADAPT= NO
LINEAR_SOLVER= FGMRES
LINEAR_SOLVER_ERROR= 0.1
LINEAR_SOLVER_ITER= 10
%
% ------------- Convergence inside each time step ----------------------%
CONV_FIELD= REL_RMS_DENSITY
CONV_RESIDUAL_MINVAL= -3
CONV_STARTITER= 0
%
% ------------- Time averages and convergence in time ------------------%
WINDOW_CAUCHY_CRIT= YES
WINDOW_START_ITER= 500
WINDOW_FUNCTION= HANN_SQUARE
CONV_WINDOW_FIELD= ( TAVG_DRAG, TAVG_LIFT )
CONV_WINDOW_STARTITER= 0
CONV_WINDOW_CAUCHY_EPS= 1E-4
CONV_WINDOW_CAUCHY_ELEMS= 10
%
% ------------- Input and output ---------------------------------------%
MESH_FILENAME= unsteady_naca0012_mesh.su2
MESH_FORMAT= SU2
HISTORY_WRT_FREQ_INNER= 0
SCREEN_WRT_FREQ_INNER= 100
SCREEN_OUTPUT= ( TIME_ITER, INNER_ITER, RMS_DENSITY, REL_RMS_DENSITY, DRAG, LIFT, CAUCHY_TAVG_DRAG, CAUCHY_TAVG_LIFT )
HISTORY_OUTPUT= ( TIME_ITER, INNER_ITER, REL_RMS_RES, RMS_RES, AERO_COEFF, TAVG_AERO_COEFF, CAUCHY )
OUTPUT_FILES= ( RESTART, PARAVIEW )
OUTPUT_WRT_FREQ= ( 1, 1 )
```

The tutorial page [Unsteady NACA0012](/tutorials/Unsteady_NACA0012/) explains dual time stepping and the windowed averages.

### DES

This config comes from the DDES regression test [`TestCases/ddes/flatplate/ddes_flatplate.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/ddes/flatplate/ddes_flatplate.cfg). We removed the adjoint and file name options, and options that have no effect with these settings. All other values are unchanged.
This is a 2D flat plate. It checks that the DES options run. It is not a realistic DES: real DES runs are 3D (see [Mesh for DES](#mesh-for-des)).

```
% ------------- Problem ------------------------------------------------%
SOLVER= RANS
KIND_TURB_MODEL= SA
HYBRID_RANSLES= SA_EDDES
MATH_PROBLEM= DIRECT
RESTART_SOL= NO
%
% ------------- Free stream --------------------------------------------%
MACH_NUMBER= 0.2
AOA= 0.0
SIDESLIP_ANGLE= 0.0
FREESTREAM_TEMPERATURE= 300.0
REYNOLDS_NUMBER= 5000000.0
REYNOLDS_LENGTH= 1.0
REF_ORIGIN_MOMENT_X= 0.25
REF_ORIGIN_MOMENT_Y= 0.00
REF_ORIGIN_MOMENT_Z= 0.00
REF_LENGTH= 1.0
REF_AREA= 2.0
%
% ------------- Time integration ---------------------------------------%
TIME_DOMAIN= YES
TIME_MARCHING= DUAL_TIME_STEPPING-2ND_ORDER
TIME_STEP= 0.000288
MAX_TIME= 10
UNST_CFL_NUMBER= 0.0
INNER_ITER= 20
TIME_ITER= 500
%
% ------------- Boundary conditions ------------------------------------%
MARKER_HEATFLUX= ( wall, 0.0 )
MARKER_INLET= ( inlet, 302.4, 118309.784, 1.0, 0.0, 0.0 )
MARKER_OUTLET= ( outlet, 115056.0, farfield, 115056.0 )
MARKER_SYM= ( symmetry )
MARKER_PLOTTING= ( wall )
MARKER_MONITORING= ( wall )
%
% ------------- Numerics -----------------------------------------------%
NUM_METHOD_GRAD= GREEN_GAUSS
CFL_NUMBER= 10.0
CFL_ADAPT= NO
CONV_NUM_METHOD_FLOW= SLAU2
MUSCL_FLOW= YES
SLOPE_LIMITER_FLOW= NONE
TIME_DISCRE_FLOW= EULER_IMPLICIT
CONV_NUM_METHOD_TURB= SCALAR_UPWIND
MUSCL_TURB= NO
TIME_DISCRE_TURB= EULER_IMPLICIT
CONV_RESIDUAL_MINVAL= -15
CONV_STARTITER= 0
%
% ------------- Input and output ---------------------------------------%
MESH_FILENAME= mesh_flatplate_turb_137x97.su2
MESH_FORMAT= SU2
OUTPUT_WRT_FREQ= 1000
SCREEN_OUTPUT= (TIME_ITER, INNER_ITER, RMS_DENSITY, RMS_NU_TILDE, LIFT, DRAG, TOTAL_HEATFLUX)
```

For a real DES run, also write the DES and time-average fields (code):

```
VOLUME_OUTPUT= ( COORDINATES, SOLUTION, PRIMITIVE, DDES, VORTEX_IDENTIFICATION, TIME_AVERAGE )
```

The mesh files of the test cases are in the [TestCases repository](https://github.com/su2code/TestCases).

## Settings that matter

### Dual time stepping

Dual time stepping splits the run into physical time steps. Inside each time step, SU2 runs "inner iterations" to find the new solution, the same way it converges a steady problem (tutorial, docs).

- `TIME_DOMAIN= YES` turns on the time-accurate solver (docs). `TIME_MARCHING= DUAL_TIME_STEPPING-2ND_ORDER` is used by the URANS test cases and by the flat plate and backscatter DES tests (test case). The short ONERA M6 DES regression tests of PR #2150 use `DUAL_TIME_STEPPING-1ST_ORDER` (test case). `DUAL_TIME_STEPPING-1ST_ORDER` and `TIME_STEPPING` (one update per time step, no inner iterations) also exist (code).
- `TIME_STEP` is the physical time step. It is always in seconds, also when the equations are non-dimensional: SU2 divides it by the reference time (code).
- `TIME_ITER` is the number of time steps. The default is `1` (code).
- `MAX_TIME` is the final physical time in seconds. The default is `1.0`. SU2 stops at `MAX_TIME` or at `TIME_ITER`, whichever comes first (code, docs). Set `MAX_TIME` larger than `TIME_STEP` × `TIME_ITER` if you want `TIME_ITER` steps.
- `INNER_ITER` is the maximum number of inner iterations per time step. The default is `1` (code). Always set it.
- Do not use `ITER` in an unsteady run. SU2 stops with an error and asks for `TIME_ITER` and `INNER_ITER` (code).
- With `UNST_CFL_NUMBER` other than `0.0`, SU2 computes the time step from this CFL number and ignores `TIME_STEP`, as the comments in `config_template.cfg` say. The default is `0.0` (code).

See [Solver Setup](../Solver-Setup/#time-dependent-simulation).

### Time step size

- The time step must resolve the fastest change you care about (advice). For vortex shedding, estimate the period from the Strouhal number St = f D / U. St is about 0.2 for many bluff bodies (advice, to be reviewed).
- Use at least 50 to 100 time steps per shedding period for URANS (advice, to be reviewed).
- Check the result by halving the time step: the period and the averaged forces should not change much (advice).
- Examples: the NACA0012 tutorial uses `TIME_STEP= 5e-4`. The square cylinder test uses `TIME_STEP= 0.0015` with `MAX_TIME= 3.75`. The von Karman cylinder tutorial uses `TIME_STEP= 0.005` with 20 inner iterations (tutorial, test case).

### Convergence inside each time step

Each time step needs converged inner iterations. If not, the time history is wrong even if the run looks stable (tutorial).

- The inner loop uses the same criteria as a steady run: `CONV_FIELD`, `CONV_RESIDUAL_MINVAL`, `CONV_STARTITER` (docs). It stops at the criterion or at `INNER_ITER`.
- `REL_RMS_DENSITY` is the residual relative to its value at the first inner iteration of the time step (code). `CONV_FIELD= REL_RMS_DENSITY` with `CONV_RESIDUAL_MINVAL= -3` asks for a drop of three orders of magnitude in each time step (tutorial).
- Set `CONV_STARTITER= 0` so the check starts at the first inner iteration (tutorial). The default is `5` (code).
- The inner iterations use `CFL_NUMBER` as in a steady run. The NACA0012 tutorial uses `CFL_NUMBER= 1e12` with `JST` (tutorial). The DES test uses `10` with `SLAU2`, the square cylinder test `2.0` with `ROE` (test case).
- Watch `INNER_ITER` on the screen. If most time steps end at the maximum without reaching the criterion, raise `INNER_ITER` or the CFL, or lower the time step (advice).
- In a time-domain run, SU2 writes the history file once per time step by default. Set `HISTORY_WRT_FREQ_INNER` to also write inner iterations (code).

### Restarting an unsteady run

SU2 writes one restart file per saved time step, with the step number in the name, for example `restart_flow_00499.dat` (tutorial, docs).

- `OUTPUT_WRT_FREQ` sets how often (in time steps) SU2 writes files (docs). With second-order time stepping, SU2 also writes the step before, because a restart needs two old solutions (code).
- To restart, set `RESTART_SOL= YES` and `RESTART_ITER` to the first new time step. With second order, SU2 reads the files of steps `RESTART_ITER`−2 and `RESTART_ITER`−1. With first order, it reads step `RESTART_ITER`−1 (code, docs).
- SU2 reads the files named after `SOLUTION_FILENAME`, so rename or copy the restart files first (docs).
- `TIME_ITER` counts from the start of the whole simulation, not from the restart. SU2 runs `TIME_ITER` − `RESTART_ITER` more steps (code). `TIME_ITER` must be larger than `RESTART_ITER` (code).
- To start URANS from a converged steady solution, copy the steady restart file to the two file names that SU2 reads for `RESTART_ITER= 2` (for example `solution_flow_00000.dat` and `solution_flow_00001.dat`) (advice, to be reviewed). The square cylinder test restarts with `RESTART_ITER= 2` (test case).

See [Restart File](../Restart-File/).

### Time averages and convergence in time

**History averages.** In a time-domain run, SU2 adds a time-averaged version of every coefficient, with the prefix `TAVG_`, for example `TAVG_DRAG` (code, tutorial).

- The average starts at time step `WINDOW_START_ITER`. If you do not set it, it starts at `RESTART_ITER`. It must not be smaller than `RESTART_ITER`, or SU2 stops with an error (code).
- Start the average after the start-up phase, when the signal is periodic or statistically steady (tutorial).
- `WINDOW_FUNCTION` sets the weight of each sample: `SQUARE` (equal weights, the default), `HANN`, `HANN_SQUARE` or `BUMP` (code). For a periodic signal, the windowed averages converge faster than `SQUARE` (tutorial).

**Stop when the average stops changing.** `WINDOW_CAUCHY_CRIT= YES` turns on a Cauchy criterion on the averages (docs). This criterion looks at how much the average changes from step to step.

- `CONV_WINDOW_FIELD` lists the averaged fields, for example `( TAVG_DRAG, TAVG_LIFT )` (tutorial).
- `CONV_WINDOW_CAUCHY_EPS` (default `1E-3`), `CONV_WINDOW_CAUCHY_ELEMS` (default `100`) and `CONV_WINDOW_STARTITER` (default `15`, counted from `WINDOW_START_ITER`) play the same role as `CONV_CAUCHY_EPS`, `CONV_CAUCHY_ELEMS` and `CONV_STARTITER` in a steady run (code, docs).
- The tutorial uses `CONV_WINDOW_CAUCHY_EPS= 1E-4` with `CONV_WINDOW_CAUCHY_ELEMS= 10` (tutorial).

**Volume averages.** Add `TIME_AVERAGE` to `VOLUME_OUTPUT` (code). SU2 then writes:

- mean values: `MEAN_DENSITY`, `MEAN_VELOCITY-X`, `MEAN_VELOCITY-Y`, `MEAN_VELOCITY-Z`, `MEAN_PRESSURE`, `MEAN_SKIN_FRICTION-X`, `MEAN_SKIN_FRICTION-Y`, `MEAN_SKIN_FRICTION-Z`;
- mean squares and products: `RMS_U`, `RMS_V`, `RMS_W`, `RMS_UV`, `RMS_UW`, `RMS_VW`, `RMS_P`;
- Reynolds stresses and pressure fluctuations: `UUPRIME`, `VVPRIME`, `WWPRIME`, `UVPRIME`, `UWPRIME`, `VWPRIME`, `PPRIME` (code).

How these averages work (code):

- They start at `WINDOW_START_ITER` and use equal weights. `WINDOW_FUNCTION` does not apply to them.
- SU2 only computes them if `TIME_AVERAGE` is in `VOLUME_OUTPUT`.
- SU2 keeps them in memory. They are not read back from the restart files, so after a restart they start again from `RESTART_ITER`.

So average over one continuous run, without restarts (advice).

### Hybrid RANS/LES: which DES variant

The `SA_*` variants build on the SA model, the `SST_*` variants on the SST model. Set `KIND_TURB_MODEL` and pick a matching variant with `HYBRID_RANSLES` (code). The SST variants come with [PR #2150](https://github.com/su2code/SU2/pull/2150) and are in develop once it is merged.

In original `SA_DES`, the length scale is min(d, C_DES Δ), where d is wall distance and Δ the grid measure. The delayed variants use d − f_d·max(0, d − C_DES Δ): f_d near zero protects attached boundary layers, and f_d near one recovers the DES limit. The SST variants use the same idea with the RANS length √k / (β* ω) in place of d. The grid measure also changes with the variant. Thus distance from the wall alone does not determine the RANS/LES mode (code, reference). See [Hybrid RANS/LES](../Hybrid-RANS-LES/#what-su2-does-differently-from-the-literature).

| `HYBRID_RANSLES` | What it is (code) |
| --- | --- |
| `NONE` | No DES (default). |
| `SA_DES` | Original DES (Spalart 1997). Switches to LES wherever the cell size times `DES_CONST` is below the wall distance. |
| `SA_DDES` | Delayed DES (Spalart et al. 2006). A shielding function keeps attached boundary layers in RANS mode. |
| `SA_ZDES` | DDES with a cell size based on the vorticity direction (Deck 2012). |
| `SA_EDDES` | DDES with a cell size adapted to shear layers (Shur et al. 2015). Meant to switch faster from RANS to LES in separated shear layers. |
| `SST_DDES` | DDES for SST (Gritskevich et al. 2012). |
| `SST_IDDES` | Improved DDES for SST (Gritskevich et al. 2012), with a wall-modelled LES branch. |
| `SST_SIDDES` | Simplified IDDES: IDDES without the elevating function. |
| `SST_EDDES` | `SST_DDES` with the shear-layer-adapted cell size of `SA_EDDES`. |

Advice:

- `SA_DES` can switch to LES inside an attached boundary layer if the mesh is fine along the wall. The mesh, not the flow, can then cause separation. `SA_DDES` and `SA_EDDES` add shielding to reduce this risk; the result still needs mesh and sensor checks (advice).
- `SA_ZDES` in SU2 is DDES with the ZDES cell size. It is not the full zonal method of the reference, where the user picks RANS and LES zones (code, to be reviewed).
- SU2 stops with an error if the variant does not match `KIND_TURB_MODEL`, or if `TIME_DOMAIN= NO` (code).

Related options (code):

- `DES_CONST`: the DES constant. The default is `0.65`.
- `LES_FILTER_WIDTH`: a fixed LES filter width. The default `-1.0` means SU2 uses the local cell size (the largest distance from a point to its neighbours).
- `ENFORCE_LES= YES`: LES mode everywhere. It needs `HYBRID_RANSLES` other than `NONE`.
- These three options act only on the `SA_*` variants. The `SST_*` variants ignore them, without a warning (code).
- `STOCHASTIC_BACKSCATTER= YES` and the `SBS_` options: a stochastic backscatter model, which feeds energy from the modelled to the resolved scales. It works only in 3D and only with an `SA_*` variant. SU2 does not stop if you use it with an `SST_*` variant. The test case `backscatter/backward_step/backwardStep.cfg` shows all its options (code, test case).

### Mesh for DES

General points for the DES mesh (advice, to be reviewed):

- DES resolves turbulent eddies, which are three-dimensional. Run DES in 3D. 2D DES runs do not give physical turbulence.
- Near the walls, the mesh must be fine enough for RANS: first-cell y+ about 1.
- In the regions you want in LES mode (wakes, separated zones), use cells of similar size in all directions. Original DES/DDES use the longest edge from a node to its neighbours; ZDES/EDDES use the variant-specific measures described in [Hybrid RANS/LES](../Hybrid-RANS-LES/#what-su2-does-differently-from-the-literature) (code). Stretched cells can limit LES resolution; inspect the chosen grid measure and the RANS/LES sensor rather than assuming that refinement in one direction is sufficient.
- Keep the cell size changes smooth between the RANS and LES regions.
- For a body with a spanwise direction, the spanwise extent must hold the largest eddies of interest.

### Time step for DES

- The time step must resolve the eddies the mesh can hold. A common target is a convective CFL number of about 1 in the LES region, that is, a time step of about cell size / local velocity (advice, to be reviewed).
- Use `DUAL_TIME_STEPPING-2ND_ORDER` (test case).
- The flat plate DES test and the backscatter test use `INNER_ITER= 20` (test case). The short ONERA M6 DES regression tests use `INNER_ITER= 2` and are not a setup example. Check the inner convergence as for URANS.

### Numerical dissipation

Reduce numerical dissipation where you can. Upwind schemes and limiters add it, and in the LES region it damps the resolved eddies (advice).

**Compressible solver.** `ROE_LOW_DISSIPATION` lowers the upwind part of the flux where the flow is resolved (code, docs). Details from the code (code):

- It works with `ROE`, `SLAU` and `SLAU2`.
- `FD`: uses the DDES shielding function, computed from the wall distance.
- `NTS`: the blending of Travin and Shur. It uses `DES_CONST` and the cell size.
- `FD_DUCROS` and `NTS_DUCROS`: as above, plus the Ducros sensor, which keeps the full dissipation at shocks (code, docs).
- SU2 keeps at least 5 % of the upwind dissipation for stability.
- Write the `ROE_DISSIPATION` output group to see where the dissipation is reduced.

No test case in develop uses `ROE_LOW_DISSIPATION` (test case).

**Incompressible solver.** The `LD2` central scheme (low dissipation, low dispersion) is available for constant density flows only. With the energy equation on, SU2 uses JST for the energy equation (code). The backscatter test uses `CONV_NUM_METHOD_FLOW= LD2` with `JST_SENSOR_COEFF= ( 0.0, 0.002 )` and `MUSCL_FLOW= NO` (test case).

**Limiters.** The DES flat plate test uses MUSCL without a limiter (`SLOPE_LIMITER_FLOW= NONE`) (test case). A limiter adds dissipation where it is active (advice).

### Averaging a DES run

- Wait until the start-up phase has left the domain before you start averaging. A common rule is a few flow-through times (advice, to be reviewed).
- Then average over many characteristic times, so that the mean and the fluctuations settle (advice).
- Use `WINDOW_START_ITER` and the `TIME_AVERAGE` volume group described above (code).
- To record time signals at points, the history output can include probes defined with `CUSTOM_OUTPUTS`. The von Karman cylinder tutorial shows how (tutorial).

## Check convergence and results

- **Inner convergence.** `REL_RMS_DENSITY` (or your `CONV_FIELD`) reaches the criterion in each time step before `INNER_ITER` (tutorial).
- **Start-up phase over.** Plot `LIFT` and `DRAG` against time. The signal should be periodic or statistically steady before `WINDOW_START_ITER` (tutorial).
- **Averages settled.** Compare averages from separate sampling blocks and extend the sampling interval. A slowly changing cumulative average alone does not establish statistical convergence, especially for DES. Monitor `TAVG_LIFT` and `TAVG_DRAG`. With `WINDOW_CAUCHY_CRIT= YES`, the `CAUCHY_TAVG_` values are below `CONV_WINDOW_CAUCHY_EPS` (tutorial).
- **Time step and mesh.** Halve the time step and refine the mesh. The frequency and the averages should change little (advice).
- **DES regions.** Write the `DDES` group: `DES_LENGTHSCALE`, `WALL_DISTANCE` and `LES_SENSOR`. `LES_SENSOR` is 0 where the model acts as RANS. In LES mode it is 1 for `SA_DES` and the value of the shielding function for the SA DDES variants (code). Attached boundary layers should stay at 0 (advice). For the `SST_*` variants, `LES_SENSOR` is always 0; see [Hybrid RANS/LES](../Hybrid-RANS-LES/#recommended-use) for another check (code).
- **Resolved eddies.** Write the `VORTEX_IDENTIFICATION` group: `VORTICITY` (2D) or `VORTICITY_X`, `VORTICITY_Y`, `VORTICITY_Z` (3D), and `Q_CRITERION` (code). Iso-surfaces of `Q_CRITERION` show the resolved eddies (advice).

See [History and Solution Output](../Custom-Output/) and the [Output Fields Reference](../Output-Fields-Reference/).

## Common problems

| Symptom | Likely cause | What to try |
| --- | --- | --- |
| The run stops at 1 s of physical time. | `MAX_TIME` has a default of `1.0`. | Set `MAX_TIME` (code). |
| Only one inner iteration per time step. | `INNER_ITER` has a default of `1`. | Set `INNER_ITER` (code). |
| SU2 stops: "ITER must not be used when running multizone and/or unsteady problems". | `ITER` in an unsteady config. | Use `TIME_ITER` and `INNER_ITER` (code). |
| SU2 stops: "TIME_DOMAIN must be set to YES ..." | `TIME_MARCHING` set without `TIME_DOMAIN= YES`. | Add `TIME_DOMAIN= YES` (code). |
| SU2 stops: "Invalid value for TIME_STEP". | `TIME_STEP` is zero and `UNST_CFL_NUMBER` is `0.0`. | Set `TIME_STEP` (code). |
| The restart fails to find a file. | Wrong file names or missing step. | For `RESTART_ITER= N` with second order, provide steps N−2 and N−1, named after `SOLUTION_FILENAME` (code, docs). |
| SU2 stops: "WINDOW_START_ITER must be larger than or equal to: RESTART_ITER!" | The average would start before the restart. | Set `WINDOW_START_ITER` at or after `RESTART_ITER` (code). |
| `MEAN_` fields are missing or zero. | `TIME_AVERAGE` not in `VOLUME_OUTPUT`, or the run has not reached `WINDOW_START_ITER`. | Add `TIME_AVERAGE` and check `WINDOW_START_ITER` (code). |
| The flow stays steady and symmetric, no shedding. | Symmetric start, too much numerical dissipation, too large time step, or a coarse wake mesh. | Lower the dissipation, reduce the time step, refine the wake (advice, to be reviewed). |
| The inner iterations never reach the criterion. | Time step too large, or CFL too low for the inner loop. | Reduce `TIME_STEP`, raise `CFL_NUMBER` or `INNER_ITER` (advice). |
| DES: the boundary layer separates too early. | LES mode inside the attached boundary layer (check `LES_SENSOR`). | Use `SA_DDES` or `SA_EDDES` instead of `SA_DES`; check the cell size along the wall (advice). |
| DES: the wake looks smooth, with no resolved eddies. | Too much dissipation, or the mesh is too coarse or too stretched in the wake. | Use `ROE_LOW_DISSIPATION` or `LD2`, remove the limiter, refine the wake with near-cubic cells (advice, to be reviewed). |
| SU2 stops: "Hybrid RANS/LES models (HYBRID_RANSLES) require an unsteady simulation ...". | `HYBRID_RANSLES` set in a steady run. | Set `TIME_DOMAIN= YES` (code). |
| SU2 stops: "The hybrid RANS/LES model (HYBRID_RANSLES) must match the turbulence model ...". | An `SA_*` variant without `KIND_TURB_MODEL= SA`, or an `SST_*` variant without `KIND_TURB_MODEL= SST`. | Pick a variant that matches the turbulence model (code). |

## Related tutorials and test cases

Tutorials:

- [Unsteady NACA0012](/tutorials/Unsteady_NACA0012/): URANS, dual time stepping, windowed averages, restart after the start-up phase.
- [Unsteady von Karman vortex shedding](/tutorials/Inc_Von_Karman/): laminar incompressible cylinder; time step, inner iterations, probes.
- [Unsteady shape optimization NACA0012](/tutorials/Unsteady_Shape_Opt_NACA0012/): unsteady adjoint with windowed objective functions.

Test cases (develop branch):

- [unsteady/square_cylinder/turb_square.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/unsteady/square_cylinder/turb_square.cfg): URANS with SST and `ROE`, restart from step 2.
- [unsteady/pitching_naca64a010_rans/turb_NACA64A010.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/unsteady/pitching_naca64a010_rans/turb_NACA64A010.cfg): URANS of a pitching airfoil with SA and rigid mesh motion.
- [ddes/flatplate/ddes_flatplate.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/ddes/flatplate/ddes_flatplate.cfg): `SA_EDDES` with `SLAU2`.
- `ddes/oneram6/ddes_oneram6_*.cfg` (PR #2150): short regression tests of `SST_DDES`, `SST_IDDES`, `SST_SIDDES`, `SST_EDDES` and `SA_EDDES` on the ONERA M6 wing. See [Hybrid RANS/LES](../Hybrid-RANS-LES/#verification-and-test-cases).
- [backscatter/backward_step/backwardStep.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/backscatter/backward_step/backwardStep.cfg): incompressible `SA_DDES` with stochastic backscatter, `LD2` scheme and time-average output.

User guide pages:

- [Solver Setup](../Solver-Setup/), [Restart File](../Restart-File/), [History and Solution Output](../Custom-Output/), [Convective Schemes](../Convective-Schemes/), [Physical Definition](../Physical-Definition/).
- All options: [Option Reference](../Option-Reference/). All output fields: [Output Fields Reference](../Output-Fields-Reference/).

Source review: 22 October 2026, against [SU2 `docs_site` at `41ea6a219a`](https://github.com/rois1995/SU2/tree/41ea6a219ac038574f3d4a5b130c0c1d8af66457). The DES statements were updated on 23 October 2026 against [PR #2150 at `e9e85686ad`](https://github.com/su2code/SU2/tree/e9e85686ad3b53fb76eb912d1e8be3b521372838). See the [review scope and outstanding validation](../Documentation-Status/#guide-and-model-review). Setup recommendations remain draft where indicated.
