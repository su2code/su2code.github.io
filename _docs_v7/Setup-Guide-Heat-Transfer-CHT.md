---
title: "Setup Guide: Heat Transfer and Conjugate Heat Transfer"
permalink: /docs_v7/Setup-Guide-Heat-Transfer-CHT/
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

Use this guide when temperature matters in your simulation:

- a fluid with heated or cooled walls,
- heat conduction in a solid alone,
- conjugate heat transfer (CHT): heat flows between a fluid zone and one or more solid zones, and SU2 solves all zones together.

The examples use the incompressible solver. CHT also works with the compressible `NAVIER_STOKES` solver; see the test case [`coupled_cht/comp_2d`](https://github.com/su2code/SU2/blob/develop/TestCases/coupled_cht/comp_2d/cht_2d_3cylinders.cfg).
For the fluid settings, read [Setup Guide: Incompressible Flows](../Setup-Guide-Incompressible/) first.
For the general multizone setup, read [Basics of Multi-Zone Computations](../Multizone/).

Every option is listed in the [option reference](../Option-Reference/).
Every output field is listed in the [output fields reference](../Output-Fields-Reference/).

## Start from

This setup is a 2D laminar air flow around three cylinders. Each cylinder is a solid zone with a hot core at 350 K.
It is the test case [`coupled_cht/incomp_2d`](https://github.com/su2code/SU2/blob/develop/TestCases/coupled_cht/incomp_2d/cht_2d_3cylinders.cfg) with fewer options. The [steady CHT tutorial](/tutorials/Static_CHT/) uses the same case.
Changes to the test case: `OUTER_ITER` is raised from 11 to 2000, and `HISTORY_OUTPUT` and `OUTPUT_FILES` are added to the main file.
The mesh `mesh_cht_3cyl.su2` holds all four zones. It is in the folder `coupled_cht/incomp_2d` of the [TestCases repository](https://github.com/su2code/TestCases).

Main config file `cht_2d_3cylinders.cfg`:

```
SOLVER= MULTIPHYSICS
CONFIG_LIST= (flow_cylinder.cfg, solid_cylinder1.cfg, solid_cylinder2.cfg, solid_cylinder3.cfg)
%
% Pairs of markers that touch: fluid side, solid side
MARKER_ZONE_INTERFACE= (cylinder_outer1, cylinder_inner1, cylinder_outer2, cylinder_inner2, cylinder_outer3, cylinder_inner3)
MARKER_CHT_INTERFACE= (cylinder_outer1, cylinder_inner1, cylinder_outer2, cylinder_inner2, cylinder_outer3, cylinder_inner3)
CHT_COUPLING_METHOD= DIRECT_TEMPERATURE_ROBIN_HEATFLUX
%
TIME_DOMAIN= NO
OUTER_ITER= 2000
%
MESH_FILENAME= mesh_cht_3cyl.su2
MESH_FORMAT= SU2
HISTORY_OUTPUT= (ITER, BGS_RES[0], BGS_RES[1], HEAT[0])
OUTPUT_FILES= (RESTART, PARAVIEW_MULTIBLOCK)
```

Fluid zone `flow_cylinder.cfg`:

```
SOLVER= INC_NAVIER_STOKES
KIND_TURB_MODEL= NONE
%
INC_DENSITY_MODEL= VARIABLE
INC_ENERGY_EQUATION= YES
INC_DENSITY_INIT= 0.000210322
INC_VELOCITY_INIT= ( 3.40297, 0.0, 0.0 )
INC_TEMPERATURE_INIT= 288.15
INC_NONDIM= DIMENSIONAL
FLUID_MODEL= INC_IDEAL_GAS
SPECIFIC_HEAT_CP= 1004.703
MOLECULAR_WEIGHT= 28.96
VISCOSITY_MODEL= CONSTANT_VISCOSITY
MU_CONSTANT= 1.7893e-05
CONDUCTIVITY_MODEL= CONSTANT_PRANDTL
PRANDTL_LAM= 0.72
%
MARKER_FAR= ( farfield )
MARKER_MONITORING= ( cylinder_outer1, cylinder_outer2, cylinder_outer3 )
%
NUM_METHOD_GRAD= GREEN_GAUSS
CONV_NUM_METHOD_FLOW= FDS
MUSCL_FLOW= YES
SLOPE_LIMITER_FLOW= NONE
TIME_DISCRE_FLOW= EULER_IMPLICIT
CFL_NUMBER= 10.0
LINEAR_SOLVER= FGMRES
LINEAR_SOLVER_PREC= ILU
LINEAR_SOLVER_ERROR= 1E-15
LINEAR_SOLVER_ITER= 5
```

Solid zone `solid_cylinder1.cfg` (zones 2 and 3 are the same, with `core2` and `core3`):

```
SOLVER= HEAT_EQUATION
INC_NONDIM= DIMENSIONAL
FREESTREAM_TEMPERATURE= 350.0
%
MATERIAL_DENSITY= 0.000210322
SPECIFIC_HEAT_CP= 1004.703
THERMAL_CONDUCTIVITY_CONSTANT= 0.1028
%
MARKER_ISOTHERMAL= ( core1, 350.0 )
%
NUM_METHOD_GRAD= GREEN_GAUSS
TIME_DISCRE_HEAT= EULER_IMPLICIT
CFL_NUMBER= 10.0
LINEAR_SOLVER= FGMRES
LINEAR_SOLVER_PREC= ILU
LINEAR_SOLVER_ERROR= 1E-15
LINEAR_SOLVER_ITER= 5
```

The zone files do not list the interface markers as boundary conditions. `MARKER_CHT_INTERFACE` in the main file sets them, and the zone files inherit every option of the main file ([Multizone](../Multizone/#how-to-set-up-a-multi-physics-problem)).

## Settings that matter

### Thermal wall conditions in the fluid

These conditions need the energy equation in the fluid: `INC_ENERGY_EQUATION= YES` for the incompressible solver.

- `MARKER_ISOTHERMAL= ( marker, T [K] )`: fixed wall temperature. Use it when you know the wall temperature.
- `MARKER_HEATFLUX= ( marker, q [W/m²] )`: fixed heat flux. Zero gives an adiabatic wall. With `INTEGRATED_HEATFLUX= YES`, the value is a total heat rate in W, spread over the marker area ([Markers and BC](../Markers-and-BC/#constant-heatflux-no-slip-wall)). In SU2 a positive value adds heat to the domain (to be reviewed).
- `MARKER_HEATTRANSFER= ( marker, h [W/(m² K)], T_inf [K] )`: the wall heat flux is h·(T_inf − T_wall). Use it to model a wall that you do not mesh, such as a thin wall to an outside fluid. h = 0 gives an adiabatic wall; a very large h gives a wall at T_inf ([Markers and BC](../Markers-and-BC/#heat-transfer-or-convection-no-slip-wall)).

Only the flow solvers implement `MARKER_HEATTRANSFER`. The heat equation solver for solids does not (code).

### Temperature without coupling to the flow

If the temperature does not change the flow (constant density and constant properties), you have two options:

- `INC_DENSITY_MODEL= CONSTANT` with `INC_ENERGY_EQUATION= YES`: the flow solver also solves for temperature ([laminar flat plate tutorial](/tutorials/Inc_Laminar_Flat_Plate/)).
- `WEAKLY_COUPLED_HEAT_EQUATION= YES` with `INC_ENERGY_EQUATION= NO`: SU2 solves the temperature with the separate heat solver, using the flow velocity (code). Its numerics use `CONV_NUM_METHOD_HEAT`, `MUSCL_HEAT`, `TIME_DISCRE_HEAT` and `TIMESTEP_HEAT`. Example: [`disc_adj_heat/primal.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/disc_adj_heat/primal.cfg).

For incompressible CHT, SU2 stops unless the fluid zone has `INC_ENERGY_EQUATION= YES` (code). So in CHT, use the energy equation, not the weakly coupled heat equation.

### Heat conduction in a solid

Set `SOLVER= HEAT_EQUATION` in the solid zone. This solver solves for temperature only.

- `THERMAL_CONDUCTIVITY_CONSTANT` [W/(m K)], `MATERIAL_DENSITY` [kg/m³] and `SPECIFIC_HEAT_CP` [J/(kg K)] define the material.
- The defaults are meant for other uses: 0.0257 W/(m K) for air, 7854 kg/m³ for steel, 1004.703 J/(kg K) for air (code). So always set all three.
- `FREESTREAM_TEMPERATURE` (default 288.15 K) is the initial solid temperature (code).
- Boundary conditions: `MARKER_ISOTHERMAL`, `MARKER_HEATFLUX`, `MARKER_PERIODIC`, and the CHT interface.
- All solid test cases use `INC_NONDIM= DIMENSIONAL` (test case).

In a steady run, only the conductivity changes the final temperature. Density and specific heat matter in unsteady runs (advice, to be reviewed).

A solid alone runs as a normal single-zone case, for example [`solid_heat_conduction/periodic_pins/configSolid.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/solid_heat_conduction/periodic_pins/configSolid.cfg).

### Zones and config files

A CHT case is a multiphysics case ([Multizone](../Multizone/#how-to-set-up-a-multi-physics-problem)):

1. Write one config file per zone. Each one sets `SOLVER`, and the boundary conditions and numerics of the zone.
2. Write a main config file with `SOLVER= MULTIPHYSICS` and `CONFIG_LIST`, the list of zone files. The order in `CONFIG_LIST` gives the zone number, starting at 0.
3. Options that are the same in all zones can go in the main file. The zone files inherit them ([Multizone](../Multizone/#how-to-set-up-a-multi-physics-problem)).

The mesh:

- One file for all zones: `MULTIZONE_MESH= YES` (default). This works with the SU2 mesh format, with `NZONE=` and `IZONE=` in the mesh file ([Multizone](../Multizone/#providing-mesh-information-for-a-multi-zone-problem)).
- One file per zone: `MULTIZONE_MESH= NO`, and `MESH_FILENAME` in each zone file. The [contact resistance tutorial](/tutorials/SS_CR_CHT/) uses three mesh files.

Run each zone alone first, with a fixed temperature or heat flux at the interface, to find numerical settings that work (advice). The [Multizone](../Multizone/#how-to-set-up-a-multi-physics-problem) page gives the same advice.

### Interface markers

Each interface has two markers, one on each side. List the pairs in the main file:

- `MARKER_ZONE_INTERFACE`: pairs of markers that exchange data.
- `MARKER_CHT_INTERFACE`: the same pairs, marked as heat transfer interfaces.

All CHT test cases and tutorials list the pairs in both options (test case, tutorial).

### Coupling method

`CHT_COUPLING_METHOD` decides what crosses the interface (code):

- `DIRECT_TEMPERATURE_ROBIN_HEATFLUX` (default): the fluid gets the solid wall temperature. The solid gets a heat flux computed from its own wall temperature and the fluid temperature next to the wall. This is a Robin condition, which mixes temperature and heat flux. All CHT test cases use this method (test case).
- `DIRECT_TEMPERATURE_NEUMANN_HEATFLUX`: the solid gets the heat flux computed by the fluid. This is a Neumann condition, a prescribed flux.
- `AVERAGED_TEMPERATURE_ROBIN_HEATFLUX` and `AVERAGED_TEMPERATURE_NEUMANN_HEATFLUX`: the fluid wall temperature is a conductivity-weighted average of the temperatures on both sides.

The Robin methods need the fluid conductivity. With `CONDUCTIVITY_MODEL= POLYNOMIAL_CONDUCTIVITY` in an incompressible fluid zone, SU2 stops (code).
Start with the default, because it is the only method used in the tests (advice, to be reviewed).

### Interface interpolation

The two sides of an interface do not need matching meshes ([Multizone](../Multizone/)).
`KIND_INTERPOLATION` chooses how SU2 moves values between them (code):

- `NEAREST_NEIGHBOR` (default): each point takes the value of the closest point on the other side. `NUM_NEAREST_NEIGHBORS` (default 1) sets how many neighbors SU2 uses.
- `ISOPARAMETRIC`: interpolation inside the faces of the other side.
- `RADIAL_BASIS_FUNCTION`: smooth interpolation with radial basis functions (`KIND_RADIAL_BASIS_FUNCTION`).

`WEIGHTED_AVERAGE` is the sliding mesh method for fluid-fluid interfaces, not for CHT.
SU2 uses the method of the donor zone, so set it in the main file to apply it everywhere (code).
No CHT test case changes the default (test case).
With very different mesh sizes on the two sides, `ISOPARAMETRIC` or `RADIAL_BASIS_FUNCTION` can give a smoother interface temperature than `NEAREST_NEIGHBOR` (advice, to be reviewed).

### Contact resistance between solids

`CHT_INTERFACE_CONTACT_RESISTANCE` models imperfect contact between two solids: the temperature jumps across the interface ([tutorial](/tutorials/SS_CR_CHT/)).

These rules come from the code (code):

- Give one value per interface pair, or one value for all pairs. Values must not be negative.
- It acts only between two `HEAT_EQUATION` zones, and only with the two `..._ROBIN_HEATFLUX` coupling methods. On fluid-solid interfaces it has no effect.
- The heat flux is (T − T_wall) / (d/k + R), where d is the distance from the wall to the next point and k the conductivity. So R is in m²·K/W, the inverse of a heat transfer coefficient.

The tutorial gives the values in the order of the pairs in `MARKER_CHT_INTERFACE`: `CHT_INTERFACE_CONTACT_RESISTANCE= (1e-4, 0, 0)` (tutorial).

### Outer and inner iterations

SU2 solves the zones one after the other and exchanges interface data between them. One pass over all zones is an outer iteration.

- `OUTER_ITER` (main file): the number of outer iterations of a steady case, or per time step of an unsteady case.
- `INNER_ITER` (default 1): the iterations of each zone inside one outer iteration (code, tutorial). You can set it per zone file.
- `MULTIZONE_SOLVER`: `BLOCK_GAUSS_SEIDEL` (default) or `BLOCK_JACOBI` (code). Gauss-Seidel uses the newest data of the zones already solved, and Jacobi uses the data of the previous outer iteration (advice).
- `RELAXATION_FACTOR_CHT` (default 1.0, no relaxation): the new interface value is factor × new + (1 − factor) × old (code).
- `ITER` is not allowed in multizone cases: SU2 stops. Use `OUTER_ITER` and `INNER_ITER` (code).

The solid often converges more slowly than the fluid, because heat conduction has no convection to carry information. A large `CFL_NUMBER` in the solid zone helps; the solid-only test case `solid_heat_conduction/periodic_pins` uses 1e8 (advice, to be reviewed).

### Unsteady CHT

Set the time settings in the main file ([unsteady CHT tutorial](/tutorials/Inc_Heated_Cylinders_Unsteady/)):

```
TIME_DOMAIN= YES
TIME_MARCHING= DUAL_TIME_STEPPING-2ND_ORDER
TIME_STEP= 0.05
MAX_TIME= 100.0
TIME_ITER= 3
OUTER_ITER= 10
```

These values are from the test case [`coupled_cht/incomp_2d_unsteady`](https://github.com/su2code/SU2/blob/develop/TestCases/coupled_cht/incomp_2d_unsteady/cht_2d_3cylinders.cfg) (test case). The tutorial uses `OUTER_ITER= 200` to converge the coupling in each time step (tutorial).

- Choose `TIME_STEP` from the time scale of the flow, for example the vortex shedding period ([tutorial](/tutorials/Inc_Heated_Cylinders_Unsteady/)).
- In unsteady runs, the solid density and specific heat matter, so set real material values.
- Solids often respond much more slowly than the fluid. Reaching a periodic state can take many time steps (advice, to be reviewed).

## Check convergence and results

- **Coupling residuals.** In a multizone case, SU2 prints for each zone how much the solution changed since the last outer iteration. These are the block Gauss-Seidel (BGS) residuals. Fields such as `BGS_PRESSURE[0]` and `BGS_TEMPERATURE[1]` are per zone; the number in brackets is the zone. Add the group `BGS_RES[i]` to `HISTORY_OUTPUT` for zone i.
- **Default stop rule.** Without `CONV_FIELD`, a multizone case monitors `AVG_BGS_RES[0]`, the averaged BGS residual of zone 0 (code). Set `CONV_FIELD` and `CONV_RESIDUAL_MINVAL` in the main file to monitor what you need, for example the solid temperature. The pin array test case sets `CONV_RESIDUAL_MINVAL` in its main file (test case).
- **Field names.** SU2 ignores unknown names in `CONV_FIELD` and prints `Ignoring Convergence Field(s)` at the start (code).
- **Heat balance.** Monitor `TOTAL_HEATFLUX` and `AVG_TEMPERATURE` (group `HEAT`) on the interface markers, through `MARKER_MONITORING` in each zone. At convergence, the heat that leaves the solid through the interface should equal the heat that enters the fluid (advice, to be reviewed: check the sign convention of each zone).
- **Per-zone history.** `WRT_ZONE_HIST= YES` writes a history file per zone. `WRT_ZONE_CONV= YES` prints the convergence of each zone (code).
- **Visual check.** `OUTPUT_FILES= (RESTART, PARAVIEW_MULTIBLOCK)` writes one ParaView file with all zones. The temperature should be continuous across solid-fluid interfaces ([contact resistance tutorial](/tutorials/SS_CR_CHT/)).

## Common problems

| Symptom | Likely cause | What to try |
|---|---|---|
| SU2 stops: "You probably want to set INC_ENERGY_EQUATION= YES for the fluid solver". | The incompressible fluid zone has no energy equation (code). | Set `INC_ENERGY_EQUATION= YES` in the fluid zone file. |
| SU2 stops: "ITER must not be used when running multizone". | `ITER` in a zone file or in the main file (code). | Use `OUTER_ITER` in the main file, and `INNER_ITER` if needed. |
| SU2 stops: "Polynomial Conductivity model not implemented for CHT interface". | `POLYNOMIAL_CONDUCTIVITY` with a Robin coupling method (code). | Use `CONSTANT_CONDUCTIVITY` or `CONSTANT_PRANDTL` in the fluid, or a Neumann coupling method. |
| SU2 stops: "Number of CHT interfaces does not match number of contact resistances". | Wrong number of values in `CHT_INTERFACE_CONTACT_RESISTANCE` (code). | Give one value per interface pair, or a single value. |
| The solid stays at its initial temperature. | The interface markers are missing from `MARKER_CHT_INTERFACE` or `MARKER_ZONE_INTERFACE`, or the marker names do not match the mesh (advice). | Check the start-up output: it prints the interface type between each pair of zones. Check the marker names. |
| A wall with `MARKER_HEATTRANSFER` in a solid zone behaves as adiabatic. | The heat equation solver does not implement this condition (code). | Mesh the outer fluid, or use `MARKER_HEATFLUX` or `MARKER_ISOTHERMAL`. |
| The solid temperatures settle far too slowly. | A small CFL number in the solid, or `INNER_ITER= 1` with a very stiff solid (advice). | Raise `CFL_NUMBER` in the solid zone, or raise `INNER_ITER` in the solid zone file (to be reviewed). |
| The outer iterations oscillate. | Strong coupling between zones (advice). | Try `RELAXATION_FACTOR_CHT` below 1, for example 0.5 (to be reviewed). |
| The solid material behaves like steel or like air. | `MATERIAL_DENSITY`, `SPECIFIC_HEAT_CP` or `THERMAL_CONDUCTIVITY_CONSTANT` left at their defaults (code). | Set all three in each solid zone file. |
| The temperature looks blocky along a non-matching interface. | `NEAREST_NEIGHBOR` interpolation between very different meshes (advice). | Try `KIND_INTERPOLATION= ISOPARAMETRIC` (to be reviewed). |
| The result files of different zones overwrite each other. | `MULTIZONE_ADAPT_FILENAME= NO` (advice). | Keep the default `YES`, which adds the zone number to the restart and solution file names (code). |

## Related tutorials and test cases

Tutorials:

- [Laminar Flat Plate with Heat Transfer](/tutorials/Inc_Laminar_Flat_Plate/): isothermal wall, energy equation with constant density.
- [Laminar Buoyancy-driven Cavity](/tutorials/Inc_Laminar_Cavity/): natural convection.
- [Steady CHT, heated cylinders](/tutorials/Static_CHT/): the start setup above.
- [Unsteady CHT, heated cylinders](/tutorials/Inc_Heated_Cylinders_Unsteady/).
- [Solid-to-Solid CHT with Contact Resistance](/tutorials/SS_CR_CHT/).
- [Streamwise Periodic Flow](/tutorials/Inc_Streamwise_Periodic/): includes a CHT pin array.

Test cases:

- [`coupled_cht/incomp_2d`](https://github.com/su2code/SU2/blob/develop/TestCases/coupled_cht/incomp_2d/cht_2d_3cylinders.cfg): steady incompressible CHT.
- [`coupled_cht/incomp_2d_unsteady`](https://github.com/su2code/SU2/blob/develop/TestCases/coupled_cht/incomp_2d_unsteady/cht_2d_3cylinders.cfg): unsteady incompressible CHT.
- [`coupled_cht/comp_2d`](https://github.com/su2code/SU2/blob/develop/TestCases/coupled_cht/comp_2d/cht_2d_3cylinders.cfg): compressible CHT.
- [`incomp_navierstokes/streamwise_periodic/chtPinArray_2d/configMaster.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/incomp_navierstokes/streamwise_periodic/chtPinArray_2d/configMaster.cfg) and [`chtPinArray_3d`](https://github.com/su2code/SU2/blob/develop/TestCases/incomp_navierstokes/streamwise_periodic/chtPinArray_3d/configMaster.cfg): CHT with streamwise periodic flow and heat flux in the pins.
- [`incomp_navierstokes/streamwise_periodic/chtPinArray_2d/BC_HeatTransfer.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/incomp_navierstokes/streamwise_periodic/chtPinArray_2d/BC_HeatTransfer.cfg): the fluid alone, with `MARKER_HEATTRANSFER` in place of the solid.
- [`solid_heat_conduction/periodic_pins/configSolid.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/solid_heat_conduction/periodic_pins/configSolid.cfg): a solid alone.
- [`disc_adj_heat/primal.cfg`](https://github.com/su2code/SU2/blob/develop/TestCases/disc_adj_heat/primal.cfg): weakly coupled heat equation.
- [`flamelet/03_laminar_premixed_ch4_flame_cht_cfd`](https://github.com/su2code/SU2/blob/develop/TestCases/flamelet/03_laminar_premixed_ch4_flame_cht_cfd/lam_prem_ch4_cht_cfd_master.cfg): CHT with a flame.

User guide pages: [Basics of Multi-Zone Computations](../Multizone/), [Markers and BC](../Markers-and-BC/), [Theory: Heat Conduction](../Theory/#heat-conduction), [Solver Setup](../Solver-Setup/), [Custom Output](../Custom-Output/).

Last checked against SU2 develop `11c177b904`.
