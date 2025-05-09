---
title: Constrained shape design of a transonic inviscid wing at a cte. C<sub>L</sub>
permalink: /tutorials/Inviscid_3D_Constrained_ONERAM6/
written_by: economon
for_version: 7.0.0
revised_by: talbring
revision_date: 2020-03-03
revised_version: 7.0.2
solver: Euler
requires: SU2_CFD, Python
complexity: advanced
follows: 
---

![Opt. ONERA Orig](../../tutorials_files/design_features/Inviscid_3D_Constrained_ONERAM6/images/onera_opt_history.png)

## Goals

Upon completing this tutorial, the user will be familiar with performing an optimal shape design of a 3D geometry. The initial geometry chosen for the tutorial is a ONERA M6 wing at transonic speed in inviscid fluid and constant Cl (common setting in aeronautical problems). The following SU2 tools will be showcased in this tutorial:
- **SU2_CFD** - performs the direct flow simulations.
- **SU2_CFD_AD** - performs the adjoint flow simulations.
- **SU2_DOT_AD** - projects the adjoint surface sensitivities into the design space to obtain the gradient.
- **SU2_DEF** - deforms the geometry and mesh with changes in the design variables during the shape optimization process.
- **SU2_GEO** - evaluates the thickness of the specified wing stations and their gradients.
- **shape_optimization.py** - automates the entire shape design process by executing the SU2 tools and optimizer.

## Resources

