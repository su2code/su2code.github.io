---
title: Gradients and Limiters
permalink: /docs_v7/Gradients-Limiters/
---

This page lists the gradient computation methods and the limiter functions in SU2 as well as their associated options, it is not meant as a detailed theory guide but some application guidance is given nonetheless. The options listed here do not apply to the high order DG solver.

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
- `VENKATAKRISHNAN_WANG` - Slope limiter using Venkatakrisnan method, with the small non-vanishing bias to prevent divisions by zero based on the min-to-max range of the solution.
- `BARTH_JESPERSEN`      - Slope limiter using Barth-Jespersen method.
- `VAN_ALBADA_EDGE`      - Slope limiter using Van Albada method.
- `SHARP_EDGES`          - Slope limiter using sharp edges.
- `WALL_DISTANCE`        - Slope limiter using wall distance.
With the default option set to `VENKATAKRISHNAN`.

The `VENKAT_LIMITER_COEFF` field is used to compute the small non-vanishing bias to prevent divisions by zero, $\epsilon$. Depending on the limiter to be used this field has different interpretations. For the `VENKATAKRISHNAN` limiter it represents the constant $K$ in $\epsilon^2=\left(K\Delta x\right)^3$. We refer to [Venkatakrishnan](https://doi.org/10.1006/jcph.1995.1084) for further details. For the `VENKATAKRISHNAN_WANG` limiter it represents the constant $\epsilon^{\prime}$ in $\epsilon = \epsilon^{\prime}(q^{\text{\max}}-q^{\text{\min}})$. We refer to [Wang](https://doi.org/10.2514/6.1996-2091) for further details. For both limiters larger values of `VENKAT_LIMITER_COEFF` decrease the extent of limiting, while values approaching zero cause lower-order approximation to the solution. The dafault value is 0.05.
  
The option `LIMITER_ITER` specifies the number of iterations afterFreeze the value of the limiter after a number of iterations. DEFAULT value $999999$.
