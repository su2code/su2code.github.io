---
title: Style Guide
permalink: /docs_v7/Style-Guide/
---

To support uniformity and consistency in the style of the source code, a C++ style guide has been included on this page, and it is strongly encouraged that outside developers adhere to the guidelines dictated in the style guide to maintain readability of the code.

Any contributions from the scientific community at-large are encouraged and welcomed. Feel free to contact the development team at any time.

This document describes the conventions that will be used when implementing new features in SU2. Consistency is fundamental, it is very important that any programmer be able to look at another part of the code and quickly understand it. Some of the ideas expressed in this document come from the Google C++ Style Guide, others from the [C++ Core Guidelines](https://github.com/su2code/SU2/issues/1218).

## C++ style guide

Below is summary of the rules we try to follow in SU2. **Older parts of SU2 are not good examples of these rules.**

**Duplicating code is absolutely not allowed.**

### Version numbering

The SU2 suite has a major release number followed the rule minor.path, where the minor number is increased each time a significant update is performed and the patch number is increased in maintenance releases.
Patch releases cannot break backward compatibility.

### Standard conformance, and formatting

SU2 is written for C++11, the formatting rules are defined in a `clang-format` file located in the root of the repository.
**New files must follow the formatting rules exactly.**

SU2 uses pre-commit to enforce a consistent formatting. To use, [install pre-commit](https://pre-commit.com/#install) and run `pre-commit install` at the root of the project. You can now force the formatting on all files with `pre-commit run -a`. This will also run all pre-commit hooks before each commit, preventing dirty commits in the repository.

### Files, functions, and variables

Basic recommendations for creating files, functions, and variables:
- C++ filenames must have extension .cpp.
- C++ header filenames must have extension .hpp. In general, every .cpp file should have an associated .hpp file.
- When defining a function, the parameter order is: inputs, then outputs.
- Order of includes. Use standard order for readability and to avoid hidden dependencies: C library, C++ library, other libraries', your project's.
- Write small and focused functions.
- Use overloaded functions (including constructors) only if a reader looking at a call site can get a good idea of what is happening without having to first figure out exactly which overload is being called.
- Local variables. Place a function's variables in the narrowest scope possible, and initialize variables in the declaration.
- Static or global variables of class type are forbidden.
- Make abundant use of `const`.
- Always use `su2double` for floating point variables, do not use `double`, `float`, or `auto`.
- Use `auto` or `auto&` or `auto*` for other types of variables.

### Code Documentation

Classes and functions must be documented with doxygen:
- Start each file with a copyright notice, followed by a description of the contents of the file.
- Every class/function definition must have an accompanying comment that describes what it is for and how it should be used.
- The code must be compiled using doxygen to be sure that there are no warnings in the commenting format.
- When describing a function or class the following tags must be used: `\brief`, `\param[in]`, `\param[out]`, `\return`, `\overload`.
- Do not document the obvious, but rather the expected behavior/usage or the class or function, use `\note` to add details of an algorithm, include links to literature when appropriate.
- In your implementation you should have comments in tricky, non-obvious, interesting, or important parts of your code.
- Pay attention to punctuation, spelling, and grammar; it is easier to read well-written comments than badly written ones.
- Short, and long comments must be in inside of /\*--- (your comment here) ---\*/, and they must be located just before the line to be commented.
- Math comments are welcome and should be in the Latex language.

### Naming

The consistency boat sailed a long time ago in SU2, the information below is more descriptive than prescriptive.

The following naming conventions are in use:
- Function names, variable names, and filenames should be descriptive; eschew abbreviation. Types and variables should be nouns, while functions should be "command" verbs.
- Elementary functions that set or get the value of a variable (e.g. Number) must be called as SetNumber(), or GetNumber(). Function names start with a capital letter and have a capital letter for each new word, with no underscores.
- The name for all the classes must start with the capital "C" letter, followed by the `NameOfTheClass` (camel case).
- Iteration: iPoint, jPoint, kPoint, iNode, jNode, kNode, iElem, jElem, kElem, iDim, iVar, iMesh, iEdge.

**Variable names**
- Acceptable styles are `lowerCamelCase` and `snake_case`.
- Member variables can be `CamelCase`, or be ended `with_underscore_`.
- Template parameters are `CamelCase`.
- Be consistent and follow the existing style if you are modifying or fixing code, do not increase entropy...

