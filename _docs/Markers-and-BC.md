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
| Solver | Version | 
| --- | --- |
| `NAVIER_STOKES`, `RANS`, `INC_NAVIER_STOKES`, `INC_RANS`, `FEM_NAVIER_STOKES` | 7.0.0 |

## Outlet Boundary Condition ##
| Solver | Version | 
| --- | --- |
| `NAVIER_STOKES`, `RANS`, `INC_NAVIER_STOKES`, `INC_RANS`, `FEM_NAVIER_STOKES` | 7.0.0 |

## Periodic Boundary Condition ##
| Solver | Version | 
| --- | --- |
| `NAVIER_STOKES`, `RANS`, `INC_NAVIER_STOKES`, `INC_RANS`, `FEM_NAVIER_STOKES` | 7.0.0 |
