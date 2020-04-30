---
title: Writing Unit Tests
permalink: /docs/Writing-Unit-Tests/
---

This document covers the question "How do I write unit tests for SU2?"
Before reading this page, make sure you are familiar with the pages
[Running Unit Tests](/docs_v7/Running-Unit-Tests/) and 
[Build SU2 on Linux/MacOS](/docs_v7/Build-SU2-Linux-MacOS/).

This document is intended to be an introduction only. There are plenty of
details that are *not* covered in this document.  This omission is
intentional.  The Catch2 documentation is the best place to learn about
using Catch2, so this guide does not duplicate any discussion of the 
complex features of Catch2. These more complex features include:

+ Grouping tests into sections with similar setup or teardown 
+ Parameterized tests
+ Logging context to report alongside failures
+ Tests that are expected to throw exceptions
+ Hiding tests from the default list
+ Using Catch2 with a debugger
+ Custom matchers

Please refer to the Catch2 documentation for more information on these
capabilities.

## Catch2 Unit-Testing Framework

A unit-testing framework takes most of the boilerplate code out of unit
testing. There's no need to manually create a `main()` for each test,
nor do you need to write your own floating-point matcher. A good unit-testing
framework also provides many command-line tools, such as filtering the tests
and controlling the output.
Catch2 was chosen for the unit testing library for the following reasons:

+ It can be included as a header-only library.
+ It has a very clean, easy-to-use syntax
+ It has widespread use, including the FEniCS library.

## Design Overview

+ Catch2 is included as a header file in the `externals` folder, and is
  distributed with the SU2 source code.
+ All tests are placed in a top-level directory named `UnitTests`.  Inside this directory is a structure just like the existing folder structure (e.g. `SU2_CFD/numerics`), except that there are not separate `src` and `include` folders.
+ Tests are grouped by class, and put in files such as `CNumerics_tests.cpp`.
+ A single test executable is compiled and run, as opposed to a separate test executable for each group of tests.  With the single test executable, you can always filter down to groups of tests or individual tests.
+ When `ninja test` or `meson test` is run, the test executable is only run once, sweeping through all the unit tests.  The result only shows a single failure or a single success.  If more detail is desired, then the test executable can be run manually.
+ The relevant SU2 code is compiled as a library (e.g. `libSU2core`) and then linked into both the main executable (`SU2_CFD`) and the test program (`test_driver`).

## Writing a Basic Unit Test 

There are many working examples of unit tests within the SU2 codebase.
To see them, browse the folder `UnitTests/`.  For an introduction, a simple
example is given here.  In order to add this test, the developer would create
a `.cpp` file with something like the following lines:

```
#include "catch.hpp"

TEST_CASE("Addition", "[arithmetic]") {

  int a = 2, b = 2;
 
  REQUIRE(a + b == 4);

}
```

+ The header `catch.hpp` contains the macros used for unit tests.  These
  macros replace a lot of the boilerplate code needed for testing.
+ `TEST_CASE` is used to define a test case. Each unit test *must* start with
  this macro.
+ Here, `Addition` is the name of the test case.  The name is a proper,
  string, and can have spaces, numbers, or puncutation.  This stands in
  contrast to many unit-testing frameworks, such as Boost test or Google
  test, where the test names must be valid C++ variable names.
+ The second argument, `[arithmetic]` is a tag.  Tags are used to group
  related tests together, even if they occur in different test cases or
  files.
+ `REQUIRE()` is similar to `assert()`.  It checks that the contained logical
  statement is true.  If not, it will display relevant error messages.
+ You can also use the macro `CHECK()`.  This also checks if the contained
  logical statment is true, but it does not stop on the first failure.  It
  will record the results and continue execution, whether or not the check
  is true.

For more detail on writing tests, please visit Catch2's documentation.

## Adding the Unit Test to the Test Driver

In order to run the unit test, it must be added to the meson build scripts.
Add the new `.cpp` file to `UnitTests/meson.build`. This will tell meson
to build your unit test, then run it using the test driver provided by Catch2.

## Floating Point Unit Tests

An important part of unit testing in scientific computing is floating
point comparisons. For tests with floating point numbers, it is not proper
to require a strong equality. Instead, Catch2 provides the wrapper
class `Approx`. `Approx` can be placed on either side of an equality
to indicate that two floating-point numbers are only *approximately* equal.

For example:
```
REQUIRE(volume == Approx(0.85478577));
```

The type of approximation and the precision can be customized.  For more
detail on these customizations, please see Catch2's documentation. 
Alternatively, Catch2 also supplies custom matchers for use with
floating-point numbers.  These include `WithinAbs`, `WithinULP`,
and `WithinRel`.

## Directdiff and AD Tests

You can also write tests that involve algorithmic differentiation (AD)
and direct differentiation (DD). There are a few things that must be done
differently when writing these tests:

- The test must be linked with the correct AD or DD libraries.  To do
  so, add the test to the meson lists `su2_cfd_tests_ad` or
  `su2_cfd_tests_dd`, respectively, in `UnitTests/meson.build`.
- When using the `su2double` datatype in and AD or DD build, the value
  stored in su2double is accessed using `SU2_TYPE::GetValue()`.  A simple
  assert such as `CHECK(y == Approx(64.0)` will fail to compile
  if `y` is an su2double. This is because you're trying to compare an
  su2double object, with both values and derivatives, with a float. The
  correct form to use is `CHECK(SU2_TYPE::GetValue(y) == Approx(64.0))`
  (and you can also use `REQUIRE`).

## Real Examples

If you find the above examples a bit simplistic, then you can refer to the
following files to find simple, real-world unit-tests:

- `UnitTests/SU2_CFD/numerics/CNumerics_tests.cpp`
- `UnitTests/Common/geometry/primal_grid/CPrimalGrid_tests.cpp`
- `UnitTests/Common/geometry/dual_grid/CDualGrid_tests.cpp`
- `UnitTests/Common/simple_ad_test.cpp`
- `UnitTests/Common/simple_directdiff_test.cpp`

## FAQ

### Where can I learn more about unit tests?

The following two books are great introductions to software testing:

+ "Working Effectively with Legacy Code," by Michael Feathers
+ "Modern C++ Programming with Test-Driven Development," by Jeff Langr
