---
title: Thermochemical Nonequilibrium
permalink: /docs_v7/Thermochemical-Nonequilibrium/
---

This page contains a summary of the physical models implemented in the NEMO solvers in SU2 designed ot simulate hypersonic flows in thermochemical nonequilibrium. This includes detials on thermodynamic and chemistry models, as well as transport properties and boundary conditions. 

---

- [Thermodynamic Model](#thermodynamic-model)
- [Finite Rate Chemistry](#finite-rate-chemistry)
  
---

# Thermodynamic Model #

| Solver | Version | 
| --- | --- |
| `NEMO_EULER`, `NEMO_NAVIER_STOKES` | 7.0.0 |

A rigid-rotor harmonic oscillator (RRHO) two-temperature model is used to model the thermodynamic state of continuum hypersonic flows. Through the independence of the energy levels, the total energy and vibrational--electronic energy per unit volume can be expressed as
$$   \rho e = \sum_s \rho_s \left(e_s^{tr} + e_s^{rot} + e_s^{vib} + e_s^{el} + e^{\circ}_s + \frac{1}{2} \bar{v}^{\top} \bar{v}\right),
$$
and
$$
        \rho e^{ve} = \sum_s \rho_{s} \left(e_s^{vib} + e_s^{el}\right).
$$

Considering a general gas mixture consisting of polyatomic, monatomic, and free electron species, expressions for the energy stored in the translational, rotational, vibrational, and electronic modes are given as
$$
    e^{tr}_s =\begin{cases}
    \frac{3}{2} \frac{R}{M_s} T & \text{for monatomic and polyatomic species,}\\
    0 & \text{for electrons,}
    \end{cases}
$$
$$
    e^{rot}_s =\begin{cases}
    \frac{\xi  }{2} \frac{R}{M_s} T & \text{for polyatomic species,}\\
    0 & \text{for monatomic species and electrons,}
    \end{cases}
$$
where $\xi$ is an integer specifying the number of axes of rotation,
$$
    e^{vib}_s =\begin{cases}
    \frac{R}{M_s} \frac{\theta^{vib}_s}{exp\left( \theta^{vib}_s / T^{ve}\right) - 1} & \text{for polyatomic species,}\\
    0 & \text{for monatomic species and electrons,}
    \end{cases}
$$
where $\theta^{vib}_s$ is the characteristic vibrational temperature of the species, and 


$$
    e^{el}_s =\begin{cases}
    \frac{R}{M_s}\frac{\sum_{i=1}^{\infty} g_{i,s}{\theta^{el}_{i,s} \exp(-\theta^{el}_{i,s}/T_{ve})}}{\sum_{i=0}^{\infty} g_{i,s} exp(-\theta^{el}_{i,s}/T_{ve})} & \text{for polyatomic and monatomic species,}\\
    \frac{3}{2} \frac{R}{M_s} T^{ve} & \text{for electrons,}
    \end{cases}
$$

where $\theta^{el}_s$ is the characteristic electronic temperature of the species and $g_i$ is the degeneracy of the $i^{th}$ state.

---

# Finite Rate Chemistry #

| Solver | Version | 
| --- | --- |
| `NEMO_EULER`, `NEMO_NAVIER_STOKES` | 7.0.0 |

The source terms in the species conservation equations are the  volumetric mass production rates which are governed by the forward and backward reaction rates, $R^f$ and $R^b$, for a given reaction $r$, and can be expressed as
$$
    \dot{w}_s = M_s \sum_r (\beta_{s,r} - \alpha_{s,r})(R_{r}^{f} - R_{r}^{b}). 
$$

From kinetic theory, the forward and backward reaction rates are dependent on the molar concentrations of the reactants and products, as well as the forward and backward reaction rate coefficients, $k^f$ and $k^b$, respectively, and can be expressed as
$$
    R_{r}^f = k_{r}^f \prod_s (\frac{\rho_s}{M_s})^{\alpha_{s,r}},
$$
and
$$
    R_{r}^b = k_{r}^b \prod_s (\frac{\rho_s}{M_s})^{\beta_{s,r}}.
$$

For an Arrhenius reaction, the forward reaction rate coefficient can be computed as
$$
    k_{r}^f = C_r(T_r)^{\eta_r} exp\left(- \frac{\epsilon_r}{k_B T_r}\right),
$$
where $C_r$ is the pre-factor, $T_r$ is the rate-controlling temperature for the reaction, $\eta_r$ is an empirical exponent, and $\epsilon_r$ is the activation energy per molecule.

The rate-controlling temperature of the reaction is calculated as a geometric average of the translation--rotational and vibrational--electronic temperatures,
$$
    T_r = (T)^{a_r}(T^{ve})^{b_r},
$$



---

