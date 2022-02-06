---
title: The SU2 V&V Collection
permalink: /vandv/home/
redirect_from: /vandv/index.html
disable_comments: true
---

The case studies presented in this section demonstrate the verification and validation (V&V) of the solvers within the SU2 suite. Verification activities assess whether a particular model has been implemented correctly in software, i.e., it is coded as specified and bug-free. Validation activities assess whether a particular model matches the physical reality for a situation of interest, typically via comparison with experiment. 

When available, rigorous verification via formal order of accuracy assessment by exact or manufactured solutions is performed. When exact or manufactured solutions are not available, code-to-code comparisons are made. By comparing SU2 results against many well-established codes on a sequence of refined grids and seeing agreement of key quantities in the limit, we can build a high degree of confidence that the models found within SU2 are implemented correctly.

We will continue to add cases over time to demonstrate V&V of additional physical models in SU2, and we encourage contributions from the community! Please see the contribute page for instructions on how to contribute.

**NOTE**: The primary purpose of this section of the website is to demonstrate V&V of the SU2 suite, and as such, the case studies are not written as tutorials. However, you can typically find the files needed to run the cases yourself in the [project V&V repository](https://github.com/su2code/vandv) or here in the [project website repository](https://github.com/su2code/su2code.github.io) .


## Summary of V&V case studies
------

#### Compressible Flow

* [Method of Manufactured Solutions for Compressible Navier-Stokes](/vandv/MMS_FVM_Navier_Stokes/)
Formal order of accuracy of the finite volume solver in SU2 for the laminar Navier-Stokes equations is assessed.
* [2D Zero Pressure Gradient Flat Plate RANS Verification Case](/vandv/Flat_Plate/)
Code-to-code comparisons of drag and skin friction on a turbulent flat plate is presented using data from the NASA Turbulence Modeling Resource.
* [2D Bump-in-Channel RANS Verification Case](/vandv/Bump_Channel/)
Code-to-code comparisons for a bump in a channel, which results in pressure gradients, is presented using data from the NASA Turbulence Modeling Resource.
* [Three-Element High-Lift Subsonic Airfoil](/vandv/30p30n/)
Results for the 30p30n airfoil, mesh independence study at low angle-of-attach, and determination of maximum lift, both comparing different numerical schemes.
