---
title: Software Components
permalink: /docs_v7/Software-Components/
---


---

- [C++ Software Modules](#c-software-modules)
  - [Algorithmic Differentiation Support and Discrete Adjoint](#algorithmic-differentiation-support-and-discrete-adjoint)
- [Python Scripts](#python-scripts)

---

The SU2 software suite is composed of a set of C++ based software modules that perform a wide range of CFD analysis and PDE-constrained optimization tasks. An overall description of each module is included below to give perspective on the suite's capabilities, while more details can be found in the Developer's Guide. Some modules can be executed individually, most notably SU2_CFD to perform high-fidelity analysis, but the real power of the suite lies in the coupling of the modules to perform complex activities, including design optimization and adaptive grid refinement, among others.

A key feature of the C++ modules is that each has been designed to separate functionality as much as possible and to leverage the advantages of the class-inheritance structure of the programming language. This makes SU2 an ideal platform for prototyping new numerical methods, discretization schemes, governing equation sets, mesh perturbation algorithms, adaptive mesh refinement schemes, parallelization schemes, etc. You simply need to define a new subclass and get down to business. This philosophy makes SU2 quickly extensible to a wide variety of PDE analyses suited to the needs of the user, and work is ongoing to incorporate additional features for future SU2 releases.
The key C++ and Python tools in the SU2 software suite are briefly described below for the current release, but note that modules may be added and removed with future development.

## C++ Software Modules

- **SU2_CFD (Computational Fluid Dynamics Code)**: Solves direct, adjoint (conitnuous?), and linearized problems for the Euler, Navier-Stokes, and Reynolds-Averaged Navier-Stokes (RANS) equation sets, among many others. SU2_CFD can be run serially or in parallel using MPI. It uses a Finite Volume Method (FVM), and an edge-based structure. A Discontinuous-Galerkin Finite Element Method solver is currently being completed and will be available to the public in an upcoming release.  Explicit and implicit time integration methods are available with centered or upwinding spatial integration schemes. The software also has several advanced features to improve robustness and convergence, including residual smoothing, preconditioners, and agglomeration multigrid.
- **SU2_DOT (Gradient Projection Code)**: Computes the partial derivative of a functional with respect to variations in the aerodynamic surface. SU2_DOT uses the surface sensitivity, the flow solution, and the definition of the geometrical variable to evaluate the derivative of a particular functional (e.g. drag, lift, etc.). This is essentially a large dot product operation between the adjoint sensitivities and geometric sensitivities for the particular design variable parameterization.
- **SU2_DEF (Mesh Deformation Code)**: Computes the geometrical deformation of an aerodynamic surface and the surrounding volumetric grid. Once the type of deformation is defined, SU2_DEF performs the grid deformation by solving the linear elasticity equations on the volume grid. Three-dimensional geometry parameterization is defined using Free Form Deformation, while two-dimensional problems can be defined by both Free From Deformation or bump functions, such as Hicks-Henne.
<!--- **SU2_MSH (Mesh Adaptation Code)**: Performs grid adaptation using various techniques based on an analysis of a converged flow solution, adjoint solution, and linearized problem to strategically refine the mesh about key flow features. This module also contains a preprocessor that creates the appropriate structures for periodic boundary conditions.-->
- **SU2_SOL (Solution Export Code)**: Generates the volumetric and surface solution files from SU2 restart files from SU2 restart files (although SU2_CFD will output as many formats as requested in the config file). HOW TO USE IT??
- **SU2_GEO (Geometry Definition Code)**: Geometry preprocessing and definition code. In particular, this module performs the calculation of geometric constraints for shape optimization. 

While they are not C++ modules, two other similar directories included in the source distribution should be mentioned. First, the **SU2_IDE** (Integrated Development Environment) directory contains files associated with various IDEs to aid developers (Eclipse, VisualStudio, Wing, Xcode). Second, the **SU2_PY** directory contains all of the files making up the Python framework, and some of these will be highlighted in a section below.

### Algorithmic Differentiation Support and Discrete Adjoint

SU2 includes integrated support for Algorithmic Differentiation (AD) based on Operator Overloading to compute arbitrary derivatives. One application of this feature is the discrete adjoint solver that is implemented in SU2. In contrast to the continuous adjoint method, special versions of the modules SU2_CFD and SU2_DOT are required to use this solver.

- **SU2_CFD_AD**: Solves the discrete adjoint equations using a consistent linearization of the flow solver with the help of AD. Although it has additionally the same features as SU2_CFD, using it for other solvers will result in a slight slow-down due to the AD overhead.
- **SU2_CFD_DIRECTDIFF**: Computes the gradients of an objective function by forward mode of AD. It has the same features as SU2_CFD, but using it for direct problems will result in a slow-down due to the AD overhead.
- **SU2_DOT_AD**: The discrete adjoint formulation does not include the influence of the mesh deformation, therefore this module will compute the required partial derivative of the functional with respect to variations in the computational mesh. Instead of SU2_DOT, SU2_DOT_AD uses the volume sensitivities to evaluate the derivative. Finally, the resulting sensitivities on the aerodynamic surface are projected on to the particular design parameterization.

## Python Scripts

The various software modules of SU2 can be coupled together to perform complex analysis and design tasks using supplied Python scripts. A brief description of the scripts included in the current release of the software is provided below.

- **High-fidelity analysis scripts**. These scripts have been designed to enhance the flexibility of the SU2 framework. More specifically, they simplify the execution of parallel tasks, grid adaptation, or interfacing with other software.
 - **parallel_computation.py**: Handles the setup and execution of parallel CFD jobs on multi-core or cluster computing architectures. The script executes SU2_CFD in parallel and after the computation is completed runs SU2_SOL to provide a solution ready to be opened by a post-processing software of your choosing.
 - **mesh_deformation.py**: Handles the setup and execution of parallel mesh deformation jobs on multi-core or cluster computing architectures. The script executes SU2_DEF in parallel.
- **Optimal shape design scripts**. These scripts have been designed to automate the optimal shape design process that includes functional and gradient computation, mesh deformation, and an optimization algorithm.
 - **continuous_adjoint.py**: Automatically computes the sensitivities of a specified functional with respect to design parameter perturbations (specified in the SU2_CFD configuration file) using the continuous adjoint method. The SU2_CFD and SU2_DOT modules are called to perform the analysis.
 - **discrete_adjoint.py**: Automatically computes the sensitivities of a specified functional with respect to design parameter perturbations (specified in the SU2_CFD configuration file) using the discrete adjoint method. The SU2_CFD_AD and SU2_DOT_AD modules are called to perform the analysis.
 - **finite_differences.py**: Automatically computes the sensitivities of a specified functional with respect to design parameter perturbations using a finite difference method. As with the continuous_adjoint.py script, design variable information is read from the configuration file and SU2_CFD is called repeatedly to calculate the appropriate gradient elements.
 - **shape_optimization.py**: Orchestrates all SU2 modules to perform shape optimization. The choice of objective function, design variables and additional module settings specifying the optimization problem are controlled through options in the configuration file.
