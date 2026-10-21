---
title: "Setup Guide: Turbomachinery"
permalink: /docs_v7/Setup-Guide-Turbomachinery/
---

> **Draft.** The settings below come from the SU2 code, the tutorials and the test cases. The advice parts need a review by experienced users.

**Source tags.** A tag at the end of a statement says where it comes from. A tag on the line that introduces a list or a table covers the whole list or table.

- **(code)**: read in the SU2 source. Option defaults come from `Common/src/CConfig.cpp`.
- **(test case)**: used in a test case config.
- **(tutorial)**: used in a tutorial.
- **(docs)**: stated in another page of this website.
- **(advice)**: general CFD practice.
- **(to be reviewed)**: added after any of the above when the statement needs a check by an experienced user.

---

- [When to use this guide](#when-to-use-this-guide)
- [Start from](#start-from)
- [Settings that matter](#settings-that-matter)
- [Check convergence and results](#check-convergence-and-results)
- [Common problems](#common-problems)
- [Related tutorials and test cases](#related-tutorials-and-test-cases)

---

## When to use this guide

Use this guide to set up a steady simulation of a blade row, or of a machine with several blade rows: compressors, turbines, stages of axial or radial machines, and linear cascades. The guide covers the turbomachinery features of the compressible solvers (`SOLVER= EULER`, `NAVIER_STOKES` or `RANS`).

Terms used below:

- **Blade row** (or zone): the mesh of one blade passage of one row, for example a stator or a rotor.
- **Mixing plane**: an interface between two rows that passes averaged flow values from one row to the next. It makes a steady stage simulation possible.
- **Span-wise section**: a band at constant height between hub and shroud. SU2 averages the flow on each band of an inlet, outlet or mixing plane.
- **Non-reflecting boundary**: a boundary that lets pressure waves leave the domain instead of bouncing back.

## Start from

The block below comes from the regression test [turbomachinery/axial_stage_2D](https://github.com/su2code/SU2/blob/develop/TestCases/turbomachinery/axial_stage_2D/Axial_stage2D.cfg). It is a 2D axial stage (a stator and a moving row) with a mixing plane, Giles boundaries and the SST model. We removed the comments, the options that the test sets to their default value, and most output settings. We also removed the options that have no effect in this setup, for example limiter settings of schemes that do not use a limiter. The mesh file `mesh_axial_stage_2d_turb.su2` is in the [TestCases repository](https://github.com/su2code/TestCases).

Main file, `Axial_stage2D.cfg`:

```
MULTIZONE= YES
CONFIG_LIST= (zone_1.cfg, zone_2.cfg)
%
SOLVER= RANS
KIND_TURB_MODEL= SST
MATH_PROBLEM= DIRECT
RESTART_SOL= NO
%
MACH_NUMBER= 0.05
FREESTREAM_PRESSURE= 140000.0
FREESTREAM_TEMPERATURE= 300.0
FREESTREAM_OPTION= TEMPERATURE_FS
FREESTREAM_TURBULENCEINTENSITY= 0.03
FREESTREAM_TURB2LAMVISCRATIO= 100.0
INIT_OPTION= TD_CONDITIONS
REF_DIMENSIONALIZATION= DIMENSIONAL
%
FLUID_MODEL= IDEAL_GAS
GAMMA_VALUE= 1.4
GAS_CONSTANT= 287.058
VISCOSITY_MODEL= SUTHERLAND
MU_REF= 1.716E-5
MU_T_REF= 273.15
SUTHERLAND_CONSTANT= 110.4
CONDUCTIVITY_MODEL= CONSTANT_PRANDTL
%
MARKER_HEATFLUX= (wall1, 0.0, wall2, 0.0)
MARKER_PERIODIC= (periodic1, periodic2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.04463756775, 0.0, periodic3, periodic4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.04463756775, 0.0)
%
MARKER_TURBOMACHINERY= (inflow, outmix, inmix, outflow)
MARKER_ANALYZE= (outflow)
MARKER_ZONE_INTERFACE= (outmix, inmix)
MARKER_MIXINGPLANE_INTERFACE= (outmix, inmix)
MARKER_GILES= (inflow, TOTAL_CONDITIONS_PT, 169623.33, 305.76, 1.0, 0.0, 0.0, 1.0, 1.0, outmix, MIXING_OUT, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, inmix, MIXING_IN, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, outflow, STATIC_PRESSURE, 99741.00, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0)
SPATIAL_FOURIER= NO
TURBOMACHINERY_KIND= AXIAL AXIAL
TURBO_PERF_KIND= TURBINE TURBINE
TURBULENT_MIXINGPLANE= YES
AVERAGE_PROCESS_KIND= MIXEDOUT
PERFORMANCE_AVERAGE_PROCESS_KIND= MIXEDOUT
MIXEDOUT_COEFF= (1.0, 1.0E-05, 15)
AVERAGE_MACH_LIMIT= 0.05
%
NUM_METHOD_GRAD= WEIGHTED_LEAST_SQUARES
CFL_NUMBER= 10.0
LINEAR_SOLVER= FGMRES
LINEAR_SOLVER_PREC= LU_SGS
LINEAR_SOLVER_ERROR= 1E-4
LINEAR_SOLVER_ITER= 10
CONV_NUM_METHOD_FLOW= ROE
MUSCL_FLOW= YES
RAMP_MUSCL= YES
RAMP_MUSCL_COEFF= (0.0, 1.0, 20.0)
SLOPE_LIMITER_FLOW= VAN_ALBADA_EDGE
ENTROPY_FIX_COEFF= 0.01
CONV_NUM_METHOD_TURB= SCALAR_UPWIND
MUSCL_TURB= NO
%
% The test stops after 21 outer iterations. Raise OUTER_ITER for a converged result.
OUTER_ITER= 21
CONV_RESIDUAL_MINVAL= -16
CONV_STARTITER= 10
SCREEN_OUTPUT= OUTER_ITER, AVG_BGS_RES[0], AVG_BGS_RES[1], RMS_DENSITY[0], RMS_ENERGY[0], RMS_DENSITY[1], RMS_ENERGY[1], SURFACE_TOTAL_PRESSURE[1], MassFlowOut_2[1], TotalStaticEfficiency[1]
MESH_FILENAME= mesh_axial_stage_2d_turb.su2
MESH_FORMAT= SU2
OUTPUT_WRT_FREQ= 1000
```

Zone file of the fixed row, `zone_1.cfg`:

```
GRID_MOVEMENT= NONE
```

Zone file of the moving row, `zone_2.cfg`. In 2D the rotor is a row that translates along y:

```
GRID_MOVEMENT= STEADY_TRANSLATION
MACH_MOTION= 0.35
TRANSLATION_RATE= 0.0 -150.0 0.0
```

For a 3D machine, start from the [Aachen turbine tutorial](/tutorials/Aachen_Turbine/) or from the test case [turbomachinery/Aachen_turbine](https://github.com/su2code/SU2/blob/develop/TestCases/turbomachinery/Aachen_turbine/aachen_3D_MP_restart.cfg). That case restarts from a solution file (`RESTART_SOL= YES`). Set `RESTART_SOL= NO` to start from scratch.

## Settings that matter

### Mesh and machine axis

- The machine axis must be the z-axis, and the flow should go in the positive z direction (tutorial). The code computes the radius as the distance from the z-axis when it builds the span-wise sections. The rotation ramp changes only the z component of `ROTATION_RATE` (code).
- Mesh one blade passage per row, and connect its sides with `MARKER_PERIODIC` (tutorial). For a rotational periodicity, give the rotation centre and the rotation angle about each axis, in degrees. The Aachen case has 41 blades per row and uses an angle of 360/41 = 8.7804878 about z (test case).
- In 3D, list the periodic pairs in `MARKER_PERIODIC` in zone order: the first pair for zone 1, the second pair for zone 2, and so on. The code that finds the span-wise sections of zone *n* looks at the *n*-th periodic pair (code, to be reviewed). All 3D test cases follow this order (test case).

### Single row or several rows

- **One row.** Use a single config file. Even with one row, you need `MARKER_TURBOMACHINERY= (inlet, outlet)` to use Giles boundaries or turbomachinery outputs (code). Example: [transonic_stator_2D](https://github.com/su2code/SU2/blob/develop/TestCases/turbomachinery/transonic_stator_2D/transonic_stator_restart.cfg) (test case).
- **Several rows.** Put each row in its own zone. Set `MULTIZONE= YES` and list one sub-config file per zone in `CONFIG_LIST`, in stream-wise order (tutorial). A sub-config file holds only the options that differ from the main file, usually the grid motion. See [Basics of Multi-Zone Computations](../Multizone/).
- In multizone runs, `OUTER_ITER` sets the number of iterations. `INNER_ITER` (default 1) is the number of iterations of each zone per outer iteration (code).

### Rotating frame or moving mesh

Choose the motion of each zone with `GRID_MOVEMENT` in its sub-config file (code):

- `ROTATING_FRAME`: the mesh does not move. SU2 solves the flow in a frame that turns with the rotor. Use it for steady simulations of rotors (tutorial). Set `ROTATION_RATE` (rad/s, vector), `MOTION_ORIGIN` and `MACH_MOTION`.
- `STEADY_TRANSLATION`: the 2D version of the above, for a row that moves along a straight line. Set `TRANSLATION_RATE` (m/s) (test case).
- `RIGID_MOTION`: the mesh really moves. This needs a time-accurate simulation (`TIME_DOMAIN= YES`) and sliding interfaces between zones (`MARKER_FLUID_INTERFACE`). See the [sliding_interface](https://github.com/su2code/SU2/tree/develop/TestCases/sliding_interface) test cases (test case). This guide does not cover unsteady rotor-stator runs.
- `NONE`: no motion, for stators.

`MACH_MOTION` is a Mach number based on the speed of the moving mesh. The [multizone page](../Multizone/) says that SU2 uses it to initialize a viscous flow from the Reynolds number, and to compute force coefficients on moving meshes (docs). The test cases use 0.35 (test case).

The Aachen and APU turbocharger test cases set `GRID_MOVEMENT= ROTATING_FRAME` without a rotation rate in the stator zones. The 2D axial stage uses `NONE`. Both run (test case).

Use `MARKER_SHROUD` to list the shroud walls. In a rotating zone, SU2 sets the grid velocity to zero on these markers, so that the shroud does not turn with the rotor (code, tutorial).

### Interfaces between rows

Every interface between two zones needs two lists. Give the markers in pairs (upstream marker, downstream marker), in stream-wise order (tutorial):

- `MARKER_ZONE_INTERFACE` tells SU2 that the two markers are connected.
- One of these two options sets the kind of interface (code):
  - `MARKER_MIXINGPLANE_INTERFACE`: mixing plane. SU2 passes averaged values for each span-wise section from one row to the next.
  - `MARKER_FLUID_INTERFACE`: frozen rotor. SU2 interpolates the local values, with no averaging (to be reviewed). The test case [multi_interface](https://github.com/su2code/SU2/blob/develop/TestCases/turbomachinery/multi_interface/multi_interface_rst.cfg) uses one interface of each kind (test case).

Mixing-plane options:

- `MIXINGPLANE_INTERFACE_KIND` sets how SU2 maps the span-wise sections of one side onto the other: `NEAREST_SPAN` (default), `LINEAR_INTERPOLATION` or `MATCHING` (code). The test cases use `LINEAR_INTERPOLATION` (test case). `MATCHING` probably needs the same span-wise sections on both sides (to be reviewed).
- `TURBULENT_MIXINGPLANE= YES` also passes the turbulence variables across the mixing plane. The default is `NO` (code). All turbulent test cases set `YES` (test case).
- On the mixing-plane markers, also set a Giles condition: `MIXING_OUT` on the upstream side and `MIXING_IN` on the downstream side (tutorial).

### Turbomachinery markers

- `MARKER_TURBOMACHINERY`: the inlet and the outlet marker of every zone, zone by zone, in stream-wise order: (inlet zone 1, outlet zone 1, inlet zone 2, outlet zone 2, ...) (tutorial).
- `TURBOMACHINERY_KIND`: the shape of each row, one entry per zone: `AXIAL`, `CENTRIFUGAL`, `CENTRIPETAL`, `CENTRIPETAL_AXIAL` or `AXIAL_CENTRIFUGAL`. SU2 uses it to decide which coordinate measures the span (code). Example: the radial turbine of the APU turbocharger test uses `CENTRIPETAL CENTRIPETAL_AXIAL` (test case).
- `TURBO_PERF_KIND`: the kind of machine for the performance outputs, one entry per zone: `TURBINE`, `COMPRESSOR` or `PROPELLOR`. SU2 stops with "Insufficient TURBO_PERF_KIND options" if there are fewer entries than zones (code).
- `MARKER_ANALYZE`: markers where SU2 writes surface-averaged values such as `SURFACE_TOTAL_PRESSURE` (tutorial). `MARKER_ANALYZE_AVERAGE` chooses `AREA` or `MASSFLUX` (default) averaging for these outputs (code).

### Inlet and outlet boundaries: Giles or Riemann

Both conditions are based on characteristics, that is, on the waves that enter and leave the domain. They work with any fluid model. The plain `MARKER_INLET` and `MARKER_OUTLET` work only with ideal gases (code).

**`MARKER_GILES`** is the non-reflecting condition for turbomachinery (tutorial).

- It works only together with `MARKER_TURBOMACHINERY`. Without it, SU2 stops with "Giles Boundary conditions can only be used with turbomachinery markers" (code).
- Format, 9 values per marker: (marker, kind, value 1, value 2, direction 1, direction 2, direction 3, average relaxation, Fourier relaxation) (tutorial).
- The last two values under-relax the update of the averaged state and of the Fourier modes: SU2 applies only this fraction of each update. The test cases use 1.0 in 2D. On most boundaries of the 3D Aachen case they use 0.3 (average) and 0.0 (Fourier) (test case).
- `SPATIAL_FOURIER= YES` makes the condition non-reflecting for the circumferential waves too. With `NO` (default), it acts as a 1D characteristic condition (code). The Aachen tutorial keeps it off (tutorial).
- `GILES_EXTRA_RELAXFACTOR` = (relaxation factor, span fraction) adds extra under-relaxation near hub and shroud in 3D. The default is (0.1, 0.1). SU2 limits the span fraction to 0.5 (code). The Aachen case uses (0.05, 0.05) (test case).

Kinds of Giles boundary (code):

| Kind | Use | Values |
|---|---|---|
| `TOTAL_CONDITIONS_PT` | inlet | total pressure, total temperature, flow direction (normal, tangential, span-wise components) |
| `TOTAL_CONDITIONS_PT_1D` | inlet | same, imposed on the average of the whole boundary |
| `STATIC_PRESSURE` | outlet | static pressure, imposed on each span-wise section |
| `STATIC_PRESSURE_1D` | outlet | static pressure, imposed on the average of the whole boundary |
| `RADIAL_EQUILIBRIUM` | outlet (3D) | static pressure at mid-span; SU2 builds the span-wise pressure profile from the radial equilibrium of the averaged flow |
| `MASS_FLOW_OUTLET` | outlet | target mass flow (value 1) and a relaxation factor (value 2) |
| `MIXING_IN`, `MIXING_OUT` | mixing plane | none (write zeros), averages for each span-wise section |
| `MIXING_IN_1D`, `MIXING_OUT_1D` | mixing plane | none, average of the whole boundary |

The `_1D` kinds impose only the average over the whole boundary, so the span-wise profile is free to develop. The tutorial uses `STATIC_PRESSURE_1D` on an outlet "where the flow is in radial equilibrium" (tutorial).

**`MARKER_RIEMANN`** is a characteristic condition with 7 values per marker: (marker, kind, value 1, value 2, direction 1, direction 2, direction 3). It accepts these kinds (code):

- Without turbomachinery markers: `TOTAL_CONDITIONS_PT`, `STATIC_PRESSURE`, `DENSITY_VELOCITY`, `STATIC_SUPERSONIC_INFLOW_PT` and `STATIC_SUPERSONIC_INFLOW_PD`.
- With turbomachinery markers, SU2 uses an averaged version on the finest mesh. It accepts `TOTAL_CONDITIONS_PT`, `STATIC_PRESSURE`, `RADIAL_EQUILIBRIUM`, `MIXING_IN` and `MIXING_OUT`.
- Any other kind stops the run with "Invalid Riemann input!".

Which one to choose: the turbomachinery test cases and the Aachen tutorial use `MARKER_GILES` (test case, tutorial). Giles boundaries can sit closer to the blades than reflecting ones (advice, to be reviewed).

### Averaging

- `AVERAGE_PROCESS_KIND` sets how SU2 averages the flow on Giles boundaries and mixing planes: `ALGEBRAIC`, `AREA` (default), `MASSFLUX` or `MIXEDOUT` (code). The tutorial says that only `MIXEDOUT` makes the mixing plane conservative (tutorial). All test cases use `MIXEDOUT` (test case).
- `PERFORMANCE_AVERAGE_PROCESS_KIND` sets the same for the performance outputs. The default is `AREA` (code).
- `MIXEDOUT_COEFF` = (relaxation factor, tolerance, maximum iterations) of the Newton method for the mixed-out average. The default is (1.0, 1.0E-05, 15) (code).
- `AVERAGE_MACH_LIMIT` (default 0.03): when the Mach number normal to the boundary is below this value, the `MASSFLUX` and `MIXEDOUT` averages fall back to the `AREA` average. This matters at the start of a run, when the flow is still slow. Below this limit SU2 also skips the Fourier part of the Giles condition (code).

### Span-wise sections (3D)

SU2 builds the span-wise sections as follows (code):

- `SPANWISE_KIND= AUTOMATIC` (default): SU2 counts the mesh points along the span where the inlet or outlet meets the periodic boundary, and makes one section per point. This suits meshes with the same span-wise point distribution on both sides of an interface (to be reviewed).
- `SPANWISE_KIND= EQUISPACED`: SU2 makes `NUM_SPANWISE_SECTIONS` sections of equal height between hub and shroud.
- In 2D, SU2 always uses one section.

### Ramps

Ramps help when the machine has a high pressure ratio or a high rotation speed (tutorial). A ramp changes a value linearly, from a start value to the final value set in the config file.

The ramp options (code):

- `RAMP_MOTION_FRAME= YES` ramps the rotation speed (z component of `ROTATION_RATE`) or, with `STEADY_TRANSLATION`, the y component of `TRANSLATION_RATE`.
- `RAMP_OUTLET= YES` ramps the outlet value of Giles `STATIC_PRESSURE`, `STATIC_PRESSURE_1D`, `RADIAL_EQUILIBRIUM` and `MASS_FLOW_OUTLET` boundaries. The Aachen tutorial text calls this option `RAMP_OUTLET_PRESSURE`, but the option in the code is `RAMP_OUTLET`.
- `RAMP_MOTION_FRAME_COEFF` and `RAMP_OUTLET_COEFF` = (start value, update every N iterations, length of the ramp in iterations). The defaults are (100.0, 1.0, 1000.0) and (100000.0, 1.0, 1000.0). Always set them.

The test values are `RAMP_MOTION_FRAME_COEFF= (0.0, 39.0, 500)` and `RAMP_OUTLET_COEFF= (140000.0, 150.0, 2000)` (test case).

Limits of the ramps (code):

- In multizone runs, the ramp follows the outer iteration.
- The rotation ramp acts only when `MARKER_TURBOMACHINERY` is set.
- The outlet ramp does not work on `MARKER_RIEMANN` outlets. SU2 stops with "Outlet pressure ramp only implemented for NRBC".
- SU2 does not set up these two ramps in discrete adjoint runs.

`RAMP_MUSCL` is a different ramp: it blends from first-order to second-order space discretization. The 2D stage uses `RAMP_MUSCL_COEFF= (0.0, 1.0, 20.0)` = (start iteration, update every N iterations, ramp length) (test case).

### Initialization and numerics

- Use `INIT_OPTION= TD_CONDITIONS` with `FREESTREAM_PRESSURE` and `FREESTREAM_TEMPERATURE` near the inlet state, and a small `MACH_NUMBER` (0.05 in the test cases) (test case). The default `INIT_OPTION= REYNOLDS` recomputes the pressure from the Reynolds number (code), which does not suit internal flows (advice). Check the initial state that SU2 prints before the first iteration (tutorial).
- The test cases use `ROE` with `MUSCL_FLOW= YES` (2D stage, transonic stator) or `JST` (Aachen). Their CFL numbers range from 2 (Aachen) to 50 (transonic stator) (test case).
- SU2 applies the Giles and the averaged Riemann conditions only on the finest mesh (code). Most turbomachinery test cases run without multigrid; the Aachen restart test uses `MGLEVEL= 1` (test case). If a run with multigrid is unstable, try `MGLEVEL= 0` (to be reviewed).
- Wall functions (`MARKER_WALL_FUNCTIONS`) let the Aachen tutorial run on a coarse mesh with high y+ (tutorial).

### Performance outputs

- Add `TURBO_PERF` to `HISTORY_OUTPUT` to write the performance values to the history file (test case).
- Values per row carry the row number, starting at 1: `MassFlowIn_1`, `MassFlowOut_1`, `TotalPressureIn_1`, `AbsFlowAngleOut_1`, `KineticEnergyLoss_1`, `TotPressureLoss_1`, ... (code).
- Values for the whole machine: `TotalStaticEfficiency`, `TotalTotalEfficiency`, `PressureRatioTS`, `PressureRatioTT`, `EulerianWork`, `EntropyGeneration`, `KineticEnergyLoss_Stage`, `TotPressureLoss_Stage` (code).
- In multizone runs, these fields belong to the last zone. Write them with the index of the last zone, for example `TotalStaticEfficiency[1]` for two zones (test case).
- Every 100 iterations, SU2 prints a table of the performance of each row and of the machine (code).
- SU2 writes span-wise profiles (`inflow_spanwise_thermodynamic_values*.dat`, `outflow_spanwise_kinematic_values*.dat`, ...) and mixing-plane interpolation details into a folder named `TURBOMACHINERY` (code). SU2 does not create this folder. Create it in the run directory before you start, otherwise these files are not written (to be reviewed).
- `WRT_ZONE_HIST= YES` writes one history file per zone (tutorial).

The full list of fields is on the [output fields](../Output-Fields-Reference/) page. The options are on the [option reference](../Option-Reference/) page.

## Check convergence and results

- **Stop criterion.** Use residuals, for example `CONV_FIELD= RMS_ENERGY[0]` with `CONV_RESIDUAL_MINVAL` (test case). SU2 checks convergence only on residual fields and coefficient fields. The turbomachinery performance fields are neither, so do not put them in `CONV_FIELD`. The `MARKER_ANALYZE` fields, such as `SURFACE_MASSFLOW`, are coefficients and work with the Cauchy criterion (`CONV_CAUCHY_ELEMS`, `CONV_CAUCHY_EPS`) (code).
- **Residuals.** Watch the residuals of every zone (`RMS_DENSITY[0]`, `RMS_DENSITY[1]`, ...) and the coupling residuals (`AVG_BGS_RES[0]`, ...) (test case).
- **Mass flow.** `MassFlowIn_n` and `MassFlowOut_n` of each row should agree, and the outlet of one row should match the inlet of the next (advice).
- **Performance.** Efficiency and pressure ratio should no longer change over the last few hundred iterations (advice).
- **Span-wise profiles.** Compare the profiles in the `TURBOMACHINERY` folder with the values you imposed, for example the outlet pressure (advice).
- **Ramps.** If you used ramps, run well past the end of the ramp before you read the results (advice).

See [Solver Setup](../Solver-Setup/) for the convergence options.

## Common problems

| Symptom | Likely cause | What to try |
|---|---|---|
| SU2 stops: "Giles Boundary conditions can only be used with turbomachinery markers". | `MARKER_TURBOMACHINERY` is missing (code). | Add the inlet and outlet markers of every zone. |
| SU2 stops: "Insufficient TURBO_PERF_KIND options specified with turbomachinery markers". | There are fewer `TURBO_PERF_KIND` entries than zones (code). | Give one entry per zone. Do the same for `TURBOMACHINERY_KIND`. |
| SU2 stops: "Outlet pressure ramp only implemented for NRBC". | `RAMP_OUTLET= YES` with a `MARKER_RIEMANN` static-pressure outlet (code). | Use a Giles outlet, or switch the ramp off. |
| SU2 stops: "Invalid Riemann input!" | A Riemann kind that this boundary does not support (code). | Check the lists in [Inlet and outlet boundaries](#inlet-and-outlet-boundaries-giles-or-riemann). |
| The run diverges in the first iterations. | A large pressure ratio or a high rotation speed at start-up (tutorial). | Use `RAMP_OUTLET` and `RAMP_MOTION_FRAME`, lower `CFL_NUMBER`, start first order and use `RAMP_MUSCL` (advice, to be reviewed). |
| The flow near hub or shroud is unstable in 3D with Giles. | Strong span-wise gradients at the endwalls (advice, to be reviewed). | Lower `GILES_EXTRA_RELAXFACTOR` and the average relaxation factor of the Giles markers, as in the Aachen case (0.05 and 0.3) (test case). |
| Efficiency or mass flow look wrong in the first iterations. | The flow is slow, so the averages use the area average (code). | Wait until the flow develops. Check `AVERAGE_MACH_LIMIT`. |
| The ramp has no effect. | A discrete adjoint run, or no `MARKER_TURBOMACHINERY` for the rotation ramp, or the machine axis is not z (code). | Run the direct solver, with turbomachinery markers and the z-axis as machine axis. |
| Wrong or missing span-wise sections, or a crash while SU2 sets up the turbomachinery boundaries. | The periodic pairs are not in zone order, or the mesh has no matching span-wise points for `AUTOMATIC` (code, to be reviewed). | Order `MARKER_PERIODIC` by zone. Try `SPANWISE_KIND= EQUISPACED`. |
| No span-wise `.dat` files. | The `TURBOMACHINERY` folder does not exist (code). | Create it in the run directory. |
| Reverse flow at the outlet. | The outlet is too close to the blade, or the outlet pressure is too high (advice, to be reviewed). | Move the outlet downstream. Check the outlet pressure value. |

## Related tutorials and test cases

Tutorials:

- [Aachen turbine stage with mixing plane](/tutorials/Aachen_Turbine/): 3D, three rows, Giles boundaries, ramps, wall functions, performance outputs.
- [Non-ideal compressible flows with physics-informed neural networks](/tutorials/NICFD_nozzle_datadriven/): uses Giles boundaries and an outlet ramp on a nozzle.

Test cases (SU2 repository):

- [turbomachinery/axial_stage_2D](https://github.com/su2code/SU2/blob/develop/TestCases/turbomachinery/axial_stage_2D/Axial_stage2D.cfg): 2D stage, mixing plane, translating row.
- [turbomachinery/Aachen_turbine](https://github.com/su2code/SU2/blob/develop/TestCases/turbomachinery/Aachen_turbine/aachen_3D_MP_restart.cfg): 3D, three rows, rotating frame, wall functions.
- [turbomachinery/APU_turbocharger](https://github.com/su2code/SU2/blob/develop/TestCases/turbomachinery/APU_turbocharger/Jones_restart.cfg): radial turbine, rotation ramp.
- [turbomachinery/multi_interface](https://github.com/su2code/SU2/blob/develop/TestCases/turbomachinery/multi_interface/multi_interface_rst.cfg): one frozen-rotor and one mixing-plane interface.
- [turbomachinery/transonic_stator_2D](https://github.com/su2code/SU2/blob/develop/TestCases/turbomachinery/transonic_stator_2D/transonic_stator_restart.cfg): single row, Peng-Robinson gas, Giles boundaries with `SPATIAL_FOURIER= YES`.
- [disc_adj_turbomachinery](https://github.com/su2code/SU2/tree/develop/TestCases/disc_adj_turbomachinery): discrete adjoint of a stator and of a stage, with the objectives `TOTAL_PRESSURE_LOSS` and `ENTROPY_GENERATION`.

User guide pages: [Basics of Multi-Zone Computations](../Multizone/), [Markers and Boundary Conditions](../Markers-and-BC/), [Solver Setup](../Solver-Setup/), [History and Solution Output](../Custom-Output/), [Setup Guide: Non-Ideal Compressible Flows](../Setup-Guide-NICFD/).

Last checked against SU2 develop `11c177b904`.
