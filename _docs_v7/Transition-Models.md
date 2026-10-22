---
title: Transition Models
permalink: /docs_v7/Transition-Models/
---

This page explains the model and its SU2 implementation. For numerical setup choices, see the [setup guide](../Setup-Guide-Transition/); use its tutorial and V&V links for worked examples and comparisons.

A turbulence model alone treats the boundary layer as turbulent from the leading edge. A transition model lets the boundary layer start laminar and become turbulent further downstream, where a transition criterion is met. SU2 has two transition models: the Langtry-Menter (LM) model, which adds two transport equations and works with SST or SA, and the algebraic Bas-Cakmakcioglu model (SA-BCM), which only changes the SA equation.

---

- [Select a model](#select-a-model)
- [Langtry-Menter (LM)](#langtry-menter-lm)
- [Bas-Cakmakcioglu (SA-BCM)](#bas-cakmakcioglu-sa-bcm)
- [What SU2 does differently from the literature](#what-su2-does-differently-from-the-literature)
- [Free-stream and inlet values](#free-stream-and-inlet-values)
- [Verification and test cases](#verification-and-test-cases)
- [Known limits](#known-limits)
- [Related pages](#related-pages)

---

## Select a model

Both models need `SOLVER= RANS` or `SOLVER= INC_RANS` and a turbulence model (see [Turbulence Models](../Turbulence-Models/)).

| Model | Settings |
| --- | --- |
| LM with SST | `KIND_TURB_MODEL= SST`, `KIND_TRANS_MODEL= LM` |
| LM with SA | `KIND_TURB_MODEL= SA`, `KIND_TRANS_MODEL= LM` |
| SA-BCM | `KIND_TURB_MODEL= SA`, `SA_OPTIONS= BCM` (leave `KIND_TRANS_MODEL` at `NONE`) |

- `KIND_TRANS_MODEL` takes `NONE` (the default) or `LM`. With `KIND_TURB_MODEL= NONE`, SU2 stops with an error.
- The old setting `KIND_TRANS_MODEL= BC` is no longer accepted. SU2 stops and tells you to use `SA_OPTIONS= BCM`.

<!-- Common/src/CConfig.cpp:1213, 3436-3439, 3815-3817; Common/include/option_structure.hpp:1363-1370 -->

This page describes the SU2 develop branch. More transition model variants are in open pull requests.

## Langtry-Menter (LM)

The LM model solves two extra equations:

- the intermittency gamma (`INTERMITTENCY` in the output): 0 where the boundary layer is laminar, 1 where it is turbulent;
- the transition onset momentum-thickness Reynolds number Re_theta_t (`RE_THETA_T`): the value of Re_theta at which transition starts, carried from the free stream into the boundary layer.

The model uses gamma to damp the production of turbulence in the boundary layer. The [TMR page of the LM model](https://tmbwg.github.io/turbmodels/langtrymenter_4eqn.html) gives the equations.

Original papers:

- R. B. Langtry and F. R. Menter, "Correlation-Based Transition Modeling for Unstructured Parallelized Computational Fluid Dynamics Codes", AIAA Journal 47(12), 2009, pp. 2894-2906.
- Crossflow extension (`LM2015`): R. B. Langtry, K. Sengupta, D. T. Yeh and A. J. Dorgan, AIAA 2015-2474.

### LM_OPTIONS keywords

`LM_OPTIONS` takes a list. With an empty list, SU2 runs the 2009 model with the default correlation of the turbulence model.

**Version.**

- `LM2015` adds the correction for stationary crossflow instabilities. It works only in 3D; in 2D SU2 stops with an error.
- `LM2015` uses `HROUGHNESS`, the RMS height of the surface roughness (default `1e-6`). SU2 divides it by a momentum thickness, so give it in the length unit of the mesh (to be reviewed).

**Correlation** (at most one; SU2 stops with an error if you give two). The correlations give the critical Reynolds number Re_theta_c and the length of the transition zone from Re_theta_t. The table shows the reference that SU2 prints at start-up.

| Keyword | Reference printed by SU2 | Notes |
| --- | --- | --- |
| `MENTER_LANGTRY` | Menter and Langtry (2009) | Default with SST. |
| `MALAN` | Malan et al. (2009) | Default with SA. |
| `SULUKSNA` | Suluksna et al. (2009) | |
| `KRAUSE` | Krause et al. (2008) | Meant for hypersonic flows (to be reviewed). |
| `KRAUSE_HYPER` | Krause et al. (2008, paper) | Meant for hypersonic flows (to be reviewed). Depends on the turbulence intensity. |
| `MEDIDA_BAEDER` | Medida and Baeder (2011) | Developed for SA (to be reviewed). Depends on the turbulence intensity. |
| `DEFAULT` | | Same as giving no correlation. |
| `NONE` | | No effect. |

<!-- option_structure.hpp:1375-1470; CConfig.cpp:1215-1217, 3848-3855, 6701-6730; SU2_CFD/include/numerics/turbulent/transition/trans_correlations.hpp -->

The code also contains a `MEDIDA` correlation (Medida PhD, 2014), but `MEDIDA` is not an accepted keyword in develop. <!-- option_structure.hpp:1383 (enum) vs 1388-1398 (map, no MEDIDA entry) -->

Example: `LM_OPTIONS= LM2015, MENTER_LANGTRY`.

Keep the default correlation unless a validation for your type of flow supports another one (to be reviewed).

## Bas-Cakmakcioglu (SA-BCM)

SA-BCM is an algebraic model: it solves no extra equation. It multiplies the production term of SA by an intermittency function, gamma_BC. This function depends on the local vorticity Reynolds number, the eddy viscosity and the free-stream turbulence intensity. SU2 implements the 2020 version listed on the [TMR SA-BCM page](https://tmbwg.github.io/turbmodels/sa-bc_1eqn.html).

- SA-BCM is built on SA-noft2. SU2 stops with an error if you combine `BCM` with `WITHFT2`, `ROTATION`, `COMPRESSIBILITY`, `QCR2000` or `NEGATIVE`, unless you add `EXPERIMENTAL`.
- The volume field `INTERMITTENCY` (group `INTERMITTENCY`) is registered for SA-BCM, but currently reads a getter that returns zero. It does not show the computed BCM intermittency; do not use it to locate transition. The LM intermittency fields are separate and do not have this getter problem.

<!-- option_structure.hpp:1336-1356; SU2_CFD/include/numerics/turbulent/turb_sources.hpp:303-324; SU2_CFD/src/output/CFlowOutput.cpp:1599-1601 -->

Original papers:

- S. C. Cakmakcioglu, O. Bas, R. Mura and U. Kaynak, AIAA 2020-2706.
- R. Mura and S. C. Cakmakcioglu, AIAA 2020-2714.

## What SU2 does differently from the literature

### LM with SST

- **Base model.** The TMR LM model is built on SST-2003. In SU2 the SST model is always the "m" form (no turbulent kinetic energy in the stress tensor), and the default is `V2003m`. The T3A tutorial uses the default; the E387 tutorial with SST uses `V1994m`. See [Turbulence Models](../Turbulence-Models/#what-su2-does-differently-from-the-literature).
- **Coupling to SST**, as in the TMR: SU2 multiplies the production of k by the effective intermittency gamma_eff, and the destruction of k by min(max(gamma_eff, 0.1), 1). gamma_eff is the larger of gamma and the separation-induced intermittency gamma_sep. The omega equation is unchanged. The blending function F1 is replaced by max(F1, F3), with F3 = exp(-(Ry/120)^8) and Ry = rho y sqrt(k) / mu, where y is the wall distance. <!-- turb_sources.hpp:1001-1005; SU2_CFD/src/variables/CTransLMVariable.cpp:48-53; SU2_CFD/src/variables/CTurbSSTVariable.cpp:86-91 -->
- **Turbulence intensity.** SU2 computes the local intensity from k: Tu = 100 sqrt(2k/3) / U, in percent, and keeps it at 0.027 % or above. <!-- trans_sources.hpp:133; CTransLMSolver.cpp:236-238 -->

### LM with SA

The LM model was published for SST. SU2 also couples it to SA, which has no k. This coupling differs from the SST one:

- **Turbulence intensity.** Tu is `FREESTREAM_TURBULENCEINTENSITY` (times 100) everywhere in the domain. It does not decay.
- **Onset and length functions.** For the ratio R_t, SU2 uses mu_t/mu in place of rho k/(mu omega). The onset function is capped at 4 instead of 2, and its third part is max(2 - (R_t/2.5)^3, 0) instead of max(1 - (R_t/2.5)^3, 0). The length function has no sublayer blending, and the wake function is 1.
- **Coupling to SA.** SU2 multiplies the SA production by gamma_eff, and the SA destruction by min(max(gamma, 0.5), 1), where gamma is the transported intermittency. The closest TMR model, [SA-noft2-Gamma-Retheta](https://tmbwg.github.io/turbmodels/sa_gamma_retheta_3eqn.html), puts no intermittency factor on the destruction term. The TMR says an older form of that factor, max(min(gamma, 0.5), 1), is always 1. A comment in the SU2 code makes the same point and asks whether the published form is wrong.
- SU2 does not check which SA variant you use with LM.

<!-- trans_sources.hpp:133-170, 196-201; CTransLMSolver.cpp:236-247; turb_sources.hpp:326-332 -->

### Both LM couplings

- **Free-stream values.** The free-stream intermittency is always 1. SU2 computes the free-stream Re_theta_t from `FREESTREAM_TURBULENCEINTENSITY` with the zero-pressure-gradient Langtry-Menter correlation. `FREESTREAM_INTERMITTENCY` is printed at start-up but has no effect. <!-- CTransLMSolver.cpp:111-130; CConfig.cpp:1530 -->
- **Inlets.** At inlets, SU2 uses the free-stream values of gamma and Re_theta_t. `MARKER_INLET_TURBULENT` changes the inlet k and omega (or nu-tilde), but not the LM variables. <!-- CTransLMSolver.cpp:163-169, 417-446 -->
- **Walls.** No flux of gamma or Re_theta_t crosses a wall (zero normal gradient). <!-- CTransLMSolver.cpp:386-407 -->
- **LM2015.** The crossflow correction also limits the time scale of the Re_theta_t equation with the local grid length. <!-- trans_sources.hpp:189-191 -->

### SA-BCM

SU2 follows the TMR description:

- the critical Reynolds number is Re_theta_c = 803.73 (Tu + 0.6067)^-1.027, with Tu in percent from `FREESTREAM_TURBULENCEINTENSITY` (times 100), constant in the domain;
- the constants are chi_1 = 0.002 and chi_2 = 50 (the TMR writes 0.02 in the denominator, which is the same);
- the destruction term is not changed;
- the free-stream nu-tilde is 0.005 times the usual SA value. With the default `FREESTREAM_NU_FACTOR= 3`, this gives 0.015 times the kinematic viscosity, the low end of the TMR range (0.015 to 0.025).

<!-- turb_sources.hpp:303-324; CTurbSASolver.cpp:110-117, 643 -->

If you set both `SA_OPTIONS= BCM` and `KIND_TRANS_MODEL= LM`, SU2 gives no error. It solves the LM equations, but the SA source term uses the BCM intermittency. Do not combine them. <!-- turb_sources.hpp:303-336 -->

## Free-stream and inlet values

| Option | Default | Used by | Meaning |
| --- | --- | --- | --- |
| `FREESTREAM_TURBULENCEINTENSITY` | `0.05` | LM, SA-BCM, SST | Turbulence intensity as a fraction: `0.001` means 0.1 %. SU2 multiplies it by 100 inside the correlations. |
| `FREESTREAM_TURB2LAMVISCRATIO` | `10.0` | SST | Eddy viscosity over laminar viscosity, used for the free-stream omega. |
| `FREESTREAM_NU_FACTOR` | `3.0` | SA | Free-stream nu-tilde over kinematic viscosity (times 0.005 with BCM). |
| `HROUGHNESS` | `1e-6` | LM with `LM2015` | RMS roughness height. |
| `FREESTREAM_INTERMITTENCY` | `1.0` | none | No effect on LM or BCM. |

<!-- CConfig.cpp:1217, 1530-1546 -->

- The default intensity of 5 % is high for most external flows. Set it to the value of your experiment or flight condition (to be reviewed).
- With SST, k decays between the far field and the body, so the intensity at the leading edge is lower than the far-field value. Check it in the output (Tu = sqrt(2k/3)/U from the `TKE` field) (to be reviewed).
- With SA (LM or BCM), the intensity is the same everywhere. Give the value expected at the body (to be reviewed).

[Setup Guide: Laminar-Turbulent Transition](../Setup-Guide-Transition/) gives more advice on these values, on the mesh and on convergence.

## Verification and test cases

- V&V page: [Langtry and Menter transition model](/vandv/LM_transition/) (T3A, T3B, T3A-, NLF0416 and E387 cases, compared with another code).
- Tutorials:
  - [Transitional Flat Plate](/tutorials/Transitional_Flat_Plate/): SA-BCM on the Schubauer-Klebanoff flat plate.
  - [Transitional Flat Plate for T3A and T3A-](/tutorials/Transitional_Flat_Plate_T3A/): LM with SST.
  - E387 airfoil with LM, with SA and with SST: config files in the [Tutorials repository](https://github.com/su2code/Tutorials/tree/develop/compressible_flow/Transitional_Airfoil/Langtry_and_Menter/E387). The tutorial regression tests run both.
- Test cases:
  - SA-BCM, incompressible: [TestCases/transition](https://github.com/su2code/SU2/tree/develop/TestCases/transition) (Schubauer-Klebanoff, T3A, E387). The regression tests run the Schubauer-Klebanoff case. Note: these configs give `FREESTREAM_TURBULENCEINTENSITY` as a percent value (`0.18`, `3.0`, `0.1`), while SU2 reads it as a fraction. The tutorial sets `0.0018` for the same Schubauer-Klebanoff flow. Do not copy these values.
  - LM with SA on the S809 airfoil: [trans_s809.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/rans/s809/trans_s809.cfg). The regression scripts do not run it.

<!-- TestCases/serial_regression.py:632-634; TestCases/parallel_regression.py:1002; TestCases/tutorials.py:239-279 -->

## Known limits

- Only LM and SA-BCM are available in develop.
- **LM has no discrete adjoint.** Do not combine `KIND_TRANS_MODEL= LM` with `MATH_PROBLEM= DISCRETE_ADJOINT`: the required transition solver is not created, and the run can crash during setup. See [the developer guide](../Adding-a-Transition-Model/#discrete-adjoint).
- **SA-BCM intermittency output is zero** in this code version, so it is not a transition-location diagnostic (see [SA-BCM](#bas-cakmakcioglu-sa-bcm)).
- LM uses the velocity magnitude and its streamwise gradient. The TMR notes that the model is therefore not Galilean invariant: results depend on the frame of reference (to be reviewed for moving walls and rotating frames).
- `LM2015` works only in 3D.
- LM with SA uses one constant turbulence intensity in the whole domain. So does SA-BCM.
- The LM correlations are built from low-speed experiments. For crossflow, supersonic and hypersonic transition, check the model against data for your flow (to be reviewed).

## Related pages

- [Setup Guide: Laminar-Turbulent Transition](../Setup-Guide-Transition/) and [Setup Guide: Steady RANS for External Aerodynamics](../Setup-Guide-RANS-External-Aero/)
- [Turbulence Models](../Turbulence-Models/)
- All options: [Option Reference](../Option-Reference/). All output fields: [Output Fields Reference](../Output-Fields-Reference/) (`INTERMITTENCY`, `RE_THETA_T`, `INTERMITTENCY_SEP`, `INTERMITTENCY_EFF`, `TURB_INDEX`).
- For developers: [Adding a Transition Model](../Adding-a-Transition-Model/)
- [NASA Turbulence Modeling Resource](https://tmbwg.github.io/turbmodels/). It moved from turbmodels.larc.nasa.gov in 2026; the old links now lead to a NASA landing page.

Last checked against SU2 develop `11c177b904`.
