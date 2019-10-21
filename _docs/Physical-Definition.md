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

## Compressible Definition ##

| Solver | Version | 
| --- | --- |
| `EULER`, `NAVIER_STOKES`, `RANS`,`FEM_EULER`, `FEM_NAVIER_STOKES` | 7.0.0 |

### Free-Stream Definition ###

The thermodynamic state of the free-stream for the compressible solvers in SU2 is defined by the pressure $$p_{\infty}$$, the density $$\rho_{\infty}$$ and the temperature $$T_{\infty}$$. Since these quantities are not independent, only two of these values have to be described and the third one can be computed by an equation of state, depending on the fluid model used. There are two possible options currently implemented:

- `FREESTREAM_OPTION= TEMPERATURE_FS` (default): Density $$\rho_{\infty}$$ is computed using the specified pressure $$p_{\infty}$$ (`FREESTREAM_PRESSURE`) and temperature $$T_{\infty}$$ (`FREESTREAM_TEMPERATURE`).
- `FREESTREAM_OPTION= DENSITY_FS`: Temperature $$T_{\infty}$$ is computed using the specified pressure $$p_{\infty}$$ (`FREESTREAM_PRESSURE`) and density $$\rho_{\infty}$$ (`FREESTREAM_DENSITY`). 

The free-stream velocity $$v_{\infty}$$ is always computed from the specified Mach number $$Ma_{\infty}$$ (`MACH_NUMBER`) and its direction from the angle of attack (`AOA`) and the side-slip angle (`SIDESLIP_ANGLE`, for 3D).

### Initialization ###

### Non-Dimensionalization Schemes ###

For all schemes, the free-stream values for Density and Temperature are used as reference values respectively, i.e. $$ \rho_{ref} = \rho_{\infty}, T_{ref} = T_{\infty}$$. The reference velocity is based on the speed of sound defined by the reference state: $$v_{ref} = \sqrt{\frac{p_{ref}}{\rho_{ref}}}$$. The dimensionalization scheme can be set using the option `REF_DIMENSIONALIZATION` and defines how the reference pressure $$p_{ref}$$ is computed:

- `DIMENSIONAL`: All reference values are set to `1.0`, i.e. the computation is dimensional.
- `FREESTREAM_PRESS_EQ_ONE`: Reference pressure equals free-stream pressure, $$p_{ref} = p_{\infty}$$.
- `FREESTREAM_VEL_EQ_MACH`: Reference pressure is chosen such that the free-stream velocity $$v_{\infty}$$ equals the Mach number: $$p_{ref} = \gamma p_{\infty}$$.
- `FREESTREAM_VEL_EQ_ONE`: Reference pressure is chosen such that the free-stream velocity $$v_{\infty}$$ is one: $$p_{ref} = Ma^2_{\infty} \gamma p_{\infty}$$.

