---
title: Turbulence Models
permalink: /docs_v7/Turbulence-Models/
---

This page explains the model and its SU2 implementation. For numerical setup choices, see the [setup guide](../Setup-Guide-RANS-External-Aero/); use its tutorial and V&V links for worked examples and comparisons.

A RANS simulation does not resolve turbulent eddies. A turbulence model adds transport equations that give the eddy viscosity, which models the extra mixing caused by turbulence. SU2 has two model families: the one-equation Spalart-Allmaras (SA) model and the two-equation k-omega Shear Stress Transport (SST) model, each with several variants.

---

- [Select a model](#select-a-model)
- [Spalart-Allmaras (SA)](#spalart-allmaras-sa)
- [Shear Stress Transport (SST)](#shear-stress-transport-sst)
- [What SU2 does differently from the literature](#what-su2-does-differently-from-the-literature)
- [Free-stream and inlet values](#free-stream-and-inlet-values)
- [Verification and test cases](#verification-and-test-cases)
- [Known limits](#known-limits)
- [Related pages](#related-pages)

---

## Select a model

- Set `SOLVER= RANS` (compressible) or `SOLVER= INC_RANS` (incompressible). The discrete adjoint of both solvers uses the same model options.
- Set `KIND_TURB_MODEL` to `SA` or `SST`. The default is `NONE`.
- SU2 stops with an error if `SOLVER` is `RANS` or `INC_RANS` and `KIND_TURB_MODEL= NONE`. It also stops if `SOLVER` is `NAVIER_STOKES` or `INC_NAVIER_STOKES` and a turbulence model is set.
- Choose the variant with `SA_OPTIONS` (for SA) or `SST_OPTIONS` (for SST). Both take a list of keywords. An empty list gives the default variant.
- SU2 prints the full name of the variant it runs at the start of the run, for example `Spalart-Allmaras-noft2` or `Menter's k-omega SST-2003m`.

<!-- Common/src/CConfig.cpp:1199-1203, 3803-3814, 6640-6697 -->

Other options that act on all turbulence models:

| Option | Default | What it does |
| --- | --- | --- |
| `PRANDTL_TURB` | `0.9` | Turbulent Prandtl number. It turns the eddy viscosity into a turbulent heat conductivity. Takes one value per species for mixtures. |
| `TURBULENT_CONDUCTIVITY_MODEL` | `CONSTANT_PRANDTL_TURB` | In incompressible flow, `NONE` switches off the fluid model's turbulent heat conductivity. Compressible viscous fluxes still add Cp × mu_t / `PRANDTL_TURB`, independently of this setting. |
| `TURB_FIXED_VALUES` | `NO` | Keeps the turbulence variables at their free-stream values in the region upstream of a plane. |
| `TURB_FIXED_VALUES_DOMAIN` | none | Position of that plane, as a distance along the free-stream direction. Required with `TURB_FIXED_VALUES= YES`. |

<!-- CConfig.cpp:1387, 1410, 4294, 4316, 2540-2542, 5288; SU2_CFD/src/solvers/CTurbSolver.cpp:234-265 -->

Old values of `KIND_TURB_MODEL` (`SST_SUST`, `SA_NEG`, `SA_E`, `SA_COMP`, `SA_E_COMP`) and `KIND_TRANS_MODEL= BC` are no longer accepted. SU2 stops and prints the new option to use. <!-- CConfig.cpp:3425-3439 -->

Hybrid RANS-LES models (DES, DDES and stochastic backscatter) build on these models. See [Hybrid RANS-LES](../Hybrid-RANS-LES/). Wall functions and wall roughness, including the SST roughness boundary conditions, are on [Wall Treatment](../Wall-Treatment/).

## Spalart-Allmaras (SA)

Select it with `KIND_TURB_MODEL= SA`. The model solves one equation for the SA working variable, nu-tilde (`NU_TILDE` in the output). The [NASA Turbulence Modeling Resource (TMR) SA page](https://tmbwg.github.io/turbmodels/spalart.html) gives the equations of every variant.

### SA_OPTIONS keywords

| Keyword | Effect | TMR name |
| --- | --- | --- |
| (empty list) or `NONE` | SA without the ft2 term. This is the SU2 default. | [SA-noft2](https://tmbwg.github.io/turbmodels/spalart.html#sanoft2) |
| `WITHFT2` | Adds the ft2 term (the laminar suppression term). | [SA](https://tmbwg.github.io/turbmodels/spalart.html#sa) |
| `NEGATIVE` | Negative SA: allows negative nu-tilde with modified source and diffusion terms. | [SA-neg](https://tmbwg.github.io/turbmodels/spalart.html#saneg) |
| `EDWARDS` | Edwards modification: uses the strain rate instead of the vorticity. | [SA-noft2-Edwards](https://tmbwg.github.io/turbmodels/spalart.html#saEdwards) |
| `ROTATION` | Rotation correction of Dacles-Mariani et al. | [SA-R](https://tmbwg.github.io/turbmodels/spalart.html#saR) |
| `COMPRESSIBILITY` | Mixing-layer compressibility correction. | [SA-comp](https://tmbwg.github.io/turbmodels/spalart.html#sacomp) |
| `QCR2000` | Quadratic constitutive relation: adds a nonlinear term to the turbulent stresses. | [SA-QCR2000](https://tmbwg.github.io/turbmodels/spalart.html#qcr2000) |
| `BCM` | Bas-Cakmakcioglu algebraic transition model. See [Transition Models](../Transition-Models/). | [SA-BCM](https://tmbwg.github.io/turbmodels/sa-bc_1eqn.html) |
| `EXPERIMENTAL` | Turns off the checks on combinations (see below). | none |

<!-- Common/include/option_structure.hpp:1264-1285 -->

### Combinations that SU2 accepts

SU2 follows the variant names of the TMR. It stops with an error for combinations that the TMR does not list:

- `NEGATIVE` and `EDWARDS` cannot be used together, even with `EXPERIMENTAL`.
- `NEGATIVE` needs `WITHFT2`, because SA-neg is defined with the ft2 term. It cannot be combined with `BCM`.
- `EDWARDS` must be alone. It cannot be combined with `WITHFT2`, `ROTATION`, `COMPRESSIBILITY`, `QCR2000` or `BCM`.
- `BCM` cannot be combined with `WITHFT2`, `ROTATION`, `COMPRESSIBILITY` or `QCR2000`.
- Without `NEGATIVE`, `EDWARDS` or `BCM`, any mix of `WITHFT2`, `ROTATION`, `COMPRESSIBILITY` and `QCR2000` is accepted.

Add `EXPERIMENTAL` to the list to run a combination that SU2 rejects, for example `SA_OPTIONS= NEGATIVE, EXPERIMENTAL` (SA-neg without ft2). <!-- option_structure.hpp:1306-1358 -->

Examples:

| TMR name | Setting |
| --- | --- |
| SA-noft2 | `SA_OPTIONS= NONE` (or leave the option out) |
| SA | `SA_OPTIONS= WITHFT2` |
| SA-neg | `SA_OPTIONS= NEGATIVE, WITHFT2` |
| SA-noft2-R-comp | `SA_OPTIONS= ROTATION, COMPRESSIBILITY` |
| SA-neg-R-comp-QCR2000 | `SA_OPTIONS= NEGATIVE, WITHFT2, ROTATION, COMPRESSIBILITY, QCR2000` |
| SA-noft2-Edwards | `SA_OPTIONS= EDWARDS` |
| SA-BCM | `SA_OPTIONS= BCM` |

Original papers:

- SA: P. R. Spalart and S. R. Allmaras, "A One-Equation Turbulence Model for Aerodynamic Flows", La Recherche Aérospatiale, No. 1, 1994, pp. 5-21.
- SA-neg: S. R. Allmaras, F. T. Johnson and P. R. Spalart, "Modifications and Clarifications for the Implementation of the Spalart-Allmaras Turbulence Model", ICCFD7-1902, 2012.
- SA-R: J. Dacles-Mariani, G. G. Zilliac, J. S. Chow and P. Bradshaw, AIAA Journal 33(9), 1995, pp. 1561-1568.
- SA-comp: P. R. Spalart, "Trends in Turbulence Treatments", AIAA 2000-2306.
- SA-QCR2000: P. R. Spalart, "Strategies for Turbulence Modelling and Simulation", Int. J. Heat and Fluid Flow 21, 2000, pp. 252-263.
- SA-noft2-Edwards: J. R. Edwards and S. Chandra, AIAA Journal 34(4), 1996, pp. 756-763.

## Shear Stress Transport (SST)

Select it with `KIND_TURB_MODEL= SST`. The model solves two equations: the turbulent kinetic energy k (`TKE` in the output) and the specific dissipation rate omega (`DISSIPATION`). The [TMR SST page](https://tmbwg.github.io/turbmodels/sst.html) gives the equations of every variant.

### SST_OPTIONS keywords

The keywords fall into four groups. SU2 has only the "m" forms of SST ([see below](#sst)).

**Version** (at most one):

| Keyword | Effect | TMR name |
| --- | --- | --- |
| `V2003m` | 2003 version, "m" form. This is the default when no version is given. | [SST-2003m](https://tmbwg.github.io/turbmodels/sst.html#sst-2003) |
| `V1994m` | Original 1994 version, "m" form. | [SSTm](https://tmbwg.github.io/turbmodels/sst.html#sst-std) |

**Production term** (at most one): what SU2 uses in place of the strain rate magnitude S in the production of k.

| Keyword | Effect | TMR name |
| --- | --- | --- |
| `VORTICITY` | Uses the vorticity magnitude. | [SST-Vm](https://tmbwg.github.io/turbmodels/sst.html#sst-v) |
| `KATO-LAUNDER` | Replaces S² in production by SΩ, the product of strain-rate and vorticity magnitudes. | [SST-KLm](https://tmbwg.github.io/turbmodels/sst.html#sst-kl) |
| `UQ` | Uses a perturbed Reynolds stress tensor, for uncertainty quantification. See the [UQ tutorial](/tutorials/UQ_NACA0012/) and the options `UQ_COMPONENT` (default `1`), `UQ_DELTA_B` (`1.0`), `UQ_URLX` (`0.1`), `UQ_PERMUTE` (`NO`). | none |

**Compressibility correction** (at most one, only with `SOLVER= RANS`):

| Keyword | Effect |
| --- | --- |
| `COMPRESSIBILITY-WILCOX` | Wilcox dilatation-dissipation correction. Active where the turbulent Mach number sqrt(2k)/a is above 0.25. |
| `COMPRESSIBILITY-SARKAR` | Sarkar correction: dilatation dissipation plus a pressure-dilatation term. Same threshold. |

**Other modifiers** (combine with anything):

| Keyword | Effect | TMR name |
| --- | --- | --- |
| `SUSTAINING` | Controlled decay: keeps k and omega from decaying below their free-stream values. | [SST-sust](https://tmbwg.github.io/turbmodels/sst.html#sst-sust) |
| `DIMENSIONLESS_LIMIT` | Sets the lower limits of k and omega relative to their free-stream values (see below). | none |
| `NONE` | No effect. | none |

<!-- option_structure.hpp:1103-1231; SU2_CFD/include/numerics/turbulent/turb_sources.hpp:925-996; CConfig.cpp:3839-3845, 3214-3227 -->

SU2 stops with an error if you give two versions, two production keywords or two compressibility keywords.

Examples:

| TMR name | Setting |
| --- | --- |
| SST-2003m | `SST_OPTIONS= V2003m` (or leave the option out) |
| SSTm | `SST_OPTIONS= V1994m` |
| SST-Vm | `SST_OPTIONS= V1994m, VORTICITY` |
| SST-KLm | `SST_OPTIONS= V1994m, KATO-LAUNDER` |
| SST-sust-m | `SST_OPTIONS= V1994m, SUSTAINING` |

Original papers:

- SST (1994): F. R. Menter, "Two-Equation Eddy-Viscosity Turbulence Models for Engineering Applications", AIAA Journal 32(8), 1994, pp. 1598-1605.
- SST-2003: F. R. Menter, M. Kuntz and R. Langtry, "Ten Years of Industrial Experience with the SST Turbulence Model", Turbulence, Heat and Mass Transfer 4, 2003, pp. 625-632.
- SST-V: F. R. Menter, "Improved Two-Equation k-omega Turbulence Models for Aerodynamic Flows", NASA TM 103975, 1992.
- SST-KL: M. Kato and B. E. Launder, 9th Symposium on Turbulent Shear Flows, Kyoto, 1993, paper 10-4.
- SST-sust: P. R. Spalart and C. L. Rumsey, "Effective Inflow Conditions for Turbulence Models in Aerodynamic Calculations", AIAA Journal 45(10), 2007, pp. 2544-2553.

## What SU2 does differently from the literature

This section lists where SU2 departs from the TMR definitions, or where the SU2 defaults differ from what the TMR calls "standard".

### SA

- **The default is SA-noft2, not standard SA.** The TMR calls the version with the ft2 term "standard". SU2 leaves ft2 out unless you add `WITHFT2`. The TMR notes that SA-noft2 gives almost the same results for most practical problems. <!-- turb_sources.hpp:415-432, 703-708 -->
- **Limiting of the modified vorticity.** In all variants except Edwards, SU2 limits the modified vorticity S-hat as in note 1(c) of Allmaras et al. (2012), and keeps it above 1e-10. In SA-neg, where nu-tilde is negative, S-hat is the vorticity. <!-- turb_sources.hpp:442-504 -->
- **Rotation correction with SA-neg.** With `ROTATION`, SU2 takes the absolute value of the production term where nu-tilde is negative. The correction constant is 2. <!-- turb_sources.hpp:276-281, 51 -->
- **Compressibility correction.** `COMPRESSIBILITY` uses C5 = 3.5. SU2 computes the speed of sound from the ideal-gas relation sqrt(gamma p / rho), whatever the fluid model. In axisymmetric runs it adds the matching axisymmetric term. SU2 does not stop you from using it with `INC_RANS` (to be reviewed: check whether the result makes sense there). <!-- turb_sources.hpp:606-670 -->
- **QCR2000.** SU2 adds the QCR term (constant 0.3) to the stress tensor, scaled by the fraction of eddy viscosity in the total viscosity. It is available only with SA. <!-- SU2_CFD/include/numerics/CNumerics.hpp:520-566; flow_diffusion.cpp:481-485 -->
- **Rough walls.** SU2 applies the Aupoix-Spalart roughness correction when a wall has a roughness height. See [Wall Treatment](../Wall-Treatment/).

### SST

- **SST is always the "m" form.** SU2 does not include the turbulent kinetic energy in the viscous stress tensor of the mean flow equations. The production of k is mu_t S^2 (or the vorticity or Kato-Launder form). The unmodified keywords `V1994` and `V2003` are not available. <!-- flow_diffusion.cpp:141; turb_sources.hpp:964; option_structure.hpp:1121-1123 -->
- **Exception: `UQ`.** With `UQ`, SU2 uses the perturbed Reynolds stress tensor, which includes k, both in the mean flow equations and in the production of k. <!-- flow_diffusion.cpp:132-138; turb_sources.hpp:927-931 -->
- **`V1994m` is consistent with the TMR since SU2 v8.** Before, SU2 dropped k from the stress tensor but kept a divergence term in the production ([issue #1551](https://github.com/su2code/SU2/issues/1551), now closed). [Pull request #2062](https://github.com/su2code/SU2/pull/2062), merged in July 2023, removed that term and made `V2003m` the default. <!-- option_structure.hpp:1168-1174 -->
- **1994 versus 2003.** As in the TMR: 1994 uses the vorticity in the eddy viscosity limiter, a production limiter of 20 and the unlimited production in the omega equation; 2003 uses the strain rate, a limiter of 10 and the limited production in the omega equation. The 2003 version also uses its own values of the constants gamma_1 = 5/9 and gamma_2 = 0.44. <!-- CTurbSSTSolver.cpp:92-109, 254-255; turb_sources.hpp:961-976 -->
- **Sustaining terms.** The TMR adds the sustaining terms to the sources. SU2 instead takes the larger of the production and the sustaining term, for k and for omega. Where production is larger, the model is unchanged. The ambient values are the free-stream k and omega that SU2 computes from `FREESTREAM_TURBULENCEINTENSITY` and `FREESTREAM_TURB2LAMVISCRATIO` (see below). The TMR recommends specific ambient values; SU2 does not set them for you. <!-- turb_sources.hpp:978-989 -->
- **Compressibility corrections replace the production keyword.** In the code, `COMPRESSIBILITY-WILCOX` and `COMPRESSIBILITY-SARKAR` overwrite the production setting. If you combine them with `VORTICITY`, `KATO-LAUNDER` or `UQ`, SU2 gives no error, but the production uses the strain rate. The start-up message shows only the compressibility correction. With `UQ`, the mean flow stress tensor is still perturbed. Do not combine the two groups. <!-- option_structure.hpp:1193-1210; turb_sources.hpp:926-959; flow_diffusion.cpp:132 -->
- **Lower limits of k and omega.** By default SU2 keeps k above 1e-10 and omega above 1e-4 (in the non-dimensional units of the solver). With `DIMENSIONLESS_LIMIT`, the limits become `LOWER_LIMIT_K_FACTOR` (default `1e-15`) times the free-stream k and `LOWER_LIMIT_OMEGA_FACTOR` (default `1e-05`) times the free-stream omega. <!-- CTurbSSTSolver.cpp:130-143; CConfig.cpp:1536-1538 -->
- **No curvature correction.** SST-RC and similar variants are not implemented.

## Free-stream and inlet values

SU2 starts the whole field from the free-stream values of the turbulence variables, and uses them at far-field boundaries. <!-- CTurbSASolver.cpp:105-145; CTurbSSTSolver.cpp:111-149 -->

**SA.**

| Option | Default | Meaning |
| --- | --- | --- |
| `FREESTREAM_NU_FACTOR` | `3.0` | Free-stream nu-tilde divided by the free-stream kinematic viscosity. |
| `ENGINE_NU_FACTOR` | `3.0` | Same ratio at engine and actuator disk boundaries. |

With `BCM`, SU2 multiplies the free-stream, inlet and engine values (not the actuator disk value) by 0.005. The default free-stream nu-tilde is then 0.015 times the kinematic viscosity. <!-- CTurbSASolver.cpp:110-131 -->

**SST.**

| Option | Default | Meaning |
| --- | --- | --- |
| `FREESTREAM_TURBULENCEINTENSITY` | `0.05` | Turbulence intensity Tu as a fraction (0.05 means 5 %). |
| `FREESTREAM_TURB2LAMVISCRATIO` | `10.0` | Ratio of eddy viscosity to laminar viscosity. |

SU2 computes k = 1.5 (Tu U)^2 from the free-stream speed U, and then omega = rho k / (mu × ratio). <!-- CTurbSSTSolver.cpp:122-127 -->

The defaults (5 % and 10) are not calibrated inlet conditions. Choose the intensity and length/time scale for the actual flow, and check their decay between the boundary and the body. The TMR gives recommended far-field values for each model, and [Setup Guide: Steady RANS for External Aerodynamics](../Setup-Guide-RANS-External-Aero/) discusses the choice.

**Inlets.** `MARKER_INLET_TURBULENT` sets values per inlet marker:

- SA: `MARKER_INLET_TURBULENT= (inlet, 3.0)`. The value is nu-tilde divided by the kinematic viscosity at the inlet, like `FREESTREAM_NU_FACTOR`. (The SU2 error message calls it a viscosity ratio, but the code uses it as the nu-tilde factor.)
- SST: `MARKER_INLET_TURBULENT= (inlet, 0.05, 10.0)`: turbulence intensity, then viscosity ratio. SU2 computes k and omega from the inlet velocity, density and viscosity.
- An inlet not listed in `MARKER_INLET_TURBULENT` uses the free-stream values of the options above.
- With an inlet profile file, the file gives nu-tilde (SA) or k and omega (SST) in dimensional units.

<!-- CTurbSASolver.cpp:611-652; CTurbSSTSolver.cpp:603-649; CConfig.cpp:5874-5886, 9630-9639 -->

## Verification and test cases

Verification and validation (V&V) pages, with configs in [TestCases/vandv](https://github.com/su2code/SU2/tree/develop/TestCases/vandv/rans):

| Page | Models | Config |
| --- | --- | --- |
| [Flat plate](/vandv/Flat_Plate/) | SA, SST 1994m and 2003m | [turb_flatplate_sst.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/vandv/rans/flatplate/turb_flatplate_sst.cfg) (`V1994m`) |
| [Bump in channel](/vandv/Bump_Channel/) | SST | [turb_bump_sst.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/vandv/rans/bump_in_channel/turb_bump_sst.cfg) (`V1994m`) |
| [DSMA661 airfoil wake](/vandv/dsma661/) | SA, SST | [dsma661_sa_config.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/vandv/rans/dsma661/dsma661_sa_config.cfg) (SA-noft2), [dsma661_sst_config.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/vandv/rans/dsma661/dsma661_sst_config.cfg) (`V2003m`) |
| [30P30N high-lift airfoil](/vandv/30p30n/) | SA-noft2 | [config.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/vandv/rans/30p30n/config.cfg) |
| [Shock-wave boundary-layer interaction](/vandv/swbli/) | SA-neg, SST-2003m with Wilcox correction | [config_sa.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/vandv/rans/swbli/config_sa.cfg), [config_sst.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/vandv/rans/swbli/config_sst.cfg) |
| [Sandia jet](/vandv/SANDIA_jet/) | SST-2003m, incompressible | [validation.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/vandv/species_transport/sandia_jet/validation.cfg) |

Test cases that show the option keywords:

- SA variants on the RAE2822 airfoil, in [TestCases/turbulence_models/sa/rae2822](https://github.com/su2code/SU2/tree/develop/TestCases/turbulence_models/sa/rae2822): baseline, `COMPRESSIBILITY`, `EDWARDS`, `EDWARDS, COMPRESSIBILITY, EXPERIMENTAL`, `NEGATIVE, EXPERIMENTAL` (SA-neg without ft2) and `QCR2000`. `TestCases/parallel_regression.py` runs all six configs as the `turbmod_sa_*_rae2822` tests.
- SST variants on the NACA 0012, in [TestCases/rans/naca0012](https://github.com/su2code/SU2/tree/develop/TestCases/rans/naca0012): `turb_NACA0012_sst.cfg` (`V1994m`), `turb_NACA0012_sst_2003m.cfg`, `turb_NACA0012_sst_2003-Vm.cfg`, `turb_NACA0012_sst_1994-KLm.cfg`, `turb_NACA0012_sst_sust.cfg` and `turb_NACA0012_sst_fixedvalues.cfg` (`TURB_FIXED_VALUES`).
- SST compressibility corrections on a flat plate: [turb_SST_flatplate_compressibility_Wilcox.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/rans/flatplate/turb_SST_flatplate_compressibility_Wilcox.cfg) and [turb_SST_flatplate_compressibility_Sarkar.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/rans/flatplate/turb_SST_flatplate_compressibility_Sarkar.cfg).
- SST with sustaining terms on the RAE2822: [turb_SST_SUST_RAE2822.cfg](https://github.com/su2code/SU2/blob/develop/TestCases/rans/rae2822/turb_SST_SUST_RAE2822.cfg).
- SST with `UQ`: [TestCases/rans_uq/naca0012](https://github.com/su2code/SU2/tree/develop/TestCases/rans_uq/naca0012).

Tutorials:

- SA: [Turbulent Flat Plate](/tutorials/Turbulent_Flat_Plate/), [Turbulent ONERA M6](/tutorials/Turbulent_ONERAM6/), [Incompressible Turbulent Flat Plate](/tutorials/Inc_Turbulent_Flat_Plate/), [Incompressible Turbulent NACA 0012](/tutorials/Inc_Turbulent_NACA0012/)
- SST with `UQ`: [Uncertainty quantification of RANS predictions (NACA 0012)](/tutorials/UQ_NACA0012/)

## Known limits

- Only SA and SST are available. There are no k-epsilon, Reynolds stress or algebraic models.
- SST has no unmodified (non-"m") form and no curvature correction.
- The SST compressibility corrections work only with `SOLVER= RANS`.
- Some SA combinations need `EXPERIMENTAL`. Results with those combinations are not verified against the TMR.
- `FEM_RANS` (the high-order finite element solver) does not use these models.
- RANS models predict a fully turbulent boundary layer. For laminar regions and transition, see [Transition Models](../Transition-Models/).

## Related pages

- [Setup Guide: Steady RANS for External Aerodynamics](../Setup-Guide-RANS-External-Aero/)
- [Transition Models](../Transition-Models/), [Hybrid RANS-LES](../Hybrid-RANS-LES/), [Wall Treatment](../Wall-Treatment/)
- All options: [Option Reference](../Option-Reference/). All output fields: [Output Fields Reference](../Output-Fields-Reference/).
- For developers: [Adding a Turbulence Model](../Adding-a-Turbulence-Model/)
- [NASA Turbulence Modeling Resource](https://tmbwg.github.io/turbmodels/). It moved from turbmodels.larc.nasa.gov in 2026; the old links now lead to a NASA landing page.

Source review: 22 October 2026, against [SU2 `docs_site` at `41ea6a219a`](https://github.com/rois1995/SU2/tree/41ea6a219ac038574f3d4a5b130c0c1d8af66457). See the [review scope and outstanding validation](../Documentation-Status/#guide-and-model-review). Setup recommendations remain draft where indicated.
