---
title: Restart File
permalink: /docs_v7/Restart-File/
---


## Saving files for restarts or adjoint runs

The restart files are used to restart the code from a previous solution and also to run the adjoint simulations, which require a flow solution as input. To save a restart file, the user needs to add the option `RESTART` to the keyword `OUTPUT_FILES` in the configuration file:

`OUTPUT_FILES= RESTART`

The SU2 binary restart format has the extension `.dat`, but it is also possible to write out restart files in a simple ASCII file format with extension `.csv`. Have a look at the [Output section](/docs_v7/Custom-Output/) to learn how to change output file formats.

A restart file with the name given by the keyword `RESTART_FILENAME` is then saved at the end of the simulation, or after every number of iterations given by the keyword `OUTPUT_WRT_FREQ`. For instance,

`RESTART_FILENAME= restart_flow` \
`OUTPUT_WRT_FREQ= 100`

will write the file restart_flow.dat every 100 iterations when the total number of iterations is larger than 100, or only once at the end of the simulation when the total number of iterations is smaller than 100. Note that the file extension (the suffix) is automatic and can be left out.
If you would like to keep copies of previously saved restart files, this is possible by setting

`WRT_RESTART_OVERWRITE= NO`

Additional to the regular restart file, a restart file with the current iteration appended to the filename will then be written every `OUTPUT_WRT_FREQ` iterations. Note that this option is available only for steady simulations. In unsteady simulations, the number of timesteps is appended to the filename automatically. 

## Starting a simulation from a saved solution

When restarting the primal or starting an adjoint, the filename given by the keyword `SOLUTION_FILENAME` will be used. In order to restart the primal or start the run of an adjoint simulation, the user must therefore first change the name of the saved file, e.g. `restart_flow.dat`  (or `restart_flow.csv` if ASCII format) to the filename `solution_flow.dat` (or `solution_flow.csv`) in the execution directory. It is important to note that the adjoint solver will create a different adjoint restart file for each objective function, e.g. `restart_adj_cd.dat`.
To restart a simulation the `RESTART_SOL` flag should be set to `YES` in the configuration file. 

`RESTART_SOL= YES` \
`SOLUTION_FILENAME= solution_flow`

If performing an unsteady restart the `RESTART_ITER` needs to be set to the iteration number which you want to restart from. For instance if we want to restart at iteration 100 and run the unsteady solver with 2nd-order dual time stepping method, we will need to specify `RESTART_ITER = 100` and have the restart files `solution_flow_00098.dat` and `solution_flow_00099.dat`.
 
 
| Option value | Default value | Description | Data type |
|---|---|---|---|
| `OUTPUT_FILES` | RESTART,PARAVIEW,SURFACE_PARAVIEW | files types to write | list of keywords |
| `RESTART_FILENAME` | restart.dat | filename under which the restart file will be saved | string |
| `OUTPUT_WRT_FREQ` | 10,250,42 | the list of frequencies with which the output files will be saved | list of integers |
| `WRT_RESTART_OVERWRITE` | YES | overwrite the restart file or (additionally) append the iteration number to the filename | boolean |
| `RESTART_SOL` | solution | restart from file or from initial conditions | boolean |
| `SOLUTION_FILENAME` | solution.dat | filename that will be used to restart the primal or start the adjoint computation | string |
| `RESTART_ITER` | 1 | iteration number that an unsteady simulation will restart from | integer |
