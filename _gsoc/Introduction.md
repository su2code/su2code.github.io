---
title: Welcome to the SU2 Google Summer of Code Page
permalink: /gsoc/Introduction/
---

**Welcome to SU2 - GSOC!**  

This is the ideas list for GSOC 2026.

## Project BP: Adding pressure-based solver
Project Description (max. 5 Sentences)
The pressure-based solver has been requested for a long time. This solver is an important addition to the CFD solvers, especially for low Mach and incompressible flows. People have worked on it (detailed documentation available), and there is a branch that contains a working version, but this was never finalized and added to the main SU2 branch. Hence, the project's objective is to evaluate the current status of attempts, and propose a strategy for getting the pressure-based solver in the latest version of SU2.
Expected Outcome (deliverables): Finalize pressure-based solver, validate with test cases, tutorial and merge the PR.
Skills Required: C++, experience with CFD and numerical methods
Possible Mentors: Nitish Anand and Edwin van der Weide
Expected Project Size: 175 hrs/medium
Difficulty rating: medium-hard (needs experience with Computational Fluid Dynamics)

## Project GPU: Continuation of GPU acceleration in SU2
Project Description (max. 5 Sentences)
The SU2 code relies heavily on sparse linear algebra. In this area, there is significant speed-up potential with the adoption of GPU-based processing, as was demonstrated in the GSOC 24 project that applied CUDA to sparse matrix-vector multiplications in SU2. The objective of this project is to move more linear algebra operations to GPU in order to avoid host-device communication bottlenecks within the sparse linear system solver.
Expected Outcome (deliverables): Make SU2’s sparse linear solver GPU-native, i.e. minimal host-device communication after the initial setup of the system. 
Skills Required C++
Possible Mentors Pedro Gomes (lead), Ole Burghardt
Expected Project Size (90 hrs/ small , 175 hrs/medium, 350 hrs/large): 175 hrs (medium)
Difficulty rating (easy (little experience/background), medium (some experience/background), hard (experienced)): medium

## Project AMR: Quick Adaptive Mesh refinement for 2D testcases  
Project Description (max. 5 Sentences)
Many users have asked for adaptive mesh refinement capabilities. Several research groups are working on this. The aim of this project is to introduce a quick and easy adaptive mesh refinement that simply reads an existing results file and adaptively refines the meshes based on the value of a field. 
Expected Outcome (deliverables): SU2_AMR, an added executable that simply splits 2D quad and triangle cells 
Skills Required: C++
Possible Mentors: Nijso Beishuizen (lead)  
Expected Project Size (90 hrs/ small , 175 hrs/medium, 350 hrs/large): 175 hrs (medium)
Difficulty rating (easy (little experience/background), medium (some experience/background), hard (experienced)): medium

