---
title: Ideas List for SU2 Google Summer of Code
permalink: /gsoc/Introduction/
---

**Welcome to SU2 - GSOC!**  

This is the updated ideas list for GSOC 2026. If you are interested in participating in [Google Summer of Code](https://summerofcode.withgoogle.com/about) with the SU2 team, then please read the page on [participation](https://su2code.github.io/gsoc/Participation/). The projects listed below have been tuned to fit within the google summer of code program and they have mentors assigned to them. We can also accept personal ideas beyond the ones presented below but you need to convince one of the mentors to support you. We also need you to be proficient in SU2 and have some kind of technical background beyond general computer science (studying physics, mechanical engineering, aerospace engineering,...). 

## Project BP: Adding pressure-based solver
Project Description (max. 5 Sentences)
The pressure-based solver has been requested for a long time. This solver is an important addition to the CFD solvers, especially for low Mach and incompressible flows. People have worked on it (detailed documentation available), and there is a branch that contains a working version, but this was never finalized and added to the main SU2 branch. Hence, the project's objective is to evaluate the current status of attempts, and propose a strategy for getting the pressure-based solver in the latest version of SU2.
Expected Outcome (deliverables): Finalize pressure-based solver, validate with test cases, tutorial and merge the PR.
- Skills Required: C++, experience with CFD and numerical methods
- Possible Mentors: Nitish Anand and Edwin van der Weide
- Expected Project Size: 175 hrs/medium
- Difficulty rating: **medium-hard** (needs experience with Computational Fluid Dynamics)

## Project GPU: Continuation of GPU acceleration in SU2
Project Description (max. 5 Sentences)
The SU2 code relies heavily on sparse linear algebra. In this area, there is significant speed-up potential with the adoption of GPU-based processing, as was demonstrated in the GSOC 24 project that applied CUDA to sparse matrix-vector multiplications in SU2. The objective of this project is to move more linear algebra operations to GPU in order to avoid host-device communication bottlenecks within the sparse linear system solver.
Expected Outcome (deliverables): Make SU2’s sparse linear solver GPU-native, i.e. minimal host-device communication after the initial setup of the system. 
- Skills Required C++
- Possible Mentors Pedro Gomes (lead), Ole Burghardt
- Expected Project Size (90 hrs/ small , 175 hrs/medium, 350 hrs/large): 175 hrs (medium)
- Difficulty rating: **medium**

## Project AMR: Quick Adaptive Mesh refinement for 2D testcases  
Project Description (max. 5 Sentences)
Many users have asked for adaptive mesh refinement capabilities. Several research groups are working on this. The aim of this project is to introduce a quick and easy adaptive mesh refinement that simply reads an existing results file and adaptively refines the meshes based on the value of a field. 
Expected Outcome (deliverables): SU2_AMR, an added executable that simply splits 2D quad and triangle cells 
- Skills Required: C++
- Possible Mentors: Nijso Beishuizen (lead)  
- Expected Project Size (90 hrs/ small , 175 hrs/medium, 350 hrs/large): 175 hrs (medium)
- Difficulty rating: **medium**

## Project CMPLX: Performance Optimization of Complex Arithmetic in SU2
Project Description (max. 5 Sentences)
Complex arithmetic operations currently cause significant performance degradation in SU2 when features requiring complex numbers are enabled. This limitation affects the efficiency of certain solver capabilities and restricts their practical application in industrial-scale problems. Preliminary observations suggest that complex arithmetic is a primary bottleneck, but systematic profiling is needed to confirm and quantify these losses. The project's objective is to profile the solver to identify performance hotspots, validate that complex arithmetic is the root cause, and develop a custom complex arithmetic library optimised for SU2's specific use cases. This work will enable more efficient execution of complex-number-dependent features without compromising computational performance.
Expected Outcome (deliverables): Performance profiling report, custom complex arithmetic library (if validated as necessary), benchmark comparisons demonstrating speedup, integration into SU2 codebase, and documentation with usage guidelines.
- Skills Required: C++
- Possible Mentors: Joshua A. Kelly (lead)  
- Expected Project Size (90 hrs/ small , 175 hrs/medium, 350 hrs/large): 175 hrs (medium)
- Difficulty rating: **medium**

## Project PIML: Towards physics-informed machine learning with SU2
Project Description (max. 5 Sentences)
SU2 uses algorithmic differentiation (AD) for the adjoint solver and has the ability to use multi-layer perceptrons in data-driven equation of state models through the [MLPCpp](https://github.com/EvertBunschoten/MLPCpp.git) submodule. The aim of this project is to combine these two functionalities to enable physics-informed machine learning (PIML) in SU2 by updating the weights and biases of multi-layer perceptrons using AD for sensitivity calculation. PIML would enable data-driven turbulence modeling, solving partial differential equations without a mesh, and open the door to many other interesting research opportunities. 
Expected Outcome (deliverables): Demonstration of training a MLP for a reference data set within SU2 and comparison, MLP training library including at least one commonly used training algorithm (e.g. Adam), and documentation explaining usage.
- Skills Required: C++, experience with machine learning
- Possible Mentors: Evert Bunschoten (lead)
- Expected Project Size (90 hrs/ small , 175 hrs/medium, 350 hrs/large): 175 hrs (medium)
- Difficulty rating: **medium-hard**

  
