---
title: Terminal Initialization
permalink: /su2gui/Terminal-Initialization/
---

SU2GUI can be initialized directly from the terminal, allowing users to provide the Case Name and other relevant files during initialization.

### Usage

The basic syntax for initializing SU2GUI from the terminal is as follows:

      usage: SU2_GUI [-h] [-p PORT] [-c CASE] [-m MESH] [--config CONFIG] [--restart RESTART]


### Options

- `-h, --help`  
  Displays the help message and exits.

- `-p , --port PORT`  
  Specifies the port to be used. The default port is `8080`.

- `-c , --case CASE`  
  Defines the name of the case to start with.

- `-m , --mesh MESH`  
  Specifies the path to the SU2 mesh file in `.su2` format.

- `--config CONFIG`  
  Specifies the path to the configuration file in `.cfg` format.

- `--restart RESTART`  
  Specifies the path to the restart file in `.csv` or `.dat` format.

### Important Notes

- **Case Name Requirement**: The Case Name must be provided for the initialization of the MESH, CONFIG, or RESTART file. Without specifying a Case Name, these files cannot be initialized.

- All the options mentioned above are completely optional. Users can choose to provide any combination of these options based on their requirements.

### Example Command

To initialize SU2GUI with a specific case name, port, mesh file, configuration file, and restart file, use the following command:


    SU2_GUI -p 5000 -c case_name -m path_to_mesh_file --config path_to_config_file --restart path_to_restart_file