The resources for this tutorial can be found in the directory [design/Inviscid_3D_Constrained_ONERAM6](https://github.com/su2code/Tutorials/tree/master/design/Inviscid_3D_Constrained_ONERAM6) in the [tutorials repository](https://github.com/su2code/Tutorials/tree/master/). You will need the configuration file ([inv_ONERAM6_adv.cfg](https://github.com/su2code/Tutorials/tree/master/design/Inviscid_3D_Constrained_ONERAM6/inv_ONERAM6_adv.cfg)) and the mesh file ([mesh_ONERAM6_inv_FFD.su2](https://github.com/su2code/Tutorials/tree/master/design/Inviscid_3D_Constrained_ONERAM6/mesh_ONERAM6_inv_FFD.su2)).

Note that the mesh file already contains information about the definition of the Free Form Deformation (FFD) used for the definition of 3D design variables, but we will discuss how this is created below.

## Tutorial

The following tutorial will walk you through the steps required when performing 3D shape design using SU2, including the FFD tools. It is assumed that you have already obtained and compiled SU2_CFD, SU2_DOT, SU2_CFD_AD, SU2_DOT_AD, SU2_GEO and SU2_DEF. The design loop is driven by the shape_optimization.py script, and thus Python along with the NumPy and SciPy Python modules are required for this tutorial. If you have yet to complete these requirements, please see the Download and Installation pages (including the AD part).

### Problem Setup

The goal of this wing design problem is to minimize the coefficient of drag by changing the shape while imposing lift and wing section thickness constraints. As design variables, we will use a free-form deformation approach. In this approach, a lattice of control points making up a bounding box are placed around the geometry, and the movement of these control points smoothly deforms the surface shape of the geometry inside. We begin with a 3D fixed-wing geometry (initially the ONERA M6) at transonic speed in air (inviscid). The flow conditions are the same as for the previous ONERA M6 tutorial.

![Opt. ONERA Grid](../../tutorials_files/design_features/Inviscid_3D_Constrained_ONERAM6/images/onera_grid.png)
Figure (1): View of the initial surface computational mesh.

### Mesh Description

The mesh consists of a far-field boundary divided in three surfaces (XNORMAL_FACES, ZNORMAL_FACES, YNORMAL_FACES), an Euler wall (flow tangency) divided into three surfaces (UPPER_SIDE, LOWER_SIDE, TIP), and a symmetry plane (SYMMETRY_FACE). The baseline mesh is the same as for the previous ONERA M6 tutorial. The surface mesh can be seen in Figure (1).

![Opt. ONERA FFD](../../tutorials_files/design_features/Inviscid_3D_Constrained_ONERAM6/images/onera_ffd.png)
Figure (2): View of the initial FFD box around the ONERA M6 wing, including the control points (spheres).

### Setting a constant Cl mode

In aeronautical application is common to design at a constant Cl instead of at constant Angle of Attack (AoA). In this case, the AoA is introduced as a design variable to achieve a particular Cl value. SU2 can directly use AoA as design variable but, that method requires to solve an adjoint equation for the Cl constraint. The preferred strategy is to run the direct solver in cte. Cl mode and the adjoint solver will compute the appropriate derivative for that mode. The basic setting for running at a constant Cl mode is described below:
```
% -------------------------- CL DRIVER DEFINITION -----------------------------%
%
% Activate fixed lift mode (specify a CL instead of AoA, NO/YES)
FIXED_CL_MODE= YES
%
% Target coefficient of lift for fixed lift mode (0.80 by default)
TARGET_CL= 0.286
%
% Estimation of dCL/dAlpha (0.2 per degree by default)
DCL_DALPHA= 0.1
%
% Maximum number of iterations between AoA updates
UPDATE_AOA_ITER_LIMIT= 150

``` 
In this particular problem we are setting a value for the lift coefficient equal to 0.286. The `FIXED_CL_MODE` works by updating the angle of attack (AoA) during the simulation run such that the resulting CL matches the `TARGET_CL` value. The `UPDATE_AOA_ITER_LIMIT` specifies the maximum number of iterations between two AoA updates. The AoA might update sooner if the solution converges (as defined by the convergence parameters) to the wrong CL. The level of CL convergence can be specified by the `CAUCHY_EPS` value which is defined in the Convergence Parameters. `DCL_DALPHA` is the proportional constant that is used to calculate the change in AoA when it updates (Change in AoA = (TARGET_CL - CURRENT_CL)/DCL_DALPHA). The `ITER_DCL_DALPHA` defines the number of iterations that the run to calculate dCL/dAlpha at the end of the Fixed CL simulation. This calculated value is used by the adjoint to give more accurate gradients with respect to the objective function, when the optimization is run in Fixed CL mode. 


### Setting up a Free-Form Deformation Box
 
The mesh file that is provided for this test case already contains the FFD information. However, if you are interested in repeating this process for your own design cases, it is necessary to calculate the position of the control points and the parametric coordinates. The description below describes how to set up FFD boxes for deformation.

The design variables are defined using the FFD methodology. We will customize a set an options that specifically target FFD box creation:
 
```
% -------------------- FREE-FORM DEFORMATION PARAMETERS -----------------------%
%
% Tolerance of the Free-Form Deformation point inversion
FFD_TOLERANCE= 1E-10
%
% Maximum number of iterations in the Free-Form Deformation point inversion
FFD_ITERATIONS= 500
%
% FFD box definition: 3D case (FFD_BoxTag, X1, Y1, Z1, X2, Y2, Z2, X3, Y3, Z3, X4, Y4, Z4,
%                              X5, Y5, Z5, X6, Y6, Z6, X7, Y7, Z7, X8, Y8, Z8)
%                     2D case (FFD_BoxTag, X1, Y1, 0.0, X2, Y2, 0.0, X3, Y3, 0.0, X4, Y4, 0.0,
%                              0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
FFD_DEFINITION= (WING, -0.0403, 0, -0.04836, 0.8463,0, -0.04836, 1.209, 1.2896, -0.04836, 0.6851, 1.2896, -0.04836, -0.0403, 0, 0.04836, 0.8463, 0, 0.04836, 1.209, 1.2896, 0.04836, 0.6851, 1.2896, 0.04836)
%
% FFD box degree: 3D case (x_degree, y_degree, z_degree)
%                 2D case (x_degree, y_degree, 0)
FFD_DEGREE= (10, 8, 1)
%
% Surface continuity at the intersection with the FFD (1ST_DERIVATIVE, 2ND_DERIVATIVE)
FFD_CONTINUITY= 2ND_DERIVATIVE
```

As the current implementation requires each FFD box to be a quadrilaterally-faced hexahedron (6 faces, 12 edges, 8 vertices), we can simply specify the 8 corner points of the box and the polynomial degree we would like to represent along each coordinate direction (x,y,z) in order to create the complete lattice of control points. It is convenient to think of the FFD box as a small structured mesh block with (i,j,k) indices for the control points, and note that the number of control points in each direction is the specified polynomial degree plus one. 

In the example above, we are creating a box with control point dimensions 11, 9, and 2 in the x-, y-, and z-directions, respectively, for a total of 198 available control points. In the `FFD_DEFINITION` option, we give a name to the box ("WING"), and then list out the x, y, and z coordinates of each corner point. The order is important, and you can use the example above to match the convention. Alternatively, [this tutorial](/tutorials/Species_Transport/) contains more in-depth information on how the numbering should be done. The degree is then specified in the `FFD_DEGREE` option. A view of the box with the control points numbered is in Figure (3). Note that the numbering in the figure is 1-based just for visualization, but within SU2, the control points have 0-based indexing. For example, the (1,1,1) control point in the figure is control point (0,0,0) within SU2. This is critical for specifying the design variables in the config file.

![Opt. ONERA FFD](../../tutorials_files/design_features/Inviscid_3D_Constrained_ONERAM6/images/onera_ffd_points.png)
Figure (3): View of the control point identifying indices, which increase in value along the positive coordinate directions. Note that the numbering here is 1-based just for visualization, but within SU2, the control points have 0-based indexing.

Lastly, the FFD capabilities within SU2 also feature a nifty technique to automatically ensure that you do not obtain any jumps or kinks in your deformed geometry. You can control this by requesting continuity in the 1st or 2nd derivative of the surface with the `FFD_CONTINUITY` option. In short, the code will automatically detect when a face of the FFD box intersects the geometry, and it will hold fixed the control points on that face (`1ST_DERIVATIVE`) or the points on the face as well as one slice of adjacent control points (`2ND_DERIVATIVE`). **Note that these control points will be held fixed during design cycles even if you specify them in your design variable list**.

Now that the FFD box has been defined using the options, follow these steps at a terminal command line to generate a **new** mesh that contains the FFD box:
 1. Move to the directory containing the config file (inv_ONERAM6_adv.cfg) and the mesh file (mesh_ONERAM6_inv_FFD.su2). Make sure that the SU2 tools were compiled, installed, and that their install location was added to your path.
 2. Check that DV_KIND= FFD_SETTING in the configuration file. 
 3. Execute SU2_DEF by entering "SU2_DEF inv_ONERAM6_adv.cfg" at the command line. This can also be executed in parallel (e.g. $mpirun -n 10 SU2_DEF inv_ONERAM6_adv.cfg).
 4. After completing the FFD mapping process, a mesh file named "mesh_out.su2" (by default) is now in the directory. Rename that file to "mesh_ONERAM6_inv_FFD.su2". Note that this new mesh file contains all the details of the FFD method.

With this preprocessing, the position of the control points and the parametric coordinates have been calculated. The preprocessing only needs to be performed once, and afterward, the new (x,y,z) coordinates of the geometry surface due to control point displacements can be quickly evaluated from the mapping. This information is stored in a native format at the bottom of the SU2 mesh file. You will use this new mesh for the design process. If you find that your particular case stalls or throws errors during the creation of the box, the `FFD_TOLERANCE` and `FFD_ITERATIONS` parameters can be adjusted to achieve convergence of the algorithm.

### Evaluating the Geometry

In this particular problem the objective is to introduce a set of geometrical constraints. The first step is to check that SU2 is able to compute the correct geometrical quantities via executing SU2_GEO. The important information for SU2_GEO configuration file is provided below

```
% ----------------------- GEOMETRY EVALUATION PARAMETERS ----------------------%
%
% Marker(s) of the surface where geometrical based function will be evaluated
GEO_MARKER= ( UPPER_SIDE, LOWER_SIDE, TIP )
%
% Description of the geometry to be analyzed (AIRFOIL, WING, FUSELAGE)
GEO_DESCRIPTION= WING
%
% Coordinate of the stations to be analyzed
GEO_LOCATION_STATIONS= (0.0, 0.2, 0.4, 0.6, 0.8)
%
% Geometrical bounds (Y coordinate) for the wing geometry analysis or
% fuselage evaluation (X coordinate)
GEO_BOUNDS= (0, 0.8)
%
% Plot loads and Cp distributions on each airfoil section
GEO_PLOT_STATIONS= YES
%
% Number of section cuts to make when calculating wing geometry
GEO_NUMBER_STATIONS= 25
%
% Geometrical evaluation mode (FUNCTION, GRADIENT)
GEO_MODE= FUNCTION
```

On other words, we need to specify where the wing stations are located to apply the thickness constraints. In this config file, 5 thickness constraints can be applied during design defined in `GEO_LOCATION_STATIONS`. The thicknesses and their gradients are computed using the SU2_GEO module. As you can see, we need to specify the names of the markers that make up the geometry of interest in `GEO_MARKER` the kind of geometry that SU2_GEO is slicing `GEO_DESCRIPTION` and the physical bounds for the wing (Y coordinate). By using `GEO_PLOT_STATIONS` SU2_CFD will plot the Cp at each section and a spanload distribution plot.

With this setting it is now appropriate to execute SU2_GEO by typing "SU2_GEO inv_ONERAM6_adv.cfg" at the command line to obtain a baseline measurement of the wing thickness at the 5 stations. Remember that SU2_GEO can also be executed in parallel (e.g. $mpirun -n 10 SU2_GEO inv_ONERAM6_adv.cfg). The following information came from the SU2_GEO screen output:

```
Wing volume: 0.0260712 m^3. Wing min. thickness: 0.0553114 m. Wing max. thickness: 0.0784087 m.
Wing min. chord: 0.5688 m. Wing max. chord: 0.805999 m. Wing min. LE radius: 78.156 1/m. Wing max. LE radius: 117.586 1/m.
Wing min. ToC: 0.0971893. Wing max. ToC: 0.0974553. Wing delta ToC: 0.0271893. Wing max. twist: 0.016874 deg.
Wing max. curvature: 0.332163 1/m. Wing max. dihedral: 0.362135 deg.

-------------------- Objective function evaluation ----------------------

Station 1. YCoord: 1e-16 m, Area: 0.0443805 m^2, Thickness: 0.0784087 m,
Chord: 0.805999 m, LE radius: 78.156 1/m, ToC: 0.0972814, Twist angle: 0 deg.
Station 2. YCoord: 0.2 m, Area: 0.0380789 m^2, Thickness: 0.0726176 m,
Chord: 0.7467 m, LE radius: 90.7731 1/m, ToC: 0.0972514, Twist angle: 0 deg.
Station 3. YCoord: 0.4 m, Area: 0.0322669 m^2, Thickness: 0.0668227 m,
Chord: 0.6874 m, LE radius: 100.28 1/m, ToC: 0.0972109, Twist angle: 0 deg.
Station 4. YCoord: 0.6 m, Area: 0.0269361 m^2, Thickness: 0.0610663 m,
Chord: 0.626609 m, LE radius: 104.201 1/m, ToC: 0.0974553, Twist angle: 0.016874 deg.
Station 5. YCoord: 0.8 m, Area: 0.0220888 m^2, Thickness: 0.0553114 m,
Chord: 0.5688 m, LE radius: 117.586 1/m, ToC: 0.0972423, Twist angle: 0 deg.
```

Furthermore, SU2_GEO has created two interesting files with geometrical information: `wing_description.dat` and `wing_slices.dat` that can be used to fully understand the wing geometry.


### Defining the Optimization Problem

Several of the key configuration file options are highlighted here. Since we are using the same flow problem from the previous tutorials, we will focus on the new design parameter options:
```
% --------------------- OPTIMAL SHAPE DESIGN DEFINITION -----------------------%
%
% Optimization objective function with scaling factor
% ex= Objective * Scale
OPT_OBJECTIVE= DRAG 
%
% Optimization constraint functions with scaling factors, separated by semicolons
% ex= (Objective = Value ) * Scale, use '>','<','='
OPT_CONSTRAINT= (STATION1_THICKNESS > 0.077) * 0.001; (STATION2_THICKNESS > 0.072) * 0.001; (STATION3_THICKNESS > 0.066) * 0.001; (STATION4_THICKNESS > 0.060) * 0.001; (STATION5_THICKNESS > 0.054) * 0.001
%
% Factor to reduce the norm of the gradient (affects the objective function and gradient in the python scripts)
% In general, a norm of the gradient ~1E-6 is desired.
OPT_GRADIENT_FACTOR= 1E-5
%
% Factor to relax or accelerate the optimizer convergence (affects the line search in SU2_DEF)
% In general, surface deformations of 0.01'' or 0.0001m are desirable
OPT_RELAX_FACTOR= 1E3
%
% Maximum number of iterations
OPT_ITERATIONS= 100
%
% Requested accuracy
OPT_ACCURACY= 1E-10
%
% Upper bound for each design variable
OPT_BOUND_UPPER= 0.3
%
% Lower bound for each design variable
OPT_BOUND_LOWER= -0.3
%
% Optimization design variables, separated by semicolons
% ex= FFD_CONTROL_POINT ( 11, Scale | Mark. List | FFD_BoxTag, i_Ind, j_Ind, k_Ind, x_Mov, y_Mov, z_Mov )
DEFINITION_DV= ( 11, 1.0 | UPPER_SIDE, LOWER_SIDE, TIP | WING, 0, 1, 0, 0.0, 0.0, 1.0 ); ( 11, 1.0 | UPPER_SIDE, LOWER_SIDE, TIP | WING, 1, 1, 0, 0.0, 0.0, 1.0 ); ...
```

Here, we define the objective function for the optimization as drag with thickness constraints along 5 sections of the wing. The `DEFINITION_DV` is the list of design variables, note that this is a simulation/optimization at a cte. Cl and the angle of attack is a design variable. For this problem, we want to minimize the drag by changing the position of the control points of the control box. To do so, we list the set of FFD control points that we would like to use as variables. Each design variable is separated by a semicolon. The first value in the parentheses is the variable type, which is 11 for an FFD control point movement. The second value is the scale of the variable (typically left as 1.0). The name between the vertical bars is the marker tag(s) where the variable deformations will be applied. The final seven values in the parentheses are the particular information about the deformation: identification of the FFD tag, the i, j, and k index of the control point, and the allowed x, y, and z movement direction of the control point. Note that other types of design variables have their own specific input format. For this example, we have a long list of design variables that are not all listed above. You can quickly generate a list of FFD variables in the necessary format using the **set_ffd_design_var.py** script that is shipped with the other Python utilities with the source code.
```
$ python set_ffd_design_var.py -i 10 -j 8 -k 1 -b WING -m 'UPPER_SIDE, LOWER_SIDE, TIP'
```

The selection of `OPT_GRADIENT_FACTOR` and `OPT_RELAX_FACTOR` has a particular impact on the optimization. The `OPT_GRADIENT_FACTOR` is used to obtain a gradient norm (GNORM column in the shape_optimization.py screen output) of the order of 1E-6. On the other hand, `OPT_RELAX_FACTOR` is used to aid the optimizer in taking a physically appropriate first step (i.e., not too small or too large), the easiest way to check the initial step is by looking at `Max Diff:` value in `DSN_002/DEFORM/log_Deform.out`, in fact that value is the maximum difference between the baseline geometry and the deformed geometry in the first step of the optimization.

In this particular optimization problem it is also important to adjust the scale of the `OPT_CONSTRAINT` this scale factor is an effective method to control how much the violated constraint is going to change the objective function gradient (push factor). The selection and adjustment of these three parameters is important to fully exploit the possibilities of the Python gradient based optimizers.


### Running SU2

A discrete adjoint methodology for obtaining surface sensitivities is implemented for several equation sets within SU2. After solving the direct flow problem, the adjoint problem is also solved. The adjoint method offers an efficient approach for calculating the gradient of an objective function with respect to a large set of design variables. This leads directly to a gradient-based optimization framework. 

With each design iteration, the direct and adjoint solutions are used to compute the objective function and gradient, and the optimizer drives the shape changes with this information in order to minimize the objective. Each flow constraint requires the solution of an additional adjoint problem to compute its gradient (lift in this case). Three other SU2 tools are used in the design process here: SU2_DOT to compute the gradient from the adjoint surface sensitivities and input design space, SU2_GEO to compute wing section thicknesses and their gradients, and SU2_DEF to deform the computational mesh between design cycles. To run this case, follow these steps at a terminal command line:
 1. Execute the shape optimization script by entering 
    
    ```
    $ shape_optimization.py -g DISCRETE_ADJOINT -f inv_ONERAM6_adv.cfg
    ```
    
    at the command line, add `-n 12` in case you want to run the optimization in parallel (12 cores). Again, note that Python,  NumPy, and SciPy are all required to run the script.

 2. The python script will drive the optimization process by executing flow solutions, adjoint solutions, gradient projection, geometry evaluations, and mesh deformation in order to drive the design toward an optimum. The optimization process will cease when certain tolerances set within the SciPy optimizer are met. Note that is is possible to start the optimization from a pre-converged solution (direct and adjoint problem), in that case the following change should be done in the configuration file: `RESTART_SOL= YES`.
 3. Solution files containing the flow and surface data will be written for each flow solution and adjoint solution and can be found in the DESIGNS directory that is created. The file named history_project.plt (or history_project.csv for ParaView) will contain the functional values of interest resulting from each evaluation during the optimization. The major iterations and function evaluations for the SLSQP optimizer will be written to the console during execution.

### Results 

The following are representative results for this transonic shape design example with the ONERA M6 geometry as a baseline. We successfully reduce the drag while satisfying the constraints.

![Opt. ONERA Pressure](../../tutorials_files/design_features/Inviscid_3D_Constrained_ONERAM6/images/onera_pressure_original.png)
Figure (4): Pressure contours showing the typical "lambda" shock on the upper surface of the initial geometry.

![Opt. ONERA Pressure](../../tutorials_files/design_features/Inviscid_3D_Constrained_ONERAM6/images/onera_pressure_final.png)
Figure (5): Pressure contours on the surface of the final wing design (reduced shocks).

![Opt. ONERA Pressure](../../tutorials_files/design_features/Inviscid_3D_Constrained_ONERAM6/images/onera_ffd_final.png)
Figure (6): View of the initial (black) and final (blue) FFD control point positions.

![Opt. ONERA History](../../tutorials_files/design_features/Inviscid_3D_Constrained_ONERAM6/images/onera_opt_history.png)
Figure (7): Optimization history. The drag is reduced and the lift constraint is easily met.

