---
title: Gradients and Limiters
permalink: /docs_v7/Gradients-Limiters-Grant/
---

Write a brief summary once we are done with most of this.
Generally, the documenation is written with one sentence per line.

---


---
## Grant version
Grant will work on:
* "Basics of describing what options are available ..." 
* "Mathematically describe limiters available in SU2"
* helping with any python scripts for postprocessing of empirical study
* general documenation logistics: building, markdown / html specifics, github pull requests

## Basics of describing what options are available and providing some references for them
<!-- Also we assume that the user will know the theory, and that they are just looking for the limiters that are available in SU2 first. -->


The field `SLOPE_LIMITER_FLOW` in the `.cfg` file specifies which limiter to use. Note that this option is only used if `MUSCL_FLOW = YES` (which specifies to use a second-order method).
The [Laminar Cylinder](https://su2code.github.io/tutorials/Laminar_Cylinder/) shows an example of this.
The [Turbulent Flat Plate example](https://su2code.github.io/tutorials/Turbulent_Flat_Plate/) sets `SLOPE_LIMITER_TURB`, which is used for the turbulence equations, rather than for the flow equations.
More possible applications of limiters are listed below.

<!-- Do I need this as a title? -->
Slope Limiter Fields

| Configuration Field | Description | Notes |
| --- | --- | --- |
| `SLOPE_LIMITER_FLOW` | Flow equations | Need `MUSCL_FLOW = YES` |
| `SLOPE_LIMITER_TURB` | Turbulence equations | Need `MUSCL_TURB = YES` |
| `SLOPE_LIMITER_SPECIES` | Species evolution equations | Need `MUSCL_SPECIES = YES` |
| `SLOPE_LIMITER_ADJFLOW` | Adjoint flow equations | Need `MUSCL_ADJFLOW = YES` |
| `SLOPE_LIMITER_ADJTURB` | Adjoint turbulence equations | Need `MUSCL_ADJTURB = YES` |


<!-- 
CLimiterDetails.hpp:
computeLimiters.hpp uses computeLimiters_impl.hpp and really just sets the limiter
computeLimiters_impl.hpp passes computation of field values (cell averages), gradients, and  to the limiter

also check out
computeGradientsGreenGauss.hpp

 -->

The `SLOPE_LIMITER_` options above may each be changed to use different limiters, which are listed and explained below.


Available Limiters

| Type | Description |
| --- | --- |
| `NONE`                  | No limiter                                      |
| `BARTH_JESPERSEN`       | Barth-Jespersen                                 |
| `VENKATAKRISHNAN`       | Venkatakrishnan                                 |
| `VENKATAKRISHNAN_WANG`  | Venkatakrishnan-Wang                            |
| `SHARP_EDGES`           | Venkatakrishnan with sharp-edge modification    |
| `WALL_DISTANCE`         | Venkatakrishnan with wall distance modification |
| `VAN_ALBADA_EDGE`       |  [^1] Van Albada (edge formulation)             |


[^1]: This limiter may or may not be implemented for certain solvers. It may also suffer from problems of not outputing limiter values.
<!-- TODO: Kal, maybe clarify / add some details to the above? -->


The `VENKAT_LIMITER_COEFF` parameter is generally a small constant, defaulting to $$0.05$$, but its specific definition depends on the limiter being used.
This is different than the small constant used to prevent division by zero, which is used for all limiters.

For the `VENKATAKRISHNAN`, `SHARP_EDGES`, and `WALL_DISTANCE` limiters, the `VENKAT_LIMITER_COEFF` parameter refers to $$K$$ in $$\epsilon^2=\left(K\bar{\Delta} \right)^3$$, where $$\bar{\Delta}$$ is an average grid size.
The $$K$$ parameter defines a threshold, below which oscillations are not damped by the limiter, as described by [Venkatakrishnan](https://doi.org/10.1006/jcph.1995.1084).
Thus, a large value will approach the case of using no limiter, while too small of a value will slow the convergence.
This value depends on both the mesh and the flow variable.
<!-- maybe change wording from flow variable to "field variable being limited" -->

<!-- ??? should this section be included ??? -->
<!-- so, \bar{\Delta} is actually config.GetRefElemLength(), which refers to RefElemLength -->
Similarly, the parameter `REF_ELEM_LENGTH` controls $$\bar{\Delta}$$, but the behavior of the limiter should be controlled through `VENKAT_LIMITER_COEFF`.
This parameter is also used in the geometric factor of the `SHARP_EDGES` and `WALL_DISTANCE` limiters.

When using the `VENKATAKRISHNAN_WANG` limiter, `VENKAT_LIMITER_COEFF` is instead $$\varepsilon '$$ in $$\varepsilon = \varepsilon ' (q_{max} - q_{min})$$, where $$q_{min}$$ and $$q_{max}$$ are the respective *global* minimum and maximum of the field variable being limited.
Note that this global operation may incur extra time costs due to communication between MPI threads.
Based on the original work by [Wang](https://doi.org/10.2514/6.1996-2091) introducing this limiter suggests using `VENKAT_LIMITER_COEFF` in the range of $$[0.01, 0.20]$$, where again larger values approach the case of using no limiter.

The `NONE`, `BARTH_JESPERSEN`, `VENKATAKRISHNAN`, and `VENKATAKRISHNAN_WANG` limiter options all have no **geometric modifier**.
A geometric modifier increases limiting near walls or sharp edges. This is done by multiplying the limiter value by a **geometric factor**. 

For both the `SHARP_EDGES` and `WALL_DISTANCE` limiters, the influence of the geometric modifier is controlled with `ADJ_SHARP_LIMITER_COEFF` which defaults to 3.0.
Increasing this parameter will decrease the value of the limiter and thus make the field more diffusive and less oscillatory near the feature (sharp edge or wall).

In the `SHARP_EDGES` limiter, the qualification of what makes an edge "sharp" is described by the parameter `REF_SHARP_EDGES` (defaults to 3.0). Increasing this will make more edges qualify as "sharp".
Other than the addition of this geometric factor, these limiters are the same as the `VENKATAKRISHNAN` limiter and should also use `VENKAT_LIMITER_COEFF` (given by $$K$$ below).

<!-- ??? Are these limiters  only for adjoints???!!! -->

Specifically, given the distance to the feature, $$d_{\text{feature}}$$, an intermediate measure of the distance, $$d$$, is calculated. The parameter $$c$$ is set by `ADJ_SHARP_LIMITER_COEFF`.

$$ d(d_{\text{feature}}; c, K) = \frac{d_{\text{feature}}} { (c \cdot K \bar{\Delta}) } - 1$$

Then, the geometric factor is given by

$$ \gamma (d) = \frac{1}{2} (1+d+\sin(\pi \cdot d)/ \pi) $$

Note that the geometric factor is nonnegative and nondecreasing in $d_{feature}$.


<!-- Maybe missing some subsection / transitions here. -->

<!-- Maybe a better way to word this. -->
After the number of iterations given by `LIMITER_ITER` (default $$999999$$), the value of the limiter will be frozen.


The option `FROZEN_LIMITER_DISC` tells whether the slope limiter is to be frozen in the discrete adjoint formulation (default is `NO`).

 
<!-- We can specify which limiters are applied through the fields
constexpr size_t MAXNVAR = 32; -->
<!-- 
Should I mention some possible errors

SU2_MPI::Error("Too many dimensions to compute limiters.", CURRENT_FUNCTION);
SU2_MPI::Error("Unknown limiter type.", CURRENT_FUNCTION);

  constexpr size_t MAXNVAR = 32;

  if (varEnd > MAXNVAR)
    SU2_MPI::Error("Number of variables is too large, increase MAXNVAR.", CURRENT_FUNCTION);

 -->

## Why Slope Limiters are used in FVM
* TVD
* Monotonic
* 2nd order accuracy


### subsection example
a subsection would go here

## Mathematically describe limiters available to user in SU2
Also discuss their properties.

<!-- We need to first figure out what is going on with:
1) venkatFunction, missing '2'
2) Barth-Jespersen using venkatFunction and not non-smooth min/max
3) Van Albada... just... what?
 -->

<!-- TODO: Kal and Grant need to resolve notation, ex: k vs. K -->

## Empirical comparison of the available limiters on a test problem
Flowfield colored by the limiter value.
Link to the Documentation on how to generate these