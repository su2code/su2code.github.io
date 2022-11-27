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

## Why Slope Limiters are used in FVM
This section should describe the purpose slope limiters have in a FVM formulation. This should cover the concepts of: 
* TVD
* Monotonic
* 2nd order accuracy

### subsection example
a subsection would go here

## Mathematically describe limiters available to user in SU2
Also discuss their properties.

## Empirical comparison of the available limiters on a test problem
This section should describe in a general sense the characteristics of the limiters in SU2. These limiters include 
* Minmod 
* Venkatakrishnan  
* Barth-Jespersen 