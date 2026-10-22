---
title: "Setup Guide: Incompressible Flows"
permalink: /docs_v7/Setup-Guide-Incompressible/
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

Use this guide for a flow where the density does not depend on the pressure.
This covers liquids and low-speed gas flows, also with heat transfer, where the density changes only with temperature.
As a rule of thumb, the Mach number is below about 0.3 (advice).

This guide covers the solvers `INC_EULER`, `INC_NAVIER_STOKES` and `INC_RANS`.
For mixing gases and flames, continue with [Setup Guide: Species Transport and Combustion](../Setup-Guide-Species-Combustion/).
For coupled heat transfer between fluid and solid, continue with [Setup Guide: Heat Transfer and Conjugate Heat Transfer](../Setup-Guide-Heat-Transfer-CHT/).

Every option is listed in the [option reference](../Option-Reference/).
Every output field is listed in the [output fields reference](../Output-Fields-Reference/).

## Start from

This config is a laminar flow through a pipe bend. It has a velocity inlet, a pressure outlet, adiabatic walls and a symmetry plane.
It is the test case [`incomp_navierstokes/bend/lam_bend.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/incomp_navierstokes/bend/lam_bend.cfg) with fewer options.
Changes to the test case: `ITER` is raised from 11 to 2000, and `MARKER_ANALYZE` and `HISTORY_OUTPUT` are added to check the mass flow.
The mesh `mesh_bend_coarse.cgns` is in the folder `incomp_navierstokes/bend` of the [TestCases repository](https://github.com/su2code/TestCases).

```
% ------------- Problem -------------%
SOLVER= INC_NAVIER_STOKES
KIND_TURB_MODEL= NONE
MATH_PROBLEM= DIRECT
RESTART_SOL= NO
%
% ------------- Fluid and initial state -------------%
INC_DENSITY_MODEL= CONSTANT
INC_ENERGY_EQUATION= NO
INC_DENSITY_INIT= 1.2886
INC_VELOCITY_INIT= ( 0.1, 0.0, 0.0 )
INC_TEMPERATURE_INIT= 288.15
INC_NONDIM= INITIAL_VALUES
VISCOSITY_MODEL= CONSTANT_VISCOSITY
MU_CONSTANT= 1.716E-5
%
% ------------- Boundary conditions -------------%
INC_INLET_TYPE= VELOCITY_INLET
MARKER_INLET= ( INLET, 288.15, 0.1, 1.0, 0.0, 0.0 )
INC_OUTLET_TYPE= PRESSURE_OUTLET
MARKER_OUTLET= ( OUTLET, 0.0 )
MARKER_HEATFLUX= ( WALL1, 0.0, WALL2, 0.0 )
MARKER_SYM= ( SYMMETRY )
MARKER_MONITORING= ( WALL1, WALL2 )
MARKER_ANALYZE= ( INLET, OUTLET )
%
% ------------- Numerics -------------%
NUM_METHOD_GRAD= GREEN_GAUSS
CONV_NUM_METHOD_FLOW= FDS
MUSCL_FLOW= YES
SLOPE_LIMITER_FLOW= NONE
TIME_DISCRE_FLOW= EULER_IMPLICIT
CFL_NUMBER= 1e2
LINEAR_SOLVER= FGMRES
LINEAR_SOLVER_PREC= ILU
LINEAR_SOLVER_ERROR= 1E-15
LINEAR_SOLVER_ITER= 5
%
% ------------- Convergence and output -------------%
ITER= 2000
CONV_FIELD= RMS_PRESSURE
CONV_RESIDUAL_MINVAL= -8
CONV_STARTITER= 10
MESH_FILENAME= mesh_bend_coarse.cgns
MESH_FORMAT= CGNS
SCREEN_OUTPUT= (INNER_ITER, RMS_PRESSURE, RMS_VELOCITY-X, SURFACE_MASSFLOW)
HISTORY_OUTPUT= (ITER, RMS_RES, FLOW_COEFF, FLOW_COEFF_SURF)
```

## Settings that matter

### Solver

Choose the solver with `SOLVER`:

- `INC_EULER`: no viscosity. Use it for quick checks of pressure fields, for example on a hydrofoil. SU2 stops if you combine it with a density model other than `CONSTANT`, or with `INC_ENERGY_EQUATION= YES` (code).
- `INC_NAVIER_STOKES`: laminar flow.
- `INC_RANS`: turbulent flow. Choose the turbulence model with `KIND_TURB_MODEL` (`SA` or `SST`).

For `INC_RANS`, the inlet turbulence comes from `FREESTREAM_TURBULENCEINTENSITY` (default 0.05) and `FREESTREAM_TURB2LAMVISCRATIO` (default 10), the ratio of turbulent to laminar viscosity (code).
You can set other values per inlet with `MARKER_INLET_TURBULENT`: two values per marker for `SST` (intensity, viscosity ratio), one value for `SA` (viscosity ratio) (code).

### Density-based or pressure-based solver

`KIND_INCOMP_SYSTEM` selects how SU2 couples pressure and velocity (code):

- `DENSITY_BASED` (default): SU2 adds a pseudo-time derivative of the pressure to the continuity equation. This is called artificial compressibility, a form of preconditioning. SU2 then solves pressure, velocity and temperature together, in one coupled system. All tutorials on this page use it.
- `PRESSURE_BASED`: a segregated method of the SIMPLE type, which solves the equations one after the other. Choose `SIMPLE` (default) or `SIMPLEC` with `KIND_PB_ITER`. It uses `CONV_NUM_METHOD_FLOW= UDS` (upwind) or `CDS` (centered).

With `PRESSURE_BASED`, SU2 stops if you use multigrid (`MGLEVEL` above 0), an adjoint, `MARKER_PERIODIC`, streamwise periodic flow, or `TIME_MARCHING= TIME_STEPPING` (code).
If you need the pressure-based solver, start from the test case [`incomp_navierstokes/bend/pb_lam_bend.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/incomp_navierstokes/bend/pb_lam_bend.cfg).
The rest of this page is about the density-based solver.

