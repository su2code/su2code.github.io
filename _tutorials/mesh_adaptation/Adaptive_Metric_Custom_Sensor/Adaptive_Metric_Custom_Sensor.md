---
title: Adaptive Metric with a Custom Sensor
permalink: /tutorials/Adaptive_Metric_Custom_Sensor/
written_by: bmunguia
for_version: 8.6.0
solver: RANS
requires: SU2_CFD, Python wrapper, mpi4py, ParaView
complexity: intermediate
follows: Adaptive_Metric_Builtin_Sensors
---

![Total pressure sensor](../../tutorials_files/mesh_adaptation/Adaptive_Metric_Custom_Sensor/images/sensor_total_pressure.png)

Figure (1): Total pressure around the NACA0012, computed in Python and used as a custom sensor (`Sensor_Total_pressure`).

## Goals

This tutorial computes the adaptive metric of a sensor that is not built into SU2, the total pressure, by defining it in Python. The following capabilities of SU2 are showcased:

- Custom sensors for the adaptive metric through the Python wrapper (`CustomSensorRegistry`)
- Built-in and custom sensors in the same run
- Adaptive metric of a turbulent (RANS) flow

It follows [Adaptive Metric with Built-In Sensors](/tutorials/Adaptive_Metric_Builtin_Sensors/), which explains the metric options and the visualization in ParaView.

## Resources

