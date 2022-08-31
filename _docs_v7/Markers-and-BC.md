---
title: Markers and Boundary Conditions
permalink: /docs_v7/Markers-and-BC/
---

The term *Marker* refers to a named entity in your mesh file. Boundary conditions are defined by assigning names of the markers to the corresponding option. Below you will find a list of the most common boundary conditions along with a short description.

---

- [Euler (Slip) Wall](#euler-slip-wall)
- [Symmetry Wall](#symmetry-wall)
- [Constant Heatflux (no-slip) Wall](#constant-heatflux-no-slip-wall)
- [Heat Transfer or Convection (no-slip) Wall](#heat-transfer-or-convection-no-slip-wall)
- [Isothermal (no-slip) Wall](#isothermal-no-slip-wall)
- [Farfield Boundary Condition](#farfield-boundary-condition)
- [Turbulence Boundary Condition](#turbulence-boundary-condition)
  - [Wall functions](#wall-functions) 
- [Inlet Boundary Condition](#inlet-boundary-condition)
  - [Total Conditions](#total-conditions)
  - [Mass Flow Inlet](#mass-flow-inlet)
  - [Velocity Inlet](#velocity-inlet)
  - [Pressure Inlet](#pressure-inlet)
- [Outlet Boundary Condition](#outlet-boundary-condition)
  - [Pressure Outlet (Compressible)](#pressure-outlet-compressible)
  - [Pressure Outlet (Incompressible)](#pressure-outlet-incompressible)
  - [Mass Flow Outlet](#mass-flow-outlet)
  - [Periodic Boundary Condition](#periodic-boundary-condition)
- [Structural Boundary Conditions](#structural-boundary-conditions)
  - [Clamped Boundary](#clamped-boundary)
  - [Displacement Boundary](#displacement-boundary)
  - [Load Boundary](#load-boundary)
  - [Normal Pressure Boundary](#normal-pressure-boundary)

---

## Euler (Slip) Wall ##

| Solver | Version | 
| --- | --- |
| `EULER`, `NAVIER_STOKES`, `RANS`, `INC_EULER`, `INC_NAVIER_STOKES`, `INC_RANS`, `FEM_EULER`, `FEM_NAVIER_STOKES` | 7.0.0 |

An Euler wall for inviscid flow is defined with the `MARKER_EULER` option. It can also be used as a slip wall in viscous flow. Only the marker name has to be given for this option.

For all Finite Volume (FVM) solvers, i.e. not the `FEM_*` solvers, its implementation is identical to `MARKER_SYM` solvers and both options can be used interchangeably.

```
MARKER_EULER = (Euler_Wall1, Euler_Wall2, ...)
```

**Note**: Be aware when switching from an Euler solver to a Navier-Stokes one that most solid walls should become `MARKER_HEATFLUX` (and vice versa).

## Symmetry Wall ##

| Solver | Version | 
| --- | --- |
| `EULER`, `NAVIER_STOKES`, `RANS`, `INC_EULER`, `INC_NAVIER_STOKES`, `INC_RANS`, `FEM_EULER`, `FEM_NAVIER_STOKES` | 7.0.0 |

A symmetry wall is defined with using the `MARKER_SYM` option. Only the marker name has to be given for this option.

For all Finite Volume (FVM) solvers, i.e. not the `FEM_*` solvers, its implementation is identical to `MARKER_SYM` solvers and both options can be used interchangeably.

```
MARKER_SYM = (Symmetry_Wall1, Symmetry_Wall2, ...)
```

## Constant Heatflux (no-slip) Wall ##

| Solver | Version | 
| --- | --- |
| `NAVIER_STOKES`, `RANS`, `INC_NAVIER_STOKES`, `INC_RANS`, `FEM_NAVIER_STOKES`, `HEAT_EQUATION_FVM` | 7.0.0 |


A wall with a prescribed constant heatflux is defined with the `MARKER_HEATFLUX` option. The option format is the marker name followed by the value of the heatflux (in Watts per square meter `[W/m^2],[J/(s*m^2)]`), e.g.
```
MARKER_HEATFLUX = (Wall1, 1e05, Wall2, 0.0)
```

Instead of a constant heatflux (in `[W/m^2]`), a constant rate of heat flow (in `[W]`) can be prescribed by additionally adding the option `INTEGRATED_HEATFLUX= YES`. For the above `MARKER_HEATFLUX`, lets consider that `Wall1` has a surface area of 0.3 `[m^2]` then one could equivalently prescribe
```
MARKER_HEATFLUX = (Wall1, 0.3e05, Wall2, 0.0)
```

when additionally using the `INTEGRATED_HEATFLUX= YES` option. In the case of a DOE or an optimization this prescription of a rate of heat flow might be the more natural boundary condition.

**Notes**:
1. Typically Navier-Stokes and RANS simulations are setup with adiabatic walls (heatflux = 0).
2. `INTEGRATED_HEATFLUX` is not available for `FEM_NAVIER_STOKES`.

## Heat Transfer or Convection (no-slip) Wall ##

| Solver | Version | 
| --- | --- |
| `NAVIER_STOKES`, `RANS`, `INC_NAVIER_STOKES`, `INC_RANS` | 7.0.0 |


A wall with a prescribed locally variable heatflux via a heat transfer coefficient and and a Temperature at infinity (or reservoir Temperature) is defined with the `MARKER_HEATTRANSFER` option. The heatflux `q` computes to `q = h(T_inf - T_wall)`, where `T_wall` is the local wall temperature and therefore no user input. The option format is the marker name followed by the value of the heat-transfer coefficient (in Watts per square meter and Kelvin `[W/(m^2*K)],[J/(s*m^2*K)]`) and the value of the Temperature at infinity (in Kelvin `[K]`), e.g.
```
MARKER_HEATTRANSFER = (Wall1, 10.0, 350.0, Wall2, 5.0, 330.0, ...)
```

**Note**: The Heat Transfer Wall degenerates to an adiabatic wall when the heat transfer coefficient is zero. On the other extreme (a very high heat transfer coefficient) the Heat Transfer Wall degenerates to an isothermal wall with Temperature at infinity being the wall temperature.

## Isothermal (no-slip) Wall ##

| Solver | Version | 
| --- | --- |
| `NAVIER_STOKES`, `RANS`, `INC_NAVIER_STOKES`, `INC_RANS`, `FEM_NAVIER_STOKES`, `HEAT_EQUATION_FVM` | 7.0.0 |

A wall with a constant temperature is defined with the `MARKER_ISOTHERMAL` option. The option format is the marker name followed by the value of the temperature (in Kelvin `[K]`), e.g.
```
MARKER_ISOTHERMAL = (Wall1, 300.0, Wall2, 250.0)
```

## Farfield Boundary Condition ##

| Solver | Version | 
| --- | --- |
| `EULER`, `NAVIER_STOKES`, `RANS`, `INC_EULER`, `INC_NAVIER_STOKES`, `INC_RANS`, `FEM_EULER`, `FEM_NAVIER_STOKES` | 7.0.0 |

A marker can be defined as a Farfield boundary by addings its name to the `MARKER_FAR` option. No other values are necesseary for that option. The actual values which will be prescribed depend on the solver and other user input settings. More details can be found in the [Physical Definition](/docs_v7/Physical-Definition/) section.

```
MARKER_FAR= (farfield)
```

## Turbulence Boundary Condition ##

| Solver | Version | 
| --- | --- |
| `RANS`, `INC_RANS`, | 7.3.0 |

The turbulence boundary conditions do not have a `MARKER_` keyword but can instead be set for inlet and freestream boundaries using the keywords: 

For the SA turbulence model:
```
FREESTREAM_NU_FACTOR= 3
```

For the SST turbulence model:
```
FREESTREAM_TURBULENCEINTENSITY= 0.05
FREESTREAM_TURB2LAMVISCRATIO= 10
```

### Wall functions ###
Accurately resolving the turbulence close to walls requires very fine meshes and can be quite expensive. When the vertices of the first cell neighboring the wall have on average a normalized distance $$y^+ >1$$, wall functions can be used. For example to activate wall functions on the markers `wall1` and `wall2`, we write:
```
MARKER_WALL_FUNCTIONS=(wall1,STANDARD_WALL_FUNCTION,wall2,STANDARD_WALL_FUNCTION)
```
The wall functions will now be used automatically. all functions have 5 additional expert parameters:
```
WALLMODEL_KAPPA= 0.41
WALLMODEL_B= 5.5
WALLMODEL_MINYPLUS= 5.0
WALLMODEL_MAXITER= 200
WALLMODEL_RELFAC= 0.5
```
The constant `WALLMODEL_KAPPA` is the von Karman constant, and `WALLMODEL_B` is an additional constant describing the universal 'law of the wall'. The constants are supposed to be universal, and do not change. The setting `WALLMODEL_MINYPLUS= 5` will activate the wall model only when the local value of $$y^+$$ is higher than the value given (default: 5). Note that in principle, this implementation is valid for any $$y^+ < 100-500$$ and will also work correctly for very small values of $$y^+$$. the upper limit that can be used depends on (and increases with) the Reynolds number. The universal law of the wall is an implicit function and a Newton iterator is used to determine $$u^+(y^+)$$. The maximum number of iterations can be set by `WALLMODEL_MAXITER` and the relaxation factor can be set with `WALLMODEL_RELFAC`. When the Newton solver does not converge within the maximum number of iterations given, a warning message will appear during the computation. When these warning messages do not disappear, you might consider increasing `WALLMODEL_MAXITER` or decreasing `WALLMODEL_RELFAC`.  

## Inlet Boundary Condition ##
Inlet boundary conditions are set using the option `MARKER_INLET`.

### Total Conditions ###

| Solver | Version | 
| --- | --- |
| `EULER`, `NAVIER_STOKES`, `RANS`, `FEM_EULER`, `FEM_NAVIER_STOKES` | 7.0.0 |

To describe the **Total Conditions** at the inlet, set the option `INLET_TYPE= TOTAL_CONDITIONS` (which is the default). The format for `MARKER_INLET` then is the marker name, followed by the Total Temperature (in Kelvin `[K]`), the total Pressure (in Pascal `[Pa]`) and the flow direction unity vector (in meter per second `[m/s]`). For example:
```
INLET_TYPE= TOTAL_CONDITIONS
MARKER_INLET = (inlet1, 300, 1e6, 1.0, 0.0, 0.0, inlet2, 400, 1e6, 0.0, 1.0, 0.0)
```

### Mass Flow Inlet ###

| Solver | Version | 
| --- | --- |
| `EULER`, `NAVIER_STOKES`, `RANS`, `FEM_EULER`, `FEM_NAVIER_STOKES` | 7.0.0 |

To describe the **Mass Flow** at the inlet, set the option `INLET_TYPE= MASS_FLOW`. The format for `MARKER_INLET` then is the marker name, followed by the Density (in `[kg/m^3`]), the Velocity magnitude (in meter per second `[m/s]`) and the flow direction unity vector (in meter per second `[m/s]`). For example:
```
INLET_TYPE= MASS_FLOW
MARKER_INLET = (inlet1, 1.13 , 20, 1.0, 0.0, 0.0, inlet2, 1.15, 10, 0.0, 1.0, 0.0)
```
**Note**: It is not possible to combine Mass Flow Inlet BCs and Total Condition Inlet BCs yet.

### Velocity Inlet ###

| Solver | Version | 
| --- | --- |
| `INC_EULER`, `INC_NAVIER_STOKES`, `INC_RANS` | 7.0.0 |

To describe the **Velocity** as well as the **Temperature** at the inlet, set the option `INC_INLET_TYPE= VELOCITY_INLET`. The format for `MARKER_INLET` then is the marker name, followed by the Temperature (in Kelvin `[K`]), the Velocity magnitude (in meter per second `[m/s]`) and the flow direction vector (the direction vector does not need to be normalized). Note that the temperature has to be provided even when `INC_ENERGY_EQUATION= NO`, but it will be ignored in the calculations.

```
INC_INLET_TYPE= VELOCITY_INLET, VELOCITY_INLET
MARKER_INLET = (inlet1, 300, 20, 1.0, 0.0, 0.0, inlet2, 200, 10, 0.0, 1.0, 0.0)
```

### Pressure Inlet ###

| Solver | Version | 
| --- | --- |
| `INC_EULER`, `INC_NAVIER_STOKES`, `INC_RANS` | 7.0.0 |

To describe the **Total Pressure** at the inlet, set the option `INC_INLET_TYPE= PRESSURE_INLET`. The format for `MARKER_INLET` then is the marker name, followed by the Temperature (in Kelvin `[K]`), the Total Pressure (in Pascal `[Pa]`) and the flow direction unity vector (in meter per second `[m/s]`). 

```
INC_INLET_TYPE= PRESSURE_INLET, PRESSURE_INLET
MARKER_INLET = (inlet1, 300 , 1e6, 1.0, 0.0, 0.0, inlet2, 200, 1e6, 0.0, 1.0, 0.0)
```

**Note 1**: It is possible to combine Velocity Inlet BCs and Pressure Inlet BCs.

**Note 2**: Updates to the velocity based on the prescribed pressure are damped in order to help with stability/convergence. The damping coefficient can be changed using the `INC_INLET_DAMPING` option (default is `0.1`).

## Outlet Boundary Condition ##

Outlet boundary conditions are set using the `MARKER_OUTLET` option.

### Pressure Outlet (Compressible) ###

| Solver | Version | 
| --- | --- |
| `EULER`, `NAVIER_STOKES`, `RANS`, `FEM_EULER`, `FEM_NAVIER_STOKES` | 7.0.0 |

To describe the static thermodynamic pressure at an outlet, the format for `MARKER_OUTLET` is the marker name, followed by the value of the static pressure (in Pascal `[Pa]`).

```
MARKER_OUTLET = (outlet, 1e5)
```

### Pressure Outlet (Incompressible) ###

| Solver | Version | 
| --- | --- |
| `INC_EULER`, `INC_NAVIER_STOKES`, `INC_RANS`| 7.0.0 |

To describe the pressure at an outlet, set the option `INC_OUTLET_TYPE= PRESSURE_OUTLET`. The format for `MARKER_OUTLET` is the marker name, followed by the value of the gauge pressure (in Pascal `[Pa]`).

```
INC_OUTLET_TYPE= PRESSURE_OUTLET
MARKER_OUTLET = (outlet, 1e1)
```

**Note**: Gauge pressure is zero-referenced against ambient air pressure, so it is equal to absolute pressure minus atmospheric pressure.

### Mass Flow Outlet ###

| Solver | Version | 
| --- | --- |
| `INC_EULER`, `INC_NAVIER_STOKES`, `INC_RANS`| 7.0.0 |

To describe the mass flow at an outlet, set the option `INC_OUTLET_TYPE= MASS_FLOW_OUTLET`. The format for `MARKER_OUTLET` is the marker name, followed by the value of the target mass flow (in kilogramm per second `[kg/s]`).

```
INC_OUTLET_TYPE= MASS_FLOW_OUTLET
MARKER_OUTLET = (outlet, 1e1)
```

**Note**: Updates to the pressure based on the prescribed mass flow are damped in order to help with stability/convergence. The damping coefficient can be changed using the `INC_OUTLET_DAMPING` option (default is `0.1`).

### Periodic Boundary Condition ###

| Solver | Version | 
| --- | --- |
| `NAVIER_STOKES`, `RANS`, `INC_NAVIER_STOKES`, `INC_RANS`, `FEM_NAVIER_STOKES` | 7.0.0 |

## Structural Boundary Conditions ##

### Clamped Boundary ###

| Solver | Version | 
| --- | --- |
| `ELASTICITY` | 7.0.0 |

The format for this boundary condition consists of a list of all clamped surfaces (markers). Structural displacements are set to 0 for the nodes on those surfaces.

```
MARKER_CLAMPED = (surface_1,...,surface_N)
```

**Note**: A well posed structural problem requires at least one surface as `MARKER_CLAMPED` or `MARKER_DISPLACEMENT`.

### Displacement Boundary ###

| Solver | Version | 
| --- | --- |
| `ELASTICITY` | 7.0.0 |

The displacements of the nodes on `surface` are enforced, the displacement vector is specified by magnitude and direction (the x/y/z components), internally the solver makes the direction unitary, the multiplier (should usually be set to 1) can be used to increase/decrease the magnitude for example after scaling an existing mesh.
```
MARKER_DISPLACEMENT = (surface, multiplier, magnitude `[m]`, x component, y component, z component)
```

**Note**: Be aware of intersecting surfaces with incompatible displacements, there are shared nodes between adjacent surfaces.

### Load Boundary ###

| Solver | Version | 
| --- | --- |
| `ELASTICITY` | 7.0.0 |

A force-like boundary condition but specified in terms of pressure (units of Pa) which is integrated to obtain nodal forces. The syntax is identical to `MARKER_DISPLACEMENT`.
```
MARKER_LOAD = (surface, multiplier, magnitude `[Pa]`, x component, y component, z component)
```

**Note**: In the context of nonlinear elasticity, this is not a following force.

### Normal Pressure Boundary ###

| Solver | Version | 
| --- | --- |
| `ELASTICITY` | 7.0.0 |

Normal pressure boundary condition (positive means into the surface). This is a following force both magnitude and direction depend of the deformation of the structure.
```
MARKER_PRESSURE = (surface, inward pressure `[Pa]`)
```

