---
title: Physical Definition
permalink: /docs/Physical-Definition/
---

The physical definition of a case includes the definition of the free-stream, the reference values and the non-dimensionalization. 
SU2 offers different ways of setting and computing this definition. This document gives a short overview on the config options and their physical relation.



## Reference Values ##

| Solver | Version | 
| --- | --- |
| `EULER`, `NAVIER_STOKES`, `RANS`, `INC_EULER`, `INC_NAVIER_STOKES`, `INC_RANS`, `FEM_EULER`, `FEM_NAVIER_STOKES` | 7.0.0 |

| Variable | Unit | Reference |
|---|---|---|
| Length | $$m$$ | $$l_{ref} = 1$$ |
| **Density** | $$\frac{kg}{m^3}$$ | $$\rho_{ref}$$ (based on user input) |
| **Velocity** | $$\frac{m}{s}$$ | $$v_{ref}$$ (based on user input)|
| **Temperature** | $$K$$ | $$T_{ref}$$ (based on user input) |
| **Pressure** | $$Pa$$ | $$p_{ref}$$ (based on user input) |
| Viscosity | $$\frac{kg}{ms}$$ | $$\mu_{ref} = \rho_{ref}v_{ref}l_{ref}$$ |
| Time | $$s$$ | $$t_{ref} = \frac{l_{ref}}{v_{ref}}$$ |
| Heatflux | $$\frac{W}{m^2}$$ | $$Q_{ref} = \rho_{ref}v^3_{ref} $$ |
| Gas Constant | $$\frac{m^2}{s^2 K}$$ | $$R_{ref} = \frac{v^2_{ref}}{T_{ref}}$$|
| Conductivity | $$\frac{W}{mK}$$ | $$k_{ref} = \mu_{ref}R_{ref}$$ |
| Force | $$N$$ | $$ F_{ref} = \rho_{ref}v^2_{ref}l^2_{ref} $$ |

The reference values of the highlighted variables in the table above are based on the solver and user-defined options.

## Non-Dimensionalization Schemes (Compressible) ##

| Solver | Version | 
| --- | --- |
| `EULER`, `NAVIER_STOKES`, `RANS`,`FEM_EULER`, `FEM_NAVIER_STOKES` | 7.0.0 |

The dimensionalization scheme can be set using the option `REF_DIMENSIONALIZATION`. For all schemes, the values set with `FREESTREAM_DENSITY` and `FREESTREAM_TEMPERATURE` are used as reference values for Density and Temperature, respectively, i.e. $$ \rho_{ref} = \rho_{\infty}, T_{ref} = T_{\infty}$$. The reference velocity is based on the speed of sound defined by the reference state: $$v_{ref} = \sqrt{\frac{p_{ref}}{\rho_{ref}}}$$.