### Density model and energy equation

`INC_DENSITY_MODEL` decides how the density can change. `INC_ENERGY_EQUATION` switches the temperature equation on or off. The table shows what the code does (code):

| `INC_DENSITY_MODEL` | Density | Energy equation | `FLUID_MODEL` |
|---|---|---|---|
| `CONSTANT` (default) | constant | your choice | SU2 sets `CONSTANT_DENSITY` |
| `BOUSSINESQ` | constant, plus a buoyancy force from temperature | always on | SU2 sets `CONSTANT_DENSITY` |
| `VARIABLE` | from the ideal gas law, changes with temperature | always on without species | `INC_IDEAL_GAS`, `INC_IDEAL_GAS_POLY`, `FLUID_MIXTURE` or `FLUID_FLAMELET` |
| `FLAMELET` | read from a flamelet table | handled by the flamelet solver | `FLUID_FLAMELET` |

How to choose:

- **No heat transfer, or temperature as a passive quantity.** Use `CONSTANT`. With `INC_ENERGY_EQUATION= YES`, SU2 solves for temperature, but the temperature does not change the flow. This one-way coupling is used in the [laminar flat plate tutorial](/tutorials/Inc_Laminar_Flat_Plate/) (tutorial). Set `SPECIFIC_HEAT_CP` (default 1004.703 J/(kg K)).
- **Small temperature differences with buoyancy.** Use `BOUSSINESQ`. The buoyancy force uses `THERMAL_EXPANSION_COEFF` (default 0.00347 1/K) and the difference to `INC_TEMPERATURE_INIT`. Gravity is fixed at 9.81 m/s², along the negative y axis in 2D and the negative z axis in 3D. You cannot add `BODY_FORCE= YES`: SU2 stops (code).
- **Large temperature differences in a gas.** Use `VARIABLE` with `FLUID_MODEL= INC_IDEAL_GAS` (constant specific heat) or `INC_IDEAL_GAS_POLY` (specific heat as a polynomial of temperature, set with `CP_POLYCOEFFS`, five coefficients). Set `MOLECULAR_WEIGHT` in g/mol (default 28.96) and `SPECIFIC_HEAT_CP`.
- **Mixtures of gases.** Use `VARIABLE` with `FLUID_MODEL= FLUID_MIXTURE`. See the [species guide](../Setup-Guide-Species-Combustion/).

