---
title: Markers and Boundary Conditions
permalink: /docs/Markers-and-BC/
---

The term *Marker* refers to a named entity in your mesh file. Boundary conditions are defined by assigning names of the markers to the corresponding option. Below you will find a list of the most common boundary conditions along with a short description.

---

## Content ##

- [Euler (Slip) Wall](#euler-slip-wall)
- [Constant Heatflux (no-slip) Wall](#constant-heatflux-no-slip-wall)
- [Isothermal (no-slip) Wall](#isothermal-no-slip-wall)
- [Farfield Boundary Condition](#farfield-boundary-condition)
- [Inlet Boundary Condition](#inlet-boundary-condition)
- [Outlet Boundary Condition](#outlet-boundary-condition)
- [Periodic Boundary Condition](#periodic-boundary-condition)

---

## Euler (Slip) Wall ##

| Solver | Version | 
| --- | --- |
| `EULER`, `NAVIER_STOKES`, `RANS`, `INC_EULER`, `INC_NAVIER_STOKES`, `INC_RANS`, `FEM_EULER`, `FEM_NAVIER_STOKES` | 7.0.0 |

## Constant Heatflux (no-slip) Wall ##

| Solver | Version | 
| --- | --- |
| `NAVIER_STOKES`, `RANS`, `INC_NAVIER_STOKES`, `INC_RANS`, `FEM_NAVIER_STOKES` | 7.0.0 |


A wall with a prescribed constant heatflux is defined with the `MARKER_HEATFLUX` option. The option format is the marker name followed by the value of the heatflux (in Joule per square meter `[J/m^2]`), e.g.
```
MARKER_HEATFLUX = (Wall1, 1e05, Wall2, 0.0)
```

## Isothermal (no-slip) Wall ##

| Solver | Version | 
| --- | --- |
| `NAVIER_STOKES`, `RANS`, `INC_NAVIER_STOKES`, `INC_RANS`, `FEM_NAVIER_STOKES` | 7.0.0 |

A wall with a constant temperature is defined with the `MARKER_ISOTHERMAL` option. The option format is the marker name followed by the value of the temperature (in Kelvin `[K]`), e.g.
```
MARKER_ISOTHERMAL = (Wall1, 300.0, Wall2, 250.0)
```

## Farfield Boundary Condition ##

| Solver | Version | 
| --- | --- |
| `NAVIER_STOKES`, `RANS`, `INC_NAVIER_STOKES`, `INC_RANS`, `FEM_NAVIER_STOKES` | 7.0.0 |

## Inlet Boundary Condition ##
Inlet boundary conditions are set using the option `MARKER_INLET`.

### Total Conditions ###

| Solver | Version | 
| --- | --- |
| `EULER`, `NAVIER_STOKES`, `RANS`, `FEM_EULER`, `FEM_NAVIER_STOKES` | 7.0.0 |

If you want to describe the total conditions at the inlet, set the option `INLET_TYPE= TOTAL_CONDITIONS` (which is the default). The format for `MARKER_INLET` than is the marker name, followed by the Total Temperature (in Kelvin `[K]`), the total Pressure (in Pascal `[Pa]`) and the flow direction unity vector (in meter per second `[m/s]`). For example:
```
MARKER_INLET = (inlet1, 300, 1e6, 1.0, 0.0, 0.0, inlet2, 400, 1e6, 0.0, 1.0, 0.0)
```

### Mass Flow (Compressible) ###

| Solver | Version | 
| --- | --- |
| `EULER`, `NAVIER_STOKES`, `RANS`, `FEM_EULER`, `FEM_NAVIER_STOKES` | 7.0.0 |

If you want to describe the mass flow at the inlet, set the option `INLET_TYPE= MASS_FLOW` (which is the default). The format for `MARKER_INLET` than is the marker name, followed by the Density (in `[kg/m^3`]), the Velocity magnitude (in meter per second `[m/s]`) and the flow direction unity vector (in meter per second `[m/s]`). For example:
```
MARKER_INLET = (inlet1, 1.13 , 20, 1.0, 0.0, 0.0, inlet2, 1.15, 10, 0.0, 1.0, 0.0)
```

### Mass Flow (Incompressible) ###

| Solver | Version | 
| --- | --- |
| `INC_EULER`, `INC_NAVIER_STOKES`, `INC_RANS`| 7.0.0 |

If you want to describe the mass flow at the inlet, set the option `INC_INLET_TYPE= MASS_FLOW` (which is the default). The format for `MARKER_INLET` than is the marker name, followed by the Density (in `[kg/m^3`]), the Velocity magnitude (in meter per second `[m/s]`) and the flow direction unity vector (in meter per second `[m/s]`). For example:
```
MARKER_INLET = (inlet1, 1.13 , 20, 1.0, 0.0, 0.0, inlet2, 1.15, 10, 0.0, 1.0, 0.0)
```

### Velocity ###

| Solver | Version | 
| --- | --- |
| `INC_EULER`, `INC_NAVIER_STOKES`, `INC_RANS` | 7.0.0 |

If you want to describe the velocity at the inlet, set the option `INC_INLET_TYPE= VELOCITY_INLET` (which is the default). The format for `MARKER_INLET` than is the marker name, followed by the Temperature (in Kelvin `[K`]), the Velocity magnitude (in meter per second `[m/s]`) and the flow direction unity vector (in meter per second `[m/s]`). 

```
MARKER_INLET = (inlet1, 300 , 20, 1.0, 0.0, 0.0, inlet2, 200, 10, 0.0, 1.0, 0.0)
```

### Pressure ###

| Solver | Version | 
| --- | --- |
| `INC_EULER`, `INC_NAVIER_STOKES`, `INC_RANS` | 7.0.0 |

If you want to describe the total pressure at the inlet, set the option `INC_INLET_TYPE= PRESSURE_INLET` (which is the default). The format for `MARKER_INLET` than is the marker name, followed by the Temperature (in Kelvin `[K]`), the Total Pressure (in Pascal `[Pa]`) and the flow direction unity vector (in meter per second `[m/s]`). 

```
MARKER_INLET = (inlet1, 300 , 1e6, 1.0, 0.0, 0.0, inlet2, 200, 1e6, 0.0, 1.0, 0.0)
```

## Outlet Boundary Condition ##

| Solver | Version | 
| --- | --- |
| `NAVIER_STOKES`, `RANS`, `INC_NAVIER_STOKES`, `INC_RANS`, `FEM_NAVIER_STOKES` | 7.0.0 |

## Periodic Boundary Condition ##

| Solver | Version | 
| --- | --- |
| `NAVIER_STOKES`, `RANS`, `INC_NAVIER_STOKES`, `INC_RANS`, `FEM_NAVIER_STOKES` | 7.0.0 |
