---
title: DG discretization of Compressible Navier-Stokes
permalink: /vandv/DG_UnitQuad/
---

The level of automation is significantly less than for the Finite Volume solver for this test case. The reason is that DG solver requires more monitoring to check the convergence. Below the steps are described how to run this test case.

Step 1: Create the grid composed out of quadrilateral elements of the required polynomial degree using create_grid_quad.py.

Step 2: Edit the .cfg file. Sample .cfg files are provided for polynomial degrees p = 1 to 5, which contain the typical parameters for this case.

Step 3: Run the case to convergence using SU2_CFD on an arbitrary number of ranks.

Step 4: Save the screen output to the file SU2_DG_n#N_p#P.out, where #N is the number of elements in one direction and #P is the polynomial degree. E.g. SU2_DG_n16_p4.out is the output for the grid, which contains 16 elements in x- and y-direction in combination with polynomial degree 4.

Step 5: Possible edit and run dg_accuracy.py, which carries out the postprocessing. Figures for global error vs relative grid size and observed order of accuracy vs relative grid size are created.
