---
title: "Setup Guide: Non-Ideal Compressible Flows"
permalink: /docs_v7/Setup-Guide-NICFD/
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

Use this guide when the ideal gas law does not describe your fluid well. This happens for dense vapours and for gases near their critical point: for example organic fluids in ORC turbines, supercritical CO2 in compressors, or refrigerants in nozzles. This field is called NICFD (non-ideal compressible fluid dynamics).

The guide covers the compressible solvers (`SOLVER= EULER`, `NAVIER_STOKES` or `RANS`) with a non-ideal fluid model. These solvers do not model phase change: the fluid must stay a single-phase gas or a supercritical fluid.

Terms used below:

- **Equation of state (EOS)**: the relation between pressure, density, temperature and energy of the fluid.
- **Critical point**: the pressure and temperature above which liquid and vapour can no longer be told apart. Near it, the fluid properties change fast.
- **Acentric factor**: a number that describes the shape of the molecule. Cubic equations of state such as Peng-Robinson use it.
- **Two-phase region**: the states where liquid and vapour coexist. Inside it, a cubic EOS gives non-physical values, for example a negative square of the speed of sound.

In this guide, (advice) also covers general thermodynamics practice.

## Start from

The block below is built from the regression test [nicf/coolprop/fluidModel.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/nicf/coolprop/fluidModel.cfg). That test runs the supersonic nozzle of the [NICFD nozzle tutorial](/tutorials/NICFD_nozzle/) with CoolProp.

