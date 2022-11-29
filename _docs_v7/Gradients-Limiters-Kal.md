---
title: Gradients and Limiters
permalink: /docs_v7/Gradients-Limiters-Kal/
---

Write a brief summary once we are done with most of this.
Generally, the documenation is written with one sentence per line.

---


---
## Kal version
Kal will work on:
* "Why Slope Limiters are used in FVM" 
* "Empirical comparison of the available limiters on a test problem"
* Help setting up and running any necessary SU2 simulations 
* general documentation logistics, formatting, CURC navigation

## Basics of describing what options are available and providing some references for them
Do this before diving into the comparisons (which can be a lot more work)
Also we assume that the user will know the theory, and that they are just looking for the limiters that are available in SU2 first.

We may want to link to another place in the docs where they mention that limiters can be activated after a specific number of iterations.

## Why are slope limiters used in a Finite Volume Method? 
For many studying compressible flow or high-speed aerodynamics, the formation of shock discontinuities are a common occurrence. The use of high-order numerical schemes are desired to resolve these regions as they provide high accuracy. However, linear high-resolution schemes often result in numerical oscillations near the shock due to high-frequency content associated with the shock. These oscillations can result on non-physical values (e.g. negative density) that greatly degrade the accuracy of your solution and pollute the domain. An example of this phenomena is shown below with the Lax-Wendroff scheme for scalar advection. Although the Lax-Wendroff method is second order, note that it introduces numerical oscillations that result in the state value of $$u$$ becoming negative. 

<!-- high order == high accuracy, maybe change wording -->
<!-- oscillations can result **in** non-physical values -->
<!-- second order to second-order ? -->

<img src="../../docs_files/LW_example.png" width="500">

Figure (1): A one period advection (red) of an initial value discontinuity (black) using the Lax-Wendroff method. 

SU2 uses **slope limiters** to avoid these oscillations by switching to a low-resolution scheme near the shock, while switching back to a high-resolution scheme where the solution is smooth. This preserves solution accuracy in regions with smooth gradients and ensures numerical stability in regions close to the shock. 

Before mathematically describing the form of the limiters implemented in SU2, it is useful to briefly understand two concepts. These include **Total Variation** and **Godunov's Theorem**. 

### Total Variation and Total Variation Diminishing
We can first introduce the concept of **total variation** (TV) which is a measure of how oscillatory a solution is. In a discrete one dimensional setting, TV can be calculated as the following:  

$$ TV(u^n) = \sum_j |u^n_{j+1} - u^n_j| $$

<img src="../../docs_files/TV_example.png" width="500">

Figure (2): A numerical scheme resulting in both high and low TV.  

A scheme can be said to be **total variation diminishing** (TVD) if 

$$ TV(u^{n+1}) \leq TV(u^n) $$

where for every successive timestep $$n$$, the total variation of the solution does not increase. 

A favorable property of TVD schemes is that they are **monotonicity preserving**. This means they do not introduce new extrema into the solution and local minimum (maximum) are non-decreasing (increasing) in time. These are both desirable qualities for correctly resolving a shock and ensuring the solution is physical. 

### Godunov's Theorem
The question of "How accurate can a TVD scheme be?" is still unanswered. For this, we turn to Godunov's Theorem.

**Godunov's Theorem**: 
1. A linear scheme is monotone if and only if it is total variation diminishing. 
2. Linear total variation diminishing schemes are at most first-order accurate. 

<!-- Maybe source? -->

The first statement is simple, stating that for linear schemes, the characteristic of being monotone and TVD is equivalent. The second statement is more interesting. It states that if we want to construct a linear TVD (monotone) scheme, the best we can be possibly hope for is first-order accuracy. 

Recall that the original motivation for a slope limiter was to prevent the formation of oscillations in the solution. In the section above, we noted that TVD schemes are monotonicity preserving (a favorable property in resolving a shock). However, through Godunov's theorem, we note that if we also want high-order accuracy, **our TVD discretization MUST be nonlinear**

The inclusion of a slope limiter into a TVD scheme accomplishes this idea. 

## Mathematically describe limiters available to user in SU2
Also discuss their properties.

## Empirical comparison of limiters on a periodic advective domain
An example problem of the linear advection problem against four unique wave-forms was simulated to illustrate differences between the limiters in SU2. The wave forms contain both smooth and discontinuous initial conditions and are advected for a single period with a CFL of $$\sigma = 0.8$$. The domain is discretized with $$N = 200$$ cells. The Lax-Wendroff scheme was used as a comparative case: 

$$ u_j^{n+1} = u_j^{n} - \sigma (u_j^{n} - u_{j-1}^{n}) - \frac{1}{2}\sigma(1-\sigma) \left[ \phi_{j+\frac{1}{2}}(u_{j+1}^{n} - u_j^{n}) - \phi_{j-\frac{1}{2}}(u_{j}^{n} - u_{j-1}^{n})  \right] $$

where $$\phi_{j+\frac{1}{2}}$$ is the scalar value of the limiter at the interface of cell $$u_j$$ and $$u_{j+1}$$. 

<img src="../../docs_files/advection_example.png" width="600">

Figure (3): A one period advection (red) of an initial condition (black) using various schemes, with and without limiters. 

From the above example we note: 
* The **Lax-Wendroff** scheme produces oscillations near sudden gradients due to dispersion errors. From Godunov's theorem this is expected as the scheme is second-order accurate and does not utilize a limiter. 
* The **Barth-Jespersen** limiter performs well for most of the waveforms. However, the Barth-Jespersen limtier is known to be compressive and will turn smooth waves into square waves. This is best seen with the value discontinuity on the very left. 
* The **Van-Albada** limiter also performs well. It is slightly more diffusive than Barth-Jespersen but has robust convergence properties. 
* The **Venkatakrishnan** limiter is similar to the Barth-Jespersen and has significantly improved convergence properties. However, it is more diffusive and does require a user-specified parameter $$k$$ that is flow dependent. 

<!-- Maybe we should add a small conclusion too? -->
