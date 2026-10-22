---
title: Troubleshooting
permalink: /docs_v7/Troubleshooting/
---

This page helps when a run does not do what you expect. Each problem has three parts: what you see, why it happens, and what to do. For short general answers, see the [FAQ](/docs_v7/FAQ/). To look up any message that stops SU2, search the [Error Messages](/docs_v7/Error-Messages/) page.

**(to be reviewed)** at the end of a statement means that the statement is general advice and needs a check by an experienced user. The rest was checked against the SU2 code, or comes from the linked pages.

---

- [How SU2 reports an error](#how-su2-reports-an-error)
- [SU2 stops while it reads the config file](#su2-stops-while-it-reads-the-config-file)
- [SU2 stops while it reads the mesh](#su2-stops-while-it-reads-the-mesh)
- [The restart does not work](#the-restart-does-not-work)
- [The solution diverges](#the-solution-diverges)
- [The residuals stop going down](#the-residuals-stop-going-down)
- [An output field or file is missing](#an-output-field-or-file-is-missing)
- [Parallel runs](#parallel-runs)

---

## How SU2 reports an error

When SU2 finds a problem it cannot fix, it prints a block like this and stops:

```
Error in "void CConfig::SetConfig_Parsing(std::istream&)":
-------------------------------------------------------------------------
Line 98 CFL_NUMBR: invalid option name. Check current SU2 options in config_template.cfg.
Did you mean CFL_NUMBER?
------------------------------ Error Exit -------------------------------
```

The first line names the function in the code that found the problem. Its exact text depends on your compiler. The lines between the dashes are the message. With MPI, the launcher (`mpirun`) usually adds a few lines about `MPI_ABORT` after the block. You can ignore them.

## SU2 stops while it reads the config file

SU2 reads the whole config file first. It collects all the problems it finds, up to 30, and prints them in one error block.

**What you see:** `Line 98 CFL_NUMBR: invalid option name. Check current SU2 options in config_template.cfg.`

- **Why:** SU2 does not know this option name. Either the name has a typo, or the option was renamed or removed in a newer version.
- **What to do:** SU2 prints a guess on the next line (`Did you mean CFL_NUMBER?`). The guess is based on shared letters at the start and end of the name, so it can be wrong. Look for the old name on [Renamed and Removed Options](/docs_v7/Renamed-Options/), and check the current name in the [Option Reference](/docs_v7/Option-Reference/). For a few old names, SU2 tells you the new one directly, for example `DYN_TIMESTEP is deprecated. Use TIME_STEP instead.`

**What you see:** a wrong value for an option with a fixed list of values:

```
MGCYCLE: invalid option value W_CYCLES.
Did you mean, FULLMG_CYCLE, V_CYCLE, W_CYCLE?
```

- **Why:** the value is not one of the allowed words. Values are case sensitive.
- **What to do:** pick one of the values that SU2 lists after "Did you mean".

**What you see:** `CONV_NUM_METHOD_FLOW: improper option value for type convect`, or `MACH_NUMBER: multiple values for type su2double`.

- **Why:** the value does not have the expected form. For example, a number option got text or two numbers.
- **What to do:** check the type and the allowed values of the option in the [Option Reference](/docs_v7/Option-Reference/).

**What you see:** `Line 102 CFL_NUMBER: option appears twice`

- **Why:** the option is set on two lines. SU2 does not pick one of them; it stops.
- **What to do:** delete one of the two lines.

**What you see:** `configfile: File does not exist: case.cfg`

- **Why:** SU2 cannot find the config file you named on the command line.
- **What to do:** check the file name, and run SU2 from the folder that holds the file.

## SU2 stops while it reads the mesh

**What you see:** `The SU2 mesh file named mesh.su2 was not found.`

- **Why:** the file in `MESH_FILENAME` is not in the folder where you run SU2. Note that SU2 sets the file extension from `MESH_FORMAT`. It removes `.su2`, `.su2b` or `.cgns` from the name you give, and adds the extension of the format. So `MESH_FILENAME= wing.cgns` with the default `MESH_FORMAT= SU2` makes SU2 look for `wing.su2`.
- **What to do:** check the file name and the folder, and set `MESH_FORMAT` to the real format of the file:

```
MESH_FILENAME= wing.cgns
MESH_FORMAT= CGNS
```

**What you see:** `wing.cgns was not found or is not a properly formatted CGNS file.` followed by `Note that SU2 expects unstructured CGNS files in ADF data format.`

- **Why:** the file is missing, or it is not a CGNS file that SU2 can read. SU2 reads unstructured CGNS meshes only.
- **What to do:** check the name and the folder. If the file exists, export it again from your mesh tool as an unstructured CGNS file in ADF format. See [Mesh File](/docs_v7/Mesh-File/).

**What you see:** `mesh.su2 is not an SU2 mesh file or has the wrong format` and `('NDIME=' not found). Please check.`, or `Could not find the keyword "NPOIN=".`

- **Why:** the file is not a native SU2 mesh, or a keyword is missing. A common cause is a mesh in another format with `MESH_FORMAT= SU2`.
- **What to do:** set `MESH_FORMAT` to the real format, or convert the mesh. The [Mesh File](/docs_v7/Mesh-File/) page shows the native format.

**What you see:** `The configuration file doesn't have any definition for marker farfield`

- **Why:** the mesh has a boundary marker (a named group of boundary faces) called `farfield`, but no `MARKER_*` option in the config file uses that name.
- **What to do:** give every mesh marker a boundary condition. Marker names must match the mesh exactly. SU2 prints the marker names it finds in the mesh just before the error, for example `50 boundary elements in index 1 (Marker = farfield).` See [Markers and BC](/docs_v7/Markers-and-BC/).

The opposite case does not stop SU2: a marker named in the config file but not present in the mesh is accepted without a warning. It shows in the boundary table at the start of the run, but no faces use it. So check the names in that table if a boundary condition seems to have no effect.

## The restart does not work

With `RESTART_SOL= YES`, SU2 reads the file named in `SOLUTION_FILENAME`, not the one in `RESTART_FILENAME`. The [Restart File](/docs_v7/Restart-File/) page explains the file names.

**What you see:** `Unable to open SU2 restart file solution_flow.dat`

- **Why:** the file does not exist. SU2 adds the extension itself: `.dat` when `READ_BINARY_RESTART= YES` (the default), `.csv` when `READ_BINARY_RESTART= NO`. A common cause is that the previous run saved the restart as `restart_flow.dat`, and nobody copied or renamed it.
- **What to do:** copy the restart file to the solution name, or point `SOLUTION_FILENAME` to it:

```
RESTART_SOL= YES
SOLUTION_FILENAME= restart_flow
```

**What you see:** `SU2 ASCII restart file solution_flow.csv not found.`, or `File solution_flow.dat is not a binary SU2 restart file.`

- **Why:** the restart format does not match `READ_BINARY_RESTART`. `OUTPUT_FILES= RESTART` writes a binary `.dat` file. `OUTPUT_FILES= RESTART_ASCII` writes a text `.csv` file.
- **What to do:** set `READ_BINARY_RESTART= NO` to read a `.csv` file, and `YES` to read a `.dat` file.

**What you see:** the restart comes from a different mesh.

- **Why:** the number of points in the file does not match the mesh.
- **What to do:** use a binary restart file. SU2 then prints `The number of points in the restart file (...) does not match the mesh (...).` and maps the old solution onto the new mesh, using the nearest points. With MPI, this needs a single rank or an even number of ranks. Otherwise SU2 stops with `Number of ranks must be multiple of 2.` An ASCII restart file stops with `The solution file does not match the mesh, currently only binary files can be interpolated.`

**What you see:** the restart file comes from a different solver or turbulence model, and the run starts badly.

- **Why:** SU2 reads the restart values by their column position, not by their name. If the file has fewer turbulence columns than the new model needs, SU2 sets the missing turbulence values to zero. A file from another turbulence model can put the wrong values into the turbulence variables, without any error.
- **What to do:** restart only from a solution of the same solver and model. If you change the model, start from the free-stream values instead (to be reviewed).

## The solution diverges

**What you see:** `SU2 has diverged (NaN detected).` or `SU2 has diverged (Residual > 10^20 detected).` SU2 stops and does not save the solution of that iteration. Before this, the residuals often grow quickly, and the history field `NONPHYSICAL_POINTS` grows. A non-physical point is a point with a negative density, pressure or temperature. When a run ends normally, SU2 also prints `Warning: there are ... non-physical points in the solution.`

**Why:** the most common causes are a time step that is too large for the current solution, a bad mesh, or wrong free-stream or boundary values.

**What to do:** try these steps, one at a time.

1. **Check the input values.** At the start of the run, SU2 prints a table called `-- Initial and free-stream conditions:`. Check that pressure, temperature, velocity and Mach number are what you meant. Check also the boundary values on each `MARKER_*` option, and their units.
2. **Check the mesh.** At the start of the run, SU2 prints the mesh quality table: `Orthogonality Angle (deg.)`, `CV Face Area Aspect Ratio` and `CV Sub-Volume Ratio`, with their minimum and maximum. A very small angle or very large ratios point to bad cells (to be reviewed). To see where these cells are, add the `MESH_QUALITY` group to the volume output and open the file in ParaView:

```
VOLUME_OUTPUT= (SOLUTION, PRIMITIVE, MESH_QUALITY)
```

3. **Lower the CFL number.** The CFL number sets the size of the pseudo time step (a step that only drives the solution to steady state). Lower `CFL_NUMBER`, or let SU2 change it as the run goes with `CFL_ADAPT= YES`. The values of `CFL_ADAPT_PARAM` are: factor down, factor up, minimum CFL, maximum CFL. See the [Glossary](/docs_v7/Glossary/) and [Solver Setup](/docs_v7/Solver-Setup/).

```
CFL_NUMBER= 10
CFL_ADAPT= YES
CFL_ADAPT_PARAM= ( 0.5, 1.1, 1.0, 100.0 )
```

4. **Start with a first-order scheme.** A first-order scheme is less accurate but more robust. Run first with `MUSCL_FLOW= NO`, then restart from that solution with `MUSCL_FLOW= YES`. Instead of two runs, `RAMP_MUSCL= YES` blends from first to second order over the iterations set in `RAMP_MUSCL_COEFF` (start iteration, update frequency, length of the ramp). See [Convective Schemes](/docs_v7/Convective-Schemes/).
5. **Use a limiter near shocks.** In flows with shocks, keep `SLOPE_LIMITER_FLOW` set to a limiter, not `NONE`. See [Slope Limiters and Shock Resolution](/docs_v7/Slope-Limiters-and-Shock-Resolution/).
6. **Look at the solution before it fails.** SU2 does not save the solution once it finds a NaN. Write the files more often, for example `OUTPUT_WRT_FREQ= 10`, and look at the last file written. The problem usually starts in one region.

The setup guides, such as [RANS External Aerodynamics](/docs_v7/Setup-Guide-RANS-External-Aero/), list safe starting values for each kind of case.

## The residuals stop going down

**What you see:** the residuals drop for a while, then stay flat or go up and down. At the end, SU2 prints `Maximum number of iterations reached (ITER = ...) before convergence.`

**Why and what to do:**

- **The linear solver does not converge.** Each iteration of an implicit solver solves a linear system. Add `LINSOL_ITER` and `LINSOL_RESIDUAL` to `SCREEN_OUTPUT` to watch it. If the linear residual stays high, raise `LINEAR_SOLVER_ITER` or lower the CFL number. See the advice in [Linear Solvers and Preconditioners](/docs_v7/Linear-Solvers-and-Preconditioners/#setup-advice).

```
SCREEN_OUTPUT= (INNER_ITER, RMS_RES, LINSOL_ITER, LINSOL_RESIDUAL, AVG_CFL)
```

- **The CFL number is too high.** Large CFL values can make the residuals go up and down without settling. Lower `CFL_NUMBER`, or lower the maximum CFL in `CFL_ADAPT_PARAM` (to be reviewed).
- **The limiter switches on and off.** This can stop the residual drop in flows with shocks. A larger `VENKAT_LIMITER_COEFF` limits less. `LIMITER_ITER` freezes the limiter after the given number of iterations (to be reviewed). See [Slope Limiters and Shock Resolution](/docs_v7/Slope-Limiters-and-Shock-Resolution/).
- **The flow is not steady.** Some flows, for example with large separation, never reach a steady state. In that case, run an unsteady simulation (to be reviewed). See the [Unsteady and DES setup guide](/docs_v7/Setup-Guide-Unsteady-DES/).
- **Unsteady runs: the time step is too large.** In an unsteady run, the inner iterations must converge in each time step. If they do not, lower `TIME_STEP` or raise `INNER_ITER` (to be reviewed).

**The run never stops early, or stops too early.** SU2 stops before `ITER` only when every field in `CONV_FIELD` meets its criterion, and not before `CONV_STARTITER` iterations:

- A residual field stops the run when its value goes below `CONV_RESIDUAL_MINVAL`. The `RMS_*` fields are log10 values, not a drop from the start. To ask for a drop, use the `REL_RMS_*` fields. They measure the drop from the largest value seen so far.
- A coefficient field, such as `DRAG`, stops the run when its average relative change over the last `CONV_CAUCHY_ELEMS` iterations is below `CONV_CAUCHY_EPS`.

```
% Stop when the density residual has dropped by 6 orders
CONV_FIELD= REL_RMS_DENSITY
CONV_RESIDUAL_MINVAL= -6
```

If a name in `CONV_FIELD` does not exist for your solver, SU2 prints `Ignoring Convergence Field(s):` with the name. If no valid field is left, SU2 prints `Warning: No (valid) fields chosen for convergence monitoring. Convergence monitoring inactive.` and runs until `ITER`. See [Setting convergence criteria](/docs_v7/Solver-Setup/#setting-convergence-criteria).

## An output field or file is missing

**What you see:** a field you asked for is not in the screen, history or volume output. At the start of the run, SU2 prints lines such as `Info: Ignoring the following screen output fields:`.

- **Why:** the field does not exist for this solver, or its name has a typo. The fields depend on the solver and the models.
- **What to do:** list the fields that exist for your exact config file with a dry run. A dry run sets up the case without solving it. It still needs the mesh file. It prints the tables `Available volume output fields for the current configuration` and `Available screen/history output fields for the current configuration`, and stops:

```
SU2_CFD -d case.cfg
```

The [Output Fields Reference](/docs_v7/Output-Fields-Reference/) lists all fields of every solver. [Custom Output](/docs_v7/Custom-Output/) explains how to choose them.

**What you see:** a volume or surface file is not written.

- **Why:** `OUTPUT_FILES` sets which files SU2 writes. If you set it, only the listed files are written. Without it, SU2 writes `RESTART`, `PARAVIEW` and `SURFACE_PARAVIEW`. `OUTPUT_WRT_FREQ` sets how often the files are written: by default every 250 iterations in steady runs, and every time step in unsteady runs. Steady runs also write the files at the end.
- **What to do:** add the file type to `OUTPUT_FILES`. Give one frequency per file type. If you give fewer frequencies than file types, SU2 repeats the last one:

```
OUTPUT_FILES= (RESTART, PARAVIEW, SURFACE_CSV)
OUTPUT_WRT_FREQ= (100, 500)
```

In unsteady runs, a file every time step can fill your disk. Set a larger `OUTPUT_WRT_FREQ`.

## Parallel runs

**What you see:** with `mpirun -n 4 SU2_CFD case.cfg`, every line of output appears four times.

- **Why:** SU2 was built without MPI, so each process runs the whole case alone. See the [FAQ](/docs_v7/FAQ/).
- **What to do:** build SU2 with MPI (`-Dwith-mpi=enabled`, see [Build from Source](/docs_v7/Build-SU2-Linux-MacOS/)), and use the `mpirun` that belongs to the same MPI library as the build (to be reviewed).

**What you see:** the run stops, or the system kills it, while SU2 reads the mesh or builds the solver.

- **Why:** the run needs more memory than the machine has. Memory grows with the number of mesh points, the number of equations, and some settings (to be reviewed).
- **What to do:**
  - Spread the run over more nodes, so that each part of the mesh is smaller (to be reviewed).
  - `FGMRES` keeps one vector per linear iteration, so its memory grows with `LINEAR_SOLVER_ITER`. Lower `LINEAR_SOLVER_ITER`, or use `RESTARTED_FGMRES` or `BCGSTAB`. See [Linear Solvers and Preconditioners](/docs_v7/Linear-Solvers-and-Preconditioners/#setup-advice).
  - Each multigrid level (`MGLEVEL`) adds a coarser copy of the mesh and its own data. Use fewer levels (to be reviewed).

If SU2 crashes without an error block, for example with a segmentation fault, the [Debugging](/docs_v7/Debugging/) page shows how to find the cause. If you think you found a bug, report it on [GitHub](https://github.com/su2code/SU2/issues) with the config file and, if possible, the mesh.
