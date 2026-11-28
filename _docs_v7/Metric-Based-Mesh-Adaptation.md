---
title: Metric-Based Anisotropic Mesh Adaptation
permalink: /docs_v7/Metric-Based-Mesh-Adaptation/
---

| Solver | Version |
| --- | --- |
| `EULER`, `NAVIER_STOKES`, `RANS`, `INC_EULER`, `INC_NAVIER_STOKES`, `INC_RANS` | develop |

This page summarizes the theory behind the adaptive metric that SU2 computes for anisotropic mesh adaptation. For the options and output fields, see the [Adaptive Metric](../Adaptive-Metric/) user guide. For worked examples, see the tutorials [Adaptive Metric with Built-In Sensors](/tutorials/Adaptive_Metric_Builtin_Sensors/) and [Adaptive Metric with a Custom Sensor](/tutorials/Adaptive_Metric_Custom_Sensor/).

---

- [Limitations](#limitations)
- [Metric Fields](#metric-fields)
- [Optimal Metric](#optimal-metric)
- [Hessian Recovery](#hessian-recovery)
- [Unsteady Flows](#unsteady-flows)
- [Implementation in SU2](#implementation-in-su2)
- [References](#references)

---

## Limitations

See [Limitations](../Adaptive-Metric/#limitations) in the user guide for the supported solvers and features.

## Metric Fields

Anisotropic mesh adaptation uses a continuous analog of the mesh: a Riemannian metric field $$\mathbf{M} = (\mathcal{M}(\mathbf{x}))_{\mathbf{x} \in \Omega}$$, which defines a symmetric positive definite $$d \times d$$ tensor $$\mathcal{M}(\mathbf{x})$$ at every point of the domain $$\Omega$$, with $$d = 2$$ or $$3$$ (Loseille and Alauzet, 2011a). A metric-based remesher generates a mesh that is *unit* in this metric, i.e. all its edges have unit length, and all its elements unit volume, when measured with $$\mathcal{M}$$. The length of an edge $$\mathbf{ab}$$ is

$$\ell_\mathcal{M}(\mathbf{ab}) = \int_0^1 \sqrt{\mathbf{ab}^T \, \mathcal{M}(\mathbf{a} + t\,\mathbf{ab}) \, \mathbf{ab}} \; dt .$$

Since $$\mathcal{M}$$ is symmetric positive definite, it can be diagonalized in an orthonormal basis:

$$\mathcal{M} = \mathcal{Q} \Lambda \mathcal{Q}^T, \qquad \Lambda = \mathrm{diag}(\lambda_1, \dots, \lambda_d), \qquad h_i = \lambda_i^{-1/2} .$$

The eigenvectors (the columns of $$\mathcal{Q}$$) are the directions of the requested elements, and $$h_i$$ are the requested element sizes along them. The metric is therefore inversely proportional to the square of the sizing field: the size tensor $$\mathcal{M}^{-1/2} = \mathcal{Q} \Lambda^{-1/2} \mathcal{Q}^T$$ maps the unit ball of the Euclidean space onto the unit ball of $$\mathcal{M}$$, an ellipse (ellipsoid in 3D) with semi-axes $$h_i$$. A unit mesh in the metric space is thus an anisotropic mesh with these sizes and directions in the physical space.

The integral of the mesh density $$\sqrt{\det \mathcal{M}}$$ over the domain is known as the *complexity*

$$\mathcal{C}(\mathbf{M}) = \int_\Omega \sqrt{\det \mathcal{M}(\mathbf{x})} \; d\mathbf{x},$$

the continuous analog of the number of vertices: the number of vertices of a unit mesh is approximately proportional to $$\mathcal{C}(\mathbf{M})$$.

## Optimal Metric

The metric is chosen to control the linear interpolation error of a scalar *sensor* $$u$$ with Hessian $$\mathcal{H}$$, e.g. the pressure or the Mach number. For a mesh that is unit in $$\mathbf{M}$$, the local interpolation error is modeled by the continuous interpolation error (Loseille and Alauzet, 2011a)

$$e_\mathbf{M}(\mathbf{x}) = c_d \, \mathrm{tr}\!\left( \mathcal{M}^{-1/2}(\mathbf{x}) \, \lvert \mathcal{H}(\mathbf{x}) \rvert \, \mathcal{M}^{-1/2}(\mathbf{x}) \right),$$

with $$c_2 = 1/8$$ and $$c_3 = 1/10$$. Here, $$\lvert \mathcal{H} \rvert$$ is the matrix absolute value of the Hessian, which has the eigenvectors of $$\mathcal{H}$$ and the absolute values of its eigenvalues (see [Hessian Recovery](#hessian-recovery)). Using $$\lvert \mathcal{H} \rvert$$ instead of $$\mathcal{H}$$ overestimates the error where the Hessian is indefinite.

The optimal metric minimizes the $$L^p$$-norm of this error for a target complexity $$\mathcal{N}$$:

$$\mathbf{M}_{L^p} = \underset{\mathbf{M}}{\mathrm{argmin}} \; E_{L^p}(\mathbf{M}) = \left( \int_\Omega e_\mathbf{M}(\mathbf{x})^p \, d\mathbf{x} \right)^{1/p} \qquad \text{subject to} \qquad \mathcal{C}(\mathbf{M}) = \mathcal{N} .$$

The complexity constraint prevents the trivial solution of vanishing element sizes, and prescribes the target number of vertices of the adapted mesh. The problem is solved by a calculus of variations, and its unique solution is given by (Loseille and Alauzet, 2011b)

$$\mathcal{M}_{L^p}(\mathbf{x}) = \left( \frac{\mathcal{N}}{G} \right)^{2/d} D(\mathbf{x}) \, \lvert \mathcal{H}(\mathbf{x}) \rvert, \qquad D(\mathbf{x}) = \left( \det \lvert \mathcal{H}(\mathbf{x}) \rvert \right)^{-\frac{1}{2p+d}}, \qquad G = \int_\Omega \left( \det \lvert \mathcal{H}(\mathbf{x}) \rvert \right)^{\frac{p}{2p+d}} d\mathbf{x} .$$

The optimal metric is aligned with the eigenvectors of $$\lvert \mathcal{H} \rvert$$ and has the same anisotropy. The local term $$D$$ accounts for the sensitivity of the $$L^p$$-norm, and the global term $$G$$ enforces the complexity constraint. The corresponding error converges at second order with respect to the complexity, $$E_{L^p}(\mathbf{M}_{L^p}) \leq C \mathcal{N}^{-2/d}$$. As $$p \to \infty$$, the metric tends to the one that controls the error in the $$L^\infty$$ norm, which equidistributes the error and focuses on the largest scales of the solution; smaller values of $$p$$ also capture its weaker features.

## Hessian Recovery

SU2 computes the Hessian by applying the Green-Gauss approximation twice on the dual control volumes $$\Omega_i$$. First, the nodal gradient $$\nabla u$$ is computed from the nodal values of $$u$$. The Green-Gauss approximation is then applied to each component of $$\nabla u$$, with face values equal to the arithmetic mean of the nodal gradients, and the result is symmetrized:

$$\mathcal{H}_{kl} = \frac{1}{2 \lvert \Omega_i \rvert} \sum_f \left[ \left( \frac{\partial u}{\partial x_k} \right)_f n_{f,l} + \left( \frac{\partial u}{\partial x_l} \right)_f n_{f,k} \right],$$

where $$\mathbf{n}_f$$ is the area-weighted normal of face $$f$$. The absolute value is obtained from the eigendecomposition $$\mathcal{H} = \mathcal{Q} \Lambda \mathcal{Q}^T$$:

$$\lvert \mathcal{H} \rvert = \mathcal{Q} \, \lvert \Lambda \rvert \, \mathcal{Q}^T, \qquad \lvert \Lambda \rvert = \mathrm{diag}\left( \max(\lvert \lambda_1 \rvert, \epsilon), \dots, \max(\lvert \lambda_d \rvert, \epsilon) \right),$$

where $$\epsilon$$ is a small lower bound on the eigenvalues, so that $$\lvert \mathcal{H} \rvert$$, and therefore the metric, is symmetric positive definite by construction.

## Unsteady Flows

For unsteady flows, the simulation $$[0, t_f]$$ is divided into $$T$$ sub-intervals $$\mathcal{S}^i = [t^i, t^{i+1}]$$, with one mesh per sub-interval (Alauzet, Loseille and Olivier, 2018). The mesh of a sub-interval must control the error over the whole sub-interval, so the Hessian in the optimal metric is replaced by the time integral of its absolute value, the *Hessian-metric*

$$\mathcal{H}^i(\mathbf{x}) = \int_{\mathcal{S}^i} \lvert \mathcal{H}(\mathbf{x}, t) \rvert \; dt \approx \sum_k \frac{\Delta t_k}{2} \left( \lvert \mathcal{H}(\mathbf{x}, t^{k-1}) \rvert + \lvert \mathcal{H}(\mathbf{x}, t^k) \rvert \right),$$

which is approximated with the trapezoidal rule over the time steps of the sub-interval. With a constant time step and sub-intervals of equal length, minimizing the space-time interpolation error for an average spatial complexity $$\mathcal{N}$$ per sub-interval gives

$$\mathcal{M}^i(\mathbf{x}) = \left( \frac{T \mathcal{N}}{G} \right)^{2/d} \left( \det \mathcal{H}^i(\mathbf{x}) \right)^{-\frac{1}{2p+d}} \mathcal{H}^i(\mathbf{x}), \qquad G = \sum_{j=0}^{T-1} \int_\Omega \left( \det \mathcal{H}^j(\mathbf{x}) \right)^{\frac{p}{2p+d}} d\mathbf{x} .$$

The global term now involves all sub-intervals, so the metric of any sub-interval can only be normalized once the whole simulation has been computed. The complexity allocated to each sub-interval is proportional to its contribution to G, so sub-intervals whose solution is harder to resolve get more vertices. For T = 1, this is the optimal metric of the previous section, applied to the time-integrated Hessian.

## Implementation in SU2

- **Sensors and options.** Each sensor in `ADAPTIVE_METRIC_SENSOR` gets its own metric. The target complexity $$\mathcal{N}$$ is `ADAPTIVE_METRIC_COMPLEXITY`, the norm $$p$$ is `ADAPTIVE_METRIC_NORM`, and $$T$$ is `ADAP_TIME_SUBINTERVAL` (currently always 1 in SU2). The integral $$G$$ is computed as a sum over the vertices, weighted by the volumes $$\lvert \Omega_i \rvert$$ of their dual control volumes, and is printed for each sensor.
- **Size and aspect ratio limits.** After the normalization, SU2 clips the eigenvalues of each metric to $$[1/h_{max}^2, 1/h_{min}^2]$$, then raises the smallest ones to at least $$\lambda_{max}/AR_{max}^2$$, with $$h_{min}$$, $$h_{max}$$ and $$AR_{max}$$ set by `ADAPTIVE_METRIC_HMIN`, `ADAPTIVE_METRIC_HMAX` and `ADAPTIVE_METRIC_ARMAX`.
- **Unsteady flows.** SU2 accumulates the Hessian-metric over the whole run, as a single sub-interval, and normalizes it when the run stops.

## References

- A. Loseille, F. Alauzet, "Continuous mesh framework part I: well-posed continuous interpolation error", *SIAM J. Numer. Anal.* 49(1), 38–60, 2011 (2011a). [doi:10.1137/090754078](https://doi.org/10.1137/090754078)
- A. Loseille, F. Alauzet, "Continuous mesh framework part II: validations and applications", *SIAM J. Numer. Anal.* 49(1), 61–86, 2011 (2011b). [doi:10.1137/10078654X](https://doi.org/10.1137/10078654X)
- F. Alauzet, A. Loseille, G. Olivier, "Time-accurate multi-scale anisotropic mesh adaptation for unsteady flows in CFD", *J. Comput. Phys.* 373, 28–63, 2018. [doi:10.1016/j.jcp.2018.06.043](https://doi.org/10.1016/j.jcp.2018.06.043)
