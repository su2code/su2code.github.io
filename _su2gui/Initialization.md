---
title: Initialization

permalink: /su2gui/Initialization/
---

SU2GUI supports three methods for initializing a problem, which are available under the Initialization section of the menu:

- [**Uniform Initialization**](#uniform-initialization)
- [**Initialization using Restart File**](#initialization-using-restart-file)
- [**Patch Initialization**](#patch-initialization)

### Opening the Initialization Options

1. Start a new case and load the mesh file. Follow these guides for detailed steps on [starting a new case](./Manage-Cases/#starting-a-new-case) and [loading a mesh file](./mesh).

2. Navigate to the Initialization section from the left menu:  
   ![](../../su2gui_files/User_guide/initialization/initialize-options.png)

Follow the steps below according to the type of initialization needed.

---

## Uniform Initialization

As the name suggests, this method sets all points to a constant value, and a solution file is created for SU2.

**Steps for Uniform Initialization**

1. After opening the Initialization options, select **Uniform Initialization** from the drop-down menu.

2. Enter the required properties. The properties will vary depending on the selected Solver and Configurations.

3. Press the **Initialize** button. The problem will be initialized, and the visualization window will update accordingly.![](../../su2gui_files/User_guide/initialization/loaded-uniform-initialize.png)

---

## Initialization using Restart File

This method uses a Restart File to initialize the problem. SU2GUI supports both `.dat` and `.csv` formats for restart files.

**Steps for Restart Initialization**

1. After opening the Initialization options, select **Restart File Initialization** from the drop-down menu.

2. Click on the **Load Restart File** option. ![](../../su2gui_files/User_guide/initialization/button-restart-file.png)

3. In the pop-up window, choose the desired restart file. ![](../../su2gui_files/User_guide/initialization/choose-restart-file.png)

4. The Restart file will be loaded, and the visualization window will update accordingly. ![](../../su2gui_files/User_guide/initialization/loaded-restart-file.png)

For instructions on loading a restart file through the terminal, refer to the guide on [ Terminal Initialization](./../terminal-initialization).

---

## Patch Initialization

SU2GUI currently supports three types of patch initialization: Plane, Sphere, and Box. In this method, a patch is created in the visualization window according to the inputs, and a solution file is generated for SU2.

**Steps for Patch Initialization**

1. After opening the Initialization options, select **Patch Initialization** from the drop-down menu.

2. Select type of Patch and enter the required properties for both zones. The properties will change according to the selected Solver and Configurations.

3. Press the **Initialize** button. The problem will be initialized, and the visualization window will update accordingly. ![](../../su2gui_files/User_guide/initialization/loaded-patch-initialize.png)
