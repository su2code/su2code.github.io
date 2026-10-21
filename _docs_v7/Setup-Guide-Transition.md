---
title: "Setup Guide: Laminar-Turbulent Transition"
permalink: /docs_v7/Setup-Guide-Transition/
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

A standard RANS run treats the boundary layer as turbulent from the leading edge. A transition model lets the boundary layer start laminar and become turbulent further downstream. The model damps the production of turbulence until a transition criterion is met (tutorial).

Use a transition model when laminar flow covers a large part of the surface, for example (advice):

- airfoils and blades at Reynolds numbers from about 10^5 to a few 10^6,
- wind turbine blades, gliders, natural laminar flow wings,
- cases with laminar separation bubbles.

In these cases, a fully turbulent run over-predicts the skin friction drag and misses laminar separation (advice).

Limits of the Langtry-Menter (LM) model in SU2 (tutorial):

- It is built from subsonic experiments: transition caused by Tollmien-Schlichting waves, by free-stream turbulence ("bypass" transition) and by laminar separation.
- It does not predict crossflow transition (except through the `LM2015` option, see below), nor supersonic and hypersonic transition mechanisms.

For the RANS settings that are not specific to transition, see [Setup Guide: Steady RANS for External Aerodynamics](../Setup-Guide-RANS-External-Aero/).

## Start from