When you set `INC_DENSITY_MODEL` to `CONSTANT` or `BOUSSINESQ`, SU2 replaces your `FLUID_MODEL` with `CONSTANT_DENSITY`. Other fluid models only take effect with `VARIABLE` or `FLAMELET` (code).

### Operating pressure of an ideal gas

With `VARIABLE` density, SU2 computes the density from an operating pressure, the molecular weight and the temperature.
The operating (thermodynamic) pressure is constant in space. The flow pressure in SU2 is a gauge pressure on top of it ([Theory](../Theory/#incompressible-navier-stokes)).

`INIT_OPTION_INC` decides which of the two you prescribe (code):

- `DENSITY_INIT`: SU2 scales `THERMODYNAMIC_PRESSURE` so that the density at `INC_TEMPERATURE_INIT` equals `INC_DENSITY_INIT`. This is the default for `INC_IDEAL_GAS` and `INC_IDEAL_GAS_POLY`.
- `OPERATING_PRESSURE`: SU2 uses `THERMODYNAMIC_PRESSURE` (default 101325 Pa) and computes the density. This is the default for `FLUID_MIXTURE` and `FLUID_FLAMELET`.

The buoyancy cavity test case uses `DENSITY_INIT` with a very small `INC_DENSITY_INIT` to reach a chosen Rayleigh number (test case).

### Gravity for variable density

For natural convection with `VARIABLE` density, set `BODY_FORCE= YES` and `BODY_FORCE_VECTOR= ( 0.0, -9.81, 0.0 )` (an acceleration in m/s²), as in the [buoyancy cavity tutorial](/tutorials/Inc_Laminar_Cavity/).
With variable density, the force is (ρ − ρ₀)·g, where ρ₀ is the initial density. So the computed pressure does not contain the hydrostatic pressure of the initial density (code).

### Viscosity and conductivity

- `VISCOSITY_MODEL`: the default is `SUTHERLAND`. SU2 stops if you use it with constant density, so set `VISCOSITY_MODEL= CONSTANT_VISCOSITY` and `MU_CONSTANT` (default 1.716e-5 kg/(m s)) (code). Sutherland's law is allowed with `INC_IDEAL_GAS`, `INC_IDEAL_GAS_POLY` and `FLUID_MIXTURE`. `POLYNOMIAL_VISCOSITY` uses `MU_POLYCOEFFS`.
- `CONDUCTIVITY_MODEL`: the default `CONSTANT_PRANDTL` computes the conductivity from viscosity, specific heat and `PRANDTL_LAM` (default 0.72). `CONSTANT_CONDUCTIVITY` uses `THERMAL_CONDUCTIVITY_CONSTANT` (default 0.0257 W/(m K)). `POLYNOMIAL_CONDUCTIVITY` uses `KT_POLYCOEFFS`.
- `TURBULENT_CONDUCTIVITY_MODEL`: `CONSTANT_PRANDTL_TURB` (default) uses `PRANDTL_TURB` (default 0.9). `NONE` switches the turbulent heat transport off.

The defaults are values for air. For water or another liquid, set all of them (advice).

### Initial state and non-dimensionalization

`INC_DENSITY_INIT`, `INC_VELOCITY_INIT` and `INC_TEMPERATURE_INIT` set the initial field. The initial pressure is always zero.
They also set the free-stream state used at `MARKER_FAR` markers, the Reynolds number printed on screen, and the free-stream turbulence level (code).

`INC_NONDIM` chooses the reference values that SU2 divides by internally (code):

- `INITIAL_VALUES` (default): the reference density, velocity and temperature are the initial values. The reference velocity is the magnitude of `INC_VELOCITY_INIT`.
- `REFERENCE_VALUES`: you set `INC_DENSITY_REF`, `INC_VELOCITY_REF` and `INC_TEMPERATURE_REF` (all default to 1.0).
- `DIMENSIONAL`: all reference values are 1, so SU2 works in SI units.

The reference pressure is the reference density times the reference velocity squared.
The inputs in the config file are always in SI units ([NACA 0012 tutorial](/tutorials/Inc_Turbulent_NACA0012/)).
The volume and restart files contain the solver variables. So pressure, velocity and temperature in these files are divided by the reference values, unless you use `DIMENSIONAL` (code).
SU2 prints the reference values and the non-dimensional values at the start of the run. Use them to convert results back to SI units.

Advice:

- Use `DIMENSIONAL` if you want SI values in the output files. Almost all CHT, species, flamelet and streamwise periodic test cases use it (test case). The choice should not change the converged solution (advice, to be reviewed).
- Do not use `INITIAL_VALUES` with a zero `INC_VELOCITY_INIT`, for example in a closed cavity: the reference velocity becomes zero. Set a small non-zero velocity (the buoyancy cavity test uses 1 m/s), or use `DIMENSIONAL` (code).
- Streamwise periodic flow needs `INC_NONDIM= DIMENSIONAL` (code).

### Inlets

`MARKER_INLET` sets the inlet markers. `INC_INLET_TYPE` gives one type per inlet marker, in the same order (code):

- `VELOCITY_INLET`: `MARKER_INLET= ( marker, temperature [K], velocity magnitude [m/s], nx, ny, nz )`. The direction vector does not need unit length. The temperature is needed even without the energy equation, but then SU2 does not use it ([Markers and BC](../Markers-and-BC/)).
- `PRESSURE_INLET`: `MARKER_INLET= ( marker, temperature [K], total gauge pressure [Pa], nx, ny, nz )`. SU2 adjusts the inlet velocity to reach the total pressure. `INC_INLET_DAMPING` (default 0.1) damps these updates.

The incompressible solver has no mass flow inlet (code).
To prescribe a mass flow, use a velocity inlet (velocity = mass flow / (density × area)) or a mass flow outlet.

For a measured or computed inlet profile, set `SPECIFIED_INLET_PROFILE= YES` and `INLET_FILENAME`, as in the [laminar step tutorial](/tutorials/Inc_Laminar_Step/).

### Outlets

`MARKER_OUTLET` sets the outlet markers. `INC_OUTLET_TYPE` gives one type per outlet marker (code):

- `PRESSURE_OUTLET`: `MARKER_OUTLET= ( marker, gauge pressure [Pa] )`. This is the usual choice. Zero is a good value, because the pressure level is arbitrary in incompressible flow (advice).
- `MASS_FLOW_OUTLET`: `MARKER_OUTLET= ( marker, mass flow [kg/s] )`. SU2 adjusts the outlet pressure to reach the target. `INC_OUTLET_DAMPING` (default 0.1) damps these updates.

Put the outlet far enough downstream that no recirculation crosses it (advice, to be reviewed).

### Walls and far field

- `MARKER_HEATFLUX= ( marker, heat flux [W/m²] )`: no-slip wall. Zero means adiabatic.
- `MARKER_ISOTHERMAL= ( marker, temperature [K] )`: no-slip wall at a fixed temperature.
- `MARKER_HEATTRANSFER= ( marker, h [W/(m² K)], T_inf [K] )`: wall with a heat transfer coefficient.
- `MARKER_EULER`: slip wall, for `INC_EULER`.
- `MARKER_SYM`: symmetry plane.
- `MARKER_FAR`: far field. It uses `INC_VELOCITY_INIT`, zero gauge pressure and `INC_TEMPERATURE_INIT` (code).

The [heat transfer guide](../Setup-Guide-Heat-Transfer-CHT/) explains the thermal wall conditions.

### Convective scheme and gradients

For the density-based solver, `CONV_NUM_METHOD_FLOW` accepts these schemes (code):

- `FDS` (flux difference splitting, an upwind scheme). Almost all incompressible test cases use it. It has no tuning parameters ([Convective Schemes](../Convective-Schemes/#incompressible-flow)).
- `JST` and `LAX-FRIEDRICH` (centered schemes with artificial dissipation).

`MUSCL_FLOW= YES` (default) makes the scheme second order. The default limiter is `VENKATAKRISHNAN`, but most incompressible test cases use `SLOPE_LIMITER_FLOW= NONE` (code, test case).
Add a limiter only if the solution shows wiggles, or if the run diverges near sharp gradients (advice, to be reviewed).

For `INC_RANS`, the test cases use `CONV_NUM_METHOD_TURB= SCALAR_UPWIND`. `BOUNDED_SCALAR` is also available for incompressible flow. It corrects for a non-zero velocity divergence during convergence ([Convective Schemes](../Convective-Schemes/#turbulence-and-scalarspecies-equations)).

### Artificial compressibility factor

The density-based solver scales its pseudo-time pressure term with β² = max(4.1, `BETA_FACTOR`) × (maximum velocity)². So `BETA_FACTOR` (default 4.1) changes the result only when you set it above 4.1 (code).
A larger value can make the pressure-velocity coupling more robust, but slower (advice, to be reviewed). Most users keep the default.

### Streamwise periodic flow

Use streamwise periodic flow for one module of a repeating geometry, such as a channel with a row of pins. Read [Streamwise Periodicity](../Streamwise-Periodicity/) and the [tutorial](/tutorials/Inc_Streamwise_Periodic/).

- Join the periodic faces with `MARKER_PERIODIC= ( periodic, donor, rotation center (3), rotation angles (3), translation (3) )`.
- Use `KIND_STREAMWISE_PERIODIC= PRESSURE_DROP` with `STREAMWISE_PERIODIC_PRESSURE_DROP` [Pa] (default 1.0), or `MASSFLOW` with `STREAMWISE_PERIODIC_MASSFLOW` [kg/s]. With `MASSFLOW`, SU2 adapts the pressure drop and damps the update with `INC_OUTLET_DAMPING` (code).
- With the energy equation, `STREAMWISE_PERIODIC_TEMPERATURE= YES` makes the temperature periodic too. It allows only `MARKER_HEATFLUX` and `MARKER_SYM`, no `MARKER_ISOTHERMAL` (code). With `NO`, SU2 removes heat at the outlet; set the amount with `STREAMWISE_PERIODIC_OUTLET_HEAT` [W].
- SU2 stops unless `INC_NONDIM= DIMENSIONAL`. `INC_EULER` and `AXISYMMETRIC= YES` are not supported (code).

### Iterations and CFL number

- Steady runs: set `ITER` (default 1000) or `INNER_ITER`. `CFL_NUMBER` sets the pseudo-time step (default 1.25) (code). The incompressible test cases use CFL numbers from 10 to 1000, and up to 50000 in a streamwise periodic case, all with `TIME_DISCRE_FLOW= EULER_IMPLICIT` (test case).
- `CFL_ADAPT= YES` with `CFL_ADAPT_PARAM` lets SU2 raise the CFL number while the residuals fall, as in the NACA 0012 RANS test case (test case).
- Unsteady runs: set `TIME_DOMAIN= YES`, `TIME_MARCHING= DUAL_TIME_STEPPING-2ND_ORDER`, `TIME_STEP`, `TIME_ITER` and `INNER_ITER`. See the [von Karman tutorial](/tutorials/Inc_Von_Karman/) and [Solver Setup](../Solver-Setup/).
- `MGLEVEL` (default 0) adds multigrid levels. Some inviscid and laminar test cases use 3 levels (test case).

## Check convergence and results

- **Residuals.** The default convergence field is `RMS_PRESSURE` for the density-based solver and `RMS_VELOCITY-X` for the pressure-based solver (code). Set `CONV_FIELD` and `CONV_RESIDUAL_MINVAL` (log10 of the residual, default −14). A drop of 4 to 6 orders is a common target for steady engineering cases (advice, to be reviewed).
- **Field names.** SU2 ignores unknown names in `CONV_FIELD` and prints `Ignoring Convergence Field(s)` at the start. If all names are unknown, the convergence check is off and the run goes on to `ITER` (code).
- **Integrated values.** Monitor a value you care about, for example `DRAG` on `MARKER_MONITORING` markers, or `SURFACE_PRESSURE_DROP` on `MARKER_ANALYZE` markers. A stop based on a coefficient uses `CONV_CAUCHY_ELEMS` and `CONV_CAUCHY_EPS` ([Solver Setup](../Solver-Setup/#setting-convergence-criteria)).
- **Mass balance.** Add the inlets and outlets to `MARKER_ANALYZE`, and `FLOW_COEFF_SURF` to `HISTORY_OUTPUT`. The history file then has the mass flow of each marker. Inlet and outlet mass flows should agree to a small fraction of a percent at convergence (advice, to be reviewed).
- **Reference values.** Read the table of reference and non-dimensional values printed at the start of the run. Check that density, viscosity and Reynolds number are what you intended.
- **Energy equation.** With the energy equation, `RMS_ENTHALPY` is the residual of the energy equation (code). `TOTAL_HEATFLUX` gives the heat flux through the `MARKER_MONITORING` markers.

## Common problems

| Symptom | Likely cause | What to try |
|---|---|---|
| SU2 stops: "Sutherland's law only valid for ideal gases in incompressible flows". | The default `VISCOSITY_MODEL` is `SUTHERLAND` (code). | Set `VISCOSITY_MODEL= CONSTANT_VISCOSITY` and `MU_CONSTANT`. |
| SU2 stops: "Inlet types for incompressible problem improperly specified". | `INC_INLET_TYPE` has fewer entries than `MARKER_INLET` has markers (code). | Give one type per inlet marker, for example `INC_INLET_TYPE= VELOCITY_INLET, PRESSURE_INLET`. The same applies to `INC_OUTLET_TYPE`. |
| SU2 stops: "Variable density incompressible solver limited to ideal gases". | `INC_DENSITY_MODEL= VARIABLE` with the default `FLUID_MODEL= STANDARD_AIR` (code). | Set `FLUID_MODEL= INC_IDEAL_GAS` or `INC_IDEAL_GAS_POLY`. |
| SU2 stops: "Inviscid incompressible problems must be constant density". | `INC_EULER` with variable density or with the energy equation (code). | Use `INC_NAVIER_STOKES`, or `INC_DENSITY_MODEL= CONSTANT` and `INC_ENERGY_EQUATION= NO`. |
| The density does not follow `THERMODYNAMIC_PRESSURE`. | With `INC_IDEAL_GAS`, the default `INIT_OPTION_INC= DENSITY_INIT` rescales the operating pressure to match `INC_DENSITY_INIT` (code). | Set `INIT_OPTION_INC= OPERATING_PRESSURE`, or choose an `INC_DENSITY_INIT` that matches your pressure. |
| `FLUID_MODEL` seems to have no effect. | `INC_DENSITY_MODEL` is `CONSTANT` or `BOUSSINESQ`, so SU2 uses `CONSTANT_DENSITY` (code). | Use `INC_DENSITY_MODEL= VARIABLE`. |
| Non-physical values or a division by zero at the start of a closed-cavity case. | `INC_VELOCITY_INIT` is zero with `INC_NONDIM= INITIAL_VALUES` (code). | Set a small non-zero initial velocity, or use `INC_NONDIM= DIMENSIONAL`. |
| The temperature hits a limit; SU2 reports non-physical points. | The temperature left `TEMPERATURE_LIMITS` (default 0 K to 5000 K), so SU2 rejects the update in those points (code). | Lower the CFL number and check the thermal boundary values. Widen `TEMPERATURE_LIMITS` only if the range is physical. |
| The residuals stall or oscillate. | The CFL number is too high, or the flow is really unsteady (advice). | Lower `CFL_NUMBER` or use `CFL_ADAPT`. If the flow sheds vortices, run it unsteady (to be reviewed). |
| A pressure inlet case converges slowly. | `INC_INLET_DAMPING` slows down the update of the inlet velocity (code). | Try a larger `INC_INLET_DAMPING` (to be reviewed). |
| A streamwise periodic case stops at the start. | `INC_NONDIM` is not `DIMENSIONAL`, or an isothermal wall is used with `STREAMWISE_PERIODIC_TEMPERATURE= YES` (code). | Set `INC_NONDIM= DIMENSIONAL`. Use `MARKER_HEATFLUX`, or set `STREAMWISE_PERIODIC_TEMPERATURE= NO`. |
| The flow from a pressure inlet or a far field goes the wrong way. | The direction vector or `INC_VELOCITY_INIT` points the wrong way (advice). | Check the signs of the direction components against the mesh axes. |

## Related tutorials and test cases

Tutorials:

- [Inviscid Hydrofoil](/tutorials/Inc_Inviscid_Hydrofoil/): `INC_EULER`.
- [Laminar Flat Plate with Heat Transfer](/tutorials/Inc_Laminar_Flat_Plate/): constant density with the energy equation.
- [Laminar Buoyancy-driven Cavity](/tutorials/Inc_Laminar_Cavity/): `VARIABLE` density, `INC_IDEAL_GAS`, gravity.
- [Laminar Backward-facing Step](/tutorials/Inc_Laminar_Step/): inlet profile from a file.
- [Turbulent Flat Plate](/tutorials/Inc_Turbulent_Flat_Plate/) and [Turbulent NACA 0012](/tutorials/Inc_Turbulent_NACA0012/): `INC_RANS` and non-dimensionalization.
- [Turbulent Bend with wall functions](/tutorials/Inc_Turbulent_Bend/).
- [Unsteady von Karman vortex shedding](/tutorials/Inc_Von_Karman/): unsteady incompressible flow.
- [Streamwise Periodic Flow](/tutorials/Inc_Streamwise_Periodic/).
- [Wind velocity and pollutant dispersion in a city](/tutorials/Inc_Urban_City/).

Test cases (density-based unless noted):

- [`incomp_euler/naca0012/incomp_NACA0012.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/incomp_euler/naca0012/incomp_NACA0012.cfg): inviscid airfoil.
- [`incomp_euler/nozzle/inv_nozzle.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/incomp_euler/nozzle/inv_nozzle.cfg): `PRESSURE_INLET` with `MASS_FLOW_OUTLET`.
- [`incomp_navierstokes/bend/lam_bend.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/incomp_navierstokes/bend/lam_bend.cfg): the start config above.
- [`incomp_navierstokes/cylinder/incomp_cylinder.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/incomp_navierstokes/cylinder/incomp_cylinder.cfg): laminar external flow with `MARKER_FAR`.
- [`incomp_navierstokes/cylinder/poly_cylinder.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/incomp_navierstokes/cylinder/poly_cylinder.cfg): `INC_IDEAL_GAS_POLY` with polynomial viscosity and conductivity.
- [`incomp_navierstokes/buoyancy_cavity/lam_buoyancy_cavity.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/incomp_navierstokes/buoyancy_cavity/lam_buoyancy_cavity.cfg): natural convection.
- [`incomp_navierstokes/streamwise_periodic/pipeSlice_3d/sp_pipeSlice_3d_dp_hf_tp.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/incomp_navierstokes/streamwise_periodic/pipeSlice_3d/sp_pipeSlice_3d_dp_hf_tp.cfg): streamwise periodic pipe.
- [`incomp_rans/naca0012/naca0012.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/incomp_rans/naca0012/naca0012.cfg): `INC_RANS` with `SA` and `CFL_ADAPT`.
- [`incomp_rans/naca0012/naca0012_SST_SUST.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/incomp_rans/naca0012/naca0012_SST_SUST.cfg): `INC_RANS` with `SST`.
- [`incomp_navierstokes/bend/pb_lam_bend.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/incomp_navierstokes/bend/pb_lam_bend.cfg): pressure-based solver.

User guide pages: [Physical Definition](../Physical-Definition/#flow-condition-incompressible), [Markers and BC](../Markers-and-BC/), [Theory](../Theory/#incompressible-navier-stokes), [Convective Schemes](../Convective-Schemes/), [Solver Setup](../Solver-Setup/), [Custom Output](../Custom-Output/).

Last checked against SU2 develop `11c177b904`.
