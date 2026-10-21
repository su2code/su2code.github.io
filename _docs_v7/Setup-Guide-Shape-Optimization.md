---
title: "Setup Guide: Shape Optimization with the Discrete Adjoint"
permalink: /docs_v7/Setup-Guide-Shape-Optimization/
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

Use this guide to change the shape of a body or a duct so that an output of the flow improves: for example less drag at a fixed lift, or a lower pressure drop.

SU2 computes the gradient of the output with respect to many shape parameters, at the cost of about one extra flow solution. It does this with the **adjoint method**: one extra solve gives the sensitivity of one output to all shape parameters.

SU2 has two adjoint solvers:

- The **discrete adjoint** differentiates the SU2 code itself with algorithmic differentiation (AD). Its gradient matches the discretized flow equations, including turbulence models and most boundary conditions. This guide focuses on it.
- The **continuous adjoint** solves separate adjoint equations derived by hand. It runs with the normal build, but supports fewer cases.

In this guide, the (code) tag also covers the Python scripts of SU2.

## Start from

The block below comes from the test case [multiple_ffd/naca0012](https://github.com/su2code/SU2/blob/develop/TestCases/multiple_ffd/naca0012/inv_NACA0012_ffd.cfg). It is an inviscid NACA 0012 airfoil with two FFD boxes, one on each side. The regression tests run it with `discrete_adjoint.py`.

- We removed the comments, the continuous adjoint options, the options that have no effect in this setup, and most file names.
- We added `GEO_MARKER` and `GEO_DESCRIPTION` from [optimization_euler/steady_naca0012](https://github.com/su2code/SU2/blob/develop/TestCases/optimization_euler/steady_naca0012/inv_NACA0012_adv.cfg), because the thickness constraint needs SU2_GEO.
- The mesh `mesh_NACA0012_multiFFD.su2` already contains the FFD boxes. It is in the [TestCases repository](https://github.com/su2code/TestCases).

```
SOLVER= EULER
MATH_PROBLEM= DIRECT
RESTART_SOL= NO
READ_BINARY_RESTART= NO
%
MACH_NUMBER= 0.8
AOA= 1.25
FREESTREAM_PRESSURE= 101325.0
FREESTREAM_TEMPERATURE= 288.15
REF_ORIGIN_MOMENT_X= 0.25
REF_ORIGIN_MOMENT_Y= 0.00
REF_ORIGIN_MOMENT_Z= 0.00
REF_LENGTH= 1.0
REF_AREA= 1.0
REF_DIMENSIONALIZATION= FREESTREAM_PRESS_EQ_ONE
%
MARKER_EULER= ( airfoil_upper, airfoil_lower )
MARKER_FAR= ( farfield )
MARKER_PLOTTING= ( airfoil_upper, airfoil_lower )
MARKER_MONITORING= ( airfoil_upper, airfoil_lower )
%
NUM_METHOD_GRAD= GREEN_GAUSS
CFL_NUMBER= 5.0
LINEAR_SOLVER= FGMRES
LINEAR_SOLVER_PREC= ILU
LINEAR_SOLVER_ERROR= 1E-1
LINEAR_SOLVER_ITER= 3
MGLEVEL= 3
MGCYCLE= V_CYCLE
MG_PRE_SMOOTH= ( 2, 2, 2, 2 )
MG_POST_SMOOTH= ( 2, 2, 2, 2 )
MG_CORRECTION_SMOOTH= ( 1, 1, 1, 1 )
MG_DAMP_RESTRICTION= 0.5
MG_DAMP_PROLONGATION= 0.5
CONV_NUM_METHOD_FLOW= JST
JST_SENSOR_COEFF= ( 0.5, 0.02 )
TIME_DISCRE_FLOW= EULER_IMPLICIT
%
OBJECTIVE_FUNCTION= DRAG
%
% The test stops after 10 iterations. A useful gradient needs a converged
% flow and adjoint solution: raise ITER.
ITER= 10
CONV_RESIDUAL_MINVAL= -9
CONV_STARTITER= 10
%
DV_KIND= FFD_SETTING
DV_MARKER= ( airfoil_upper, airfoil_lower )
DV_PARAM= ( UPPER, 1, 0, 0, 0.0, 1.0, 0.0 )
DV_VALUE= 0.001
DEFORM_LINEAR_SOLVER_ITER= 500
DEFORM_NONLINEAR_ITER= 1
DEFORM_CONSOLE_OUTPUT= YES
DEFORM_LINEAR_SOLVER_ERROR= 1E-14
DEFORM_STIFFNESS_TYPE= INVERSE_VOLUME
%
FFD_TOLERANCE= 1E-10
FFD_ITERATIONS= 500
FFD_DEFINITION= ( LOWER, 0.075, -0.075, 0.0, 0.625, -0.075, 0.0, 0.625, -0.02, 0.0, 0.075, -0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ); ( UPPER, 0.075, 0.02, 0.0, 0.625, 0.02, 0.0, 0.625, 0.075, 0.0, 0.075, 0.075, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 )
FFD_DEGREE= ( 4, 1, 0 ); ( 4, 1, 0 )
FFD_CONTINUITY= USER_INPUT
FFD_FIX_I= (0,4)
FFD_FIX_J= (15)
FFD_FIX_K= (15)
%
GEO_MARKER= ( airfoil_upper, airfoil_lower )
GEO_DESCRIPTION= AIRFOIL
%
MESH_FILENAME= mesh_NACA0012_multiFFD.su2
MESH_FORMAT= SU2
HISTORY_OUTPUT= (ITER, RMS_RES, AERO_COEFF)
OUTPUT_FILES= (RESTART_ASCII)
%
OPT_OBJECTIVE= DRAG * 0.001
OPT_CONSTRAINT= ( LIFT > 0.327 ) * 0.001; ( MOMENT_Z > 0.0 ) * 0.001; ( AIRFOIL_THICKNESS > 0.12 ) * 0.001
OPT_ITERATIONS= 1
OPT_ACCURACY= 1E-6
OPT_BOUND_UPPER= 0.1
OPT_BOUND_LOWER= -0.1
% This test uses the 3D kind 11 (FFD_CONTROL_POINT) on a 2D mesh.
% The 2D tutorials use kind 19 (FFD_CONTROL_POINT_2D).
DEFINITION_DV= ( 11, 1.0 | airfoil_upper | UPPER, 1, 0, 0, 0.0, 1.0, 0.0 ); ( 11, 1.0 | airfoil_lower | LOWER, 1, 0, 0, 0.0, 1.0, 0.0 )
```

Run the gradient only:

```
discrete_adjoint.py -f inv_NACA0012_ffd.cfg
```

Run an optimization (raise `OPT_ITERATIONS` first):

```
shape_optimization.py -g DISCRETE_ADJOINT -f inv_NACA0012_ffd.cfg
```

For a RANS case, start from the [RAE 2822 tutorial](/tutorials/Turbulent_2D_Constrained_RAE2822/) or the test case [optimization_rans/steady_rae2822](https://github.com/su2code/SU2/blob/develop/TestCases/optimization_rans/steady_rae2822/turb_SA_RAE2822.cfg). For a 3D wing, start from the [ONERA M6 tutorial](/tutorials/Inviscid_3D_Constrained_ONERAM6/).

## Settings that matter

### Build SU2 with AD

- Configure with `./meson.py setup build -Denable-autodiff=true` (code). See [Build SU2 on Linux/MacOS](../Build-SU2-Linux-MacOS/).
- This build gives the AD programs `SU2_CFD_AD` and `SU2_DOT_AD`, next to the normal `SU2_CFD`, `SU2_DEF`, `SU2_DOT` and `SU2_GEO` (tutorial). The optimization loop needs all of them.
- `SU2_CFD` stops with "MATH_PROBLEM= DISCRETE_ADJOINT requires AD support" if you give it a discrete adjoint config (code). Use `SU2_CFD_AD` for the adjoint run.
- The Python scripts need NumPy and SciPy (tutorial).
- The CoolProp fluid models cannot be used with the AD build (code).
- To check gradients with forward-mode AD, also build with `-Denable-directdiff=true` (code).

### Discrete or continuous adjoint

- `MATH_PROBLEM` takes `DIRECT`, `CONTINUOUS_ADJOINT` or `DISCRETE_ADJOINT` (code).
- With the Python scripts, keep `MATH_PROBLEM= DIRECT` in your file. The scripts set the adjoint value themselves, from the gradient method you choose on the command line (code).
- To run by hand: run `SU2_CFD` for the flow, and copy the restart file to the name in `SOLUTION_FILENAME`. Then run `SU2_CFD_AD` with `MATH_PROBLEM= DISCRETE_ADJOINT`. Then run `SU2_DOT_AD`, which turns the surface sensitivities into the gradient for the design variables (tutorial, to be reviewed: check the file names against the scripts).
- The discrete adjoint uses the numerical settings of the flow solver. It ignores the continuous adjoint options, such as `CONV_NUM_METHOD_ADJFLOW`, `ADJ_JST_SENSOR_COEFF`, `CFL_REDUCTION_ADJFLOW` and `LIMIT_ADJFLOW` (tutorial). The tutorial text calls the switch that changes this `INCONSISTENT_AD`; the option in the code is `INCONSISTENT_DISC` (default `NO`) (code).
- `FROZEN_VISC_DISC` (default `NO`) freezes the turbulence model in the adjoint. `FROZEN_LIMITER_DISC` (default `NO`) freezes the slope limiter (code). Both make the adjoint cheaper or more robust, but the gradient then no longer matches finite differences exactly (advice, to be reviewed).
- `QUASI_NEWTON_NUM_SAMPLES` above 1 adds a quasi-Newton correction to the adjoint iterations. The default is 0 (off) (code). It can speed up the adjoint convergence (to be reviewed).

### Objective function

- `OBJECTIVE_FUNCTION` sets the output to differentiate. `MARKER_MONITORING` sets the surfaces where SU2 evaluates it (code). Examples of values: `DRAG`, `LIFT`, `MOMENT_Z`, `EFFICIENCY`, `TOTAL_HEATFLUX`, `SURFACE_TOTAL_PRESSURE`, `SURFACE_PRESSURE_DROP`, `SURFACE_UNIFORMITY`, `TOTAL_PRESSURE_LOSS`, `ENTROPY_GENERATION`, `CUSTOM_OBJFUNC` (code). The full list is on the [option reference](../Option-Reference/) page.
- The `SURFACE_*` objectives use the markers in `MARKER_ANALYZE`. List the same marker in `MARKER_MONITORING` too (tutorial).
- **Weighted sum.** Give several objectives separated by commas, with `OBJECTIVE_WEIGHT` and `MARKER_MONITORING` in the same order (code). See the [multi-objective tutorial](/tutorials/Multi_Objective_Shape_Design/).
- **Custom expression.** With `OBJECTIVE_FUNCTION= CUSTOM_OBJFUNC`, `CUSTOM_OBJFUNC` holds a formula of history outputs, for example `'DRAG + 10 * pow(fmax(0.4-LIFT, 0), 2)'` (code).
- **In the Python scripts**, `OPT_OBJECTIVE` sets the objective and its scale, for example `DRAG * 0.001` (tutorial). Separate several objectives with semicolons. With `OPT_COMBINE_OBJECTIVE= YES`, SU2 solves one adjoint for the weighted sum, instead of one per objective (tutorial).
- **Fixed lift.** To minimize drag at a given lift, use `FIXED_CL_MODE= YES` with `TARGET_CL`: the flow solver then changes the angle of attack. The adjoint gives the drag gradient at fixed lift, so you need no lift constraint and no extra adjoint for it (tutorial).

### Constraints

- `OPT_CONSTRAINT` lists constraints separated by semicolons, in the form `( NAME > value ) * scale`, with `>`, `<` or `=` (tutorial).
- Each flow constraint (for example `LIFT`) needs its own adjoint solution (tutorial).
- Geometric constraints come from SU2_GEO: `AIRFOIL_THICKNESS` for airfoils, `STATION1_THICKNESS`, `STATION2_THICKNESS`, ... for wings (tutorial). Set `GEO_MARKER`, `GEO_DESCRIPTION` (`AIRFOIL`, `WING`, `FUSELAGE` or `NACELLE`) and, for wings, `GEO_LOCATION_STATIONS` and `GEO_BOUNDS` (code, tutorial). Run `SU2_GEO` once on the baseline to check the values (tutorial).
- **Penalty.** You can also write a constraint inside `OPT_OBJECTIVE`, for example `(DRAG = 0.05)*1E6`. SU2 then adds a quadratic penalty when the constraint is violated (tutorial).
- The scale of each constraint sets how strongly the optimizer reacts when the constraint is violated. The tutorials use 0.001 (tutorial).

### Design variables

`DEFINITION_DV` lists the design variables for the Python scripts. Each one has the form `( kind, scale | markers | parameters )`. Separate them with semicolons, with no semicolon after the last one (tutorial). The kind is a number (code):

| Number | Kind | Parameters |
|---|---|---|
| 1 | `TRANSLATION` | x, y, z |
| 11 | `FFD_CONTROL_POINT` | box tag, i, j, k, x, y, z direction |
| 14 | `FFD_CAMBER` | box tag, i, j |
| 15 | `FFD_TWIST` | box tag, j, axis end points |
| 16 | `FFD_THICKNESS` | box tag, i, j |
| 19 | `FFD_CONTROL_POINT_2D` | box tag, i, j, x, y direction |
| 20 | `FFD_CAMBER_2D` | box tag, i |
| 21 | `FFD_THICKNESS_2D` | box tag, i |
| 30 | `HICKS_HENNE` | lower (0) or upper (1) side, x position on a unit chord |
| 34 | `CST` | see the test case [deformation/cst](https://github.com/su2code/SU2/tree/develop/TestCases/deformation/cst) |
| 35 | `SURFACE_BUMP` | x start, x end, x location of the bump |
| 101 | `ANGLE_OF_ATTACK` | 1.0 |

These points come from the tutorials (tutorial):

- Hicks-Henne bumps (kind 30) are simple for 2D airfoils. FFD control points (kinds 11 and 19) work for any shape, in 2D and 3D.
- `set_ffd_design_var.py` writes the `DEFINITION_DV` list for all control points of a box, for example `set_ffd_design_var.py -i 10 -j 8 -k 1 -b WING -m 'UPPER_SIDE, LOWER_SIDE, TIP'`. Add `--dimension 2` in 2D. Remove the points that should not move.
- `DV_KIND`, `DV_MARKER`, `DV_PARAM` and `DV_VALUE` define one deformation for `SU2_DEF` alone, for example to test a mesh deformation by hand.

### FFD boxes

FFD (free-form deformation) puts a box of control points around the surface. Moving a control point bends the surface inside the box smoothly (tutorial).

- `FFD_DEFINITION` = (tag, then the 8 corner points x, y, z) in 3D. In 2D, give 4 corners with z = 0, and fill the other 12 values with zeros (tutorial). Start at the corner with the lowest x, y, z. Go along x, then along y, then to the remaining corner of that face. In 3D, repeat for the top face (tutorial).
- `FFD_DEGREE` = (i, j, k) degrees. The box has degree + 1 control points in each direction. In 2D, use (i, j, 0) (tutorial).
- Several boxes: separate them with semicolons in `FFD_DEFINITION` and `FFD_DEGREE` (test case).
- `FFD_CONTINUITY` keeps the surface smooth where it leaves the box: `2ND_DERIVATIVE` (default), `1ST_DERIVATIVE`, `NO_DERIVATIVE`, or `USER_INPUT` (code). With `USER_INPUT`, you choose the fixed planes of control points with `FFD_FIX_I`, `FFD_FIX_J` and `FFD_FIX_K`. A plane index larger than the degree fixes nothing (tutorial, test case).
- Other options: `FFD_BLENDING` (`BEZIER` default, or `BSPLINE_UNIFORM` with `FFD_BSPLINE_ORDER`), `FFD_COORD_SYSTEM` (`CARTESIAN` default, `CYLINDRICAL`, `SPHERICAL`, `POLAR`, with `FFD_AXIS`), `FFD_SYMMETRY_PLANE` (default `NO`) (code).
- `FFD_TOLERANCE` (default 1E-10) and `FFD_ITERATIONS` (default 500) control how SU2 finds the position of each surface point inside the box (code).
- `FFD_INTPREV= YES` (default `NO`) checks the box for self-intersection after a deformation. If SU2 finds one, it reduces the deformation step by step (`FFD_INTPREV_ITER`, default 10; `FFD_INTPREV_DEPTH`, default 3) (code).

To add the boxes to your mesh (tutorial):

1. Set `DV_KIND= FFD_SETTING`, `DV_PARAM= ( 1.0 )` and `DV_MARKER` to the surfaces to deform.
2. Run `SU2_DEF config.cfg`.
3. SU2_DEF writes the mesh with the boxes to the file in `MESH_OUT_FILENAME` (default `mesh_out`). Use that file as `MESH_FILENAME` from now on.

The box moves only the surface points that lie inside it (tutorial). Make the box enclose the whole region that should change (advice).

### Mesh deformation

After the surface moves, `SU2_DEF` moves the volume mesh by treating it as an elastic solid (tutorial).

- `DEFORM_STIFFNESS_TYPE`: `WALL_DISTANCE` (default), `INVERSE_VOLUME` or `CONSTANT_STIFFNESS` (code). The first two make small cells near walls stiffer, so that the boundary layer cells keep their shape (advice, to be reviewed).
- `DEFORM_LINEAR_SOLVER` (default `FGMRES`), `DEFORM_LINEAR_SOLVER_PREC` (default `ILU`), `DEFORM_LINEAR_SOLVER_ITER` (default 1000), `DEFORM_LINEAR_SOLVER_ERROR` (default 1E-14) (code).
- `DEFORM_NONLINEAR_ITER` (default 1) splits the deformation into this many smaller steps (code). More steps help with large deformations (advice, to be reviewed).
- `DEFORM_LIMIT` (default 1E6) deforms only the cells closer to the wall than this distance (code).
- `DEFORM_COEFF` is used as the Poisson ratio of the elastic mesh. Its option text gives a range from -1.0 to 0.5, but the default is 1E6 (code). The [species transport tutorial](/tutorials/Species_Transport/) sets 0.0. Set it in your file (to be reviewed).
- `DEFORM_KIND= RBF` uses radial basis functions instead of the elastic solid (default `ELASTIC`) (code). See the test case [deformation/naca0012](https://github.com/su2code/SU2/blob/develop/TestCases/deformation/naca0012/def_NACA0012_rbf.cfg) (test case).
- Boundaries that are not in `DV_MARKER` stay fixed. Points on `MARKER_SYM` boundaries can slide in their plane. Declaring a flat outlet as `MARKER_SYM` avoids torn cells there (tutorial).
- `HOLD_GRID_FIXED= YES` with `HOLD_GRID_FIXED_COORD` keeps the mesh outside a box fixed (code).
- Set `DEFORM_CONSOLE_OUTPUT= YES` to see the minimum cell volume after each step (code).

The options `DEFORM_MESH` and `MARKER_DEFORM_MESH` belong to the mesh solver inside SU2_CFD, for moving boundaries during a flow simulation. Shape optimization with the Python scripts uses SU2_DEF.

### Python scripts

All scripts are in `SU2_PY`. They take the config file with `-f` and the number of MPI ranks with `-n` (code). See also [Execution](../Execution/).

- `shape_optimization.py`: the full loop of flow, adjoint, gradient, deformation and optimizer (tutorial). Its arguments (code):
  - `-g`: the gradient method, `DISCRETE_ADJOINT` (default), `CONTINUOUS_ADJOINT`, `FINDIFF` or `NONE`.
  - `-o`: the optimizer from SciPy, `SLSQP` (default), `CG`, `BFGS` or `POWELL`.
  - `-q`: quiet mode, default `True`.
  - Each design is written to `DESIGNS/DSN_001`, `DSN_002`, ... The history of the optimization is in the `history_project` file (tutorial).
- `discrete_adjoint.py`: one flow solution, one adjoint solution and the gradient. `-m adj` reuses an existing flow solution; `-m grad` reuses both solutions (code).
- `continuous_adjoint.py`: the same with the continuous adjoint (code).
- `finite_differences.py`: the gradient by finite differences, with one flow solution per design variable (code).
- `set_ffd_design_var.py`: writes `DEFINITION_DV` lists for FFD boxes (tutorial).

Optimizer settings (tutorial):

- `OPT_ITERATIONS`, `OPT_ACCURACY`: the maximum number of iterations and the requested accuracy.
- `OPT_BOUND_UPPER`, `OPT_BOUND_LOWER`: the bounds of each design variable. The script divides them by `OPT_RELAX_FACTOR` before it passes them to the optimizer (code).
- `OPT_GRADIENT_FACTOR`: scales objective and gradient. The tutorials aim at a gradient norm (column GNORM) near 1E-6 for SLSQP.
- `OPT_RELAX_FACTOR`: scales the first step. Check the size of the first deformation in `DESIGNS/DSN_002/DEFORM/log_Deform.out` (the `Max Diff` line in the ONERA M6 tutorial).
- `OPT_LINE_SEARCH_BOUND` (default 1E6) bounds the line search in SU2_DEF (code).

**FADO.** The tutorials [Species Transport](/tutorials/Species_Transport/) and [Turbulent 3D pipe bend](/tutorials/Inc_Turbulent_Bend_Opt/) use [FADO](https://github.com/su2code/FADO), a separate Python framework, instead of `shape_optimization.py` (tutorial). FADO gives more control over the steps and over the optimizer. The Species Transport tutorial shows a full workflow: restart check, FFD setup, mesh deformation test, gradient check, optimization (tutorial).

## Check convergence and results

**Converge the flow first.** The adjoint linearizes the flow around the current solution. A poorly converged flow gives a wrong gradient (advice). Set `CONV_RESIDUAL_MINVAL` low, and check that the objective no longer changes.

**Converge the adjoint.** With the compressible solver, the adjoint run stops on `RMS_ADJ_DENSITY` by default (code). Watch it, and the sensitivity outputs (`SENS_GEO`, `SENS_AOA`, `SENS_MACH`) in the adjoint history (code). The sensitivities should settle to steady values (advice).

**Check the restart.** Before a gradient check, verify that a flow restart and an adjoint restart reproduce the residuals of a continuous run. The [Species Transport tutorial](/tutorials/Species_Transport/) shows a script for this (tutorial).

**Check the gradient against finite differences** before you optimize (tutorial):

1. Run `discrete_adjoint.py -f config.cfg`. The gradient is in a file named after `GRAD_OBJFUNC_FILENAME` (default `of_grad`) plus a short name of the objective, for example `of_grad_cd.csv` for `DRAG`. The extension follows `TABULAR_FORMAT` (code).
2. Run `finite_differences.py -f config.cfg`. The gradient is in `of_grad_findiff`, with the same extension. The step comes from `FIN_DIFF_STEP`; the script uses 0.001 when the option is missing. The template suggests 0.001 times `REF_LENGTH` (code).
3. Compare the two files, design variable by design variable. Signs and orders of magnitude must agree. Try two or three step sizes: a step that is too large adds truncation error, and a step that is too small adds noise from the incomplete convergence (advice).

With a direct-diff build, `discrete_adjoint.py -v True` compares the adjoint gradient with forward-mode AD, instead of finite differences (code, to be reviewed).

**Check each new design.** Look at the deformed meshes in `DESIGNS/DSN_*/DEFORM`, the flow solutions in `DESIGNS/DSN_*/DIRECT`, and the history in `history_project` (tutorial).

## Common problems

| Symptom | Likely cause | What to try |
|---|---|---|
| SU2 stops: "MATH_PROBLEM= DISCRETE_ADJOINT requires AD support". | The adjoint config was given to `SU2_CFD` (code). | Use `SU2_CFD_AD`, or let the Python scripts call it. Build with `-Denable-autodiff=true`. |
| The gradient differs from finite differences. | The flow or the adjoint is not converged; the finite difference step is too large or too small; the turbulence or the limiter is frozen (advice). | Converge both deeper. Try several `FIN_DIFF_STEP` values. Set `FROZEN_VISC_DISC= NO` and `FROZEN_LIMITER_DISC= NO`. |
| The adjoint diverges or stalls. | The flow solution oscillates (limiter, shock, separation), so the adjoint of the last iteration has no fixed point (advice, to be reviewed). | Converge the flow deeper. Freeze the limiter in the flow with `LIMITER_ITER`. Try `FROZEN_LIMITER_DISC= YES` or `QUASI_NEWTON_NUM_SAMPLES` (to be reviewed). |
| The flow does not converge on a new design. | The step was too large, or the shape became unphysical (advice). | Lower `OPT_RELAX_FACTOR` or the bounds. Restart the optimization from its project file with `-r` (to be reviewed). |
| SU2_DEF reports: "There are N elements with negative volume". | The deformation is too large for the mesh (code). | Lower the step (`OPT_RELAX_FACTOR`, bounds). Raise `DEFORM_NONLINEAR_ITER`. Try another `DEFORM_STIFFNESS_TYPE` or `DEFORM_KIND= RBF`. Set `FFD_INTPREV= YES` (to be reviewed). |
| The mesh is torn at an outlet or a side boundary. | That boundary is fixed while its neighbour moves (tutorial). | Declare flat boundaries next to the moving surface as `MARKER_SYM`. |
| Kinks at the edge of the FFD box. | Control points on the box faces move (tutorial). | Use `FFD_CONTINUITY= 2ND_DERIVATIVE`, or fix the outer planes with `FFD_FIX_I`, `FFD_FIX_J`, `FFD_FIX_K`. |
| Part of the surface does not move. | It lies outside the FFD box (tutorial). | Enlarge the box and run the `FFD_SETTING` step again. |
| The FFD point inversion does not converge. | The box is badly shaped, or points sit near its faces (advice, to be reviewed). | Raise `FFD_ITERATIONS`. Make the box larger and closer to a regular hexahedron. |
| The optimizer stops after one step. | The gradient norm is far from the scale that the optimizer expects (tutorial). | Change `OPT_GRADIENT_FACTOR` so that GNORM is near 1E-6. |
| The thickness constraint has no value. | `GEO_MARKER` or `GEO_DESCRIPTION` is missing (test case). | Set them, and run `SU2_GEO` on the baseline. |

## Related tutorials and test cases

Tutorials:

- [Unconstrained shape design of a transonic inviscid airfoil](/tutorials/Inviscid_2D_Unconstrained_NACA0012/): Hicks-Henne bumps, `shape_optimization.py`.
- [Constrained shape design of a transonic inviscid wing](/tutorials/Inviscid_3D_Constrained_ONERAM6/): FFD boxes, SU2_GEO thickness constraints, fixed lift.
- [Constrained shape design of a transonic turbulent airfoil](/tutorials/Turbulent_2D_Constrained_RAE2822/): RANS discrete adjoint, moment and thickness constraints.
- [Shape design with multiple objectives and penalty functions](/tutorials/Multi_Objective_Shape_Design/): weighted objectives, `OPT_COMBINE_OBJECTIVE`, penalties.
- [Unconstrained shape design of a two way mixing channel](/tutorials/Species_Transport/): FADO, FFD setup, gradient check.
- [Adjoint design optimization of a turbulent 3D pipe bend](/tutorials/Inc_Turbulent_Bend_Opt/): FADO, incompressible RANS.
- [Unsteady shape optimization NACA0012](/tutorials/Unsteady_Shape_Opt_NACA0012/): unsteady discrete adjoint.

Test cases (SU2 repository):

- [multiple_ffd/naca0012](https://github.com/su2code/SU2/blob/develop/TestCases/multiple_ffd/naca0012/inv_NACA0012_ffd.cfg): two FFD boxes, `discrete_adjoint.py`.
- [optimization_euler/steady_naca0012](https://github.com/su2code/SU2/blob/develop/TestCases/optimization_euler/steady_naca0012/inv_NACA0012_adv.cfg): `shape_optimization.py` with the continuous adjoint.
- [optimization_rans/steady_rae2822](https://github.com/su2code/SU2/blob/develop/TestCases/optimization_rans/steady_rae2822/turb_SA_RAE2822.cfg): RANS airfoil with constraints.
- [optimization_rans/naca0012](https://github.com/su2code/SU2/blob/develop/TestCases/optimization_rans/naca0012/naca0012.cfg): unsteady RANS, `shape_optimization.py` restarted from a solution.
- [disc_adj_euler](https://github.com/su2code/SU2/tree/develop/TestCases/disc_adj_euler) and [disc_adj_rans](https://github.com/su2code/SU2/tree/develop/TestCases/disc_adj_rans): discrete adjoint runs.
- [disc_adj_turbomachinery](https://github.com/su2code/SU2/tree/develop/TestCases/disc_adj_turbomachinery): adjoint of turbomachinery objectives.
- [deformation](https://github.com/su2code/SU2/tree/develop/TestCases/deformation): SU2_DEF with many kinds of design variables.

User guide pages: [Build SU2 on Linux/MacOS](../Build-SU2-Linux-MacOS/), [Execution](../Execution/), [Advanced AD Techniques](../Advanced-AD-Techniques/), [Solver Setup](../Solver-Setup/), [Setup Guide: Turbomachinery](../Setup-Guide-Turbomachinery/).

Last checked against SU2 develop `11c177b904`.
