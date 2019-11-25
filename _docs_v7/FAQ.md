---
title: FAQ
permalink: /docs_v7/FAQ/
---

# Frequently Asked Questions
### I have a question that isn't answered here. Where can I get more help?
If the answer to your question is not here, try the [forum](http://cfd-online.com/Forums/su2/).

### I am new to CFD and I don't know where to start. Can you help me?
The best place to start for a new user after installing the code is the [Quick Start](/docs_v7/Quick-Start/) tutorial. 

### Where is the documentation?
The most easy-to-use documentation is here on GitHub, and you just found it! Users are especially encouraged to go through the docs in the Installation and Users Guide sections for all of the necesary details for running your first calculations.

For more detail on what configuration options are available and their syntax, see the file config_template.cfg in the SU2 root directory: https://github.com/su2code/SU2/blob/master/config_template.cfg


### My simulation diverges. What should I do?
Adjust the configuration file options, or improve mesh quality. Refer to the forum, tutorials, and TestCases for more specific examples (many of the config files there can be used as initial templates for your own cases. The most common option to change is to lower the CFL number to improve stability.


### When I run in parallel, the code prints multiples of the same line, for example:
```
> Iter    Time(s)     Res[Rho]     Res[RhoE]   CLift(Total)   CDrag(Total)

> Iter    Time(s)     Res[Rho]     Res[RhoE]   CLift(Total)   CDrag(Total)

> Iter    Time(s)     Res[Rho]     Res[RhoE]   CLift(Total)   CDrag(Total)

> 0   0.190073    -3.585391     -2.989014       0.114015       0.100685

> 0   0.190073    -3.585391     -2.989014       0.114015       0.100685

> 0   0.190073    -3.585391     -2.989014       0.114015       0.100685
```

The code has not been compiled properly with parallel support. Refer to the installation instructions. 


### What is the format of the residuals that are written to the console, and what do they mean?
Residuals are printed in log10 format, and indicate how close the solution is to satisfying the governing equations. Convergence is usually determined by a desired reduction in the residual - a reduction of "6" would mean the residual is 10^-6 of its initial value. If possible, it is recommended to converge your simulations until the residuals reach machine precision.


### Help! I just updated the code from a version that previously worked for me, and now there is an error. What do I do?
* Easy fix: read the error output. If it says that there is an unrecognized config file option, remove the associated line from the config file. Note that the config options may change between code releases to allow more control, use new features, or simplify the config file. 
* Medium fix: revert to the release you used to use. Make sure that the release/version number for the TestCases repository is the same, and remember to recompile. If a case which previously converged now diverges, or otherwise doesn't do what you expect, try changing the options like CFL number, artificial dissipation coefficients, etc. Read the initial output of the code to make sure that what you have set in the config file is being applied - some config file options only apply to certain solvers.
* Advanced fix: after exhausting the easy and medium options, or if a clear bug like a segfault occurs, [post an Issue on the GitHub repository](https://github.com/su2code/SU2/issues). 


### I'm getting a warning about "Nonphysical points". What does that mean, and how do I fix it? 
A nonphysical point means the flow solution has encountered a negative density, pressure, or temperature. If the warnings stop after a few iterations, it's ok. If the warnings continue, the solution is likely diverging and you may need to adjust the config file options. 


### Where can I get the suite of test cases for SU2?
The test case config files are found in the SU2 code repo, while the meshes are located in a separate repository under the SU2 organization. We recommend copying the meshes into place within the SU2 source directory where the config files reside (under version control). See [this page](/docs_v7/Test-Cases/) for directions.
