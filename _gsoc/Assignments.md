---
title: Student Assignments 
permalink: /gsoc/Assignments/
---

**Welcome to SU2 - GSOC!**  
What is Google Summer of Code?

[Google Summer of Code](https://summerofcode.withgoogle.com/)


## SU2 introduction assignments

To help newcomers start with SU2 and to help GSOC mentors with evaluating the level of students who would like to participate in Google Summer of Code, we have prepared a couple of introduction assignments. These assignments have to be made in the order they are given. These assignments give us an indication of your familiarity with SU2 and the SU2 code. These assignments, together with your active participation in the SU2 community, will be taken into account when deciding on GSOC projects.

## Assignment 1: Compile SU2

- Clone SU2 from github [SU2](https://github.com/su2code/SU2) on your system and compile it [compile instructions](https://su2code.github.io/docs_v7/Build-SU2-Linux-MacOS/) with different options, and run some tutorials [Tutorials](https://su2code.github.io/tutorials/home/). Get a proper understanding of the input and output of SU2.
- Deliverable: None

## Assignment 2: Set up a test case from scratch

- Generate a 2D mesh for an axisymmetric, steady-state, turbulent jet case (for instance with [gmsh](https://gmsh.info/)), setup the configuration file, run the simulation, and extract results.
- Deliverable: Testcase and small report (markdown) describing motivation for set-up, configuration options, convergence history, comparison with experimental values.
Reference paper that could be used for comparison [report](https://www.researchgate.net/publication/254224677_Investigation_of_the_Mixing_Process_in_an_Axisymmetric_Turbulent_Jet_Using_PIV_and_LIF)

## Assignment 3: Python wrapper test case

- Set up a problem in the python wrapper (compile with python support) and run a test case. 
Testcase for the python wrapper: [flatplate](https://github.com/su2code/SU2/blob/master/TestCases/py_wrapper/flatPlate_unsteady_CHT/launch_unsteady_CHT_FlatPlate.py)
- Deliverable: Testcase and small report describing the test case and showing the results.

## Assignment 4: Modification of the python wrapper setup

- Enable a spatially varying wall temperature for a steady-state compressible turbulent flat plate testcase.
- Deliverable: Testcase and small report describing the results.

## Assignment 5: Addition of new volume output:

- Add the local speed of sound as computed by SU2 in the volume output (paraview files) and the screen output. Run the turbulent test case from point 2 with this new volume and screen output enabled.
- Deliverable: explain implementation, show the history output of the new screen output and show some image with the volume output.
