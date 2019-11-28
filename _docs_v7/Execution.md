---
title: Execution
permalink: /docs_v7/Execution/
---

Once downloaded and installed, and now that you know the basics for setting up your problems, SU2 will be ready to run simulations and design problems. Using simple command line syntax, users can execute the individual C++ programs while specifying the problem parameters in the all-purpose configuration file. For users seeking to utilize the more advanced features of the suite (such as shape optimization or adaptive mesh refinement), Python scripts that automate more complex tasks are available. Appropriate syntax and information for running the C++ modules and python scripts can be found below.

---


- [C++ Modules](#c-modules)
- [Python Scripts](#python-scripts)
  - [Parallel Computation Script (parallel_computation.py)](#parallel-computation-script-parallelcomputationpy)
  - [Continuous Adjoint Gradient Calculation (continuous_adjoint.py)](#continuous-adjoint-gradient-calculation-continuousadjointpy)
  - [Discrete Adjoint Gradient Calculation (discrete_adjoint.py)](#discrete-adjoint-gradient-calculation-discreteadjointpy)
  - [Finite Difference Gradient Calculation (finite_differences.py)](#finite-difference-gradient-calculation-finitedifferencespy)
  - [Shape Optimization Script (shape_optimization.py)](#shape-optimization-script-shapeoptimizationpy)
  
---

## C++ Modules

As described in the [Software Components](/docs_v7/Software-Components/) page, there are a number of C++ modules that are the core of the SU2 suite. After compilation, each can be executed at the command line using a Unix-based terminal (or appropriate emulator, such as Cygwin). The executables for these modules can be found in the `$SU2_HOME/<MODULE_NAME>/bin` directories and in the `$SU2_HOME/SU2_PY` directory.  The configuration file specifies the problem and solver parameters for all SU2 modules and must be included at runtime.

The syntax for running each C++ module individually in serial is:
```
$ SU2_MODULE your_config_file.cfg
```
where `SU2_MODULE` can be any of the C++ modules on the [Software Components](/docs_v7/Software-Components/) and `your_config_file.cfg` is the name of the configuration file that you have prepared for the problem. An example of a call to SU2_CFD with a configuration file "default.cfg" is included below:
```
$ ./SU2_CFD default.cfg
```
where the executable, SU2_CFD, and the [Configuration File](/docs_v7/Configuration-File/), default.cfg, are located in the current working directory.  Please see the [Build from Source](/docs_v7/Build-SU2-Linux-MacOS/) page for how you can set up environment variables to run the modules from any directory. Additionally, SU2 is a fully-parallel suite, and assuming that you have compiled with MPI support, each of the modules can be executed in parallel. For example, to run the CFD solver on 8 cores, you might enter:
```
$ mpirun -n 8 SU2_CFD default.cfg
```
Note that, depending on your flavor of MPI, you may need to use a different launcher, such as *mpiexec*. Please see the documentation for your particular MPI implementation.

## Python Scripts

The distribution of SU2 includes several Python scripts that coordinate the use of the C++ modules to perform more advanced analyses and simulations. A working installation of Python is highly recommended, as a number of tasks can be easily automated using provided scripts (e.g., computing a drag polar). These Python scripts can be found in the `$SU2_HOME/SU2_PY`.

All of the scripts can be executed by calling python and passing the appropriate SU2 python script and options at runtime. The syntax is as follows:
```
$ python script_name.py [options]
```
where *script_name.py* is the name of the script to be run, and [options] is a list of options available to each script file.  A brief description of the most commonly used scripts, their execution syntax, and runtime options are included below. Users are encouraged to look at the source code of the python scripts. As with many Python programs, the code is easily readable and gives the specifics of the implementation. They can also be used as templates for writing your own scripts for automating SU2 tasks.

### Parallel Computation Script (parallel_computation.py)

The parallel computation script, parallel_computation.py, coordinates the steps necessary to run SU2_CFD in parallel and produce solution output files. The script calls SU2_CFD in parallel (using MPI) with the indicated number of ranks. At the conclusion of the simulation, the parallel_computation.py script generates the solution files from the restart file written during execution by calling the SU2_SOL module. The SU2_SOL module can be executed at any time (in serial or parallel) to generate solution files in a specified format from a restart file and corresponding mesh.

Usage: `$ python parallel_computation.py [options]`

Options:
* `-h, --help` show help message and exit
* `-f FILE, --file=FILE` read config from FILE
* `-n PARTITIONS, --partitions=PARTITIONS` number of PARTITIONS
* `-c COMPUTE, --compute=COMPUTE COMPUTE` direct and adjoint problem

### Continuous Adjoint Gradient Calculation (continuous_adjoint.py)

The continuous adjoint calculation script, continuous_adjoint.py, automates the procedure for calculating sensitivities using a continuous adjoint method. The script calls SU2_CFD to first run a direct analysis to obtain a converged solution, then calls SU2_CFD again to run an adjoint analysis on the converged flow solution to obtain surface sensitivities. The SU2_DOT module is then called to project design variable perturbations onto the surface sensitivities calculated in the adjoint solution to arrive at the gradient of the objective function with respect to the specified design variables.

Usage: `$ python continuous_adjoint.py [options]`

Options:
* `-h, --help` show help message and exit
* `-f FILE, --file=FILE` read config from FILE
* `-n PARTITIONS, --partitions=PARTITIONS` number of PARTITIONS
* `-c COMPUTE, --compute=COMPUTE COMPUTE` direct and adjoint problem
* `-s STEP, --step=STEP DOT` finite difference STEP

### Discrete Adjoint Gradient Calculation (discrete_adjoint.py)

Similar to the continuous adjoint script, the discrete adjoint script calls SU2_CFD to generate a flow solution and then calls SU2_CFD_AD to run an adjoint computation based on the objective function specified in the config file. Finally, SU2_DOT_AD is called to map the surface sensitivities onto the design variables specified desig variables.

Usage: `$ python discrete_adjoint.py [options]`

Options:
* `-h, --help` show help message and exit
* `-f FILE, --file=FILE` read config from FILE
* `-n PARTITIONS, --partitions=PARTITIONS` number of PARTITIONS
* `-c COMPUTE, --compute=COMPUTE COMPUTE` direct and adjoint problem

### Finite Difference Gradient Calculation (finite_differences.py)

The finite difference calculation script is used to calculate the gradient of an objective function with respect to specified design variables using a finite difference method. This script calls SU2_CFD repeatedly, perturbing the input design variables and mesh using SU2_DEF, stores the sensitivity values, and outputs the gradient upon exit.

Usage: `$ python finite_differences.py [options]`

Options:
* `-h, --help` show help message and exit
* `-f FILE, --file=FILE` read config from FILE
* `-n PARTITIONS, --partitions=PARTITIONS` number of PARTITIONS
* `-s STEP, --step=STEP` finite difference STEP
* `-q QUIET, --quiet=QUIET` if True, output QUIET to log files 

### Shape Optimization Script (shape_optimization.py)

The shape optimization script coordinates and synchronizes the steps necessary to run a shape optimization problem using the design variables and objective function specified in the configuration file. The optimization is handled using SciPy's SLSQP optimization algorithm by default. Objective functions (drag, lift, etc.) are determined by running a direct flow solution in SU2_CFD, and gradients are obtained using the adjoint solution by default (other options can be selected). For each major iteration in the design process, the mesh is deformed using SU2_DEF, and the sequence is repeated until a local optimum is reached.

Usage: `$ python shape_optimization.py [options]`

Options:
* `-h, --help` show help message and exit
* `-f FILE, --file=FILE` read config from FILE
* `-r NAME, --name=NAME` try to restart from project file NAME
* `-n PARTITIONS, --partitions=PARTITIONS` number of PARTITIONS
* `-g GRADIENT, --gradient=GRADIENT` Method for computing the GRADIENT (ADJOINT, DISCRETE_ADJOINT, FINDIFF, NONE)
* `-q QUIET, --quiet=QUIET` True/False Quiet all SU2 output (optimizer output only)
