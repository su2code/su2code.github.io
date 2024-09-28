---
title: Result Analysis
permalink: /su2gui/Result-Analysis/
---

## Analyzing SU2 Output Files

When working with SU2, several key output files are generated that are crucial for analyzing the performance and results of your simulations. These files include `History.csv`, `Restart.csv`, and various files representing the current state of the solver. Understanding and analyzing these files is essential for extracting meaningful insights and further refining your simulations.

### History Tab

The `History.csv` file logs the convergence history of your simulation. It typically includes data such as iteration number, residuals, lift and drag coefficients, and other relevant metrics. By analyzing this file, you can:

- **Monitor Convergence**: Ensure your simulation is converging by tracking how residuals decrease over iterations.
- **Evaluate Performance**: Assess key metrics like lift and drag coefficients to determine the aerodynamic characteristics of your model.
- **Identify Issues**: Detect irregularities that may indicate problems with your simulation setup.

SU2GUI provides a convenient "History Tab" feature that allows you to visualize the `History.csv` file in real time, enabling you to monitor the convergence and track key metrics as they evolve. You can also select specific parameters to plot, enabling more focused analysis of key metrics.


![History Tab](../../su2gui_files/User_guide/result-analysis/history-tab.png)
---
### Geometry Tab

The `Restart.csv` file stores the simulation state at a specific point in time. It is essential for:

- **Real-Time Monitoring**: Track the solver's state in real time to monitor progress and make necessary adjustments.
- **Resuming Simulations**: Continue an interrupted simulation from the last saved state.
- **Debugging**: Examine the current state to identify and resolve issues if the simulation encounters problems.

SU2GUI offers a "Geometry Tab" feature that lets you visualize the `Restart.csv` file in real time, facilitating real-time monitoring.

![Geometry Tab](../../su2gui_files/User_guide/result-analysis/geometry-tab.png)
---
### Output Files for Further Analysis

SU2 generates various output files, such as:

- **Flow Field Data**: Velocity, pressure, and temperature distributions.
- **Surface Data**: Pressure and skin friction coefficients.
- **Visualization Files**: Files compatible with tools like ParaView.

SU2GUI allows you to download all output files from a case. For instructions on case management, refer to the [case installation procedure](../Manage-Cases/). By thoroughly analyzing these files, you can gain insights, validate models, and make informed decisions for future simulations.
