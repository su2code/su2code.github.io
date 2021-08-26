---
title: Gradients and Limiters
permalink: /docs_v7/Gradients-Limiters/
---

This page lists the gradient computation methods and the limiter functions in SU2 as well as their associated options, it is not meant as a detailed theory guide but some application guidance is given nonetheless. The options listed here do not apply to the high order DG solver.?

---


---

## Gradient Computation ##
The numerical method for the computation of the spatial gradients used for viscous fluxes and source terms is specified by the `NUM_METHOD_GRAD` field. The list of available options is given below.
`GREEN_GAUSS`: Classic gradient reconstruction based on the Green-Gauss theorem.
`WEIGHTED_LEAST_SQUARES`: Compute the gradient of a field using inverse-distance-weighted approximation.
The default option is set to `WEIGHTED_LEAST_SQUARES`.

The spatial gradients method used only for upwind reconstruction is specified by the `NUM_METHOD_GRAD_RECON` field. An additional method is available; `LEAST_SQUARES`: Compute the gradient of a field using unweighted Least- Squares approximation. If the `NUM_METHOD_GRAD_RECON` field is left empty or set to `NONE` it defaults to `NUM_METHOD_GRAD`.

Thin Shear Layer gradient reconstruction is always used for the construction of the Jacobian.

## Limiters ##
SU2 implements limiter functions to prevent the generation of oscillations when using upwind spatial discretisations. These are specified by the config field `SLOPE_LIMITER_FLOW`. The available options are:
- `NONE`                 - No limiter
- `VENKATAKRISHNAN`      - Slope limiter using Venkatakrisnan method.
- `VENKATAKRISHNAN_WANG` - Slope limiter using Venkatakrisnan method, eps based on solution. EPS is...?
- `BARTH_JESPERSEN`      - Slope limiter using Barth-Jespersen method.
- `VAN_ALBADA_EDGE`      - Slope limiter using Van Albada method.
- `SHARP_EDGES`          - Slope limiter using sharp edges.
- `WALL_DISTANCE`        - Slope limiter using wall distance.
The default option is set to `VENKATAKRISHNAN`.

   *  \n DESCRIPTION: Coefficient for the limiter. DEFAULT value 0.5. Larger values decrease the extent of limiting, values approaching zero cause lower-order approximation to the solution. \ingroup Config */
  addDoubleOption("VENKAT_LIMITER_COEFF", Venkat_LimiterCoeff, 0.05);
  
  
The option `LIMITER_ITER` specifies the number of iterations afterFreeze the value of the limiter after a number of iterations. DEFAULT value $999999$.
