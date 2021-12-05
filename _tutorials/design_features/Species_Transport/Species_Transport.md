---
title: Unconstrained shape design of a two way mixing channel
permalink: /tutorials/Species_Transport/
written_by: TobiKattmann
for_version: 7.2.1
revised_by:
revision_date: 
revised_version: 
solver: INC_RANS
requires: SU2_CFD, FADO
complexity: advanced
follows: Inc_Species_Transport
---

## Disclaimer

This Tutorial builds directly on the case given as Prerequisite on the top of the site [link](tutorials/Inc_Species_Transport/). Therefore details to the problem setup, mesh, etc. are not repeated here. However the process outlined in this tutorial is directly applicable to many other cases using SU2.

Instead of the python tools for finite differences or shape optimization that are part of SU2 directly, the standalone python tool [FADO](https://github.com/su2code/FADO) is used. Please follow the information on the given github repo in order to use FADO.

## Goals

This tutorial is a rather extensive guide covering the following steps, assuming a converging primal case is present:
1. Validation of perfect restarts as a basis for the Discrete Adjoint solver. This is done using a separate bash-script
2. Setting up an FFD-box and writing it to the mesh
3. Manual testing of the mesh deformation
4. Gradient validation using FADO
5. Shape optimization using FADO

Following these steps proved to be especially useful when developing new features as each step is an incremental rise in complexity and is much easier to debug, compared starting right away with an optimization that then fails to provide satisfactory results.

## Resources

You can find the resources for this tutorial in the folder [incompressible_flow/Inc_Species_Transport](https://github.com/su2code/Tutorials/tree/master/incompressible_flow/Inc_Species_Transport) and the respective subfolders.

## 1. Restart Validation

The script [restart_validation.sh](https://github.com/su2code/Tutorials/tree/master/incompressible_flow/Inc_Species_Transport/restart_validation.sh) performs 4 simulations using `species3_venturiPrimitive.cfg` to check whether primal and primal-adjoint restarts work. This script is best used with `HISTORY_OUTPUT= RMS_RES` as then the output comparison is the most straight forward. The SU2 binary is deduced from the environmental variable `SU2_RUN`, so make sure that is set correctly. With the explanation given here and the comments in the script it should be straight forward adaptable to other cases.
1. Primal simulation with n+1 timesteps. This is the ground truth of the expected residual values. Takes Residuals from the `history` file.
2. Primal simulation with n timesteps. We will restart steps 3. and 4. from this simulation.
3. Primal simulation with 1 timestep, restarted from simulation in 2nd step. Takes Residuals from the `history` file.
4. Adjoint simulation with 1 timestep, using the primal restart file from simulation in 2nd step. The primal residuals that are printed in the screen output are taken for comparison.

When using the recommended `HISTORY_OUTPUT= RMS_RES` the output should provide the following: 
```
-5.010542647 -4.537626591 -4.207538398 0.4686163065 -6.594021422 0.4978738082 -5.253262361 -5.467591972
-5.010542647 -4.537626591 -4.207538398 0.4686163065 -6.594021422 0.4978738082 -5.253262361 -5.467591972
-5.010542647 -4.537626591 -4.207538398 0.4686163065 -6.594021422 0.4978738082 -5.253262361 -5.467591972
```
Where in each row the residual of each equation is listed (P, vx, vy, T, k, w, Species_0, Species_0). The primal restart (2nd row) and the adjoint primal restart (3rd row) provide identical results compared to the 'full' primal simulation (1st row). Small deviations in the last digits are not an issue, especially when higher iteration counts are used (here only 10). But if the adjoint restart provides a clearly different result then this should be debugged before attempting a gradient validation or even optimization.

The config option `OUTPUT_PRECISION= 16` can be set to compare more digits if necessary.

Execute the scipt by:
```
$ bash restart_validation.sh
```

## 2. FFD-Box Setup

The setup is fairly simple when following some simple rules. The additional block of code necessary to write the FFD box is given below. Essentially, there are only 2 options (`FFD_DEFINITION` and `FFD_DEGREE`) where user input is necessary. `DV_KIND= FFD_SETTING` and `DV_PARAM= ( 1.0 )` are fixed and not to be changed.

```
% -------------------- FREE-FORM DEFORMATION PARAMETERS -----------------------%
%
% FFD box definition: 3D case (FFD_BoxTag, X1, Y1, Z1, X2, Y2, Z2, X3, Y3, Z3, X4, Y4, Z4,
%                              X5, Y5, Z5, X6, Y6, Z6, X7, Y7, Z7, X8, Y8, Z8)
%                     2D case (FFD_BoxTag, X1, Y1, 0.0, X2, Y2, 0.0, X3, Y3, 0.0, X4, Y4, 0.0,
%                              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
% Start at the lowest leftest corner and turn counter-clockwise
FFD_DEFINITION= (BOX, \
0.065, 0.01, 0.0, \
0.15, 0.01, 0.0 \
0.15, 0.02, 0.0, \
0.065, 0.02, 0.0, \
0.0, 0.0 ,0.0, \
0.0 ,0.0, 0.0, \
0.0, 0.0, 0.0, \
0.0, 0.0, 0.0 )
%
% FFD box degree: 3D case (i_degree, j_degree, k_degree)
%                 2D case (i_degree, j_degree, 0)
FFD_DEGREE= (6, 1, 0)
%
DV_KIND= FFD_SETTING
%
% Marker of the surface in which we are going apply the shape deformation
% NOTE: for deformation the outlet should be a MARKER_SYM to hinder the mesh being ripped apart.
DV_MARKER= ( wall )
%
% Parameters of the shape deformation
% - FFD_SETTING ( 1.0 )
% - FFD_CONTROL_POINT ( FFD_BoxTag, i_Ind, j_Ind, k_Ind, x_Disp, y_Disp, z_Disp )
DV_PARAM= ( 1.0 )
```

`FFD_DEFINITION`: The first input to this option is the FFD-Box name. Here simply `BOX` was chosen. Following are the 4 (or 8 in 3D) corner points of the FFD box. The order of how the points are written is crucial. The FFD-box points are addressed via i-j-k indices and for keeping the minimum leftover sanity it of course is highly desirable to have these i-j-k indices align with the x-y-z cartesian axes. Or, in case the FFD box sides do not coincide with the cartesian axes, you know how the i-j-k indices work.
Now assuming FFD-sides align with cartesian axes. The first point in `FFD_DEFINITION` has to be the corner point with the lowest x,y,z-value. The second point is the point following the x-axes only (i.e. keeping y and z constant). Like that the i-index coincides with the x-axes. The third point is found following the y-axes (keeping x and z constant). The fourth point is the remaining on that z-constant plane. In 3D follow the first point in z-direction and repeat the process on the higher z-plane. In 2D the process can be explained simplified by: Start with the point with smallest x,y-value and turn counter-clockwise.

`FFD_DEGREE`: Determines the number of FFD-Box points per i-j-k-index. The degree plus 1 gives the number of points used. Note: for ease of manual use it is highly recommended to start with a low amount here. Using more once the process is dialed in, is no problem.  


## 3. Mesh deformation test

a

## 4. Gradient Validation

a
## 5. Optimization

a
