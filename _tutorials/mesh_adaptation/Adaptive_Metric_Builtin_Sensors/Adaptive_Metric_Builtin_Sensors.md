---
title: Adaptive Metric with Built-In Sensors
permalink: /tutorials/Adaptive_Metric_Builtin_Sensors/
written_by: bmunguia
for_version: develop
solver: Euler
requires: SU2_CFD, ParaView
complexity: basic
follows:
---

![Size tensor glyphs](../../tutorials_files/mesh_adaptation/Adaptive_Metric_Builtin_Sensors/images/size_glyphs_pressure.png)

Figure (1): Cell sizes and stretching requested by the pressure metric around the NACA0012, drawn as ellipses colored by the Mach number over the initial mesh.

## Goals

This tutorial computes the adaptive metric of a transonic, inviscid flow around the NACA0012 airfoil, and shows how to visualize it in ParaView. The following capabilities of SU2 are showcased:

- Computation of the adaptive metric for anisotropic mesh adaptation
- Built-in sensors (a primitive variable and a computed quantity)
- $$L^p$$-norm normalization with size limits
- Tensor output for ParaView, and visualization of the requested cell sizes

SU2 computes the metric only; it does not generate the adapted mesh. The adaptation loop with a remesher is WIP.

## Resources

The resources for this tutorial can be found in the [mesh_adaptation/Adaptive_Metric_Builtin_Sensors](https://github.com/su2code/Tutorials/tree/master/mesh_adaptation/Adaptive_Metric_Builtin_Sensors) directory in the [tutorial repository](https://github.com/su2code/Tutorials). You will need the configuration file [inv_naca0012.cfg](https://github.com/su2code/Tutorials/tree/master/mesh_adaptation/Adaptive_Metric_Builtin_Sensors/inv_naca0012.cfg) and the mesh file [mesh_NACA0012_inv.su2](https://github.com/su2code/Tutorials/tree/master/mesh_adaptation/Adaptive_Metric_Builtin_Sensors/mesh_NACA0012_inv.su2). The ParaView script [size_ellipses_2d.py](https://github.com/su2code/Tutorials/tree/master/mesh_adaptation/size_ellipses_2d.py), shared by the mesh adaptation tutorials, is in the parent directory [mesh_adaptation](https://github.com/su2code/Tutorials/tree/master/mesh_adaptation).

## Tutorial

The following sections explain the configuration, run the case and visualize the metric. It is assumed that SU2_CFD has been compiled and is in your path. If not, see the [Download](/docs_v7/Download/) and [Installation](/docs_v7/Installation/) pages.

### Background

A metric field is a symmetric positive definite tensor $$\mathcal{M}$$ at every point. It prescribes the mesh that a remesher should build, a mesh that is unit in the metric: its eigenvectors are the directions of the cells, and its eigenvalues $$\lambda_i$$ give the requested cell sizes $$h_i = \lambda_i^{-1/2}$$ along them. SU2 computes, for each *sensor* field $$u$$, the metric that minimizes the $$L^p$$ norm of the interpolation error of $$u$$ for a target complexity $$\mathcal{N}$$ (approximately the number of vertices):

$$\mathcal{M}(\mathbf{x}) = \left( \frac{\mathcal{N}}{G} \right)^{2/d} \left( \det \lvert \mathcal{H}(\mathbf{x}) \rvert \right)^{-\frac{1}{2p+d}} \lvert \mathcal{H}(\mathbf{x}) \rvert, \qquad G = \int_\Omega \left( \det \lvert \mathcal{H}(\mathbf{x}) \rvert \right)^{\frac{p}{2p+d}} d\mathbf{x},$$

where $$\lvert \mathcal{H} \rvert$$ is the absolute value of the Hessian of the sensor and $$d$$ the number of dimensions. See [Metric-Based Anisotropic Mesh Adaptation](/docs_v7/Metric-Based-Mesh-Adaptation/) for the theory and [Adaptive Metric](/docs_v7/Adaptive-Metric/) for all options.

### Problem Setup

The flow is the transonic case of the [QuickStart](/docs_v7/Quick-Start/) tutorial:

- Freestream Mach number = 0.8
- Angle of attack (AoA) = 1.25 deg

It has a strong shock on the upper surface and a weaker one on the lower surface, which the metric should resolve with cells stretched along the shocks.

### Mesh Description

The mesh is the unstructured triangular mesh of the QuickStart tutorial, with 5233 vertices and 10216 triangles, an Euler wall on the airfoil and a far-field boundary.

### Configuration File Options

The flow options are those of an inviscid steady case. The adaptive metric is set up by:

```
% MESH ADAPTATION
%
COMPUTE_ADAPTIVE_METRIC= YES
NORMALIZE_ADAPTIVE_METRIC= YES
ADAPTIVE_METRIC_SENSOR= PRESSURE, MACH
ADAPTIVE_METRIC_NORM= 2
ADAPTIVE_METRIC_HMAX= 10.0
ADAPTIVE_METRIC_HMIN= 1.0e-6
% ADAPTIVE_METRIC_ARMAX= 10.0
ADAPTIVE_METRIC_COMPLEXITY= 10000
NUM_METHOD_HESS= GREEN_GAUSS
ADAP_TIME_SUBINTERVAL= 1
```

- `ADAPTIVE_METRIC_SENSOR` lists two sensors: the pressure, a primitive variable, and the Mach number, which SU2 computes. Each sensor gets its own metric.
- `ADAPTIVE_METRIC_NORM= 2` and `ADAPTIVE_METRIC_COMPLEXITY= 10000` select the $$L^2$$ norm of the interpolation error and a target of about 10000 vertices, about twice the current mesh.
- `ADAPTIVE_METRIC_HMIN` and `ADAPTIVE_METRIC_HMAX` bound the requested cell sizes, in mesh units (the chord is 1). The far field is about 20 chords away, so `ADAPTIVE_METRIC_HMAX= 10.0` lets the metric coarsen there. The maximum aspect ratio is left at its default, 10<sup>6</sup>.

The metric and the fields it is computed from are written with the volume output groups `SENSOR_VALUE`, `SENSOR_GRADIENT`, `SENSOR_HESSIAN` and `ADAPTIVE_METRIC`:

```
VOLUME_OUTPUT= ( COORDINATES, SOLUTION, PRIMITIVE, SENSOR_VALUE, SENSOR_GRADIENT, SENSOR_HESSIAN, ADAPTIVE_METRIC, VOLUME, TOTAL_VOLUME )
OUTPUT_FILES= ( RESTART, PARAVIEW )
WRT_RESTART_COMPACT= NO
```

### Running SU2

Run the case from the tutorial directory:

```bash
SU2_CFD inv_naca0012.cfg
```

or in parallel, for example with 4 ranks:

```bash
mpirun -n 4 SU2_CFD inv_naca0012.cfg
```

At startup, SU2 reports how it resolved the sensors:

```
Resolving adaptive metric sensor indices.
  Sensor 'PRESSURE': primitive variable 3.
  Sensor 'MACH': computed.
Successfully resolved 2 adaptive metric sensors.
```

The flow solver runs until the density residual has dropped by three orders of magnitude. SU2 then computes the Hessians and the metrics, and prints the normalization integral of each sensor:

```
------------------------ Compute Adaptive Metric ------------------------
Storing sensor values needed for the adaptive metric.
Computing Hessians using Green-Gauss.
Computing feature-based adaptive metric tensor.
Global adaptive metric normalization integral for sensor PRESSURE: 18523.8
Global adaptive metric normalization integral for sensor MACH: 9.5526
```

The volume file `flow.vtu` contains:

- `Sensor_Pressure` and `Sensor_Mach`, the sensor values;
- `Gradient_Pressure` and `Gradient_Mach`, the Green-Gauss gradients (vectors);
- `Hessian_Pressure` and `Hessian_Mach`, the Green-Gauss Hessians (symmetric tensors);
- `AdaptiveMetric_Pressure` and `AdaptiveMetric_Mach`, the metrics (symmetric tensors).

The restart file `restart_flow.dat` has the same fields as separate columns (`AdaptiveMetric_Pressure_xx`, `_xy`, `_yy`, ...), which is the form a remeshing script would read.

### Visualizing the Metric in ParaView

The metric eigenvalues are $$1/h^2$$, so the metric is largest where the mesh should be finest and spans many orders of magnitude. Two derived quantities are easier to read:

- the **requested vertex density** $$\sqrt{\det \mathcal{M}} = 1/(h_1 h_2)$$, whose integral over the domain is the complexity;
- the **requested cell sizes**, drawn as ellipses whose axes are the eigenvectors of the metric and whose diameters are the requested sizes $$h_i$$.

The steps below were checked with ParaView 6.0. Open `flow.vtu`, click **Apply**, switch the view to 2D (the **2D/3D** button at the top left of the render view) and zoom to the airfoil.

#### Requested vertex density

1. Select `flow.vtu`, then **Filters → Alphabetical → Calculator**.
2. Set **Result Array Name** to `Density_Pressure` and the expression to `sqrt(AdaptiveMetric_Pressure_XX*AdaptiveMetric_Pressure_YY-AdaptiveMetric_Pressure_XY^2)`, the square root of the determinant of the 2D metric, and click **Apply**.
3. Color the Calculator output by `Density_Pressure`. In the **Color Map Editor**, enable **Use log scale when mapping data to colors**, since the density varies over several orders of magnitude.

Repeat with `AdaptiveMetric_Mach` for the Mach metric.

![Vertex density of the pressure metric](../../tutorials_files/mesh_adaptation/Adaptive_Metric_Builtin_Sensors/images/metric_density_pressure.png)

Figure (2): Requested vertex density of the pressure metric (log scale).

![Vertex density of the Mach metric](../../tutorials_files/mesh_adaptation/Adaptive_Metric_Builtin_Sensors/images/metric_density_mach.png)

Figure (3): Requested vertex density of the Mach metric (log scale, same range as Figure 2).

Both metrics request the highest vertex density at the leading and trailing edges, and a higher density in a band across the upper-surface shock and around the weaker shock on the lower surface. The density increases only moderately at the shocks, since the metric refines them anisotropically: it asks for small cells across the shock only. The Mach metric also refines the region above the upper surface and the wake behind the trailing edge more than the pressure metric.

#### Requested cell sizes and stretching

The script `size_ellipses_2d.py` draws the metric of one sensor as an unfilled ellipse at every vertex. The axes of each ellipse are the eigenvectors of the metric, and its diameters are the requested cell sizes.

1. Select `flow.vtu`, set its **Representation** to *Wireframe* and its color to a light gray, so the current mesh is shown behind the ellipses.
2. Select `flow.vtu`, then **Filters → Alphabetical → Programmable Filter**. Paste the contents of `size_ellipses_2d.py` into **Script**, and click **Apply**. The sensor is set by `SENSOR = "Pressure"` at the top of the script.

   If the filter fails with `module 'numpy' has no attribute 'in1d'` (ParaView builds that use NumPy 2.4 or later, such as some Linux distribution packages), run `import numpy; numpy.in1d = numpy.isin` in **View → Python Shell**, then delete the filter and add it again.
3. Color the ellipses by `Mach`. All point arrays of `flow.vtu` are copied to the ellipses, so any field can be used.

Setting `SCALE = 1` in the script draws the unit ball of the metric instead, whose semi-axes are the requested sizes.

![Size tensor glyphs at the shock](../../tutorials_files/mesh_adaptation/Adaptive_Metric_Builtin_Sensors/images/size_glyphs_shock.png)

Figure (4): requested cell sizes of the pressure metric at the upper-surface shock.

At the upper-surface shock, the ellipses are thin across the shock and long along it: the metric asks for small cells only in the direction in which the pressure jumps. Near the wall, they are stretched along the surface, and far from the airfoil they are nearly round. Near the weaker shock on the lower surface, the ellipses are less regular. There, the shock is spread over a few cells of the initial mesh, and the recovered Hessian is noisy; converging the flow solution further does not change this. The metric of a coarse initial mesh is only the first step of an adaptation, and it becomes more regular as the mesh is adapted.

### Things to Try

- Change `ADAPTIVE_METRIC_NORM`. A larger norm concentrates the vertices more at the shocks, a smaller one spreads them more evenly.
- Change `ADAPTIVE_METRIC_COMPLEXITY`. The requested sizes scale as $$\mathcal{N}^{-1/2}$$ in 2D; the shape of the metric does not change.
- Set `ADAPTIVE_METRIC_ARMAX= 10.0` (uncomment it in the configuration). Without it, the requested aspect ratio is below 10 at 99% of the vertices, but reaches about 130 at the shocks, so the limit mainly shortens the ellipses there.
- Set limits per sensor, for example `ADAPTIVE_METRIC_HMIN= ( 1.0e-4, 1.0e-3 )` for the pressure and Mach metrics.
- Set `NORMALIZE_ADAPTIVE_METRIC= NO` to write the absolute value of the Hessians instead of the normalized metrics.

To compute the metric of a sensor that is not built in, see [Adaptive Metric with a Custom Sensor](/tutorials/Adaptive_Metric_Custom_Sensor/).
