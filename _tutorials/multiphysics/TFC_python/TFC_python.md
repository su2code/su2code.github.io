---
title: User Defined combustion model with Python
permalink: /tutorials/multiphysics/
written_by: Nijso Beishuizen 
for_version: 8.3.0
revised_by:  
revision_date:
revised_version:
solver: INC_NAVIER_STOKES
requires: SU2_CFD, python
complexity: advanced
---

![TFC_temp](../../../tutorials_files/multiphysics/TFC_python/images/TFC_temp.png)
Figure (1): high-pressure turbulent premixed flame of the Paul-Scherrer Institute (PSI), Switzerland

## Goals

In this tutorial we will simulate a high pressure turbulent premixed flame using the Turbulent Flamespeed Closure (TFC) model. This is a simple turbulent combustion model that can be implemented with a User Defined Source (UDS) in python.
In this tutorial we will touch upon the following aspects:
- Compile and run SU2 from within python.
- Create a User Defined Source
- Create User Defined boundary conditions
- Create User Defined initial conditions


## Resources

The resources for this tutorial can be found in the [TFC_python](https://github.com/su2code/Tutorials/tree/master/multiphysics/TFC_python) directory in the [tutorial repository](https://github.com/su2code/Tutorials). You will need the configuration file ([psi.cfg](https://github.com/su2code/Tutorials/tree/master/multiphysics/TFC_python/psi.cfg)) and the mesh file ([psi.su2](https://github.com/su2code/Tutorials/tree/master/multiphysics/TFC_python/psi.su2)). Additionally, the Gmsh geometry is also provided so you can recreate the mesh yourself: [psi.geo](https://github.com/su2code/Tutorials/tree/master/multiphysics/TFC_python/psi.geo).


### Background

Turbulent combustion can be very expensive to simulate with high accuracy. The Turbulent Flamespeed Closure model, first pioneered by Zimont, is a very simple model for turbulent premixed combustion that aims to give accurate predictions for temperature in turbulent premixed combustion. In the TFC model, a transport equation for the progress variable is solved:

$$ \frac{\partial c}{\dt} + \nabla \cdot (\rho u c) = \nabla\cdot (\frac{\mu_t}{Sc_t}\nabla c) + \rho S_c$$

and the combustion source term is given by 
$$ S_c = \rho_u U_t \nabla c$$,
with $\rho_u$ the unburnt density of the gas an $U_t$ the turbulent flamespeed.

### Problem Setup

First, SU2 needs to be compiled with python support. add the option *-Ddenable-pywrapper=true* to the meson setup. In this case, we compile including mpi support:

```bash	
$ ./meson.py setup build --optimization=2 -Denable-mixedprec=true -Ddebug=false -Denable-pywrapper=true --warnlevel=3 -Denable-autodiff=false -Denable-directdiff=false -Dwith-mpi=enabled -Dcustom-mpi=true --prefix=/home/user/Codes/su2_github_develop/su2/
```

Note that the python wrapper (or your python setup) might need additional python packages that you need to install. Especially the python package mpi4py is important if you would like to work with mpi. The mpi4py package should match your installed mpi library, usually openmpi or mpich. 


### Mesh Description

The geometry of this testcase is provided as a gmsh file and matches the size of the experiment of Griebel et al (2007), https://doi.org/10.1016/j.proci.2006.07.042.

The mesh consists of a a coarse structured mesh with 12.4k cells and 12.7k points. The mesh was created using Gmsh and the configuration file to create the mesh can be found here: [psi.geo](https://github.com/su2code/Tutorials/tree/master/multiphysics/TFC_python/psi.geo). The only thing you need to do to create a mesh from the geometry is start Gmsh, and then load the .geo file. You will then see the geometry in the Gmsh visualization window. If you click on *Mesh->2D* the 2D mesh will be generated. You can then export the mesh as a .su2 file by choosing *File->Export*. The mesh will automatically be saved in su2 format when the filename has been given the extension .su2. In general, you should not choose *save all elements* because this will also save additional points that were used to construct the geometry but are not part of the final mesh, like for example the center of a circle. 


### Configuration File Options

The setup for this testcase consists of 2 files:
- the run.py file is the python file that runs the case. in this file, we simply import the su2 capabilities using *import pysu2*
- the psi.cfg file for the basic setup. Some settings will be overwritten by python.

In the configuration file, we have set up a case for turbulent incompressible flow using the k-omega SST model. We have also activated the energy equation (sensible enthalpy) and species transport. 
```
SOLVER= INC_RANS
KIND_TURB_MODEL= SST
INC_ENERGY_EQUATION= YES
KIND_SCALAR_MODEL= SPECIES_TRANSPORT
```


in the python file, we have defined several functions to set up the testcase. The first function creates a simple initial condition for the progress variable c:
```python ################################################################## #
# create a function for the initial progress variable c              # ################################################################## #
def initC(coord):
    x = coord[0]
    #y = coord[1]
    #z = coord[2]
    # location where the flame should be
    flame_x = 0.012
    if (x < flame_x):
      C = 0.0
    else:
      C = 1.0

    return C
    
# ################################################################## #
# loop over all vertices and set the species progress variable c     # ################################################################## #
def SetInitialSpecies(SU2Driver):
    allCoords = SU2Driver.Coordinates()
    iSPECIESSOLVER = SU2Driver.GetSolverIndices()['SPECIES']
    for iPoint in range(SU2Driver.GetNumberNodes()):
      coord = allCoords.Get(iPoint)
      C = initC(coord)
      # now update the initial condition for the species
      SU2Driver.Solution(iSPECIESSOLVER).Set(iPoint,0,C)

```

![TFC_temp_init](../../../tutorials_files/multiphysics/TFC_python/images/TFC_temp_init.png)
Figure(2): initial temperature field created using the python wrapper

Note that when setting the solution, we use the index=0, because we have only 1 species transport equation. When setting a flow solution, the index to the required field should be used. The indices can be retrieved using:
```python
print("indices of solver variables: ", getsolvar(driver))
```
with the result:
```
indices of solver variables:  {'PRESSURE': 0, 'VELOCITY_X': 1, 'VELOCITY_Y': 2, 'TEMPERATURE': 3}
```


in the main function, we simply check in the config file if **RESTART=YES** to decide if we want to overwrite the solution for the progress variable.

```python
  # ### Check if we do a restart or not. ###
  with open('psi.cfg') as f:
    if 'RESTART_SOL= YES' in f.read():
      if rank == 0:
        print("restarting from file")
    else:
        # We can set an initial condition by calling this function:
        if rank == 0:
          print("Using user defined initial condition.")
        SetInitialSpecies(driver)

```

The functions *update_temperature* and *zimont* implement the algebraic temperature relationship and the source term for the progress variable. Then in the main file, we simply loop over all points in the domain, compute the source term and add it to the progress variable equation:
```python
    Source = driver.UserDefinedSource(iSPECIESSOLVER)

    # set the source term, per point
    for i_node in range(driver.GetNumberNodes() - driver.GetNumberHaloNodes()):
      # add source term:
      # default TFC of Zimont: rho*Sc = rho_u * U_t * grad(c)
      S = zimont(driver,i_node)
      Source.Set(i_node,0,S)

```

Note that we do not add the source term to the halo nodes, which are used in parallel computing. In parallel computing we divide the mesh in parts and each cpu gets a part, which is called a rank. the points on the interface between ranks need information from the other side of the interface, but this information is computed on another rank. This is why each rank has halo points, which are copies of the points on the other side of the rank. They should not be taken into account in any computation, because they are in fact copies of points that *are* taken into account during the computation. 


### Running SU2

If possible, always use a parallel setup to reduce computational time (wall clock time). Run the SU2_CFD executable in parallel using MPI and 4 nodes by entering: 

    $ mpirun -n 4 python run.py

### Results

![TFC_source](../../../tutorials_files/multiphysics/TFC_python/images/TFC_source.png)
Figure (3): visualization of the TFC source term for the turbulent combustion model, together with the streamlines. A large recirculation region has formed between the flame and the wall of the combustion chamber.

Also note that we clip the species between [0,1]. Sometimes this clipping is necessary on coarse grids. In that case, this will be visible in the residuals of the progress variable, since clipping prevents convergence to the actual solution.