- We replaced the CoolProp fluid with the Peng-Robinson fluid block of the tutorial (siloxane MDM), so that the config runs with a normal SU2 build.
- We set `RESTART_SOL= NO`, and removed the comments and the file names.
- We replaced `LIFT` and `DRAG` in the screen output with `NONPHYSICAL_POINTS`.
- The mesh `coolprop_nozzle.su2` is in the [TestCases repository](https://github.com/su2code/TestCases).

```
SOLVER= RANS
KIND_TURB_MODEL= SST
MATH_PROBLEM= DIRECT
RESTART_SOL= NO
%
MACH_NUMBER= 1E-9
INIT_OPTION= TD_CONDITIONS
FREESTREAM_OPTION= TEMPERATURE_FS
FREESTREAM_PRESSURE= 904388
FREESTREAM_TEMPERATURE= 542.13
REF_DIMENSIONALIZATION= DIMENSIONAL
%
FLUID_MODEL= PR_GAS
GAMMA_VALUE= 1.01767
GAS_CONSTANT= 35.17
CRITICAL_TEMPERATURE= 565.3609
CRITICAL_PRESSURE= 1437500
ACENTRIC_FACTOR= 0.524
%
VISCOSITY_MODEL= CONSTANT_VISCOSITY
MU_CONSTANT= 1.21409E-05
CONDUCTIVITY_MODEL= CONSTANT_CONDUCTIVITY
THERMAL_CONDUCTIVITY_CONSTANT= 0.030542828
%
MARKER_HEATFLUX= ( WALL, 0.0 )
MARKER_SYM= ( SYMMETRY )
MARKER_RIEMANN= ( INFLOW, TOTAL_CONDITIONS_PT, 904388, 542.13, 1.0, 0.0, 0.0, OUTFLOW, STATIC_PRESSURE, 200000.0, 0.0, 0.0, 0.0, 0.0 )
%
NUM_METHOD_GRAD= GREEN_GAUSS
CFL_NUMBER= 10.0
CFL_ADAPT= YES
CFL_ADAPT_PARAM= ( 0.1, 2.0, 10.0, 1000.0 )
MAX_DELTA_TIME= 1E6
LINEAR_SOLVER= FGMRES
LINEAR_SOLVER_PREC= ILU
LINEAR_SOLVER_ILU_FILL_IN= 0
LINEAR_SOLVER_ERROR= 1E-6
LINEAR_SOLVER_ITER= 10
CONV_NUM_METHOD_FLOW= ROE
ENTROPY_FIX_COEFF= 0.1
MUSCL_FLOW= YES
SLOPE_LIMITER_FLOW= NONE
CONV_NUM_METHOD_TURB= SCALAR_UPWIND
MUSCL_TURB= NO
%
% The test stops after 101 iterations. Raise ITER for a converged result.
ITER= 101
CONV_RESIDUAL_MINVAL= -24
CONV_STARTITER= 10
SCREEN_OUTPUT= (INNER_ITER, RMS_DENSITY, RMS_TKE, RMS_DISSIPATION, NONPHYSICAL_POINTS)
MESH_FILENAME= coolprop_nozzle.su2
MESH_FORMAT= SU2
OUTPUT_WRT_FREQ= 50
```

To use CoolProp instead, replace the fluid block with the one of the test case: `FLUID_MODEL= COOLPROP` and `FLUID_NAME= nitrogen` (test case). The inlet and outlet values of the test then describe nitrogen, not MDM.

## Settings that matter

### Build options

These rules come from the code (code):

- CoolProp needs `-Denable-coolprop=true` at configure time.
- The data-driven model with neural networks needs `-Denable-mlpcpp=true`. The data-driven tutorial uses it too (tutorial).
- CoolProp cannot be used with the AD builds, so there is no discrete adjoint with CoolProp.
- `VW_GAS` and `PR_GAS` need no extra build option.

See [Build SU2 on Linux/MacOS](../Build-SU2-Linux-MacOS/).

### Fluid model

Choose the equation of state with `FLUID_MODEL` (code):

| Value | Model | Parameters |
|---|---|---|
| `STANDARD_AIR`, `IDEAL_GAS` | ideal gas | `GAMMA_VALUE`, `GAS_CONSTANT` |
| `VW_GAS` | van der Waals | `GAMMA_VALUE`, `GAS_CONSTANT`, `CRITICAL_TEMPERATURE`, `CRITICAL_PRESSURE` |
| `PR_GAS` | Peng-Robinson | as `VW_GAS`, plus `ACENTRIC_FACTOR` |
| `COOLPROP` | multiparameter EOS from the CoolProp library | `FLUID_NAME` |
| `DATADRIVEN_FLUID` | look-up table or neural network | `INTERPOLATION_METHOD`, `FILENAMES_INTERPOLATOR`, `USE_PINN`, `DATADRIVEN_NEWTON_RELAXATION` |

How to choose (advice, to be reviewed):

- `VW_GAS` is the simplest non-ideal model. It is mainly useful for qualitative studies and code tests.
- `PR_GAS` is a common choice for organic fluids. It gives fair accuracy away from the critical point. The NICFD nozzle tutorial uses it (tutorial).
- `COOLPROP` is the most accurate near the critical point, but each property evaluation is slower.
- `DATADRIVEN_FLUID` gives accuracy close to the reference EOS at a lower cost. First you must build a table, or train a network, for your fluid and your range of states.

Parameters and their defaults (code):

- `GAMMA_VALUE` (default 1.4) and `GAS_CONSTANT` (default 287.058 J/(kg K)). For `VW_GAS` and `PR_GAS`, take the ratio of specific heats in the dilute-gas limit, that is, at low pressure (tutorial). These models use a constant ideal-gas heat capacity, derived from `GAMMA_VALUE`. `GAS_CONSTANT` is the universal gas constant divided by the molar mass of the fluid (advice).
- `CRITICAL_TEMPERATURE` (default 131.00 K), `CRITICAL_PRESSURE` (default 3588550.0 Pa), `ACENTRIC_FACTOR` (default 0.035). The defaults do not describe your fluid, so always set these values.
- `CRITICAL_DENSITY` exists (default 263.0) and the test cases set it, but the finite-volume solvers do not use it.
- `FLUID_NAME` (default `nitrogen`) is the CoolProp name of the fluid. With `COOLPROP`, SU2 takes the critical point and the acentric factor from CoolProp, so the `CRITICAL_*` options are not needed.

Data-driven options (code):

- `INTERPOLATION_METHOD`: `LUT` (look-up table, default) or `MLP` (multi-layer perceptron, a neural network). The comment in the code says that the default is `MLP`, but the code sets `LUT`.
- `FILENAMES_INTERPOLATOR`: the `.mlp` files of the networks, or one `.drg` table file for `LUT`. The file types are from `config_template.cfg`.
- `USE_PINN= YES` uses a physics-informed network, default `NO`. The network gives the entropy as a function of density and internal energy. SU2 computes the other properties from its derivatives, which keeps them consistent (tutorial).
- `DATADRIVEN_NEWTON_RELAXATION` (default 1.0) relaxes a Newton solver. The model takes density and internal energy as inputs. When SU2 knows another pair of properties, for example pressure and temperature, this Newton solver finds the matching density and energy.
- The [data-driven tutorial](/tutorials/NICFD_nozzle_datadriven/) shows how to make the network with SU2 DataMiner.

### Reference values

- `REF_DIMENSIONALIZATION` (default `DIMENSIONAL`) sets how SU2 scales the variables. See [Physical Definition](../Physical-Definition/).
- `COOLPROP` must run with `DIMENSIONAL`. Otherwise SU2 stops with "CoolProp can not be used with non-dimensionalization" (code).
- `DATADRIVEN_FLUID`: the test case and the tutorial use `DIMENSIONAL` (test case, tutorial). The code builds this model without reference scaling, so keep `DIMENSIONAL` (code, to be reviewed).
- `PR_GAS` and `VW_GAS` work with both. The transonic stator test uses `DIMENSIONAL`, and the LS89 cascade test uses `FREESTREAM_PRESS_EQ_ONE` (test case).

### Transport properties

Viscosity, `VISCOSITY_MODEL` (code):

- `CONSTANT_VISCOSITY` with `MU_CONSTANT` (default 1.716E-5 Pa s, the value of air).
- `SUTHERLAND` with `MU_REF`, `MU_T_REF`, `SUTHERLAND_CONSTANT` (default model). Sutherland's law is a fit for dilute gases (advice).
- `COOLPROP`: viscosity from CoolProp, for the fluids listed in the code. `FLUID_NAME` must match the list exactly, for example `Nitrogen`, `CarbonDioxide`, `R134a`.
- `POLYNOMIAL_VISCOSITY` works only with the incompressible solvers.

Thermal conductivity, `CONDUCTIVITY_MODEL` (code):

- `CONSTANT_CONDUCTIVITY` with `THERMAL_CONDUCTIVITY_CONSTANT` (default 0.0257 W/(m K), the value of air).
- `CONSTANT_PRANDTL` with `PRANDTL_LAM` (default 0.72) (default model).
- `COOLPROP`: conductivity from CoolProp, with the same exact-name rule as the viscosity.
- `POLYNOMIAL_CONDUCTIVITY` works only with the incompressible solvers.

`PRANDTL_TURB` (default 0.9) sets the turbulent heat conduction in RANS (code).

What the examples use:

- `PR_GAS` tests and tutorial: `CONSTANT_VISCOSITY` and `CONSTANT_CONDUCTIVITY` (test case, tutorial). The tutorial says that these are the only models available with `PR_GAS`. The current code accepts the other models too (code). Whether they suit a dense gas is to be reviewed.
- Data-driven test: `CONSTANT_VISCOSITY` and `CONSTANT_PRANDTL` (test case).
- CoolProp test `transportModel.cfg`: `COOLPROP` for both (test case).

With `CONDUCTIVITY_MODEL= COOLPROP`, also set `TURBULENT_CONDUCTIVITY_MODEL= NONE`. With the default `CONSTANT_PRANDTL_TURB`, the code replaces the CoolProp conductivity with `THERMAL_CONDUCTIVITY_CONSTANT` (code, to be reviewed). `NONE` does not remove the turbulent heat flux: the compressible solvers add it from `PRANDTL_TURB` in any case (code).

### Boundary conditions

- With a non-ideal fluid, `MARKER_INLET`, `MARKER_OUTLET` and `MARKER_FAR` are not allowed. SU2 stops with "Riemann Boundary conditions or Giles must be used ..." (code).
- Use `MARKER_RIEMANN` for inlets and outlets. It is a characteristic condition, built on the waves that enter and leave the domain, and it uses the fluid model (tutorial). Format: (marker, kind, value 1, value 2, direction 1, direction 2, direction 3) (code).

Riemann kinds accepted by the general Riemann condition (code):

| Kind | Use | Values |
|---|---|---|
| `TOTAL_CONDITIONS_PT` | subsonic inlet | total pressure, total temperature, flow direction |
| `DENSITY_VELOCITY` | inlet | density, velocity magnitude, flow direction |
| `STATIC_PRESSURE` | subsonic outlet | static pressure, then four zeros |
| `STATIC_SUPERSONIC_INFLOW_PT` | supersonic inlet | static pressure, static temperature, Mach number components |
| `STATIC_SUPERSONIC_INFLOW_PD` | supersonic inlet | static pressure, static density, Mach number components |

Other kinds in the Riemann list, such as `SUPERSONIC_OUTFLOW`, stop the run with "Invalid Riemann input!" unless turbomachinery markers are set (code). The supersonic edge test uses `STATIC_PRESSURE` with a low value at its supersonic outlet (test case).

- `MARKER_GILES` is a non-reflecting condition. It needs `MARKER_TURBOMACHINERY` (code). The [data-driven tutorial](/tutorials/NICFD_nozzle_datadriven/) uses it on a nozzle, with an outlet pressure ramp (tutorial). See [Setup Guide: Turbomachinery](../Setup-Guide-Turbomachinery/) for its kinds and options.
- Walls: `MARKER_HEATFLUX`, `MARKER_EULER` and `MARKER_SYM` work as usual (test case).

### Initialization

- Use `INIT_OPTION= TD_CONDITIONS` (test case, tutorial). The default `REYNOLDS` recomputes the pressure from the Reynolds number (code), which does not suit internal flows (advice).
- The nozzle tests start from the inlet total state at rest: `FREESTREAM_PRESSURE` and `FREESTREAM_TEMPERATURE` equal to the inlet total values, and `MACH_NUMBER= 1E-9` (test case).
- `FREESTREAM_OPTION= DENSITY_FS` gives the state from pressure and density, instead of pressure and temperature. The supersonic edge tests use it (test case).
- Make sure that the initial state lies in the single-phase region, away from the saturation curve (advice).
- Check the initial state that SU2 prints before the first iteration (tutorial).

### Schemes and limiters

- With a non-ideal fluid, only `ROE`, `HLLC` and `JST` are allowed for `CONV_NUM_METHOD_FLOW` (code). The test cases use `ROE` (test case).
- The nozzle tests raise `ENTROPY_FIX_COEFF` to 0.1 (default 0.001) (test case). The entropy fix adds dissipation to the Roe scheme where wave speeds are close to zero (advice).
- Second order: the nozzle tutorial uses `MUSCL_FLOW= YES` with `SLOPE_LIMITER_FLOW= NONE` (tutorial). The LS89 cascade test, with shocks, uses `VENKATAKRISHNAN` (test case). Use a limiter when the flow has shocks (advice).
- The nozzle tests use `CFL_ADAPT= YES` with `CFL_ADAPT_PARAM= ( 0.1, 2.0, 10.0, 1000.0 )` (test case). The four values are the factor down, the factor up, and the minimum and maximum CFL (code).
- The edge and LS89 tests use multigrid (`MGLEVEL= 3`) (test case).

Near the critical point (advice, to be reviewed):

- The speed of sound and the heat capacity change fast there. Small errors in the reconstructed states can give non-physical states. Start first order (`MUSCL_FLOW= NO`) or with `RAMP_MUSCL`, then switch to second order.
- Start with a low CFL number, and let `CFL_ADAPT` raise it.
- Use a limiter, for example `VENKATAKRISHNAN`, if non-physical points appear near steep gradients.
- Refine the mesh where the flow passes close to the critical point.

What SU2 does with non-physical states (code):

- After each update, SU2 checks the density, pressure, temperature and square of the speed of sound of each point. If one is negative, SU2 goes back to the previous solution at that point and counts the point. The count is the history field `NONPHYSICAL_POINTS`.
- When a second-order reconstruction gives a negative pressure or density on an edge, SU2 uses first-order values on that edge.
- At start-up, SU2 prints "Warning. The original solution contains N points that are not physical." when the initial state is non-physical.

## Check convergence and results

- **Non-physical points.** Watch `NONPHYSICAL_POINTS`. It should drop to zero long before convergence (advice).
- **Residuals.** Watch the residuals (`RMS_DENSITY`, ...) as for any compressible case. See [Solver Setup](../Solver-Setup/).
- **Mass flow.** Check the mass flow balance between inlet and outlet, for example with `MARKER_ANALYZE` and `SURFACE_MASSFLOW` (advice).
- **Phase.** Check where the flow lies on a pressure-temperature or temperature-entropy diagram of the fluid. All points must stay outside the two-phase region (advice).
- **Non-ideal effects.** Compute the compressibility factor Z = p / (rho R T) in post-processing. Values far from 1 show where the non-ideal effects matter (tutorial). SU2 does not write Z as an output field (code).
- **Data-driven model.** With `DATADRIVEN_FLUID`, look at the volume field `EXTRAPOLATION`. It marks points where the state is outside the range of the training data. `FLUIDMODEL_NEWTONITER` shows how many Newton iterations the fluid model needed (code).
- **Experiments.** Compare with experiments where you can. The NICFD nozzle tutorial compares pressure and Mach number on the nozzle axis with measurements (tutorial).

## Common problems

| Symptom | Likely cause | What to try |
|---|---|---|
| SU2 stops: "Riemann Boundary conditions or Giles must be used for inlet and outlet with Not Ideal Compressible Fluids". | `MARKER_INLET`, `MARKER_OUTLET` or `MARKER_FAR` with a non-ideal fluid (code). | Use `MARKER_RIEMANN` or `MARKER_GILES`. |
| SU2 stops: "Only ROE Upwind, HLLC Upwind scheme, and JST scheme can be used for Non-Ideal Compressible Fluids". | Another convective scheme (code). | Use `ROE`, `HLLC` or `JST`. |
| SU2 stops: "CoolProp can not be used with non-dimensionalization." | `REF_DIMENSIONALIZATION` is not `DIMENSIONAL` (code). | Set `REF_DIMENSIONALIZATION= DIMENSIONAL`. |
| SU2 stops: "SU2 was not compiled with CoolProp (-Denable-coolprop=true)". | A build without CoolProp (code). | Rebuild with `-Denable-coolprop=true`, without AD. |
| SU2 stops: "SU2 was not compiled with MLPCpp enabled (-Denable-mlpcpp=true)." | A build without MLPCpp (code). | Rebuild with `-Denable-mlpcpp=true`. |
| SU2 stops: "Viscosity model not available for this fluid in CoolProp library." (or the same for conductivity). | `FLUID_NAME` is not in the list of the transport model, or is spelled with other capitals (code). | Use the exact name, for example `Nitrogen`, or use a constant model. |
| SU2 stops: "POLYNOMIAL_VISCOSITY and POLYNOMIAL_CONDUCTIVITY are for incompressible only currently." | A polynomial transport model with a compressible solver (code). | Use a constant model or `COOLPROP`. |
| `NONPHYSICAL_POINTS` stays above zero, or the speed of sound is negative. | States inside the two-phase region, where a cubic EOS has no physical solution; or too large a step at start-up (advice). | Check the boundary values against the saturation curve. Lower the CFL, start first order, and refine near the critical point (to be reviewed). |
| Strange results close to saturation with `COOLPROP`. | In a two-phase state, the code raises the temperature by 0.1 K and evaluates the speed of sound of the gas phase (code). | Keep the flow out of the two-phase region: the results there are not reliable. |
| The results look like air. | `CRITICAL_*`, `ACENTRIC_FACTOR`, `GAMMA_VALUE`, `GAS_CONSTANT`, `MU_CONSTANT` or `THERMAL_CONDUCTIVITY_CONSTANT` left at their defaults, which are air values (code). | Set all fluid and transport parameters for your fluid. |
| The CoolProp conductivity has no effect. | `TURBULENT_CONDUCTIVITY_MODEL` is left at `CONSTANT_PRANDTL_TURB` (code). | Set `TURBULENT_CONDUCTIVITY_MODEL= NONE` (to be reviewed). |
| `EXTRAPOLATION` is 1 in parts of the domain. | The data-driven model is used outside its training range (code). | Generate data and retrain over a wider range of density and energy. |
| The inlet flow angle is wrong on a 2D inlet that is not normal to x. | In 2D, SU2 reads the direction of the Riemann `TOTAL_CONDITIONS_PT` inlet relative to the boundary normal. In 3D, it reads it as x, y, z components (code, to be reviewed). | In 2D, give the direction as (normal, tangential) components. |
| The run diverges at the start with a large pressure ratio. | The outlet pressure is applied at once (advice). | With `MARKER_GILES`, use `RAMP_OUTLET` as in the data-driven tutorial (tutorial). With `MARKER_RIEMANN`, start with a higher outlet pressure and lower it in steps (to be reviewed). |

## Related tutorials and test cases

Tutorials:

- [Non-ideal compressible flow in a supersonic nozzle](/tutorials/NICFD_nozzle/): Peng-Robinson, Riemann boundaries, comparison with experiments.
- [Non-ideal compressible flows with physics-informed neural networks](/tutorials/NICFD_nozzle_datadriven/): data-driven model, SU2 DataMiner, Giles boundaries.
- [Aachen turbine stage with mixing plane](/tutorials/Aachen_Turbine/): turbomachinery setup, which also applies to non-ideal fluids.

Test cases (SU2 repository):

- [nicf/coolprop](https://github.com/su2code/SU2/tree/develop/TestCases/nicf/coolprop): CoolProp fluid model (`fluidModel.cfg`) and CoolProp transport models (`transportModel.cfg`).
- [nicf/datadriven](https://github.com/su2code/SU2/blob/develop/TestCases/nicf/datadriven/datadriven_nozzle.cfg): data-driven model with a physics-informed network.
- [nicf/edge](https://github.com/su2code/SU2/tree/develop/TestCases/nicf/edge): supersonic flow over an edge with `PR_GAS` and `VW_GAS`, Euler, multigrid.
- [nicf/LS89](https://github.com/su2code/SU2/tree/develop/TestCases/nicf/LS89): turbine cascade with `PR_GAS`, SA and SST models.
- [turbomachinery/transonic_stator_2D](https://github.com/su2code/SU2/blob/develop/TestCases/turbomachinery/transonic_stator_2D/transonic_stator_restart.cfg): stator with `PR_GAS` and Giles boundaries.
- [turbomachinery/centrifugal_stage](https://github.com/su2code/SU2/blob/develop/TestCases/turbomachinery/centrifugal_stage/centrifugal_stage.cfg) uses `PR_GAS` but old option names; it is not part of the regression tests.

User guide pages: [Physical Definition](../Physical-Definition/), [Markers and Boundary Conditions](../Markers-and-BC/), [Convective Schemes](../Convective-Schemes/), [Slope Limiters and Shock Resolution](../Slope-Limiters-and-Shock-Resolution/), [Theory](../Theory/), [Option reference](../Option-Reference/), [Output fields](../Output-Fields-Reference/).

Last checked against SU2 develop `11c177b904`.
