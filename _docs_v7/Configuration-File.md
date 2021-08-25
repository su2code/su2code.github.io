---
title: Configuration File
permalink: /docs_v7/Configuration-File/
---

The configuration file is a text file that contains a user's options for a particular problem to be solved with the SU2 suite. It is specified as an input upon execution of SU2 components. This section briefly describes the file format and other conventions. 

The SU2 configuration file name typically carries a name of the form *filename.cfg*. The file extension .cfg is optional (this is our own convention), and the prefix can be any valid string with no spaces; e.g. config.cfg, su2-config.cfg, and flow_config.cfg are all suitable file names. 

**Note: An example configuration file, called config_template.cfg, can be found in the root SU2/ directory or [here](https://github.com/su2code/SU2/blob/master/config_template.cfg). The developers keep this file up to date with the latest options, and it serves as the first reference for the available options in SU2. It is a very important document because it supplements the documentation in this website.**

The configuration file consists of only three elements:
- **Options**. An option in the file has the following syntax: option_name = value, where option_name is the name of the option and value is the desired option value. The value element may be a scalar data type, a list of data types, or a more complicated structure. The "=" sign must come immediately after the option_name element and is not optional. Lists of data types may be formatted for appearance using commas, ()-braces, {}-braces, and []-braces, though this is not required. Semicolons are semantically relevant for several option types and may not be used as convenience delimiters. SU2 will exit with an error if there are options in the config file which do not exist or if there are options with improper formatting. Some example option formats are given below.
  - `FREESTREAM_VELOCITY = ( 5.0, 0.00, 0.00 ) % braces and commas can be used for list options`
  - `REF_ORIGIN_MOMENT= 0.25 0.0 0.0 % however, braces and commas are optional for lists`
  - `KIND_TURB_MODEL     = NONE % space between elements is not significant`
- **Comments**. On a given line in the file, any text appearing after a % is considered a comment and is ignored by SU2. Additional % signs after the first on a given line are not significant.
- **White space**. Empty lines are ignored. On text lines that define options, white space (tabs, spaces) can be used to format the appearance of the file

SU2 includes strict error checking of the config file upon execution of one of the C++ modules. For example, the code will throw errors if unknown options are specified, options appear more than once, extra text appears outside of comments, etc.
