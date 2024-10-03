---
title: Log Tab and Errors
permalink: /su2gui/Logs-Errors/
---

The SU2 and SU2GUI logs provide essential information about the execution and performance of both the SU2 software and SU2GUI. These logs can be accessed and analyzed real-time on SU2GUI under LOGS Tab.


## SU2 Logs

![SU2 Log Tab](../../su2gui_files/User_guide/Logs/su2-logs.png)

The SU2 logs contain detailed information about the solver's execution, including convergence history, residual values, and solution progress. These logs are invaluable for identifying convergence issues, detecting numerical instabilities, and gaining insights into the overall simulation process.

Each SU2 log file is stored within the corresponding case folder and is unique to that specific case. To access the SU2 log for a particular case, you can download the case folder. Reviewing these log files allows for a detailed analysis of the solver's performance and the progress of individual simulations.

---
## SU2GUI Logs

![SU2GUI Log Tab](../../su2gui_files/User_guide/Logs/su2gui-logs.png)

The SU2GUI logs capture interactions and events within the graphical user interface. These logs are useful for understanding user actions, identifying errors or warnings, and tracking the workflow followed during a simulation setup.

Unlike the SU2 logs, the SU2GUI log file is updated and cleared each time SU2GUI is started. This ensures that the log file only contains information from the current session, preventing the accumulation of data from previous sessions.

---

## Error/Warn Message

![Error message](../../su2gui_files/User_guide/Logs/error-message.png)

In addition to capturing interactions and events within the graphical user interface, SU2GUI also displays any Error and Warning messages received in the log files as pop-up dialog box. This feature helps users quickly identify and address any issues or potential problems during the simulation setup or execution.

By presenting these messages in a pop-up format, SU2GUI ensures that users are immediately alerted to any errors or warnings, allowing for prompt action to be taken. This real-time feedback enhances the user experience and facilitates efficient troubleshooting.

### Importance of Log Analysis

Analyzing the SU2 and SU2GUI logs can provide valuable insights into the simulation process, help diagnose issues, and optimize the performance of your simulations. It is recommended to review these logs whenever you are troubleshooting or optimizing your SU2 simulations to ensure a smooth and efficient workflow.
