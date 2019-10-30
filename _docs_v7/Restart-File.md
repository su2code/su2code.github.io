---
title: Restart File
permalink: /docs_v7/Restart-File/
---

The SU2 binary restart format has the extension `.dat`, but it is also possible to write out restart files in a simple ASCII file format with extension `.csv`. Have a look at the [Output section](/docs_v7/Custom-Output/) to learn how to change output file formats.

The restart files are used to restart the code from a previous solution and also to run the adjoint simulations, which require a flow solution as input. In order to run an adjoint simulation, the user must first change the name of the `restart_flow.dat`  file (or `restart_flow.csv` if ASCII format) to `solution_flow.dat` (or `solution_flow.csv`) in the execution directory (these default file names can be adjusted in the config file). It is important to note that the adjoint solver will create a different adjoint restart file for each objective function, e.g. `restart_adj_cd.dat`.

To restart a simulation the `RESTART_SOL` flag should be set to `YES` in the configuration file. If performing an unsteady restart the `RESTART_ITER` needs to be set to the iteration number which you want to restart from. For instance if we want to restart at iteration 100 and run the unsteady solver with 2nd-order dual time stepping method, we will need to specify `RESTART_ITER = 100` and have the restart files `solution_flow_00098.dat` and `solution_flow_00099.dat`.
 