This config comes from the E387 airfoil tutorial with SA and LM: `compressible_flow/Transitional_Airfoil/Langtry_and_Menter/E387/transitional_SA_LM_model_ConfigFile.cfg` in the [Tutorials repository](https://github.com/su2code/Tutorials/tree/develop/compressible_flow/Transitional_Airfoil/Langtry_and_Menter/E387). The SU2 tutorial regression tests run it.
We removed the output file name options and `JST_SENSOR_COEFF` (it has no effect with `ROE`). All other values are unchanged.

```
% ------------- Problem ------------------------------------------------%
SOLVER= RANS
KIND_TURB_MODEL= SA
KIND_TRANS_MODEL= LM
FREESTREAM_TURBULENCEINTENSITY= 0.001
MATH_PROBLEM= DIRECT
RESTART_SOL= NO
%
% ------------- Free stream --------------------------------------------%
MACH_NUMBER= 0.06
AOA= 2
FREESTREAM_TEMPERATURE= 288.15
REYNOLDS_NUMBER= 200000.0
REYNOLDS_LENGTH= 1.0
REF_ORIGIN_MOMENT_X= 0.25
REF_ORIGIN_MOMENT_Y= 0.00
REF_ORIGIN_MOMENT_Z= 0.00
REF_LENGTH= 1.0
REF_AREA= 0
REF_DIMENSIONALIZATION= FREESTREAM_VEL_EQ_MACH
%
% ------------- Boundary conditions ------------------------------------%
MARKER_HEATFLUX= ( Airfoil, 0.0 )
MARKER_FAR= ( Farfield )
MARKER_PLOTTING= ( Airfoil )
MARKER_MONITORING= ( Airfoil )
%
% ------------- Numerics -----------------------------------------------%
NUM_METHOD_GRAD= GREEN_GAUSS
CFL_NUMBER= 1
CFL_ADAPT= YES
CFL_ADAPT_PARAM= ( 0.1, 2.0, 40.0, 1e10, 0.001 )
ITER= 100000
LINEAR_SOLVER= FGMRES
LINEAR_SOLVER_PREC= LU_SGS
LINEAR_SOLVER_ERROR= 1E-6
LINEAR_SOLVER_ITER= 5
CONV_NUM_METHOD_FLOW= ROE
USE_VECTORIZATION= NO
MUSCL_FLOW= YES
SLOPE_LIMITER_FLOW= VENKATAKRISHNAN
VENKAT_LIMITER_COEFF= 0.05
LIMITER_ITER= 99999
TIME_DISCRE_FLOW= EULER_IMPLICIT
CONV_NUM_METHOD_TURB= SCALAR_UPWIND
MUSCL_TURB= NO
SLOPE_LIMITER_TURB= NONE
TIME_DISCRE_TURB= EULER_IMPLICIT
CFL_REDUCTION_TURB= 1.0
%
% ------------- Convergence --------------------------------------------%
CONV_FIELD= ( RMS_DENSITY )
CONV_RESIDUAL_MINVAL= -13
CONV_STARTITER= 500
%
% ------------- Input and output ---------------------------------------%
MESH_FILENAME= ogrid_e387.su2
MESH_FORMAT= SU2
OUTPUT_FILES= (RESTART, PARAVIEW, SURFACE_PARAVIEW)
WRT_FORCES_BREAKDOWN= YES
VOLUME_OUTPUT= (COORDINATES, SOLUTION, PRIMITIVE, RESIDUAL)
HISTORY_OUTPUT= (ITER, LINSOL, RMS_RES, MAX_RES, AERO_COEFF, CFL_NUMBER)
OUTPUT_WRT_FREQ= 500
SCREEN_WRT_FREQ_INNER= 10
SCREEN_OUTPUT= (INNER_ITER, WALL_TIME, RMS_DENSITY, RMS_INTERMITTENCY, RMS_RE_THETA_T, LIFT, DRAG, LINSOL_ITER_TRANS, LINSOL_RESIDUAL_TRANS)
WRT_PERFORMANCE= YES
```

The same tutorial folder has an SST version, `transitional_SST_LM_model_ConfigFile.cfg`. It differs in three lines (tutorial):

```
KIND_TURB_MODEL= SST
SST_OPTIONS= V1994m
MUSCL_TURB= YES
```

## Settings that matter

### Turn on the LM model

- `KIND_TRANS_MODEL= LM` turns on the Langtry-Menter model. `NONE` (the default) and `LM` are the only values (code).
- LM needs a turbulence model. With `KIND_TURB_MODEL= NONE`, SU2 stops with an error (code).
- LM adds two transport equations (code):
  - the intermittency, gamma: 0 where the boundary layer is laminar, 1 where it is turbulent;
  - the transition onset Reynolds number, Re_theta_t: a Reynolds number based on the momentum thickness, at which transition starts.
- The model uses gamma to damp the production term of the turbulence model (tutorial).

### Base turbulence model: SST or SA

Develop supports LM with both SST and SA (code, docs). The two couplings differ in how they get the turbulence intensity Tu. Tu drives the transition correlations, the empirical formulas that predict where transition starts:

| | `KIND_TURB_MODEL= SST` | `KIND_TURB_MODEL= SA` |
| --- | --- | --- |
| Turbulence intensity used by LM | Local value from k: Tu = 100·sqrt(2k/3)/U, not below 0.027 % (code) | `FREESTREAM_TURBULENCEINTENSITY` everywhere (code) |
| Default correlation | `MENTER_LANGTRY` (code) | `MALAN` (code) |
| Tutorials | T3A and T3A- flat plates, E387 airfoil (tutorial) | E387 airfoil (tutorial) |

What this means (advice, to be reviewed):

- With SST, the intensity at the body depends on how much k decays on its way from the far field. You control it with `FREESTREAM_TURBULENCEINTENSITY` and `FREESTREAM_TURB2LAMVISCRATIO`.
- With SA, there is no decay in the correlation. Set `FREESTREAM_TURBULENCEINTENSITY` to the intensity you expect at the leading edge.

The original LM model was published with SST (advice).

More transition variants are in open pull requests.

### LM_OPTIONS

`LM_OPTIONS` takes a list. With an empty list, SU2 runs the 2009 version of the model with the default correlation of the base turbulence model (code).

**Version.**

- `LM2015` adds a correction for stationary crossflow instabilities (docs). It works in 3D only; in 2D SU2 stops with an error (code).
- `LM2015` uses the surface roughness `HROUGHNESS` (RMS roughness height, default `1e-6`) (code, docs). The code divides it by a momentum thickness, so give it in the same length unit as the mesh (code, to be reviewed).

**Correlation.** The correlation computes the transition onset Reynolds number. Choose at most one; two or more stop SU2 with an error (code).

| Value | Notes |
| --- | --- |
| `MENTER_LANGTRY` | Default with SST (code). |
| `MALAN` | Default with SA (code, docs). |
| `SULUKSNA` | Use with SST only (docs). |
| `KRAUSE`, `KRAUSE_HYPER` | Meant for hypersonic flows. The docs say their implementation is unclear because of inconsistencies in the literature (docs). |
| `MEDIDA_BAEDER` | Designed for SA. Has problems with separation-induced transition (docs). |
| `DEFAULT` | Same as leaving the correlation out (code). |

Some pages also list `MEDIDA`. The develop code does not accept it as a keyword (code).

Keep the default correlation unless you have a reason to change it, for example a validation for your type of flow (advice).

Example: `LM_OPTIONS= LM2015, MENTER_LANGTRY` (docs).

### Free-stream turbulence intensity and viscosity ratio

The free-stream turbulence intensity is the main input of the transition correlations (tutorial).

- `FREESTREAM_TURBULENCEINTENSITY` is a fraction, not a percentage: `0.001` means 0.1 %. SU2 multiplies it by 100 inside the correlations (code).
- The default is `0.05` (5 %) (code). This is high for most external flows (docs).
- SU2 computes the far-field value of Re_theta_t from this intensity with the Langtry-Menter correlation (code).
- `FREESTREAM_INTERMITTENCY` has no effect on LM: SU2 prints it, but the far-field intermittency is fixed at 1 (code).

**With SST.**

- SU2 builds the far-field k from the intensity, and omega from `FREESTREAM_TURB2LAMVISCRATIO` (eddy viscosity over laminar viscosity, default `10.0`) (code).
- k decays between the far field and the body. A larger viscosity ratio gives a slower decay (advice, to be reviewed).
- The T3A tutorial sets `FREESTREAM_TURBULENCEINTENSITY= 0.05855` and `FREESTREAM_TURB2LAMVISCRATIO= 11.9` at the inflow (tutorial).
- Check the intensity just upstream of the body. Compute it from the `TKE` output field: Tu = sqrt(2k/3)/U (advice).
- `SST_OPTIONS= SUSTAINING` and `TURB_FIXED_VALUES= YES` stop the decay of k (docs, code). No transition test case uses them with LM (to be reviewed).

**With SA.**

- `FREESTREAM_TURB2LAMVISCRATIO` is not used. The free-stream SA variable comes from `FREESTREAM_NU_FACTOR` (default `3.0`) (code, docs).
- The E387 tutorial uses `FREESTREAM_TURBULENCEINTENSITY= 0.001` (0.1 %) (tutorial).

### Mesh

General points for the mesh of an LM run (advice, to be reviewed):

- First-cell y+ about 1 or below, all along the walls. Do not use wall functions.
- A smooth wall-normal growth in the boundary layer, with a growth ratio near 1.1.
- Enough points along the wall where transition or a laminar separation bubble is expected. The transition location moves on meshes that are too coarse in this direction.
- Check the transition location on at least two meshes. Transition models are more sensitive to the mesh than fully turbulent RANS.

### Numerics

- The transition equations use the settings of the turbulence equations: `CONV_NUM_METHOD_TURB`, `MUSCL_TURB`, `SLOPE_LIMITER_TURB` and `TIME_DISCRE_TURB` (code).
- The tutorials use `ROE` with MUSCL and `VENKATAKRISHNAN` (E387), and `L2ROE` with MUSCL (T3A) for the flow (tutorial). `L2ROE` is a Roe scheme with low dissipation at low Mach number (docs).
- Both E387 configs start at `CFL_NUMBER= 1` with `CFL_ADAPT= YES` and use `LU_SGS` (tutorial).
- Transition cases often run at low Mach numbers (0.06 for E387, 0.2 for T3A) (tutorial). The compressible solver converges more slowly at very low Mach numbers (advice, to be reviewed).
- Add `RMS_INTERMITTENCY`, `RMS_RE_THETA_T`, `LINSOL_ITER_TRANS` and `LINSOL_RESIDUAL_TRANS` to `SCREEN_OUTPUT` to follow the transition equations (tutorial, code).

### The algebraic BC model: a lighter option with SA

Develop also has an algebraic transition model for SA, the Bas-Cakmakcioglu (BC) model: `KIND_TURB_MODEL= SA` with `SA_OPTIONS= BCM` (tutorial, code).

- It adds no transport equation. It damps the SA production term until a local criterion is met (tutorial).
- It also uses `FREESTREAM_TURBULENCEINTENSITY` as a fraction (code). The tutorial uses `0.0018` for 0.18 % (tutorial).
- Do not combine `BCM` with other SA options. SU2 stops with an error unless you add `EXPERIMENTAL` (code).
- The old option `KIND_TRANS_MODEL= BC` is removed. SU2 stops with a message that points to `SA_OPTIONS= BCM` (code).
- Add the `INTERMITTENCY` group to `VOLUME_OUTPUT` to write its intermittency (code).
- See the tutorial [Transitional Flat Plate](/tutorials/Transitional_Flat_Plate/).

## Check convergence and results

**Convergence.**

- Residuals: `RMS_DENSITY`, the turbulence residuals, `RMS_INTERMITTENCY` and `RMS_RE_THETA_T` (code).
- Lift and drag must be flat at the end (advice).
- The transition location must stop moving. Compare the skin friction plots of the last saved solutions (advice).

**Where transition happens.** The default output groups `SOLUTION` and `PRIMITIVE` contain the fields below (code).

| Field | Group | What to look for |
| --- | --- | --- |
| `SKIN_FRICTION-X` (surface) | `PRIMITIVE` | Low in the laminar part, then a sharp rise at transition. Negative values mark a laminar separation bubble (advice). |
| `INTERMITTENCY` | `SOLUTION` | Transported intermittency: 0 laminar, 1 turbulent (code). |
| `INTERMITTENCY_EFF` | `PRIMITIVE` | Effective intermittency that multiplies the production term. It can exceed 1 in separated regions (advice, to be reviewed). |
| `INTERMITTENCY_SEP` | `PRIMITIVE` | Extra intermittency for separation-induced transition (advice, to be reviewed). |
| `RE_THETA_T` | `SOLUTION` | Transported transition onset Reynolds number (code). |
| `EDDY_VISCOSITY` | `PRIMITIVE` | Rises where the boundary layer becomes turbulent (advice). |
| `TURB_INDEX` | `PRIMITIVE` | Turbulence index on wall nodes: near 0 laminar, near 1 turbulent. Use it only as a rough indicator (code, to be reviewed). |

Plot `SKIN_FRICTION-X` from the surface output (`SURFACE_PARAVIEW` or `SURFACE_CSV` in `OUTPUT_FILES`) along the wall, and compare it with experiments. The T3A tutorial compares it with ERCOFTAC data as a function of the local Reynolds number (tutorial).

See the [Output Fields Reference](../Output-Fields-Reference/).

## Common problems

| Symptom | Likely cause | What to try |
| --- | --- | --- |
| The boundary layer is turbulent from the leading edge. | Turbulence intensity too high; or given in percent (for example `3.0` instead of `0.03`). | Give `FREESTREAM_TURBULENCEINTENSITY` as a fraction (code). Check the intensity near the body (advice). |
| Transition happens too late, or not at all. | With SST, k has decayed to a very low value before the body. Or the mesh is too coarse at the wall. | Check Tu near the leading edge from `TKE`; adjust `FREESTREAM_TURB2LAMVISCRATIO` (advice, to be reviewed). Check y+ (advice). |
| The transition location moves when you refine the mesh. | Too few points along the wall in the transition region. | Refine along the wall (advice). |
| The residuals stall or oscillate. | A laminar separation bubble that is unsteady, or a CFL that is too high. | Start at a low CFL with `CFL_ADAPT= YES` (tutorial). If the bubble is unsteady, run time-accurate, see [Setup Guide: Unsteady Flows and DES](../Setup-Guide-Unsteady-DES/) (advice, to be reviewed). |
| SU2 stops: "LM2015 is available only for 3D problems". | `LM2015` in a 2D case. | Remove `LM2015` (code). |
| SU2 stops: "Two correlations selected for LM_OPTIONS". | More than one correlation in `LM_OPTIONS`. | Keep one (code). |
| SU2 stops: "KIND_TURB_MODEL cannot be NONE to use a transition model". | No base turbulence model. | Set `KIND_TURB_MODEL= SST` or `SA` (code). |
| SU2 stops: "Option KIND_TRANS_MODEL=BC is deprecated". | Old config. | Use `KIND_TURB_MODEL= SA` with `SA_OPTIONS= BCM` (code). |
| Changing `FREESTREAM_INTERMITTENCY` does nothing. | The option is not used by the solver. | Leave it out (code). |
| An old config stops with "invalid option name" for `EXT_ITER`. | `EXT_ITER` was replaced. | Use `ITER` for steady runs (code). |

## Related tutorials and test cases

Tutorials:

- [Transitional Flat Plate for T3A and T3A-](/tutorials/Transitional_Flat_Plate_T3A/): SST with LM, comparison with ERCOFTAC skin friction data.
- [Transitional Flat Plate](/tutorials/Transitional_Flat_Plate/): SA with the BC model (`SA_OPTIONS= BCM`), Schubauer and Klebanoff flat plate.
- E387 airfoil with LM, SA and SST versions: [Tutorials repository folder](https://github.com/su2code/Tutorials/tree/develop/compressible_flow/Transitional_Airfoil/Langtry_and_Menter/E387) (no tutorial page yet).

Test cases (develop branch):

- [transition/Schubauer_Klebanoff/transitional_BC_model_ConfigFile.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/transition/Schubauer_Klebanoff/transitional_BC_model_ConfigFile.cfg): BC model, incompressible, regression test.
- [rans/s809/trans_s809.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/rans/s809/trans_s809.cfg): S809 airfoil with SA and LM. This config is older and is not in the regression tests. It uses options that develop no longer accepts: `EXT_ITER` (replace it with `ITER`), `SOLUTION_LIN_FILENAME`, `RESTART_LIN_FILENAME` and `SURFACE_LIN_FILENAME` (delete them) (code). Its `FREESTREAM_INTERMITTENCY` line has no effect (code).

User guide pages:

- [Physical Definition: Transition Models](../Physical-Definition/#transition-models) and [Turbulence Models](../Physical-Definition/#turbulence-models).
- [Governing Equations](../Theory/), [Convective Schemes](../Convective-Schemes/), [History and Solution Output](../Custom-Output/).
- All options: [Option Reference](../Option-Reference/). All output fields: [Output Fields Reference](../Output-Fields-Reference/).

Last checked against SU2 develop `11c177b904`.
