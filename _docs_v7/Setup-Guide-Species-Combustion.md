---
title: "Setup Guide: Species Transport and Combustion"
permalink: /docs_v7/Setup-Guide-Species-Combustion/
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

Use this guide when the flow carries more than one chemical species, or a flame:

- **Species transport**: mixing of gases, or a pollutant in air, without reactions. SU2 transports the mass fraction of each species: the mass of that species divided by the total mass.
- **Flamelet model** (FGM, flamelet-generated manifold): laminar premixed, partially premixed and diffusion flames. SU2 transports a few controlling variables. It reads the gas properties and the reaction rates from a table computed beforehand.

`KIND_SCALAR_MODEL` selects one of the two. Both run on top of the flow solver, so read [Setup Guide: Incompressible Flows](../Setup-Guide-Incompressible/) first.
For flames next to solid walls that conduct heat, also read [Setup Guide: Heat Transfer and Conjugate Heat Transfer](../Setup-Guide-Heat-Transfer-CHT/).

Every option is listed in the [option reference](../Option-Reference/).
Every output field is listed in the [output fields reference](../Output-Fields-Reference/).

## Start from

### Species transport: two gas streams mixing

This config mixes two gas streams in a 2D venturi, with the SST turbulence model.
The mixture density depends on the composition (`FLUID_MIXTURE`).
It is the test case [`species_transport/venturi_primitive_3species/species2_primitiveVenturi_mixingmodel.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/species_transport/venturi_primitive_3species/species2_primitiveVenturi_mixingmodel.cfg) with fewer options.
One change from the test case: here `CONV_FIELD` uses `RMS_SPECIES_0`. The test case lists `RMS_SPECIES`, which is not an output field, so SU2 ignores it.
The mesh `primitiveVenturi.su2` is in the same folder of the [TestCases repository](https://github.com/su2code/TestCases).

```
% ------------- Problem -------------%
SOLVER= INC_RANS
KIND_TURB_MODEL= SST
%
% ------------- Flow and mixture -------------%
INC_DENSITY_MODEL= VARIABLE
INC_ENERGY_EQUATION= YES
INC_DENSITY_INIT= 1.1766
INC_VELOCITY_INIT= ( 1.00, 0.0, 0.0 )
INC_TEMPERATURE_INIT= 300.0
INC_NONDIM= DIMENSIONAL
FLUID_MODEL= FLUID_MIXTURE
THERMODYNAMIC_PRESSURE= 101325.0
MOLECULAR_WEIGHT= 28.96, 16.043
SPECIFIC_HEAT_CP= 1009.39, 1009.39
CONDUCTIVITY_MODEL= CONSTANT_CONDUCTIVITY
THERMAL_CONDUCTIVITY_CONSTANT= 0.0357, 0.0357
PRANDTL_LAM= 0.72, 0.72
TURBULENT_CONDUCTIVITY_MODEL= NONE
PRANDTL_TURB= 0.90, 0.90
VISCOSITY_MODEL= CONSTANT_VISCOSITY
MU_CONSTANT= 1.716E-5, 1.716E-5
%
% ------------- Species -------------%
KIND_SCALAR_MODEL= SPECIES_TRANSPORT
DIFFUSIVITY_MODEL= CONSTANT_DIFFUSIVITY
DIFFUSIVITY_CONSTANT= 0.001
SPECIES_INIT= 1.0
SPECIES_CLIPPING= YES
SPECIES_CLIPPING_MIN= 0.0
SPECIES_CLIPPING_MAX= 1.0
%
% ------------- Boundary conditions -------------%
MARKER_HEATFLUX= ( wall, 0.0 )
MARKER_SYM= ( axis )
INC_INLET_TYPE= VELOCITY_INLET, VELOCITY_INLET
MARKER_INLET= ( gas_inlet, 300, 1.0, 1.0, 0.0, 0.0, air_axial_inlet, 300, 1.0, 0.0, -1.0, 0.0 )
MARKER_INLET_SPECIES= ( gas_inlet, 1.0, air_axial_inlet, 0.6 )
INC_OUTLET_TYPE= PRESSURE_OUTLET
MARKER_OUTLET= ( outlet, 0.0 )
MARKER_ANALYZE= ( outlet, gas_inlet, air_axial_inlet )
%
% ------------- Numerics -------------%
NUM_METHOD_GRAD= WEIGHTED_LEAST_SQUARES
CFL_NUMBER= 60
CONV_NUM_METHOD_FLOW= FDS
MUSCL_FLOW= YES
SLOPE_LIMITER_FLOW= NONE
TIME_DISCRE_FLOW= EULER_IMPLICIT
CONV_NUM_METHOD_TURB= SCALAR_UPWIND
MUSCL_TURB= NO
CFL_REDUCTION_TURB= 1.0
CONV_NUM_METHOD_SPECIES= SCALAR_UPWIND
MUSCL_SPECIES= NO
SLOPE_LIMITER_SPECIES= NONE
TIME_DISCRE_SPECIES= EULER_IMPLICIT
CFL_REDUCTION_SPECIES= 1.0
LINEAR_SOLVER= FGMRES
LINEAR_SOLVER_PREC= ILU
LINEAR_SOLVER_ERROR= 1E-8
LINEAR_SOLVER_ITER= 5
%
% ------------- Convergence and output -------------%
ITER= 1000
CONV_FIELD= RMS_PRESSURE, RMS_VELOCITY-X, RMS_VELOCITY-Y, RMS_TKE, RMS_SPECIES_0
CONV_RESIDUAL_MINVAL= -18
CONV_STARTITER= 10
MESH_FILENAME= primitiveVenturi.su2
SCREEN_OUTPUT= INNER_ITER, RMS_PRESSURE, RMS_VELOCITY-X, RMS_TKE, RMS_SPECIES_0, SURFACE_SPECIES_VARIANCE
HISTORY_OUTPUT= RMS_RES, FLOW_COEFF, LINSOL, SPECIES_COEFF, SPECIES_COEFF_SURF
VOLUME_OUTPUT= RESIDUAL, PRIMITIVE
```

With two species, SU2 solves one species equation. The first value of each property list belongs to species 0, the one SU2 solves for. The last species fills the rest of the mass (code).

### Flamelet: laminar premixed methane flame

This config is a laminar premixed methane flame on a burner, with a wall at 450 K.
It is the test case [`flamelet/01_laminar_premixed_ch4_flame_cfd/lam_prem_ch4_cfd.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/flamelet/01_laminar_premixed_ch4_flame_cfd/lam_prem_ch4_cfd.cfg) with fewer options.
The mesh `mesh_structured.cgns` and the table `fgm_ch4.drg` are in the same folder of the [TestCases repository](https://github.com/su2code/TestCases).

Changes to the test case: the test restarts from a converged solution, with `RESTART_SOL= YES` and `FLAME_INIT_METHOD= NONE`.
Here the run starts from scratch, so `RESTART_SOL= NO` and `FLAME_INIT_METHOD= FLAME_FRONT`, with the `FLAME_INIT` values of the test case. The regression tests do not run this combination (to be reviewed).

```
% ------------- Problem -------------%
SOLVER= INC_NAVIER_STOKES
KIND_TURB_MODEL= NONE
RESTART_SOL= NO
%
% ------------- Flow and flamelet fluid model -------------%
INC_DENSITY_MODEL= FLAMELET
INC_DENSITY_INIT= 1.00
INC_VELOCITY_INIT= ( 0.5, 0.0, 0.0 )
INC_TEMPERATURE_INIT= 300.0
INC_NONDIM= DIMENSIONAL
FLUID_MODEL= FLUID_FLAMELET
KIND_SCALAR_MODEL= FLAMELET
DIFFUSIVITY_MODEL= FLAMELET
VISCOSITY_MODEL= FLAMELET
CONDUCTIVITY_MODEL= FLAMELET
%
% ------------- Manifold -------------%
FILENAMES_INTERPOLATOR= (fgm_ch4.drg)
CONTROLLING_VARIABLE_NAMES= (ProgressVariable, EnthalpyTot)
CONTROLLING_VARIABLE_SOURCE_NAMES= (ProdRateTot_PV, NULL)
USER_SCALAR_NAMES= (CO, NOx)
USER_SOURCE_NAMES= (ProdRatePos_Y-CO, ProdRateNegScaled_Y-CO, ProdRateTot_Y-NOx, NULL)
LOOKUP_NAMES= (MolarWeightMix, Conductivity, Cp, HeatRelease, Diffusivity)
%
% ------------- Initial state and ignition -------------%
SPECIES_INIT= (0.0, -210000, 0.0, 0.0)
FLAME_INIT_METHOD= FLAME_FRONT
FLAME_INIT= (0.0032, 0.00, 0.00, 1.0, 0.1, 0.0, 1.0e-3, 0.1)
%
% ------------- Boundary conditions -------------%
INC_INLET_TYPE= VELOCITY_INLET
MARKER_INLET= (inlet, 300.0, 0.20, 1.0, 0.0, 0.0)
MARKER_INLET_SPECIES= (inlet, 0, -193600.0, 0.0, 0.0)
INC_OUTLET_TYPE= PRESSURE_OUTLET
MARKER_OUTLET= (outlet, 0.0)
MARKER_ISOTHERMAL= (wall, 450)
MARKER_SYM= (symmetry, symmetry_2-part-fluid)
MARKER_SPECIES_STRONG_BC= (inlet, outlet, wall)
MARKER_ANALYZE= (inlet, outlet)
%
% ------------- Numerics -------------%
NUM_METHOD_GRAD= WEIGHTED_LEAST_SQUARES
CONV_NUM_METHOD_FLOW= FDS
MUSCL_FLOW= YES
SLOPE_LIMITER_FLOW= NONE
TIME_DISCRE_FLOW= EULER_IMPLICIT
CONV_NUM_METHOD_SPECIES= BOUNDED_SCALAR
MUSCL_SPECIES= YES
SLOPE_LIMITER_SPECIES= NONE
TIME_DISCRE_SPECIES= EULER_IMPLICIT
CFL_NUMBER= 100
CFL_ADAPT= YES
CFL_ADAPT_PARAM= ( 0.95, 1.01, 10.0, 1000, 0.01, 0 )
MGLEVEL= 0
LINEAR_SOLVER= FGMRES
LINEAR_SOLVER_PREC= ILU
LINEAR_SOLVER_ERROR= 1E-03
LINEAR_SOLVER_ITER= 10
%
% ------------- Convergence and output -------------%
ITER= 10000
CONV_FIELD= RMS_PRESSURE
CONV_RESIDUAL_MINVAL= -15
MESH_FILENAME= mesh_structured.cgns
MESH_FORMAT= CGNS
SCREEN_OUTPUT= INNER_ITER, RMS_VELOCITY-X, RMS_PRESSURE, RMS_ProgressVariable, RMS_EnthalpyTot, RMS_CO, RMS_NOx
VOLUME_OUTPUT= SOLUTION, PRIMITIVE, SOURCE, LOOKUP
```

With the default `FLAME_ENTHALPY_BC= FLOW_MARKERS`, SU2 does not use the enthalpy value −193600 in `MARKER_INLET_SPECIES`. It computes the inlet enthalpy from the 300 K of `MARKER_INLET` instead. In the same way, it replaces the initial enthalpy of `SPECIES_INIT` with the value at `INC_TEMPERATURE_INIT` (code).

## Settings that matter

### Choose the scalar model

`KIND_SCALAR_MODEL` takes these values (code):

- `NONE` (default): no species.
- `SPECIES_TRANSPORT`: transport of N species mass fractions. It works with `INC_NAVIER_STOKES`, `INC_RANS`, `NAVIER_STOKES` and `RANS`.
- `FLAMELET`: the flamelet model. All tutorials and test cases use it with `INC_NAVIER_STOKES`.

### Number of species and list lengths

For N species, SU2 solves N−1 transport equations. The last mass fraction is 1 minus the sum of the others ([Theory](../Theory/#species-transport)).

SU2 counts the equations from `SPECIES_INIT`. These lists need exactly one value per equation (code):

- `SPECIES_INIT`,
- `SPECIES_CLIPPING_MIN` and `SPECIES_CLIPPING_MAX` (when clipping is on),
- the values after each marker in `MARKER_INLET_SPECIES` and `MARKER_WALL_SPECIES`.

With `FLUID_MODEL= FLUID_MIXTURE`, these lists need one value per species, that is N values, including the last species (code):

- `MOLECULAR_WEIGHT` and `SPECIFIC_HEAT_CP`,
- `MU_CONSTANT` (or `MU_REF`, `MU_T_REF`, `SUTHERLAND_CONSTANT` for Sutherland's law),
- `THERMAL_CONDUCTIVITY_CONSTANT` or `PRANDTL_LAM`, depending on `CONDUCTIVITY_MODEL`,
- `PRANDTL_TURB` with `TURBULENT_CONDUCTIVITY_MODEL= CONSTANT_PRANDTL_TURB`,
- `CONSTANT_LEWIS_NUMBER` with `DIFFUSIVITY_MODEL= CONSTANT_LEWIS`.

SU2 checks that each mass fraction in `SPECIES_INIT` and `MARKER_INLET_SPECIES`, and their sum, lies between 0 and 1. If not, it prints a message but does not stop (code). Read the start-up output.

### Passive scalar or active mixture

- **Passive scalar** (the species does not change the flow, for example a dilute pollutant): use `INC_DENSITY_MODEL= CONSTANT`. The flow properties are those of a single fluid. Example: [`passive_transport.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/species_transport/passive_transport_validation/passive_transport.cfg) (test case).
- **Active mixture** (density and properties depend on the composition): use `FLUID_MODEL= FLUID_MIXTURE`. It requires `INC_DENSITY_MODEL= VARIABLE` and `KIND_SCALAR_MODEL= SPECIES_TRANSPORT`. The density follows from the ideal gas law, using the mixture molecular weight and `THERMODYNAMIC_PRESSURE` (default 101325 Pa). For this model, `INIT_OPTION_INC` defaults to `OPERATING_PRESSURE`, so `INC_DENSITY_INIT` does not change the operating pressure (code).

For a mixture ([composition-dependent tutorial](/tutorials/Inc_Species_Transport_Composition_Dependent_Model/)):

- The mean molecular weight is a mole-fraction average, equivalently 1/M_mix = Σ(Y_i/M_i) for mass fractions Y_i. Specific heat is a mass-fraction average (tutorial, code).
- `MIXING_VISCOSITY_MODEL` sets the mixing rule for viscosity: `DAVIDSON` (default) or `WILKE` (code).
- With a species model and variable density, SU2 does not switch the energy equation on for you (code). If all streams have the same temperature and the walls are adiabatic, `INC_ENERGY_EQUATION= NO` is possible, as in the tutorial. Otherwise set `INC_ENERGY_EQUATION= YES`.

### Mass diffusivity

`DIFFUSIVITY_MODEL` sets the laminar diffusion coefficient D, in m²/s (code):

| Value | D | Options |
|---|---|---|
| `CONSTANT_DIFFUSIVITY` (default) | constant | `DIFFUSIVITY_CONSTANT`. You must set it; SU2 stops otherwise. |
| `CONSTANT_SCHMIDT` | μ / (ρ Sc) | `SCHMIDT_NUMBER_LAMINAR` (default 1.0) |
| `UNITY_LEWIS` | k / (ρ c_p) | none |
| `CONSTANT_LEWIS` | k / (Le ρ c_p) | `CONSTANT_LEWIS_NUMBER`, one value per species |
| `FLAMELET` | read from the flamelet table | only with `FLUID_FLAMELET` |

Here μ is the viscosity, k the thermal conductivity, c_p the specific heat, Sc the Schmidt number and Le the Lewis number.
For RANS, turbulence adds μ_t / Sc_t to ρD, with `SCHMIDT_NUMBER_TURBULENT` (default 0.7) as Sc_t ([Theory](../Theory/#species-transport)).

For gases that diffuse fast, such as hydrogen, the [composition-dependent tutorial](/tutorials/Inc_Species_Transport_Composition_Dependent_Model/) suggests `CONSTANT_LEWIS` (tutorial).
`UNITY_LEWIS` and `CONSTANT_LEWIS` prescribe the ratio of thermal to mass diffusivity; they do not reproduce general multicomponent diffusion or thermal diffusion. Hydrogen-rich mixtures can require differential-diffusion treatment, but choose coefficients for the actual composition and state (advice, to be reviewed).

### Species boundary conditions

Species boundary conditions sit on top of the flow boundary conditions (code):

- **Inlet**: every `MARKER_INLET` marker needs an entry in `MARKER_INLET_SPECIES= ( marker, Y_1, ..., Y_N-1, ... )`. The values are mass fractions. Inlet profiles from a file are possible, see [`species3_primitiveVenturi_inletFile.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/species_transport/venturi_primitive_3species/species3_primitiveVenturi_inletFile.cfg).
- **Outlet**: zero gradient. Nothing to set.
- **Far field**: the values of `SPECIES_INIT`.
- **Walls**: zero flux by default. `MARKER_WALL_SPECIES= ( marker, FLUX, value, VALUE, value, ... )` sets, per species, a flux (`FLUX`) or a fixed mass fraction (`VALUE`). The pairs follow the species order, for example `MARKER_WALL_SPECIES= ( wall, VALUE, 1.0, FLUX, 0.01 )` (test case). The `FLUX` value enters `CSpeciesSolver::BC_Wall_Generic` directly as a scalar mass flux per area, with positive values adding the species to the domain. With `INC_NONDIM= DIMENSIONAL` its units are kg/(m² s). Otherwise normalize by the reference density times reference velocity; this boundary routine performs no automatic dimensional conversion (code).

`MARKER_SPECIES_STRONG_BC` lists markers where SU2 imposes the species values directly in the solution: a strong, or Dirichlet, condition. By default, SU2 imposes them through the boundary flux: a weak condition (code).

- At an inlet, the strong condition fixes the inlet mass fractions.
- At an outlet, it copies the value of the neighbor point inside.
- For the flamelet model, at an isothermal wall it fixes the enthalpy that matches the wall temperature.

The sources give different advice:

- The [composition-dependent tutorial](/tutorials/Inc_Species_Transport_Composition_Dependent_Model/) advises strong conditions with `SCALAR_UPWIND`, and no strong conditions with `BOUNDED_SCALAR` (tutorial).
- The flamelet test cases use strong conditions at inlets, outlets and walls together with `BOUNDED_SCALAR` (test case).

Start from the test case closest to your problem (to be reviewed).

### Numerics for the species equations

- `CONV_NUM_METHOD_SPECIES`: `SCALAR_UPWIND` (default) or `BOUNDED_SCALAR`. Centered schemes are not available for scalars (code). `BOUNDED_SCALAR` subtracts the effect of a non-zero velocity divergence during convergence, which helps avoid scalar overshoots from an unconverged continuity equation; it is not a general bound-preservation guarantee ([Convective Schemes](../Convective-Schemes/#turbulence-and-scalarspecies-equations)). The [combustion tutorial](/tutorials/Inc_Combustion/) highly recommends it for flamelet runs.
- `MUSCL_SPECIES` (default `NO`) makes the scheme second order. `SLOPE_LIMITER_SPECIES` (default `NONE`) adds a limiter (code).
- `TIME_DISCRE_SPECIES`: `EULER_IMPLICIT` (default) or `EULER_EXPLICIT`. No other value is allowed (code).
- `CFL_REDUCTION_SPECIES` (default 1.0) multiplies the CFL number for the species equations (code).
- `SPECIES_CLIPPING= YES` clips each transported mass fraction to `SPECIES_CLIPPING_MIN` and `SPECIES_CLIPPING_MAX`. For more than two species, clipping individual fractions to [0,1] does not guarantee their sum is at most one or that the reconstructed last species stays nonnegative. Clipping can also disturb species conservation; inspect all fractions and balances. SU2 stops if you switch it on without both limits (code). The composition-dependent tutorial uses clipping with `SCALAR_UPWIND` only; that example uses `BOUNDED_SCALAR` without clipping (tutorial).
- Unsteady runs with dual time stepping and a density that depends on the species cannot use multigrid (`MGLEVEL` above 0) (code).

### Flamelet model: required options

`KIND_SCALAR_MODEL= FLAMELET` requires all of these (code):

- `FLUID_MODEL= FLUID_FLAMELET`,
- `DIFFUSIVITY_MODEL= FLAMELET`, `VISCOSITY_MODEL= FLAMELET`, `CONDUCTIVITY_MODEL= FLAMELET`,
- `INC_DENSITY_MODEL= FLAMELET` (density read from the table, column `Density`) or `VARIABLE` (density from the ideal gas law with the table column `MolarWeightMix`),
- no `WEAKLY_COUPLED_HEAT_EQUATION`.

SU2 switches the energy equation of the flow solver off. The flamelet solver transports the total enthalpy and reads the temperature from the table. So `INC_ENERGY_EQUATION` has no effect (code).

### Flamelet model: the manifold

The manifold is the table of flame data. The [combustion tutorial](/tutorials/Inc_Combustion/) explains how to build it.

- `INTERPOLATION_METHOD`: `LUT` (default, a look-up table in a `.drg` file) or `MLP` (one or more neural networks in `.mlp` files) (code).
- `FILENAMES_INTERPOLATOR`: the file name(s).
- The table must contain `Temperature`, `Cp`, `ViscosityDyn`, `Conductivity` and `DiffusionCoefficient`, plus `Density` or `MolarWeightMix` (see the density model above) (code).
- SU2 divides `MolarWeightMix` by 1000, so it expects g/mol (code).

A look-up table is faster to query, but a 3D table can need a lot of memory per core. Neural networks need less memory and give smoother data, but they are harder to train ([combustion tutorial](/tutorials/Inc_Combustion/)).

### Flamelet model: controlling variables and extra scalars

- `CONTROLLING_VARIABLE_NAMES`: the transported variables, with the names used in the table. The order is progress variable, total enthalpy, then optionally mixture fraction (code, tutorial). The progress variable measures how far combustion has advanced. The mixture fraction measures how much of the mixture came from the fuel stream.
- `CONTROLLING_VARIABLE_SOURCE_NAMES`: one table column per controlling variable, for its reaction source term. Write `NULL` when there is none, for example for enthalpy (tutorial).
- `USER_SCALAR_NAMES`: extra species to transport, such as CO or NO.
- `USER_SOURCE_NAMES`: two names per extra species, a production term and a consumption term. The source is production + consumption × Y. Use `NULL` or `zero` for a missing term (code).
- `LOOKUP_NAMES`: table columns to write in the volume output, with `LOOKUP` in `VOLUME_OUTPUT` (tutorial).
- `PREFERENTIAL_DIFFUSION= YES` adds the preferential diffusion model for hydrogen flames. The table must then contain `Beta_ProgVar`, `Beta_Enth_Thermal`, `Beta_Enth` and `Beta_MixFrac`. This is stated in the config template and used in the tutorial (code, tutorial).
- `THICKENED_FLAME_CORRECTION` (default `YES`) lowers the source terms and raises the diffusion in cells that are larger than the flame thickness. This is intended to improve resolution of an under-resolved flame, but does not guarantee stability or mesh-independent flame properties (code, advice).

`SPECIES_INIT` and `MARKER_INLET_SPECIES` need one value per controlling variable, plus one per extra species (code). In the start config, these are: progress variable, enthalpy, CO, NOx.

### Flamelet model: ignition

The solver must start ("ignite") the flame. `FLAME_INIT_METHOD` takes these values (code, tutorial):

- `NONE` (default): no ignition. Use it for cold flow and for restarts.
- `FLAME_FRONT`: a flat flame front at the start. `FLAME_INIT= ( x, y, z, nx, ny, nz, thickness, burnt length )`: a point on the front, the normal that points to the burnt side, the thickness of the transition, and the length of the burnt zone. This works well when the flow is simple at the start (tutorial).
- `SPARK`: a sphere where SU2 adds source terms for a few iterations. `SPARK_INIT= ( x, y, z, radius, start iteration, number of iterations )`. This works well when the flow needs many iterations to develop, such as in partially premixed flames (tutorial).

Rules (code):

- `SPARK` needs both `SPARK_INIT` and `SPARK_REACTION_RATES`, with at least one rate per transported scalar (controlling variables and extra species).
- `FLAME_INIT_IGNITION` (default 5000 K) is the burnt temperature for `FLAME_FRONT`, and the upper temperature inside the spark. It must be higher than `INC_TEMPERATURE_INIT`.
- The ignition also runs when you restart, unless `FLAME_INIT_METHOD= NONE`.

### Flamelet model: thermal boundary conditions

`FLAME_ENTHALPY_BC` decides where the enthalpy boundary values come from (code):

- `FLOW_MARKERS` (default): from temperatures and heat fluxes. The inlet enthalpy follows from the temperature in `MARKER_INLET`. Walls use `MARKER_ISOTHERMAL` or `MARKER_HEATFLUX`. SU2 finds the enthalpy that gives the wall temperature with a Newton iteration on the table.
- `SPECIES_MARKERS`: the enthalpy and all other scalars come directly from `MARKER_INLET_SPECIES` and `MARKER_WALL_SPECIES`. You must give values that match the temperature you want.

Some pages write `FLAMELET_ENTHALPY_BC`; the option name is `FLAME_ENTHALPY_BC`.
For wall values set per point from Python, see [`SU2_CFD/flamelet_python_bc.md`](https://github.com/su2code/SU2/blob/develop/SU2_CFD/flamelet_python_bc.md) in the code.

Use `FLOW_MARKERS` when you know the temperatures, which is the usual case. It avoids an enthalpy that does not match the table ([diffusion flame tutorial](/tutorials/Inc_Laminar_Diffusion_Flame/)).

## Check convergence and results

- **Residual names.** Species transport: `RMS_SPECIES_0`, `RMS_SPECIES_1`, ... Flamelet: `RMS_` plus the name of the controlling variable or extra species, for example `RMS_ProgressVariable` or `RMS_CO` (code). In multizone runs, `BGS_` fields are available too.
- **Field names.** SU2 ignores unknown names in `CONV_FIELD` and prints `Ignoring Convergence Field(s)` at the start. `RMS_SPECIES` without a number is not a field (code).
- **Linear solver.** `LINSOL_ITER_SPECIES` and `LINSOL_RESIDUAL_SPECIES` (or `LINSOL_ITER_FLAMELET` and `LINSOL_RESIDUAL_FLAMELET`) show whether SU2 solves the species linear systems well (code).
- **Mixing quality.** With `MARKER_ANALYZE`, `SURFACE_SPECIES_0` gives the average mass fraction on those markers, and `SURFACE_SPECIES_VARIANCE` measures how uneven the mixture is there. Add the groups `SPECIES_COEFF` and `SPECIES_COEFF_SURF` to `HISTORY_OUTPUT` (code, tutorial).
- **Mass balance of a species.** For a steady non-reacting case with no volume source and impermeable walls, the advective plus diffusive species influx must balance the outflux. Include prescribed wall fluxes and reaction/volume sources when present; an inlet/outlet-only balance is then insufficient (advice). No output field gives this species mass flow directly. A `CUSTOM_OUTPUTS` expression, such as the one in [`passive_transport.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/species_transport/passive_transport_validation/passive_transport.cfg), can compute a mass-flow-averaged value (to be reviewed).
- **Table misses (flamelet).** Add `LOOKUP` to `VOLUME_OUTPUT` and check the field `TABLE_MISSES`. Points with misses have controlling variables outside the table (code).
- **Flame position (flamelet).** Look at the progress variable and the temperature in ParaView. The flame should not move between the last outputs of a steady run (advice, to be reviewed).

## Common problems

| Symptom | Likely cause | What to try |
|---|---|---|
| SU2 stops: "Make sure all species inputs have the same size". | A species list has a different length from `SPECIES_INIT` (code). | Give N−1 values in `SPECIES_INIT`, in the clipping limits, and per marker in `MARKER_INLET_SPECIES` and `MARKER_WALL_SPECIES`. |
| SU2 stops: "The use of FLUID_MIXTURE requires the number of entries for MOLECULAR_WEIGHT and SPECIFIC_HEAT_CP". | A mixture property list does not have N values (code). | Give one value per species, the last species included. |
| SU2 stops: "The use of FLUID_MIXTURE requires the INC_DENSITY_MODEL option to be VARIABLE". | `FLUID_MIXTURE` with constant density (code). | Set `INC_DENSITY_MODEL= VARIABLE`. For a passive scalar, use constant density without `FLUID_MIXTURE`. |
| SU2 stops: "A DIFFUSIVITY_CONSTANT=<value> has to be set". | `CONSTANT_DIFFUSIVITY` without a value (code). | Set `DIFFUSIVITY_CONSTANT` in m²/s. |
| SU2 stops: "SPECIES_CLIPPING= YES requires the options SPECIES_CLIPPING_MIN/MAX". | Clipping is on without limits (code). | Add both lists. |
| The run never stops at the residual target. | A `CONV_FIELD` name is unknown, for example `RMS_SPECIES` (code). | Use `RMS_SPECIES_0` and the other numbered names. |
| Mass fractions go below 0 or above 1. | Unbounded convection during convergence (advice). | Use `BOUNDED_SCALAR`, or `SPECIES_CLIPPING= YES` with limits 0 and 1 (to be reviewed). |
| Message "... is out of bounds [0,1]" at start-up. | A mass fraction, or a sum of mass fractions, in `SPECIES_INIT` or `MARKER_INLET_SPECIES` is outside 0 to 1. SU2 continues anyway (code). | Fix the values. |
| SU2 stops: "Number of initial species incompatible with number of controlling variables and user scalars". | `SPECIES_INIT` does not have one value per controlling variable and extra species (code). | Count `CONTROLLING_VARIABLE_NAMES` plus `USER_SCALAR_NAMES`. |
| SU2 stops: "Flame ignition temperature must be higher than the initial temperature". | `FLAME_INIT_IGNITION` is not above `INC_TEMPERATURE_INIT` (code). | Raise `FLAME_INIT_IGNITION`. |
| SU2 stops with an error about `FLAME_INIT_METHOD= SPARK`. | `SPARK_INIT` or `SPARK_REACTION_RATES` is missing, or there are too few rates (code). | Give both, with one rate per transported scalar. |
| No flame appears. | `FLAME_INIT_METHOD= NONE` (the default) on a fresh start (code). | Use `FLAME_FRONT` or `SPARK`. |
| The converged flame is reset after a restart. | Ignition runs again on restart, unless `FLAME_INIT_METHOD= NONE` (code). | Set `FLAME_INIT_METHOD= NONE` when you restart. |
| The inlet enthalpy in `MARKER_INLET_SPECIES` has no effect. | `FLAME_ENTHALPY_BC= FLOW_MARKERS` (default) uses the inlet temperature instead (code). | Set the temperature in `MARKER_INLET`, or use `FLAME_ENTHALPY_BC= SPECIES_MARKERS`. |
| SU2 stops with an unknown option `FLAMELET_ENTHALPY_BC`. | Wrong option name, from an older page (code). | Use `FLAME_ENTHALPY_BC`. |
| Many table misses; the temperature jumps. | Controlling variables outside the table, often an enthalpy below the table range at cold walls (advice). | Check the wall and inlet temperatures. Extend the table to lower enthalpy ([diffusion flame tutorial](/tutorials/Inc_Laminar_Diffusion_Flame/)). |
| SU2 stops: "Dual-time stepping with species-dependent variable density does not support MGLEVEL > 0". | Multigrid in an unsteady mixture run (code). | Set `MGLEVEL= 0`. |

## Related tutorials and test cases

Tutorials:

- [Species Transport](/tutorials/Inc_Species_Transport/): mixing in a venturi, species options and output.
- [Composition-Dependent model for Species Transport](/tutorials/Inc_Species_Transport_Composition_Dependent_Model/): `FLUID_MIXTURE`, Lewis number models, `BOUNDED_SCALAR`.
- [Wind velocity and pollutant dispersion in a city](/tutorials/Inc_Urban_City/): smoke as a species, with a source term set from the Python wrapper.
- [Incompressible, Laminar Combustion Simulation](/tutorials/Inc_Combustion/): premixed hydrogen flame with neural networks, preferential diffusion and spark ignition.
- [Incompressible, Laminar counterflow diffusion flame](/tutorials/Inc_Laminar_Diffusion_Flame/): mixture fraction and enthalpy, `FLAME_ENTHALPY_BC`.

Test cases:

- [`species_transport/venturi_primitive_3species`](https://github.com/su2code/SU2/blob/develop/TestCases/species_transport/venturi_primitive_3species/species2_primitiveVenturi_mixingmodel.cfg): mixing, with variants for `BOUNDED_SCALAR`, Wilke viscosity mixing, wall species fluxes and inlet files.
- [`species_transport/passive_transport_validation/passive_transport.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/species_transport/passive_transport_validation/passive_transport.cfg): passive scalar with strong boundary conditions.
- [`species_transport/multizone/configMaster.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/species_transport/multizone/configMaster.cfg): species across two fluid zones.
- [`flamelet/01_laminar_premixed_ch4_flame_cfd`](https://github.com/su2code/SU2/blob/develop/TestCases/flamelet/01_laminar_premixed_ch4_flame_cfd/lam_prem_ch4_cfd.cfg): the flamelet start config.
- [`flamelet/03_laminar_premixed_ch4_flame_cht_cfd`](https://github.com/su2code/SU2/blob/develop/TestCases/flamelet/03_laminar_premixed_ch4_flame_cht_cfd/lam_prem_ch4_cht_cfd_master.cfg): flame with conjugate heat transfer.
- [`flamelet/05_laminar_premixed_ch4_flame_cfd_axi`](https://github.com/su2code/SU2/blob/develop/TestCases/flamelet/05_laminar_premixed_ch4_flame_cfd_axi/lam_prem_ch4_cfd_axi.cfg): axisymmetric flame.
- [`flamelet/06_laminar_partial_premixed_ch4_flame_cfd`](https://github.com/su2code/SU2/blob/develop/TestCases/flamelet/06_laminar_partial_premixed_ch4_flame_cfd/lam_partial_prem_ch4_cfd.cfg): partially premixed flame with a 3D table and mixture fraction.
- [`flamelet/07_laminar_premixed_h2_flame_cfd`](https://github.com/su2code/SU2/blob/develop/TestCases/flamelet/07_laminar_premixed_h2_flame_cfd/laminar_premixed_h2_flame_cfd.cfg): hydrogen flame with neural networks.
- [`flamelet/08_flame_init_method/flamelet_initialization.py`](https://github.com/su2code/SU2/blob/develop/TestCases/flamelet/08_flame_init_method/flamelet_initialization.py): flame front and spark ignition.
- [`flamelet/09_laminar_premixed_ch4_flame_unsteady`](https://github.com/su2code/SU2/blob/develop/TestCases/flamelet/09_laminar_premixed_ch4_flame_unsteady/lam_prem_ch4_unsteady.cfg): unsteady flame.

User guide pages: [Theory: Species Transport and Combustion](../Theory/#species-transport), [Convective Schemes](../Convective-Schemes/), [Markers and BC](../Markers-and-BC/), [Custom Output](../Custom-Output/).

Source review: 22 October 2026, against [SU2 `docs_site` at `41ea6a219a`](https://github.com/rois1995/SU2/tree/41ea6a219ac038574f3d4a5b130c0c1d8af66457). See the [review scope and outstanding validation](../Documentation-Status/#guide-and-model-review). Setup recommendations remain draft where indicated.
