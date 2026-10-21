---
title: "Setup Guide: Steady RANS for External Aerodynamics"
permalink: /docs_v7/Setup-Guide-RANS-External-Aero/
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

Use this guide for a steady, compressible, turbulent flow around a body in open air: an airfoil, a wing, a fuselage or a full aircraft.
"Steady" means that the flow settles to one state that does not change in time.

Use another guide if:

- the flow does not settle, for example with vortex shedding or large separated regions. See [Setup Guide: Unsteady Flows and DES](../Setup-Guide-Unsteady-DES/).
- large laminar regions matter, for example at low Reynolds numbers. See [Setup Guide: Laminar-Turbulent Transition](../Setup-Guide-Transition/).

## Start from

This config comes from the ONERA M6 wing tutorial: `compressible_flow/Turbulent_ONERAM6/turb_ONERAM6.cfg` in the [Tutorials repository](https://github.com/su2code/Tutorials/blob/develop/compressible_flow/Turbulent_ONERAM6/turb_ONERAM6.cfg).
We removed the adjoint, design and output file name options, and the options that have no effect with these settings. All other values are unchanged.
The mesh file is in the same tutorial folder.

```
% ------------- Problem ------------------------------------------------%
SOLVER= RANS
KIND_TURB_MODEL= SA
MATH_PROBLEM= DIRECT
RESTART_SOL= NO
%
% ------------- Free stream (from Mach and Reynolds number) ------------%
MACH_NUMBER= 0.8395
AOA= 3.06
SIDESLIP_ANGLE= 0.0
INIT_OPTION= REYNOLDS
FREESTREAM_OPTION= TEMPERATURE_FS
FREESTREAM_TEMPERATURE= 288.15
REYNOLDS_NUMBER= 11.72E6
REYNOLDS_LENGTH= 0.64607
REF_DIMENSIONALIZATION= FREESTREAM_VEL_EQ_ONE
%
% ------------- Gas and viscosity --------------------------------------%
FLUID_MODEL= STANDARD_AIR
VISCOSITY_MODEL= SUTHERLAND
MU_REF= 1.716E-5
MU_T_REF= 273.15
SUTHERLAND_CONSTANT= 110.4
CONDUCTIVITY_MODEL= CONSTANT_PRANDTL
PRANDTL_LAM= 0.72
PRANDTL_TURB= 0.90
%
% ------------- Reference values for the coefficients ------------------%
REF_ORIGIN_MOMENT_X= 0.25
REF_ORIGIN_MOMENT_Y= 0.00
REF_ORIGIN_MOMENT_Z= 0.00
REF_LENGTH= 0.64607
REF_AREA= 0
%
% ------------- Boundary conditions ------------------------------------%
MARKER_HEATFLUX= ( WING, 0.0 )
MARKER_FAR= ( FARFIELD )
MARKER_SYM= ( SYMMETRY )
MARKER_PLOTTING= ( WING )
MARKER_MONITORING= ( WING )
%
% ------------- Numerics -----------------------------------------------%
NUM_METHOD_GRAD= GREEN_GAUSS
CFL_NUMBER= 100.0
CFL_ADAPT= NO
ITER= 999999
LINEAR_SOLVER= FGMRES
LINEAR_SOLVER_PREC= ILU
LINEAR_SOLVER_ERROR= 1E-10
LINEAR_SOLVER_ITER= 10
MGLEVEL= 0
CONV_NUM_METHOD_FLOW= JST
JST_SENSOR_COEFF= ( 0.5, 0.02 )
TIME_DISCRE_FLOW= EULER_IMPLICIT
CONV_NUM_METHOD_TURB= SCALAR_UPWIND
MUSCL_TURB= NO
TIME_DISCRE_TURB= EULER_IMPLICIT
%
% ------------- Convergence: stop when the drag stops changing ---------%
CONV_FIELD= DRAG
CONV_STARTITER= 10
CONV_CAUCHY_ELEMS= 100
CONV_CAUCHY_EPS= 1E-6
%
% ------------- Input and output ---------------------------------------%
MESH_FILENAME= mesh_ONERAM6_turb_hexa_43008.su2
MESH_FORMAT= SU2
SCREEN_OUTPUT= (INNER_ITER, WALL_TIME, RMS_DENSITY, RMS_NU_TILDE, LIFT, DRAG)
```

The tutorial page [Turbulent ONERA M6](/tutorials/Turbulent_ONERAM6/) explains the free-stream and convergence options of this config.

## Settings that matter

### Turbulence model: SA or SST

Set `SOLVER= RANS` and pick the model with `KIND_TURB_MODEL`. With `SOLVER= RANS`, SU2 stops with an error if `KIND_TURB_MODEL` is `NONE` (code).

**Spalart-Allmaras (`SA`).** SA solves one transport equation, for a modified eddy viscosity.

- With an empty `SA_OPTIONS`, SU2 runs SA without the ft2 term ("SA-noft2") (docs, code).
- `SA_OPTIONS` accepts `NEGATIVE`, `EDWARDS`, `WITHFT2`, `QCR2000`, `COMPRESSIBILITY`, `ROTATION`, `BCM` and `EXPERIMENTAL` (code).
- SA-neg needs the ft2 term: write `SA_OPTIONS= NEGATIVE, WITHFT2`. Without `WITHFT2`, SU2 stops with an error unless you add `EXPERIMENTAL` (code). The test cases use both forms (test case).
- The free-stream value of the SA variable is `FREESTREAM_NU_FACTOR` times the free-stream kinematic viscosity. The default is `3.0` (code, docs).
- Most SU2 external aerodynamics tests use SA: ONERA M6, the SA versions of RAE2822, and 30P30N (test case).

**Menter SST (`SST`).** SST solves two transport equations: one for the turbulent kinetic energy k, one for the specific dissipation rate omega.

- With an empty `SST_OPTIONS`, SU2 runs the 2003 version, "SST-2003m". This is set in `ParseSSTOptions` in `option_structure.hpp` (code). Some older pages say that the default is `V1994m`; the code uses `V2003m`.
- The other `SST_OPTIONS` values are `V1994m`, `V2003m`, `SUSTAINING`, `VORTICITY`, `KATO-LAUNDER`, `UQ`, `COMPRESSIBILITY-WILCOX`, `COMPRESSIBILITY-SARKAR` and `DIMENSIONLESS_LIMIT`. Write `KATO-LAUNDER` with a dash (code).
- SST needs free-stream values for k and omega. They come from `FREESTREAM_TURBULENCEINTENSITY` (a fraction: `0.001` means 0.1 %) and `FREESTREAM_TURB2LAMVISCRATIO` (eddy viscosity over laminar viscosity). The defaults are `0.05` and `10.0` (code). These defaults suit internal flows and may be too high for external aerodynamics (docs).
- External aerodynamics tests use, for example, `FREESTREAM_TURBULENCEINTENSITY= 0.001` with `FREESTREAM_TURB2LAMVISCRATIO= 100.0` (RAE2822 SST), or `0.001` with `0.1` (NACA0012 SST with `SUSTAINING`) (test case).
- In SST, k decays between the far field and the body. Two options stop this decay. `SST_OPTIONS= SUSTAINING` adds source terms that keep the free-stream values (docs). `TURB_FIXED_VALUES= YES` holds k and omega at the far-field values in an upstream region set by `TURB_FIXED_VALUES_DOMAIN` (code). The test `rans/naca0012/turb_NACA0012_sst_fixedvalues.cfg` uses the second one (test case).

**Which one to pick.**

- SA is robust and widely used for attached flows over wings and airfoils (advice).
- SST is often preferred when adverse pressure gradients and separation matter (advice, to be reviewed).
- If the two models give different lift or drag, treat the difference as model uncertainty. Look at the flow where they differ (advice).

See [Physical Definition](../Physical-Definition/#turbulence-models) for the full option list.

### Convective scheme: JST or an upwind scheme

The convective scheme computes the flux of mass, momentum and energy through each cell face. Set it with `CONV_NUM_METHOD_FLOW`. It has no default, so always set it (code).

**JST** (Jameson-Schmidt-Turkel) is a central scheme with added artificial dissipation.

- The two dissipation coefficients are `JST_SENSOR_COEFF= (2nd order, 4th order)`. The default is `( 0.5, 0.02 )` (code, docs).
- JST is robust and allows high CFL numbers. It over-predicts viscous drag on coarse meshes or at low Reynolds numbers (docs).
- `JST_MAT` uses matrix dissipation and gives better viscous drag on such meshes (docs).
- The ONERA M6 tutorial and the RAE2822 tests use JST (tutorial, test case).

**Upwind schemes** use the direction of the waves in the flow. `ROE` is the most used (test case). The others are `L2ROE` and `LMROE` (low Mach number variants), `AUSMPLUSUP`, `AUSMPLUSUP2`, `SLAU`, `SLAU2`, `HLLC` and `MSW` (docs, code).

- An upwind scheme is first order unless you turn on MUSCL reconstruction, see the next section (docs).
- `ENTROPY_FIX_COEFF` sets a lower bound on the Roe dissipation. The default is `0.001` (code). The 30P30N validation case uses `1e-5` (test case).
- The tests `rans/oneram6/turb_ONERAM6.cfg` and `rans/naca0012/turb_NACA0012_sst.cfg` use `ROE` (test case).

**Turbulence equations.** Use `CONV_NUM_METHOD_TURB= SCALAR_UPWIND`. All external aerodynamics tests use it (test case). The code also accepts `BOUNDED_SCALAR`, and the RAE2822 tests use it (code, test case). `MUSCL_TURB` defaults to `NO`, so the turbulence convection is first order unless you change it (code). Most tests keep `MUSCL_TURB= NO` (test case).

See [Convective Schemes](../Convective-Schemes/).

### MUSCL reconstruction and slope limiters

MUSCL reconstruction makes an upwind scheme second order. It uses the solution gradient to compute the values on each side of a face. A slope limiter reduces this gradient near shocks and steep changes, so that the solution does not oscillate.

- `MUSCL_FLOW` defaults to `YES` and `SLOPE_LIMITER_FLOW` defaults to `VENKATAKRISHNAN` (code). MUSCL has no effect on central schemes such as JST (docs).
- For transonic flows with shocks, keep a limiter. The ONERA M6 test uses `VENKATAKRISHNAN` with `VENKAT_LIMITER_COEFF= 1.0` (test case).
- For subsonic flows without shocks, you can turn the limiter off. The NACA0012 SST test at Mach 0.15 uses `SLOPE_LIMITER_FLOW= NONE` and `MUSCL_KAPPA_FLOW= 0.5` (test case).
- `VENKAT_LIMITER_COEFF` defaults to `0.05`. Larger values limit less (code). For `VENKATAKRISHNAN`, its effect depends on the cell size in mesh units. So the right value changes with the mesh and with the non-dimensional scaling (docs).
- `VAN_ALBADA_EDGE` is another option. The 30P30N validation case uses it (test case).
- `LIMITER_ITER` freezes the limiter after this many iterations. The default is `999999` (code). Freezing can help when the residuals stall because the limiter keeps switching (advice, to be reviewed).
- `NUM_METHOD_GRAD` sets the gradient method (default `WEIGHTED_LEAST_SQUARES`). `NUM_METHOD_GRAD_RECON` can set a different method for MUSCL only. By default MUSCL uses `NUM_METHOD_GRAD` (code).

See [Slope Limiters and Shock Resolution](../Slope-Limiters-and-Shock-Resolution/).

### CFL number and adaptive CFL

SU2 marches a steady case in pseudo-time. The CFL number sets the local pseudo-time step. A higher CFL converges in fewer iterations, but each iteration needs a harder linear solve.

- The default `CFL_NUMBER` is `1.25` (code). Implicit RANS runs use much higher values: `100` in the ONERA M6 tutorial, `1000` in the RAE2822 SA and NACA0012 SST tests (tutorial, test case).
- `CFL_ADAPT= YES` lets SU2 change the CFL during the run. `CFL_NUMBER` is then the starting value (code).
- `CFL_ADAPT_PARAM` has up to six values: factor down, factor up, minimum CFL, maximum CFL, acceptable linear solver residual, start iteration. Missing values take the defaults `( 0.1, 1.2, 10.0, 100.0, 0.001, 0 )` (code).
- The comments in `config_template.cfg` explain the rules. The CFL goes up by the "factor up" while the solution update is not limited and the linear solver converges well enough. It goes down when the update is limited, when the linear solver does not converge enough, or when the residuals stall or oscillate. It returns to the minimum if the linear solver diverges or the residuals grow too much (code).
- Examples: the E387 transition tutorial uses `CFL_NUMBER= 1` with `CFL_ADAPT_PARAM= ( 0.1, 2.0, 40.0, 1e10, 0.001 )`. The 30P30N case uses `CFL_ADAPT_PARAM= ( 1, 1.05, 10, 400 )` (tutorial, test case).
- `CFL_REDUCTION_TURB` scales the CFL of the turbulence equations. The default is `1.0` (code). The RAE2822 SST test uses `0.5` (test case).
- Add `AVG_CFL` to `SCREEN_OUTPUT` to see the CFL during the run (test case).

### Multigrid

Multigrid also solves the equations on coarser versions of the mesh. This removes large-scale errors faster.

- `MGLEVEL` sets the number of coarse levels. The default is `0` (off) (code).
- `MGCYCLE` is `V_CYCLE` (default), `W_CYCLE` or `FULLMG_CYCLE` (code).
- The RAE2822 tests use `MGLEVEL= 3` with `JST`, `MGCYCLE= V_CYCLE`, `MG_DAMP_RESTRICTION= 0.75` and `MG_DAMP_PROLONGATION= 0.75` (test case). The code default for both damping factors is `0.5` (code).
- With a central scheme, the coarse levels always use the Lax-Friedrich scheme. MUSCL has no effect on coarse levels (docs).
- If the run is unstable with multigrid, reduce `MGLEVEL` or turn multigrid off (advice).

### Linear solver and preconditioner

Each implicit iteration solves a linear system. You do not need to solve it exactly: only the final nonlinear residual matters for accuracy (docs).

The defaults are `LINEAR_SOLVER= FGMRES`, `LINEAR_SOLVER_PREC= ILU`, `LINEAR_SOLVER_ERROR= 1E-6` and `LINEAR_SOLVER_ITER= 10` (code).

The [Linear Solvers and Preconditioners](../Linear-Solvers-and-Preconditioners/) page gives this advice (docs):

- Use the loosest tolerance that keeps the run stable, usually between `0.05` and `0.001`.
- About 10 linear iterations are enough for upwind schemes. Central schemes may need up to 50.
- Use `ILU` at high CFL. `LU_SGS` can be faster at low CFL because it has no setup cost.
- If memory is a problem, use `RESTARTED_FGMRES` or `BCGSTAB`.

Two more points (test case):

- Add `LINSOL_ITER` and `LINSOL_RESIDUAL` to `SCREEN_OUTPUT` to see how well the linear solver converges.
- A Newton-Krylov method is also available with `NEWTON_KRYLOV= YES`. The 30P30N validation case shows its parameters.

### Convergence criteria

`CONV_FIELD` names the output fields that decide when the run stops. For the compressible solver the default is `RMS_DENSITY` (code). If you list several fields, all of them must meet their criterion (code).

**Residual fields** (such as `RMS_DENSITY`): the run stops when the log10 of the residual falls below `CONV_RESIDUAL_MINVAL`. The default is `-14` (code).

**Coefficient fields** (such as `LIFT` or `DRAG`) use a Cauchy criterion. This criterion looks at how much the coefficient changes from one iteration to the next (code):

- At each iteration, SU2 computes the change of the coefficient divided by the coefficient. If the coefficient is smaller than 0.1 in size, SU2 divides by 0.1 instead.
- SU2 averages this value over the last `CONV_CAUCHY_ELEMS` iterations (default `100`).
- The run stops when the average is below `CONV_CAUCHY_EPS` (default `1E-10`).
- `CONV_STARTITER` (default `5`) sets the first iteration where SU2 checks the criteria.

The ONERA M6 tutorial stops on `CONV_FIELD= DRAG` with `CONV_CAUCHY_EPS= 1E-6` (tutorial).
A coefficient can look converged while the residuals are still high, so check both (advice).

`ITER` sets the maximum number of iterations. The default is `1000` (code).

See [Solver Setup](../Solver-Setup/#setting-convergence-criteria).

### Fixed lift (fixed CL)

In fixed-CL mode, SU2 changes the angle of attack until the lift coefficient reaches a target. These rules come from the code (code):

- `FIXED_CL_MODE= YES` turns it on. `TARGET_CL` is the target (default `0.0`). `AOA` is the starting angle.
- `DCL_DALPHA` is your estimate of the lift slope, per degree. The default is `0.2`, also in `config_template.cfg`. SU2 changes the angle by (target CL − current CL) / `DCL_DALPHA`.
- SU2 updates the angle when the convergence criteria are met but CL is still away from the target. It also updates it at the latest every `UPDATE_AOA_ITER_LIMIT` iterations (default `200`).
- The lift counts as reached when it is within `CONV_CAUCHY_EPS`/2 of the target. So `CONV_CAUCHY_EPS` sets both the convergence tolerance and the lift tolerance.
- At the end, SU2 runs `ITER_DCL_DALPHA` more iterations (default `500`) to compute dCL/dalpha by finite differences. These are added to `ITER`. Set `ITER_DCL_DALPHA= 0` to skip this step.
- Fixed-CL mode is for compressible solvers only.
- Add the `AOA` history field to see the angle during the run.

The RAE2822 design tutorial runs SA in fixed-CL mode with `TARGET_CL= 0.724`, `DCL_DALPHA= 0.2`, `UPDATE_AOA_ITER_LIMIT= 100`, `ITER_DCL_DALPHA= 500` and `CONV_CAUCHY_EPS= 1E-6` (tutorial). The fixed-CL test case `fixed_cl/naca0012/inv_NACA0012.cfg` is inviscid (test case).

### Free stream from Mach and Reynolds number

With `INIT_OPTION= REYNOLDS` (the default), SU2 builds the free stream from the Mach number and the Reynolds number (code, tutorial):

1. It computes the speed of sound from `FREESTREAM_TEMPERATURE` and the gas constants.
2. It computes the velocity from `MACH_NUMBER`, `AOA` and `SIDESLIP_ANGLE`.
3. It computes the viscosity with the viscosity model.
4. It computes the density from `REYNOLDS_NUMBER` and `REYNOLDS_LENGTH`.
5. It computes the pressure from the gas law. `FREESTREAM_PRESSURE` is ignored.

Things to check:

- The mesh must be in meters. `REYNOLDS_LENGTH` is the length (in mesh units) that the Reynolds number refers to, for example the chord (tutorial).
- With `INIT_OPTION= TD_CONDITIONS`, SU2 uses `FREESTREAM_PRESSURE` and `FREESTREAM_TEMPERATURE` instead, and ignores the Reynolds number (tutorial).
- SU2 prints a table of free-stream values before the first iteration. Check it (tutorial).
- `REF_DIMENSIONALIZATION` sets the scaling of the equations. The default is `DIMENSIONAL` (code). The tests also use `FREESTREAM_VEL_EQ_ONE`, `FREESTREAM_VEL_EQ_MACH` and `FREESTREAM_PRESS_EQ_ONE` (tutorial, test case).

**Reference values for the coefficients** (code). `REF_LENGTH` is used for moments. `REF_AREA` is used for all force coefficients. With `REF_AREA= 0`, SU2 computes the area as the projection of the body on the y plane (2D) or the z plane (3D). `REF_ORIGIN_MOMENT_X`, `_Y` and `_Z` set the moment reference point.

See [Physical Definition](../Physical-Definition/#free-stream-definition-compressible).

### Far-field and wall boundary conditions

- `MARKER_FAR` sets a far-field boundary. SU2 imposes the free-stream state there with a characteristic-based condition (docs, tutorial).
- Place the far-field boundary far from the body, often 50 to 100 chords for airfoils, so that it does not change the lift (advice, to be reviewed).
- `MARKER_HEATFLUX= ( wall, 0.0 )` is an adiabatic no-slip wall. All external aerodynamics tests use it (test case). `MARKER_ISOTHERMAL` sets a wall temperature instead (docs).
- `MARKER_SYM` is a symmetry plane, for example at the root of a half wing (tutorial).
- `MARKER_MONITORING` lists the surfaces whose forces give `LIFT`, `DRAG` and the other coefficients (code). `MARKER_PLOTTING` lists the surfaces written to the surface output files (tutorial).

See [Markers and Boundary Conditions](../Markers-and-BC/).

### Near-wall mesh, y+ and wall functions

y+ is the distance of the first point from the wall, in wall units. It tells you if the mesh resolves the thin layer next to the wall.

- Without wall functions, the first point must be in the viscous sublayer: y+ below 5 (docs). y+ about 1 is the usual target (advice).
- With wall functions, SU2 models the near-wall layer, so the first point can be further from the wall. Turn them on per marker: `MARKER_WALL_FUNCTIONS= ( wall, STANDARD_WALL_FUNCTION )`. They work with SA and SST, compressible and incompressible (docs).
- For RANS, only `NO_WALL_FUNCTION` and `STANDARD_WALL_FUNCTION` are tested. `ADAPTIVE_WALL_FUNCTION`, `SCALABLE_WALL_FUNCTION` and `NONEQUILIBRIUM_WALL_MODEL` stop SU2 with an error (code, test case).
- The wall function is active only where y+ is above `WALLMODEL_MINYPLUS` (default `5.0`) (code, docs). The docs give an upper limit of y+ 100 to 500, rising with the Reynolds number (docs).
- Wall functions and `WALL_ROUGHNESS` cannot be used together (code).
- Wall functions assume an attached boundary layer in equilibrium. They are less accurate near separation and strong pressure gradients (advice).
- Check the `Y_PLUS` output field on the wall. It is in the default `PRIMITIVE` output group (code).

See [Markers and Boundary Conditions](../Markers-and-BC/#wall-functions) and the test cases in `TestCases/wallfunctions/flatplate/`.

## Check convergence and results

- **Residuals.** Plot `RMS_DENSITY` and the turbulence residual (`RMS_NU_TILDE` for SA, `RMS_TKE` and `RMS_DISSIPATION` for SST). A drop of several orders of magnitude is a good sign (advice).
- **Coefficients.** `LIFT`, `DRAG` and the moments must be flat at the end of the run. Add the `CAUCHY` group to `HISTORY_OUTPUT` to see the Cauchy values (code).
- **Linear solver and CFL.** `LINSOL_RESIDUAL` should stay below `LINEAR_SOLVER_ERROR` most of the time. With `CFL_ADAPT= YES`, `AVG_CFL` should grow and stay high (advice).
- **Free stream.** Read the free-stream table that SU2 prints at the start: Reynolds number, density, pressure, velocity (tutorial).
- **y+.** Look at `Y_PLUS` on the walls (code).
- **Surface data.** Put `SURFACE_PARAVIEW` or `SURFACE_CSV` in `OUTPUT_FILES`, and plot `PRESSURE_COEFF` and `SKIN_FRICTION-X` along the wall (code, tutorial).
- **Force breakdown.** `WRT_FORCES_BREAKDOWN= YES` writes a file that splits the forces into pressure and viscous parts, per surface (code, tutorial).
- **Mesh.** Run at least two, better three, meshes of different size. Check that the coefficients change less and less (advice).

See [History and Solution Output](../Custom-Output/) and the [Output Fields Reference](../Output-Fields-Reference/).

## Common problems

| Symptom | Likely cause | What to try |
| --- | --- | --- |
| The run diverges in the first iterations. | The CFL is too high for the initial flow. | Start with a low `CFL_NUMBER` and use `CFL_ADAPT= YES`. Check the free-stream table (tutorial). |
| SU2 stops: "A non-standard version of SA-neg was requested". | `NEGATIVE` without the ft2 term. | Use `SA_OPTIONS= NEGATIVE, WITHFT2` (code). |
| The residuals stop dropping and the coefficients oscillate a little. | The limiter keeps switching, or the flow is not steady (buffet, separation). | Raise `VENKAT_LIMITER_COEFF` or freeze the limiter with `LIMITER_ITER` (advice, to be reviewed). If the flow is really unsteady, see [Setup Guide: Unsteady Flows and DES](../Setup-Guide-Unsteady-DES/). |
| `LINSOL_RESIDUAL` stays near 1. | The linear system is too hard at this CFL. | Lower the CFL, use `ILU`, raise `LINEAR_SOLVER_ITER` (docs). |
| The drag is too high with `JST` on a coarse mesh. | Too much numerical dissipation. | Try `JST_MAT`, or an upwind scheme with MUSCL (docs). Refine the mesh. |
| The skin friction or drag is far from the expected value. | Wrong Reynolds number: the mesh is not in meters, or `REYNOLDS_LENGTH` is wrong. | Check the mesh units and the free-stream table (tutorial). |
| SST results depend on the far-field distance. | The free-stream k decays before it reaches the body. | Use `SST_OPTIONS= SUSTAINING` or `TURB_FIXED_VALUES= YES` (docs, code). |
| The run stops at iteration 1000. | `ITER` has a default of `1000`. | Set `ITER` (code). |
| A fixed-CL run ends before CL reaches the target. | The angle is updated too rarely, or `CONV_CAUCHY_EPS` is too large. | Lower `UPDATE_AOA_ITER_LIMIT` and check `CONV_CAUCHY_EPS` (code). |

## Related tutorials and test cases

Tutorials:

- [Turbulent ONERA M6](/tutorials/Turbulent_ONERAM6/): 3D transonic wing, SA, JST, Cauchy criterion on drag.
- [Turbulent Flat Plate](/tutorials/Turbulent_Flat_Plate/): zero pressure gradient flat plate with SA.
- [Constrained shape design of a transonic turbulent airfoil](/tutorials/Turbulent_2D_Constrained_RAE2822/): RAE2822 with SA in fixed-CL mode, used for shape design.
- [UQ NACA0012](/tutorials/UQ_NACA0012/): SST with the `UQ` option.

Test cases (develop branch):

- [rans/oneram6/turb_ONERAM6.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/rans/oneram6/turb_ONERAM6.cfg): ONERA M6 with `ROE`, MUSCL and `VENKATAKRISHNAN`.
- [rans/rae2822/turb_SA_RAE2822.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/rans/rae2822/turb_SA_RAE2822.cfg) and [turb_SST_RAE2822.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/rans/rae2822/turb_SST_RAE2822.cfg): transonic airfoil with `JST` and multigrid.
- [rans/naca0012/turb_NACA0012_sst.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/rans/naca0012/turb_NACA0012_sst.cfg): subsonic airfoil, SST, `ROE` without limiter.
- [rans/naca0012/turb_NACA0012_sst_fixedvalues.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/rans/naca0012/turb_NACA0012_sst_fixedvalues.cfg): `TURB_FIXED_VALUES`.
- [turbulence_models/sa/rae2822/](https://github.com/su2code/SU2/tree/develop/TestCases/turbulence_models/sa/rae2822): SA variants (`NEGATIVE`, `EDWARDS`, `QCR2000`, `COMPRESSIBILITY`).
- [vandv/rans/30p30n/config.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/vandv/rans/30p30n/config.cfg): high-lift airfoil, `ROE` with `VAN_ALBADA_EDGE`, adaptive CFL, Newton-Krylov.
- [vandv/rans/swbli/config_sst.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/vandv/rans/swbli/config_sst.cfg): Mach 5 shock-boundary layer interaction with SST.
- [fixed_cl/naca0012/inv_NACA0012.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/fixed_cl/naca0012/inv_NACA0012.cfg): fixed-CL mode (inviscid).
- [wallfunctions/flatplate/compressible_SA/turb_SA_flatplate.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/wallfunctions/flatplate/compressible_SA/turb_SA_flatplate.cfg): wall functions with SA.

User guide pages:

- [Physical Definition](../Physical-Definition/), [Convective Schemes](../Convective-Schemes/), [Slope Limiters and Shock Resolution](../Slope-Limiters-and-Shock-Resolution/), [Linear Solvers and Preconditioners](../Linear-Solvers-and-Preconditioners/), [Markers and Boundary Conditions](../Markers-and-BC/), [Solver Setup](../Solver-Setup/), [Governing Equations](../Theory/), [History and Solution Output](../Custom-Output/).
- All options: [Option Reference](../Option-Reference/). All output fields: [Output Fields Reference](../Output-Fields-Reference/).

Last checked against SU2 develop `11c177b904`.
