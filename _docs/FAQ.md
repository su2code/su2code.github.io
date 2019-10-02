---
title: FAQ
permalink: /docs/FAQ/
---

# Frequently Asked Questions
### I have a question that isn't answered here. Where can I get more help?
If the answer to your question is not here, try the [forum](http://cfd-online.com/Forums/su2/).

### I am new to CFD and I don't know where to start. Can you help me?
The best place to start for a new user after installing the code is the [Quick Start](/docs/Quick-Start/) tutorial. 

### Where is the documentation?
The most easy-to-use documentation is the github wiki, and you just found it! Try starting with the [[Quick Start]].
For more detail on what configuration options are available and their syntax, see the file config_template.cfg in the SU2 root directory: https://github.com/su2code/SU2/blob/master/config_template.cfg
Further documentation is available in the su2code/Documentation repository.

### My simulation diverges. What should I do?
Adjust the configuration file options, or improve mesh quality. Refer to the forum, tutorials, and TestCases for more specific examples. The most common option to change is to lower the CFL number, usually to something around 1.0. 

### When I run in parallel, the code prints multiples of the same line, for example:
```
> Iter    Time(s)     Res[Rho]     Res[RhoE]   CLift(Total)   CDrag(Total)

> Iter    Time(s)     Res[Rho]     Res[RhoE]   CLift(Total)   CDrag(Total)

> Iter    Time(s)     Res[Rho]     Res[RhoE]   CLift(Total)   CDrag(Total)

> 0   0.190073    -3.585391     -2.989014       0.114015       0.100685

> 0   0.190073    -3.585391     -2.989014       0.114015       0.100685

> 0   0.190073    -3.585391     -2.989014       0.114015       0.100685
```

The code has not been compiled with parallel support. Refer to the installation instructions. 

### Where are my solution files?
When running in serial (or a parallel version on one MPI rank), SU2_CFD will write solution files for Tecplot or ParaView upon exit. In parallel, only restart files will be written by SU2_CFD in order to save I/O overhead during the calculation. Solution files can then be generated at the end of the calculation by using the SU2_SOL module along with the restart file. Users can also use the parallel_computation.py script to automate this process.


### What are Conservative_1, Conservative_2, etc? What about Residual[0], Residual[1], etc? What about Primitive[0], etc? Why don't you use the flow variables I'm used to?
* The conservative variables and the residuals refer to the quantities conserved in the flow equations: density, momentum, and energy. [\rho, \rho u, \rho v, \rho w, \rho e]. 
* The primitive variables refer to density, velocity, pressure, etc.
* Residuals are printed in log10 format, and indicate how close the solution is to satisfying the governing equations. Convergence is usually determined by a desired reduction in the residual - a reduction of "6" would mean the residual is 10^-6 of its initial value. 
* They are referred to as "conservative" and "primitive" to allow different solvers to use the same structure without confusion - rather than vary the name, the length and the values are varied. For example, in the RANS solver additional turbulent terms are needed, and in the incompressible solver fewer primitive variables are required. 


### Help! I just updated the code from a version that previously worked for me, and now there is an error. What do I do?
* Easy fix: read the error output. If it says that there is an unrecognized config file option, remove the associated line from the config file. Note that the config options may change between code releases to allow more control, use new features, or simplify the config file. 
* Medium fix: revert to the release you used to use. Make sure that the release/version number for the TestCases repository is the same, and remember to recompile. If a case which previously converged now diverges, or otherwise doesn't do what you expect, try changing the options like CFL number, artificial dissipation coefficients, etc. Read the initial output of the code to make sure that what you have set in the config file is being applied - some config file options only apply to certain solvers.
* Advanced fix: after exhausting the easy and medium options, or if a clear bug like a segfault occurs, post to the forum at cfd-online.com/Forums/su2/. 


### I'm getting a warning about "Nonphysical points". What does that mean, and how do I fix it? 
A nonphysical point means the solution has encountered a negative density. If the warnings stop after a few iterations it's ok. If the warnings continue, the solution is likely diverging and you may need to adjust the config file options. 

### Where can I get the suite of test cases for SU2?
The test case config files are found in the SU2 code repo, while the meshes are located in a separate repository under the SU2 organization. We recommend copying the meshes into place within the SU2 source directory where the config files reside (under version control). See [this page](/docs/Test-Cases/) for directions.
