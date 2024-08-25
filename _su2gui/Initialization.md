---
title: Initialization

permalink: /su2gui/Initialization/
---

Initialization is the process of setting up the initial conditions and parameters required to start a simulation. Proper initialization is crucial as it significantly influences the convergence and accuracy of the simulation. By specifying initial values or states, you provide a starting point for the solver, which helps in stabilizing the simulation and achieving reliable results more efficiently.

SU2GUI supports three methods for initializing a problem, which are available under the Initialization section of the menu:

- [**Uniform Initialization**](#uniform-initialization)
- [**Initialization using Restart File**](#initialization-using-restart-file)
- [**Patch Initialization**](#patch-initialization)

### Opening the Initialization Options

1. Start a new case and load the mesh file. Follow these guides for detailed steps on [starting a new case](../Manage-Cases/#starting-a-new-case) and [loading a mesh file](../mesh-file).

2. Navigate to the Initialization section from the left menu:  
   ![](../../su2gui_files/User_guide/initialization/initialize-options.png)

Follow the steps below according to the type of initialization needed.

---

## Uniform Initialization

**Description**: This method involves assigning a single set of initial values (like pressure, velocity, temperature, etc.) uniformly across the entire computational domain.

**Use Case**: Uniform initialization is commonly used when you have little prior knowledge about the flow field or when you want to start with a simple baseline.

**Steps for Uniform Initialization**

1. After opening the Initialization options, select **Uniform Initialization** from the drop-down menu.

2. Enter the required properties. The properties will vary depending on the selected Solver and Configurations.

3. Press the **Initialize** button. The problem will be initialized, and the visualization window will update accordingly.![](../../su2gui_files/User_guide/initialization/loaded-uniform-initialize.png)

---

## Initialization using Restart File

**Description**: This method uses a previously saved simulation state from a Restart file to initialize the current simulation.

**Use Case**: This is ideal for continuing simulations from where they left off or for testing variations without starting from scratch, which can save time and resources.

SU2GUI supports both `.dat` and `.csv` formats for restart files.

**Steps for Restart Initialization**

1. After opening the Initialization options, select **Restart File Initialization** from the drop-down menu.

2. Click on the **Load Restart File** option. ![](../../su2gui_files/User_guide/initialization/button-restart-file.png)

3. In the pop-up window, choose the desired restart file. ![](../../su2gui_files/User_guide/initialization/choose-restart-file.png)

4. The Restart file will be loaded, and the visualization window will update accordingly. ![](../../su2gui_files/User_guide/initialization/loaded-restart-file.png)

For instructions on loading a restart file through the terminal, refer to the guide on [ Terminal Initialization](./../terminal-initialization).

---

## Patch Initialization

**Description**: Patch initialization allows you to define different initial conditions for specific regions (or patches) within the computational domain.

**Use Case**: This method is useful for simulations with complex geometries or varying conditions, enabling more precise control over the initial state of the simulation.

SU2GUI currently supports three types of patch initialization: Plane, Sphere, and Box.

**Steps for Patch Initialization**

1. After opening the Initialization options, select **Patch Initialization** from the drop-down menu.

2. Select type of Patch and enter the required properties for both zones. The properties will change according to the selected Solver and Configurations.

3. Press the **Initialize** button. The problem will be initialized, and the visualization window will update accordingly. ![](../../su2gui_files/User_guide/initialization/loaded-patch-initialize.png)
