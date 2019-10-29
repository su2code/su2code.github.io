---
title: Method of Manufactured Solutions (MMS) for the DG discretization of the Compressible Navier-Stokes
permalink: /vandv/FVM_Incomp_Navier_Stokes/
---

The compute_order_of_accuracy.py script drives the other files in this folder. Simply set the number of ranks on which to run the cases by modifying the 'nRank' variable at the top of the script and then execute with:

$ compute_order_of_accuracy.py

The script will automatically generate the required meshes and executed SU2 solutions for up to four different cases on those meshes for comparison. Four config files are provided, but you can modify them or add new ones. Simply change the config files listed at the top of the compute_order_of_accuracy.py script. Postprocessing is also automatically performed by the script, including the creation of figures for global error vs relative grid size and observed order of accuracy vs relative grid size.