The resources for this tutorial can be found in the [mesh_adaptation/Adaptive_Metric_Custom_Sensor](https://github.com/su2code/Tutorials/tree/master/mesh_adaptation/Adaptive_Metric_Custom_Sensor) directory in the [tutorial repository](https://github.com/su2code/Tutorials). You will need the configuration file [rans_naca0012.cfg](https://github.com/su2code/Tutorials/tree/master/mesh_adaptation/Adaptive_Metric_Custom_Sensor/rans_naca0012.cfg), the mesh file [mesh_NACA0012_inv.su2](https://github.com/su2code/Tutorials/tree/master/mesh_adaptation/Adaptive_Metric_Custom_Sensor/mesh_NACA0012_inv.su2) and the Python script [metric.py](https://github.com/su2code/Tutorials/tree/master/mesh_adaptation/Adaptive_Metric_Custom_Sensor/metric.py). The ParaView script [size_ellipses_2d.py](https://github.com/su2code/Tutorials/tree/master/mesh_adaptation/size_ellipses_2d.py) is in the parent directory.

## Tutorial

It is assumed that SU2 has been compiled with the Python wrapper (`-Denable-pywrapper=true`, see the [build instructions](/docs_v7/Build-SU2-Linux-MacOS/)), that `mpi4py` is installed, and that the SU2 install directory is in your `PYTHONPATH`, so that both `pysu2` and the `SU2` Python package can be imported.

### Background

The built-in sensors of the adaptive metric are the primitive variables of the flow solver, the velocity magnitude, the Mach number and the solution variables of the turbulence, transition and species solvers (see [Adaptive Metric](/docs_v7/Adaptive-Metric/#sensors)). Any other scalar field can be used as a sensor by computing it in Python and passing it to SU2 before SU2 computes the metric.

The Mach number is the usual sensor for RANS adaptation, and it is built in. This tutorial uses the total pressure instead, to show how to define a custom sensor, and compares the two metrics. The total pressure is constant in the inviscid part of the flow outside of shocks, and drops in the boundary layers, the wake and across shocks.

### Problem Setup

The flow is the turbulent counterpart of the built-in sensor tutorial:

- Freestream Mach number = 0.8
- Angle of attack (AoA) = 1.25 deg
- Reynolds number = 6 × 10<sup>6</sup>, based on the chord
- Spalart-Allmaras turbulence model

### Mesh Description

The mesh is the inviscid mesh of the built-in sensor tutorial, with no boundary-layer cells. This is on purpose: the flow solution on this mesh is not accurate, but it is the starting point of an adaptation. The Hessian recovery is sensitive to highly stretched boundary-layer meshes, so RANS adaptations commonly start from a mesh like this one and let the adaptation create the boundary-layer resolution.

### Configuration File Options

```
% MESH ADAPTATION
%
COMPUTE_ADAPTIVE_METRIC= YES
NORMALIZE_ADAPTIVE_METRIC= YES
ADAPTIVE_METRIC_SENSOR= TOTAL_PRESSURE, MACH
ADAPTIVE_METRIC_CUSTOM_SENSOR= TOTAL_PRESSURE
ADAPTIVE_METRIC_NORM= 4
ADAPTIVE_METRIC_HMAX= 10.0
ADAPTIVE_METRIC_HMIN= 1.0e-6
ADAPTIVE_METRIC_COMPLEXITY= 10000
NUM_METHOD_HESS= GREEN_GAUSS
ADAP_TIME_SUBINTERVAL= 1
```

- `ADAPTIVE_METRIC_SENSOR` lists all sensors: the custom `TOTAL_PRESSURE` and the built-in `MACH`.
- `ADAPTIVE_METRIC_CUSTOM_SENSOR` marks `TOTAL_PRESSURE` as filled through the Python wrapper. Without it, SU2 would stop with an error, since `TOTAL_PRESSURE` is not a built-in sensor.
- `ADAPTIVE_METRIC_NORM= 4` concentrates the vertices more at the strongest features (the shock, the wake and the boundary layers) than the $$L^2$$-norm of the built-in sensor tutorial.

### The Python Script

`metric.py` defines the sensor as a function of the driver, which returns the sensor value at each domain node. It uses the primitive variables of the flow solver:

```python
def total_pressure(driver) -> list[float]:
    """Compute local total pressure at all nodes for compressible flow."""
    prim_idx = driver.GetPrimitiveIndices()
    nDim = driver.GetNumberDimensions()
    primVars = driver.Primitives()
    nNodes = driver.GetNumberNodes() - driver.GetNumberHaloNodes()

    gamma = 1.4
    coeff = 0.5 * (gamma - 1.0)
    exp_fac = gamma / (gamma - 1.0)
    press_col = prim_idx["PRESSURE"]
    vel_cols = [prim_idx["VELOCITY_X"], prim_idx["VELOCITY_Y"]]
    a_col = prim_idx["SOUND_SPEED"]
    if nDim == 3:
        vel_cols.append(prim_idx["VELOCITY_Z"])

    p_tot = [0.0] * nNodes
    for iNode in range(nNodes):
        row = primVars(iNode)
        p = row[press_col]
        a = row[a_col]
        vel2 = sum(row[k] ** 2 for k in vel_cols)
        mach2 = vel2 / (a * a)

        p_tot[iNode] = p * pow(1.0 + coeff * mach2, exp_fac)
    return p_tot
```

The main function registers the sensor with `CustomSensorRegistry`, runs the flow solver, and passes the sensor values to SU2 before the post-processing step, in which SU2 computes the Hessians and the metrics:

```python
def main():
    driver = pysu2.CSinglezoneDriver("rans_naca0012.cfg", 1, comm)

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

- `initialize` checks that each registered sensor is listed in `ADAPTIVE_METRIC_SENSOR`, and finds its index.
- `populate` evaluates each sensor function and passes the values to SU2. It must be called after the flow solution and before `Postprocess`.
- `FinalizeAdaptiveMetric` does nothing for a steady run. For an unsteady run, it normalizes the time-integrated metric and must be called after the last time step, before the last `Output`; `populate` must then be called at every time step.

### Running SU2

Run the script from the tutorial directory:

```bash
python metric.py
```

or in parallel, for example with 4 ranks:

```bash
mpirun -n 4 python metric.py
```

At startup, SU2 reports the custom sensor:

```
Resolving adaptive metric sensor indices.
  Sensor 'TOTAL_PRESSURE': custom (Python wrapper).
  Sensor 'MACH': computed.
Successfully resolved 2 adaptive metric sensors.
```

After the flow solution, SU2 computes the metrics from the sensor values passed by `populate`, and prints the normalization integral of each sensor:

```
Global adaptive metric normalization integral for sensor TOTAL_PRESSURE: 25985.7
Global adaptive metric normalization integral for sensor MACH: 13.7329
```

The volume file `flow.vtu` contains `Sensor_Total_pressure`, `Gradient_Total_pressure`, `Hessian_Total_pressure` and `AdaptiveMetric_Total_pressure`, and the same fields for the Mach number.

### Visualizing the Metric

Follow the [ParaView steps of the built-in sensor tutorial](/tutorials/Adaptive_Metric_Builtin_Sensors/#visualizing-the-metric-in-paraview), with `AdaptiveMetric_Total_pressure` or `AdaptiveMetric_Mach` in the Calculator expression for the vertex density, and `SENSOR = "Total_pressure"` in `size_ellipses_2d.py` for the ellipses.

#### Requested vertex density

![Vertex density of the total pressure metric](../../tutorials_files/mesh_adaptation/Adaptive_Metric_Custom_Sensor/images/metric_density_total_pressure.png)

Figure (2): Requested vertex density of the total pressure metric (log scale).

![Vertex density of the Mach metric](../../tutorials_files/mesh_adaptation/Adaptive_Metric_Custom_Sensor/images/metric_density_mach.png)

Figure (3): Requested vertex density of the Mach metric of the same run (log scale, same range as Figure 2).

#### Requested cell sizes and stretching

![Ellipses of the total pressure metric](../../tutorials_files/mesh_adaptation/Adaptive_Metric_Custom_Sensor/images/size_glyphs_total_pressure.png)

Figure (4): Cell sizes and stretching requested by the total pressure metric, drawn as ellipses colored by the Mach number over the initial mesh.

![Ellipses of the Mach metric](../../tutorials_files/mesh_adaptation/Adaptive_Metric_Custom_Sensor/images/size_glyphs_mach.png)

Figure (5): Cell sizes and stretching requested by the Mach metric of the same run, in the same view as Figure 4.

#### Comparison

The total pressure is constant outside of the boundary layers and the wake (Figure 1), so the total pressure metric requests the highest vertex density along the wall, especially near the leading edge, and in the wake (Figure 2). There, the ellipses are strongly stretched along the flow (Figure 4). Away from the airfoil, the total pressure is nearly constant, so its recovered Hessian is small and noisy: the requested density is low but irregular, and the ellipses are large and randomly oriented.

The Mach metric (Figures 3 and 5) also refines the wall and the wake, with sizing tensors stretched along the flow, as well as in the vicinity of the shocks.