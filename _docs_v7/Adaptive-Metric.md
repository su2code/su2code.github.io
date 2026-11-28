---
title: Adaptive Metric
permalink: /docs_v7/Adaptive-Metric/
---

This page explains how to compute the adaptive metric for anisotropic mesh adaptation: the options, the sensors and the output fields. For the theory, see [Metric-Based Anisotropic Mesh Adaptation](../Metric-Based-Mesh-Adaptation/). For worked examples, see the tutorials [Adaptive Metric with Built-In Sensors](/tutorials/Adaptive_Metric_Builtin_Sensors/) and [Adaptive Metric with a Custom Sensor](/tutorials/Adaptive_Metric_Custom_Sensor/).

---

- [Limitations](#limitations)
- [Workflow](#workflow)
- [Options](#options)
- [Sensors](#sensors)
  - [Built-In Sensors](#built-in-sensors)
  - [Custom Sensors](#custom-sensors)
- [Choosing the Norm](#choosing-the-norm)
- [Size and Aspect Ratio Limits](#size-and-aspect-ratio-limits)
- [Steady and Unsteady Flows](#steady-and-unsteady-flows)
- [Output Fields](#output-fields)

---

## Limitations

- SU2 computes the metric field only. Generating the adapted mesh (remeshing) and the adaptation loop are not yet supported.
- The metric is available for single-zone flow problems only. SU2 stops with an error for periodic boundaries, multizone problems, harmonic balance and the discrete adjoint.
- Only the Green-Gauss Hessian is available (`NUM_METHOD_HESS= GREEN_GAUSS`).
- Each sensor gets its own metric; metric intersection (to combine several sensors) and size gradation are not available.
- Only feature-based metrics are available; goal-oriented (adjoint-based) metrics are not, and the `GOAL` sensor is rejected.
- For unsteady flows, SU2 computes a single metric over the entire time series; adaptation over several time sub-intervals is not yet supported.

## Workflow

1. Choose one or more *sensors*, the scalar fields whose interpolation error the adapted mesh should control, for example the pressure and the Mach number.
2. Set `COMPUTE_ADAPTIVE_METRIC= YES` and list the sensors in `ADAPTIVE_METRIC_SENSOR`.
3. Set the target complexity (approximately the number of vertices of the adapted mesh), the norm and the size limits.
4. Add `ADAPTIVE_METRIC` to `VOLUME_OUTPUT` and run `SU2_CFD` (or the Python wrapper for custom sensors).
5. Pass the metric of the volume or restart output to a remesher.

For example:

```
COMPUTE_ADAPTIVE_METRIC= YES
ADAPTIVE_METRIC_SENSOR= ( PRESSURE, MACH )
ADAPTIVE_METRIC_NORM= 2
ADAPTIVE_METRIC_COMPLEXITY= 10000
ADAPTIVE_METRIC_HMIN= 1e-6
ADAPTIVE_METRIC_HMAX= 10.0
%
VOLUME_OUTPUT= ( COORDINATES, SOLUTION, PRIMITIVE, ADAPTIVE_METRIC )
```

## Options

The options are listed in the [Option Reference](../Option-Reference-adaptation-options/), with their defaults. The main ones are:

| Option | Meaning | Default |
| --- | --- | --- |
| `COMPUTE_ADAPTIVE_METRIC` | Compute the adaptive metric of each sensor. | `NO` |
| `ADAPTIVE_METRIC_SENSOR` | List of sensors (case-insensitive), see [Sensors](#sensors). | none, at least one is required |
| `ADAPTIVE_METRIC_CUSTOM_SENSOR` | Sensors of `ADAPTIVE_METRIC_SENSOR` filled through the Python wrapper. | `NONE` |
| `NORMALIZE_ADAPTIVE_METRIC` | Perform the $$L^p$$-norm normalization. With `NO`, the metric is the absolute value of the Hessian (integrated in time for unsteady flows). | `YES` |
| `ADAPTIVE_METRIC_NORM` | Norm p of the normalization, see [Choosing the Norm](#choosing-the-norm). | `2` |
| `ADAPTIVE_METRIC_COMPLEXITY` | Target complexity N. | `10000` |
| `ADAPTIVE_METRIC_HMIN` | Minimum cell size, one value or one per sensor. | `1e-8` |
| `ADAPTIVE_METRIC_HMAX` | Maximum cell size, one value or one per sensor. | `100` |
| `ADAPTIVE_METRIC_ARMAX` | Maximum cell aspect ratio, one value or one per sensor. | `1e6` |

The sizes are in mesh units. `ADAPTIVE_METRIC_HGRAD`, `ADAP_ITER` and `ADAP_COMPLEXITIES` are read only by the Python tools of the adaptation loop, not by `SU2_CFD`.

## Sensors

Each sensor in `ADAPTIVE_METRIC_SENSOR` gets its own metric, normalized with the same norm and complexity. SU2 does not combine the metrics of several sensors into one (metric intersection) yet.

### Built-In Sensors

SU2 matches each sensor name, case-insensitively, against these fields, in this order:

1. a custom sensor listed in `ADAPTIVE_METRIC_CUSTOM_SENSOR` (see below);
2. a primitive variable of the flow solver, for example `PRESSURE`, `DENSITY`, `TEMPERATURE`, `VELOCITY_X`, `VELOCITY_Y`, `VELOCITY_Z`, `LAMINAR_VISCOSITY` or `EDDY_VISCOSITY`;
3. a computed quantity: `VELOCITY` (velocity magnitude) or `MACH` (compressible solvers only);
4. a solution variable of another solver: `NU_TILDE` (SA), `TKE` and `DISSIPATION` (SST), `INTERMITTENCY` and `RE_THETA_T` (LM transition), `SPECIES_<i>` (species transport).

An unknown name stops SU2 with an error that lists the available sensors. At startup, SU2 prints how it resolved each sensor, for example for the 2D compressible solver:

```
  Sensor 'PRESSURE': primitive variable 3.
  Sensor 'MACH': computed.
```

### Custom Sensors

Any other scalar field can be used as a sensor through the Python wrapper. List it in both `ADAPTIVE_METRIC_SENSOR` and `ADAPTIVE_METRIC_CUSTOM_SENSOR`:

```
ADAPTIVE_METRIC_SENSOR= ( TOTAL_PRESSURE, MACH )
ADAPTIVE_METRIC_CUSTOM_SENSOR= ( TOTAL_PRESSURE )
```

Then register a function that returns the sensor value at each node with `CustomSensorRegistry` (from `SU2.adaptive_metric`), and call `populate` after the flow solution and before `Postprocess`, where SU2 computes the metric:

```python
from mpi4py import MPI
import pysu2
from SU2.adaptive_metric import CustomSensorRegistry

comm = MPI.COMM_WORLD
driver = pysu2.CSinglezoneDriver("config.cfg", 1, comm)
custom_sensors = CustomSensorRegistry({"TOTAL_PRESSURE": total_pressure})
custom_sensors.initialize(driver)

driver.Preprocess(0)
driver.Run()
custom_sensors.populate(driver)
driver.Postprocess()
driver.Update()
driver.Monitor(0)
driver.FinalizeAdaptiveMetric()
driver.Output(0)
driver.Finalize()
```

Each function takes the driver and returns a list with one value per domain node (or per node, including halo nodes). The [custom sensor tutorial](/tutorials/Adaptive_Metric_Custom_Sensor/) shows a complete example.

## Choosing the Norm

The norm p sets how the vertices are distributed (see [Optimal Metric](../Metric-Based-Mesh-Adaptation/#optimal-metric)). A larger p concentrates them in the regions of strongest curvature of the sensor, such as shocks and boundary layers, while a smaller p spreads them more evenly and also resolves weaker features. Recommended values:

- **Inviscid flows:** p = 1 or 2.
- **Viscous (RANS) flows:** p = 4. Both Park, Balan et al. (2019) and Alauzet and Frazza (2021) found that p = 4 converges faster than p = 2 for RANS, since p = 2 under-refines the boundary layers on coarse adapted meshes:
  - M. A. Park, A. Balan et al., "Verification of unstructured grid adaptation components", AIAA 2019-1723, 2019. [doi:10.2514/6.2019-1723](https://doi.org/10.2514/6.2019-1723)
  - F. Alauzet, L. Frazza, "Feature-based and goal-oriented anisotropic mesh adaptation for RANS applications in aeronautics and aerospace", *J. Comput. Phys.* 439, 110340, 2021. [doi:10.1016/j.jcp.2021.110340](https://doi.org/10.1016/j.jcp.2021.110340)

## Size and Aspect Ratio Limits

After the normalization, SU2 clips each metric so that the requested cell sizes lie between `ADAPTIVE_METRIC_HMIN` and `ADAPTIVE_METRIC_HMAX`, and the requested aspect ratio is at most `ADAPTIVE_METRIC_ARMAX`. Each limit takes either one value for all sensors, or one value per sensor of `ADAPTIVE_METRIC_SENSOR`, in the same order:

```
ADAPTIVE_METRIC_SENSOR= ( PRESSURE, MACH )
ADAPTIVE_METRIC_HMIN= ( 1e-4, 1e-3 )
ADAPTIVE_METRIC_HMAX= 10.0
```

The limits keep the metric well defined: `ADAPTIVE_METRIC_HMAX` and `ADAPTIVE_METRIC_ARMAX` bound the sizes where the Hessian is singular, for example in regions of nearly constant flow, and `ADAPTIVE_METRIC_HMIN` prevents null volume sizes, for example at discontinuities. They affect the complexity when they are active.

## Steady and Unsteady Flows

- **Steady flows.** SU2 computes the metric once, from the final solution.
- **Unsteady flows.** SU2 integrates the absolute value of the Hessians in time with the trapezoidal rule, using the time step that the solver actually takes (which may vary, for example with `UNST_CFL_NUMBER`). The first sample is the solution after the first time step, or the restart solution of an unsteady restart. SU2 normalizes the metric when the run stops (at `TIME_ITER`, `MAX_TIME` or time convergence), so only the last volume output holds the final metric; earlier outputs hold the running time integral. With the Python wrapper, call `driver.FinalizeAdaptiveMetric()` before the last `driver.Output()`.

For each sensor, SU2 prints the global integral used by the normalization:

```
Global adaptive metric normalization integral for sensor PRESSURE: 18523.8
```

## Output Fields

With `COMPUTE_ADAPTIVE_METRIC= YES`, the following volume output groups are available. In the field names, `<Sensor>` is the sensor name with only its first letter capitalized, for example `Pressure` or `Total_pressure`.

| Group | Fields | Content |
| --- | --- | --- |
| `SENSOR_VALUE` | `Sensor_<Sensor>` | Sensor value |
| `SENSOR_GRADIENT` | `Gradient_<Sensor>_x`, `_y` (, `_z`) | Green-Gauss gradient of the sensor |
| `SENSOR_HESSIAN` | `Hessian_<Sensor>_xx`, `_xy`, `_yy` (, `_xz`, `_yz`, `_zz`) | Green-Gauss Hessian of the sensor |
| `ADAPTIVE_METRIC` | `AdaptiveMetric_<Sensor>_xx`, `_xy`, `_yy` (, `_xz`, `_yz`, `_zz`) | Adaptive metric of the sensor |

The ParaView writers (`PARAVIEW`, `PARAVIEW_ASCII`, `PARAVIEW_LEGACY`) group the gradients as vectors and the Hessians and metrics as symmetric tensors, named `Gradient_<Sensor>`, `Hessian_<Sensor>` and `AdaptiveMetric_<Sensor>`. In 2D, the z components of the tensors are written as zero. By default, the restart file only contains the variables needed to restart the solver; with `WRT_RESTART_COMPACT= NO`, it also contains these fields, one column per component. The [built-in sensor tutorial](/tutorials/Adaptive_Metric_Builtin_Sensors/) shows how to visualize the metric in ParaView.
