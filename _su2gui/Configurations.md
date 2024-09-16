---
title: Configurations
permalink: /su2gui/configurations/
---

This section explains how to use the configuration file and Config Tab in SU2GUI. For an overview of what a configuration file is, please refer to the [configuration file](../../docs_v7/Configuration-File/) page.

## Loading a Configuration File
SU2GUI allows users to load a configuration file through both the GUI and the terminal. Loading the file is optional, as SU2GUI will create one if the user does not provide it. Before doing so, it is necessary for the user to initialize a Case. It is recommended to load the mesh file before the configuration file to set boundary condition properties and ensure proper functionality.

**Steps to load configuration file:**

 1. Start a new case and load mesh file. Follow these guides for detailed steps on [starting a new case](../Manage-Cases/#starting-a-new-case) and [loading a mesh file](../mesh-file).
 

 2. Click on the "Load Config File" option. ![](../../su2gui_files/User_guide/Configuration/button-config-file.png)
 

 3. In the pop-up window, choose the desired configuration file. ![](../../su2gui_files/User_guide/Configuration/choose-config-file.png)
 

 4.  The configuration file should now be loaded, and the properties in the GUI should be updated accordingly. ![](../../su2gui_files/User_guide/Configuration/loaded-config-file.png)



For instructions on loading a configuration file through the terminal, refer to the guide on [ Terminal Initialization](./../terminal-initialization).

## Config Tab

The Config Tab allows users to analyze and modify the current state of the Configuration File. It presents the data in JSON format, which is then converted into a configuration file for SU2 when the solver is initiated.

![Config Tab](../../su2gui_files/User_guide/Configuration/config-tab.png)

### Adding New Properties

User can add/modify Properties in configuration file using this. Place the Key in key textbox and Value in Value textbox. By default, Key is capitalised and preceding and trailing spaces are removed from the Key. Ways to add Value for property are given below:

- **Adding Float/Int**: The system attempts to convert all input into a float. If the conversion fails, it proceeds with other data types.
  
- **Adding Boolean**: The system recognizes "YES," "NO," "TRUE," and "FALSE" in any case (uppercase or lowercase) and stores them as boolean values.

- **Adding List**: When a list is added, it creates a list of elements and checks if each element is a digit. Below are examples of correct and incorrect list formats:



  | **Correct List**  | (outlet1, 101325, outlet2, 101325) | [outlet1, 101325, outlet2, 101325] | outlet1, 101325, outlet2, 101325 | outlet1 101325 outlet2 101325 |
  |-------------------|------------------------------------|------------------------------------|---------------------------------|--------------------------------|
  | **Incorrect List** | (outlet1, 101325, outlet2, 101325 | outlet1, 101325, outlet2, 101325} | outlet1, 101325 outlet2 101325 | outlet1101325 outlet2101325 |