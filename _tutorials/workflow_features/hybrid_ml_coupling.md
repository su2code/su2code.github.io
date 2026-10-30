---
layout: default
title: Hybrid PyTorch-SU2 Coupling
description: Examples of coupling SU2 with external ML libraries (PyTorch) via the Python Wrapper.
group: "Workflow Features"
---

# Hybrid Physics-ML Coupling with PyTorch

This tutorial demonstrates how to establish a bidirectional coupling between the SU2 solver and **PyTorch** using the standard Python Wrapper (`pysu2`).

Unlike offline training (where data is saved to disk and trained later), this workflow allows for **online (in-situ) learning**, where a neural network is trained on flow physics as the simulation progresses.

### Goals
1.  Execute the SU2 solver step-by-step via Python.
2.  Extract flow variables (e.g., `RMS_DENSITY`) from memory in real-time.
3.  Train a PyTorch surrogate model inside the MPI loop.
4.  Demonstrate the "Physics → ML" data bridge.

### Resources
The complete scripts and configuration files for this tutorial are available in the [SU2 Tutorials Repository](https://github.com/su2code/Tutorials/tree/master/PyWrapper/PyTorch_Coupling).

### Prerequisites
* **SU2** compiled with MPI and Python Wrapper support:
    * `-Dwith-mpi=enabled`
    * `-Denable-pywrapper=true`
* **Python packages**: `mpi4py`, `torch`, `numpy`

### The Coupling Loop
The core of the workflow is the `CSinglezoneDriver`, which allows Python to control the C++ solver iteration-by-iteration.

```python
# Initialize Driver with MPI
driver = pysu2.CSinglezoneDriver("inv_NACA0012.cfg", 1, MPI.COMM_WORLD)
driver.Preprocess(0)

# Training Loop
for i in range(n_iterations):
    # 1. Run Physics (SU2)
    driver.Run()
    
    # 2. Extract Data (C++ -> Python)
    physics_state = driver.GetOutputValue("RMS_DENSITY")
    
    # 3. Train Model (PyTorch)
    # ... standard pytorch forward/backward pass ...
    
    # 4. (Optional) Feedback
    # Update flow boundary conditions or deformations based on ML prediction.
