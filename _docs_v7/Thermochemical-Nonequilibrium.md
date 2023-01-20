---
title: Thermochemical Nonequilibrium
permalink: /docs_v7/Thermochemical-Nonequilibrium/
---

This page contains a summary of the physical models implemented in the NEMO solvers in SU2 designed ot simulate hypersonic flows in thermochemical nonequilibrium. This includes detials on thermodynamic and chemistry models, as well as transport properties and boundary conditions. 

---

- [Thermodynamic Model](#thermodynamic-model)
- [Finite Rate Chemistry](#finite-rate-chemistry)
- [Vibrational Relaxation](#vibrational-relaxation)
- [Viscous Phenomena and Transport Coefficients](#viscous-phenomena-and-transport-coefficients)
    - [Wilkes-Blottner-Eucken](#wilkes-blottner-eucken)
    - [Gupta-Yos](#gupta-yos)
    - [Sutherland Viscosity Model](#sutherland-viscosity-model)
- [Slip Flow](#slip-flow)
- [Gas-surface Interaction](#gas-surface-interaction)
  
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

The rate-controlling temperature of the reaction is calculated as a geometric average of the translation-rotational and vibrational-electronic temperatures,
$$
    T_r = (T)^{a_r}(T^{ve})^{b_r}.
$$

The value of he equilibrium constant $K_{eq}$ is expressed as 

$$
    K_{eq} = \exp( A_0 \left(\frac{T^c}{10,000}\right) + A_1 + A_2 \log \left( \frac{10,000}{T^c} \right) + A_3 \left( \frac{10,000}{T^c} \right) + A_4 \left( \frac{10,000}{T^c} \right)^2  ),
$$

where $T^c$ is a controlling temperature and $A_0 - A_4$ are constants dependent on the reaction. These reaction constants, the rate constrolling temperature and Arrhenius parameters are stored within the fluid model class in SU2 NEMO.

---

# Vibrational Relaxation #

| Solver | Version | 
| --- | --- |
| `NEMO_EULER`, `NEMO_NAVIER_STOKES` | 7.0.0 |

Vibrational relaxation is computed using a standard Landau-Teller relaxation time with a Park high-temperature correction
$$
     \dot{\Theta}^{tr:ve} = \sum _s \rho_s \frac{de^{ve}_{s}}{dt} = \sum _s \rho_s \frac{e^{ve*}_{s} - e^{ve}_{s}}{\tau_s},
$$
where $\tau_s$ is computed using a combination of the Landau-Teller relaxation time, $\langle \tau_s \rangle_{L-T}$, and a limiting relaxation time from Park, $\tau_{ps}$ using
$$
    \tau_s = \langle \tau_s \rangle_{L-T} + \tau_{ps},
$$
and
$$
    \langle \tau_s \rangle_{L-T} = \frac{\sum_r X_r}{\sum_r X_r/\tau_{sr}}.
$$
The interspecies relaxation times are taken from experimental data from Millikan and White, expressed as
$$
    \tau_{sr} = \frac{1}{P}exp\left[A_sr\left(T^{-1/3} - 0.015\mu_{sr}^{1/4}\right) - 18.42\right].
$$
A limiting relaxation time, $\tau_{ps}$, is used to correct for under-prediction of the Millikan--White model at high temperatures. $\tau_{ps}$ is defined as
$$
    \tau_{ps} = \frac{1}{\sigma_s c_s n},
$$

where $\sigma_s$ is the effective collision~cross-section.

---

# Viscous Phenomena and Transport Coefficients #

| Solver | Version | 
| --- | --- |
| `NEMO_EULER`, `NEMO_NAVIER_STOKES` | 7.0.0 |


Mass, momentum, and  energy transport in fluids are all governed by molecular collisions, and  expressions for these transport properties can be derived from the kinetic theory. The  mass diffusion fluxes, $\mathbf{J}_s$, are computed using Fick's Law of Diffusion:
$$
    \mathbf{J}_s = - \rho D_s \nabla(Y_s) + Y_s \sum_k \rho D_k \nabla(Y_k)
$$

where $c_s$ is the species mass fraction and $D_s$ is the species multi-component diffusion coefficient. The  values of $D_s$ are computed as a weighted sum of binary diffusion coefficients between all species in the mixture. These are obtained by solving the Stefan--Maxwell equations under the Ramshaw approximations. The  viscous stress tensor is written as
$$
   \boldsymbol{\sigma} = \mu \left( \nabla \mathbf{u} + \nabla {\mathbf{u}}^\mathsf{T} - \frac{2}{3} \mathbf{I} (\nabla \cdot \mathbf{u}) \right),
$$
where $\mu$ is the mixture viscosity coefficient. The  conduction heat flux for each thermal energy mode, $\mathbf{q}^{k}$, is assumed to be given by Fourier’s Law of heat conduction:
$$
\mathbf{q}^{k} = \kappa^{k}  \nabla(T^k),
$$

where $\kappa^{k}$ is the thermal conductivity associated with energy mode $k$.

$D_s$, $\mu$, and $\kappa$ can be evaluated using the models discussed below by selecting the appropriate options in the configuration file.


## Wilkes-Blottner-Eucken ##

The mixture dynamic viscosity and thermal conductivity are computed using Wilke's semi-empirical mixing rule as 

$$
\mu = \sum_s \frac{X_s \mu_s}{\phi_s},
$$

and 

$$
\kappa = \sum_s \frac{X_s \kappa_s}{\phi_s},
$$

where $X_s$ is the mole fraction of species $s$. The species dynamic viscosity is computed using Blottner's three paramter curve fit for high temperature air,

$$
\mu_s = 0.1 \exp [(A_s\log(T) + B_s)\log(T) + C_s].
$$
 
The species thermal conductivities are computed according to Eucken's formula as

$$
\kappa^{tr}_s = \mu_s \left( \frac{5}{2} C_{v_s}^{trans} + C_{v_s}^{rot} \right),
$$

$$
\kappa^{ve}_s = \mu_s C^{ve}_{v_s}.
$$

And the term $\phi_s$ is given by
$$
\phi_s = \sum_r X_r \left[ 1 + \sqrt{\frac{\mu_r}{\mu_s}}\left( \frac{M_r}{M_s} \right)^{1/4} \right]^{2} \left[ \sqrt{8 \left(1 + \frac{M_s}{M_r} \right)} \right]^{-1}.
$$

The effective species diffusion coefficeint is copmuted as a weighted sum of the species binary diffusion coefficients

$$
\frac{(1 - X_i)}{D_i} = \sum_{i \neq j} \frac{X_j}{D_{ij}},
$$

where the binary diffusion coefficients are computed as

$$
\rho D_{ij} = 1.1613 \times 10^{-25} \frac{M \sqrt{T \left( \frac{1}{M_i} + \frac{1}{M_j} \right) }}{\Omega_{ij}^{(1,1)}},
$$

and the collision integral for the mass diffusion coefficient is computed as

$$
\pi \Omega_{ij}^{(1,1)} = D T^{A(\log(T))^2 + B \log(T) + C},
$$

where A-D are constants.

The Wilkes-Blottner-Eucken model is generally efective up to temperatures of 10,000 K. Above these temperatures it is recommended to use the Gupta-Yos model.

## Gupta-Yos ##

Aother model develped by Gupta focuses on the transport properties of weakly ionized flows, and is generally more  accurate than the Wilkes-Blottner-Eucken model at temperatures above 10,000 K.

The forumalae for the transport coefficients are dependent on the collision terms

$$
\Delta_{s,r}^{(1)}(T) = \frac{8}{3} \left[ \frac{2M_s M_r}{\pi R T (M_s + M_r)}  \right]^{1/2} \pi {\Omega_{s,r}^{(1,1)}}
$$

and 
$$
\Delta_{s,r}^{(2)}(T) = \frac{16}{5} \left[ \frac{2M_s M_r}{\pi R T (M_s + M_r)}  \right]^{1/2} \pi {\Omega_{s,r}^{(2,2)}}.
$$
The mixutre viscoisty is computed as

$$
\mu = \sum_{s \neq e} \frac{m_s \gamma_s}{\sum_{r \neq e} \gamma_r \Delta_{s,r}^{(2)}(T_{tr}) + \gamma_r \Delta_{e,r}^{(2)}(T_{ve})} + \frac{m_e \gamma_e}{\sum_r \gamma_r \Delta_{e,r}^{(2)}(T_{ve}) }
$$

where 

$$
\gamma_s = \frac{\rho_s}{\rho M_s}.
$$

Thermal conductivity is computed in terms of different energy modes. The contribution due to translation  modes is expressed as

$$
\kappa_t = \frac{15}{4} k_{B} \sum_{s \neq e} 
\frac{\gamma_s}{\sum_{r \neq e} a_{s,r} \gamma_r \Delta_{s,r}^{(2)}(T_{tr}) + 3.54 \gamma_e \Delta_{s,e}^{(2)}(T_{ve})},
$$

where

$$
a_{s,r} = 1 + \frac{\left[1 - (m_s/m_r) \right] \left[ 0.45 - 2.54(m_s/m_r)  \right]  }{\left[1 + (m_s/m_r) \right]^2}
$$

and where

$$
m_s = \frac{M_s}{N_{av}}
$$

with $N_{av}$ being Avogadro's Number. The thermal conductivity for the rotational modes is expressed as

$$
\kappa_r = k_{B} \sum_{s \neq e} 
\frac{\gamma_s}{\sum_{r \neq e} \gamma_r \Delta_{s,r}^{(1)}(T_{tr}) + \gamma_e \Delta_{s,e}^{(1)}(T_{ve})}.
$$

The mixture translational/rotational thermal conductivity can then be expressed as

$$
\kappa_{tr} = \kappa_t + \kappa_r.
$$

The vibrational/electronic mode thermal conductivity is 

$$
\kappa_{ve} = k_{B} \frac{C_{ve}}{R} \sum_{s \in molecules} \frac{\gamma_s}
{\sum_{r \neq e} \gamma_r \Delta_{s,r}^{(1)}(T_{tr}) + \gamma_e \Delta_{s,r}^{(1)}(T_{ve}) }
$$

and the thermal conductivity for electrons is given by

$$
\kappa_e = \frac{15}{4} k_{B} \frac{\gamma_e}{\sum_r 1.45 \gamma_r \Delta_{e,r}^{(2)}(T_{ve})}.
$$

Finally, the binary diffusion coefficient for heavy particles is given by

$$
D_{s,r} = \frac{k_{B} T_{tr}}{p \Delta_{s,r}^{(1)}(T_{tr})},
$$

and for electrons,

$$
D_{e,r} = \frac{k_{B} T_{ve}}{p \Delta_{e,r}^{(1)}(T_{ve})}.
$$

## Sutherland Viscosity Model ##

In addition to the two models discussed above, there is the option to use a Sutherland model to calculate the flow viscosity. The Sutherland model is not applicable at high temperatures.

In this case the viscosity is computed as

$$
\mu = \mu_{0} \left( \frac{T}{T_{0}} \right)^{3/2} \frac{T_0 + S_{\mu}}{T + S_{\mu}},
$$

where $T_0$ is a reference temperature (273.15 K), $\mu_0$ is a reference viscosity, and $S_{\mu}$ is the Sutherland constant.

If the Sutherland model is selected with a NEMO solver, species diffusion coefficients and thermal conductivity are computed using the models described in the Wilkes-Blottner-Eucken section.

---

# Slip Flow #

| Solver | Version | 
| --- | --- |
| `NEMO_EULER`, `NEMO_NAVIER_STOKES` | 7.0.0 |

SU2-NEMO uses the Maxwell velocity and Smoluchowski temperature jump  equations to compute the velocity and temperature of the gas in contact with the surface. The equations are given as
$$
v_s =  \frac{2 - \sigma}{\sigma} \lambda \frac{\partial v}{\partial n } + \\
\frac{3}{4} \frac{\mu}{\rho T} \frac{\partial T}{\partial x},
$$

and
$$
T - T_w =  \frac{2 - \alpha}{\alpha} \lambda \frac{2\gamma}{(\gamma + 1 )Pr} \frac{\partial T}{\partial n}, 
$$

respectively, where $\mu$ is the flow viscosity, $\rho$ is the mixture density, $Pr$ is the Prandtl number, $\gamma$ is the specific heat ratio, $T$ is the temperature of the gas, $T_w$ is the temperature of the surface, and~= $\lambda$ is the mean free path, calculated as
$$
    \lambda = \frac{\mu}{\rho} \frac{\pi}{\sqrt{2RT}}.
$$

The coefficients $\sigma$ and $\alpha$ are referred to as the Tangential Momentum Accommodation Coefficient (TMAC) and the Thermal Accommodation Coefficient (TAC), respectively. The values of the accommodation coefficients depend on the physical characteristics of the surface, and are usually determined empirically.


---

# Gas-surface Interaction #

| Solver | Version | 
| --- | --- |
| `NEMO_EULER`, `NEMO_NAVIER_STOKES` | 7.0.0 |

Mechanisms of gas-surface interaction are implemented as specific boundary conditions within the SU2-NEMO computational suite. The net result of recombination reactions occurring on the surface is a production of chemical species due to catalytic reactions, $\dot{\omega}_s^{cat}$, that must be balanced by the normal diffusive and convective flux at the wall. For steady flow and a no-slip boundary, this can be expressed as

$$
    \mathbf{J}_s  \cdot \mathbf{n}  = \dot{\omega}_s^{cat}.
$$

In SU2-NEMO, the chemical production of species due to catalytic processes is included in the computation of the viscous component of the residual, as an additional diffusive flux equivalent to the chemical source term computed due to catalytic reactions. Gradients of species density are then computed directly as part of the SU2-NEMO computational routine, which are used to compute gradients of species mass fraction at wall vertices. 

Options in SU2-NEMO include a super-catalytic wall in which species concentrations are set to specify full recombination to a specified equilibrium concentration (typically the free-stream conditions)

$$
Y_{w,s} = Y_{eq,s},
$$

as well as a partiall catalytic wall using a specified reaction efficiency model 

$$
    \dot{\omega}_s^{cat} = \gamma_s Y_s \rho_w \sqrt{\frac{R_s T_w}{2\pi}},
$$

where $\gamma_{s}$ is the species catalytic efficiency, and represents the proportion of incident mass flux of monatomic species $s$ which recombines into its heteronuclear diatomic molecule at the wall.

---
