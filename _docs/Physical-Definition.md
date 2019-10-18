---
title: Physical Definition and Non-dimensionalization
permalink: /docs/Physical-Definition/
---

The physical definition of a case includes the definition of the free-stream, the reference values and the non-dimensionalization. 
SU2 offers different ways of setting and computing this definition. This document gives a short overview on the config options and their physical relation.



## Reference Values ##

| Variable | Unit | Reference |
|---|---|---|
| Length | $$m$$ | $$l_{ref} = 1$$ |
| Density | $$\frac{kg}{m^3}$$ | $$\rho_{ref} = \rho_{\infty}$$ |
| Velocity | $$\frac{m}{s}$$ | $$v_{ref} = v_{\infty}$$ |
| Temperature | $$K$$ | $$T_{ref} = T_{\infty}$$ |
| Viscosity | $$\frac{kg}{ms}$$ | $$\mu_{ref} = \rho_{ref}v_{ref}l_{ref}$$ |
| Time | $$s$$ | $$t_{ref} = \frac{l_{ref}}{v_{ref}}$$ |
| Heatflux | $$\frac{W}{m^2}$$ | $$Q_{ref} = \rho_{ref}v^3_{ref} $$ |
