---
title: Thermochemical Nonequilibrium
permalink: /docs_v7/Thermochemical-Nonequilibrium/
---

This page contains a summary of the physical models implemented in the NEMO solvers in SU2 designed ot simulate hypersonic flows in thermochemical nonequilibrium. This includes detials on thermodynamic and chemistry models, as well as transport properties and boundary conditions. 

---

- [Thermodynamic Model](#thermodynamic-model)
  
---

# Thermodynamic Model #

| Solver | Version | 
| --- | --- |
| `NEMO_EULER`, `NEMO_NAVIER_STOKES` | 7.0.0 |

A rigid-rotor harmonic oscillator (RRHO) two-temperature model is used to model the thermodynamic state of continuum hypersonic flows. Through the independence of the energy levels, the~total energy and vibrational--electronic energy per unit volume can be expressed as
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
\begin{equation}
    e^{rot}_s =\begin{cases}
    \frac{\xi  }{2} \frac{R}{M_s} T & \text{for polyatomic species,}\\
    0 & \text{for monatomic species and electrons,}
    \end{cases}
\end{equation}
where $\xi$ is an integer specifying the number of axes of rotation,
\begin{equation}
    e^{vib}_s =\begin{cases}
    \frac{R}{M_s} \frac{\theta^{vib}_s}{exp\left( \theta^{vib}_s / T^{ve}\right) - 1} & \text{for polyatomic species,}\\
    0 & \text{for monatomic species and electrons,}
    \end{cases}
\end{equation}
where $\theta^{vib}_s$ is the characteristic vibrational temperature of the species, and~\begin{equation}
    e^{el}_s =\begin{cases}
    \frac{R}{M_s}\frac{\sum_{i=1}^{\infty} g_{i,s}{\theta^{el}_{i,s} exp(-\theta^{el}_{i,s}/T_{ve})}}{\sum_{i=0}^{\infty} g_{i,s} exp(-\theta^{el}_{i,s}/T_{ve})} & \text{for polyatomic and monatomic species,}\\
    \frac{3}{2} \frac{R}{M_s} T^{ve} & \text{for electrons,}
    \end{cases}
\end{equation}

\noindent where $\theta^{el}_s$ is the characteristic electronic temperature of the species and $g_i$ is the degeneracy of the $i^{th}$ state.

---

