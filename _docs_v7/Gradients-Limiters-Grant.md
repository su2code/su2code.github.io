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
Do this before diving into the comparisons (which can be a lot more work)
Also we assume that the user will know the theory, and that they are just looking for the limiters that are available in SU2 first.


The field `SLOPE_LIMITER_FLOW` in the `.cfg` file specifies which limiter to use, and defaults to `VENKATAKRISHNAN` (see below). Note that this option is only used if `MUSCL_FLOW = YES` (which specifies to use a second-order method).
An example is shown here: https://su2code.github.io/tutorials/Laminar_Cylinder/. The [Turbulent Flat Plate example](https://su2code.github.io/tutorials/ Turbulent_Flat_Plate/) sets `SLOPE_LIMITER_TURB` (also defaulting to `VENKATAKRISHNAN`), which is used for the turbulence equations, rather than for the flow equations. Using a limiter similarly requires `MUSCL_TURB = YES` The settings `MUSCL_ADJFLOW`, `MUSCL_ADJTURB`, `SLOPE_LIMITER_ADJFLOW`, and `SLOPE_LIMITER_ADJTURB` set the corresponding options for the respective adjoint equations. For species transport, the options `MUSCL_SPECIES` and `SLOPE_LIMITER_SPECIES` are used.

<!-- There's also: 
% Frozen the slope limiter in the discrete adjoint formulation (NO, YES)
FROZEN_LIMITER_DISC= NO
 -->


<!-- 
CLimiterDetails.hpp:
computeLimiters.hpp uses computeLimiters_impl.hpp and really just sets the limiter
computeLimiters_impl.hpp passes computation of field values (cell averages), gradients, and  to the limiter

also check out
computeGradientsGreenGauss.hpp

 -->

The `SLOPE_LIMITER_` options above may each be changed to use different limiters, as explained below.


All of the limiters depend on variables `proj`, `delta`, and `eps`/`eps2` (and maybe `dist` for `raisedSine` in `SHARP_EDGES`)

Limiters

| Type | Description | Notes |
| --- | --- | --- |
| `NONE`                  | No limiter                                      |  | 
| `BARTH_JESPERSEN`       | Barth-Jespersen                                 |  | 
| `VENKATAKRISHNAN`       | Venkatakrishnan                                 |  | 
| `VENKATAKRISHNAN_WANG`  | Venkatakrishnan-Wang                            |  | 
| `SHARP_EDGES`           | Venkatakrishnan with sharp edge modification    |  | 
| `WALL_DISTANCE`         | Venkatakrishnan with wall distance modification |  |


The `VENKAT_LIMITER_COEFF` parameter is generally a small constant, defaulting to $0.05$, but its specific definition depends on the limiter being used.

For the `VENKATAKRISHNAN` option, the `VENKAT_LIMITER_COEFF` parameter refers to $K$ in $\epsilon^2=\left(K\bar{\Delta} x\right)^3$, where $\bar{\Delta}$ is an average grid size. The $K$ parameter defines a threshold, below which oscillations are not damped by the limiter, as described by [Venkatakrishnan](https://doi.org/10.1006/jcph.1995.1084). Thus, a large value will approach the case of using no limiter, while too small of a value will slow the convergence.


[Wang](https://doi.org/10.2514/6.1996-2091)

<!-- Maybe a better way to word this. -->
After the number of iterations given by `LIMITER_ITER` (default $999999$), the value of the limiter will be frozen.



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

## Empirical comparison of the available limiters on a test problem
Flowfield colored by the limiter value.
Link to the Documentation on how to generate these