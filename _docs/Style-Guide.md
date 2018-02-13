---
title: Style Guide
permalink: /docs/Style-Guide/
---

SU2 is released under an open source license to facilitate its widespread use and development in the scientific computing community. To support uniformity and consistency in the style of the source code, a C++ style guide has been included on this page, and it is strongly encouraged that outside developers adhere to the guidelines dictated in the style guide to maintain readability of the source.

Any contributions from the scientific community at-large are encouraged and welcomed. Feel free to contact the development team at any time.

This document describes the conventions that will be used when implementing new features in SU2. This includes allowed syntactic and semantic language features, filename conventions, indentation conventions and more. The consistency is fundamental, it is very important that any programmer be able to look at another part of the code and quickly understand it, the uniformity in the style is a key issue. Some of the ideas expressed in this document comes from the Google C++ Style Guide (revision 3.188).

## C++ style guide

### Version numbering

Each code of the SU2 suite must have a release number following the rule Major.Patch, where the Major number is increased each time a new major update is performed and the Patch number is increased each time new features are added. The configuration file also has a number following the rule Major.Patch, where Major correspond with the SU2_CFD major version and Patch is increased with new changes.

### Standard conformance, and formatting

Source code must comply with the C++ ISO/ANSI standard. with respect to the formatting some recommendation can be made:
- Each line of text in your code should be at most 80 characters long.
- Non-ASCII characters should be rare, and must use UTF-8 formatting.
- Use only spaces (default indent is 2 spaces). You can set your editor to emit spaces when you hit the tab key.
- Sections in public, protected and private order, each indented one space.
- The hash mark that starts a preprocessor directive should always be at the beginning of the line.
- When you have a boolean expression that is longer than the standard line length, be consistent in how you break up the lines.

### Files, functions, and variables

Here some basic recommendation are made for creating files, functions, and variables:
- C++ filenames must have extension .cpp.
- C++ header filenames must have extension .hpp. In general, every .cpp file should have an associated .hpp file.
- C++ inline filenames must have extension .inl. Define functions inline only when they are small, say, 10 lines or less.
- All subprograms (subroutines of functions) must be contained in a class. Each parent class must be contained in a file with the same name as the class (plus extension ’.cpp’, and ’.hpp’). This implies that there can only be one parent class per file.
- When defining a function, parameter order is: inputs, then outputs.
- Order of includes. Use standard order for readability and to avoid hidden dependencies: C library, C++ library, other libraries', your project's.
- Prefer small and focused functions.
- Use overloaded functions (including constructors) only if a reader looking at a call site can get a good idea of what is happening without having to first figure out exactly which overload is being called.
- Local variables. Place a function's variables in the narrowest scope possible, and initialize variables in the declaration.
- Static or global variables of class type are forbidden: they cause hard-to-find bugs due to indeterminate order of construction and destruction.
- In the initialization, use 0 for integers, 0.0 for reals, NULL for pointers, and '\0' for chars.

### Classes

The classes are the key element of the object oriented programming, here some basic rules are specified.
In general, constructors should merely set member variables to their initial values. Any complex initialization should go in an explicit Init() method.
- You must define a default constructor, and destructor.
- Use the C++ keyword explicit for constructors with one argument.
- Use a struct only for passive objects that carry data; everything else is a class.
- Do not overload operators except in rare, special circumstances.
- Use the specified order of declarations within a class: public: before private:, methods before data members (variables), etc.

### Syntactic and semantic requirements

In this section you can find some basic rules for programming:
- All allocated memory must be deallocated at program termination.
- Read or write operations outside an allocated memory block are not allowed.
- Read or write outside index bounds in arrays or character variables are not allowed.
- No uninitialized/undefined values may be used in a way that could affect the execution.
- Local variables that are not used must be removed.
- Pointer variables must be initialized with NULL unless they are obviously initialized in some other way before they are used.
- Indentation will be two steps for each nested block-level.
- In the header file, at the beginning of each program unit (class, subroutine or function) there must be a comment header describing the purpose of this code. The doxygen format should be used.
- When possible, it is better to use #DEFINE with a physical meaning to simplify the code.
- The code must be compiled using doxygen to be sure that there is no warning in the commenting format.
- When describing a function the following tag must be used: \brie_, \para_\[in\], \para_\[out\], \retur_, \overload.
- Static or global variables of class type are forbidden: they cause hard-to-find bugs due to indeterminate order of construction and destructionUse 0 for integers, 0.0 for reals, NULL for pointers, and '\0' for chars.
- All parameters passed by reference must be labeled const. We strongly recommend that you use const whenever it makes sense to do so.
- In the code short, int, and the unsigned version of both must be used case depending.
- Code should be 64-bit and 32-bit friendly. Bear in mind problems of printing, comparisons, and structure alignment

### Naming

The most important consistency rules are those that govern naming. The style of a name immediately informs us what sort of thing the named entity is: a type, a variable, a function, a constant, a macro, etc., without requiring us to search for the declaration of that entity.

The following naming conventions for variables must be used:
- Geometry: Normal, Area (2D, and 3D), Volume (2D, and 3D), Coord, Position. Solution: Solution, Residual, Jacobian.
- Function names, variable names, and filenames should be descriptive; eschew abbreviation. Types and variables should be nouns, while functions should be "command" verbs.
- Elementary functions that set or get the value of a variable (e.g. Number) must be called as GetNumber(), or GetNumber(). Function names start with a capital letter and have a capital letter for each new word, with no underscores.
- Variable names are all lowercase, with underscores between words.
- The name for all the classes must start with the capital "C" letter, followed by the name of the class (capitalizing the first letter), if the name is composed by several words, all the words must be together, e.g.: CPrimalGrid.
- All the variables that are defined in a class must be commented using /\*< \brief \________.\*/.

### Comments

The documentation, and comments must be Doxygen friendly, here I include some basic features:
- Start each file with a copyright notice, followed by a description of the contents of the file.
- Every class definition should have an accompanying comment that describes what it is for and how it should be used.
- Declaration comments describe use of the function; comments at the definition of a function describe operation.
- In general the actual name of the variable should be descriptive enough to give a good idea of what the variable is used for.
- In your implementation you should have comments in tricky, non-obvious, interesting, or important parts of your code.
- Pay attention to punctuation, spelling, and grammar; it is easier to read well-written comments than badly written ones.
- Short, and long comments must be in inside of /\*--- (your comment here) ---\*/, and they must be located just before the line to be commented.
- Math comments are welcome and should be in the Latex language.

### Debugger tools

- The C++ code must support the following features for debugging:
- Array index bounds may be checked at runtime.
- Conformance with C++ may be checked.
- Use of obsolescent features may be reported as compilation warnings.
- Unused variables may be reported as compilation warnings.
- Iteration: iPoint, jPoint, kPoint, iNode, jNode, kNode, iElem, jElem, kElem, iDim, iVar, iMesh, iEdge.
