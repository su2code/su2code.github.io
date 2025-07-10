---
title: Running Unit Tests
permalink: /docs_v7/Running-Unit-Tests/
---

Unit tests are small tests of individual "units" of code.  They allow
developers and users to check that specific parts of the code are
behaving as expected.  These tests differ from integration or validation
tests, which test how different units of the code interact.

If you are building from source, you can run the unit tests yourself to
verify the the specific behaviors in the tests. Unit tests can never be
comprehensive; the unit tests may all pass even if there is a bug in the
code.

## Compiling Unit Tests

Unit tests are only supported with meson builds.  You must build from
source to build the unit tests.  They are not part of the pre-compiled
executables. For more information, see [Installation](/docs_v7/Installation.md),
and [Build SU2 on Linux/MacOS](/docs_v7/Build-SU2-Linux-MacOS/).

In order to compile the unit tests, add the flag `-Denable-tests=true`
to your meson configure call. Then, you can build and run the tests by
calling `ninja test`.

## Running Tests

There are three ways to run the main unit tests:

1. `meson test -C [builddir]`, where `[builddir]` is the build directory.
2. `ninja test -C [builddir]`, where `[builddir]` is the build directory.
3. `./UnitTests/test_driver` from the SU2 build directory.

If you have run `ninja install`, then the `test_driver` executable will
also be located in the `bin` directory where you have installed SU2. The
first option will call ninja, which will then run the `test_driver`
executable.  The second option will call the `test_driver` executable.
The last option, manually running the test driver, gives the most flexibility.
This help page will focus on the command-line options for that last option.

By default, Catch2 will only show the output from failing tests.  To also
see the output for failing tests, add the command line argument `-s` when
running the `test_driver` manually.

The above discussion over-simplifies the test driver setup. There
are actually three test drivers:
`test_driver`, `test_driver_AD`, and `test_driver_DD`.  These test drivers
are built or run depending on the type of installation (e.g. direcdiff,
autodiff). For the most common use-case, you will not have a directdiff
or autodiff build and will only use `test_driver`. If you call
`meson_test` or `ninja test`, the correct
drivers will run automatically.  For more on tests using algorithmic
differentiation or direct differentiation, see the section "AD and
Direct-differentiation tests" below.

### Selecting subsets of the tests

You can also filter tests in two ways. The most basic, top-level
grouping is by test cases. You can see all the test cases by running:
```
./UnitTests/test_driver --list-tests
```
You can then select a test case by name.  For example, if I want to run
the test case "Volume Computation", I would run:
```
./UnitTests/test_driver "Volume Computation"
```
Within each test case, the test sections form trees of arbitrary depth.
Each branch can be selected with the `-c` or the `--section` command line
argument. For example, if I want to run the test section "2D Edge" from
the test case "Volume Computation", I would run:
```
./UnitTests/test_driver "Volume Computation" -c "2D Edge"
```

Further sub-sections can be selected by chaining together multiple "-c"
selections, e.g.
```
./UnitTests/test_driver "Volume Computation" -c "Section Name" -c "Subsection Name"
```

You can also filter tests by tags.  To see all the available tags,
run:

```
./UnitTests/test_driver --list-tags
```

To run tests matching a specific tag, write the tag name in square braces
as an argument for the test driver.  For example, if I want to run the
tests with the tag "Dual Grid", I would run:

```
./UnitTests/test_driver "[Dual Grid]"
```

If you want to run tests matching any of multiple tags, then include them all
in the quotations, but keep the square brackets separate.  For example:

```
./UnitTests/test_driver "[Primal Grid], [Dual Grid]"
```

There is also a fundamental difference between
`"[Primal Grid], [Dual Grid]"` and `"[Primal Grid][Dual Grid]"`.  The first
selects all test matching *either* "Primal Grid" or "Dual Grid".
The second selects all tests matching *both* "Primal Grid" and "Dual Grid".
If that's confusing to you or you would like to know more, then please read
Catch2's documentation.

## AD and Direct-differentiation tests

While the above discussion focused on the `test_driver`, there are also
two additional test drivers for algorithmic differentiation (AD) and
direct-differentiation (DD). Because these executables need to be linked
to different libraries (normal vs AD vs DD libraries), each exists as a
standalone executable.  As an example, `test_driver_AD` will test the
SU2 libraries compiled with AD support.

Depending on your installation, one or two of these test drivers may be
missing.  This is normal.  SU2 will only install the test drivers that
match the compilation type you requested.  For example, neither
`test_driver_AD` nor `test_driver_DD` will be compiled if
you build SU2 with the default options `-Denable-autodiff=false` and
`-Denable-directdiff=false`.

To run the test drivers manually, you can run any of the three options
from the build directory.  If you installed the program, these test
drivers will also be found in the `bin` folder of your install directory:
```
./UnitTests/test_driver
./UnitTests/test_driver_AD
./UnitTests/test_driver_DD
```

## FAQ

#### What's the difference between a test case, a test section, and a tag?

Test cases are the highest level of organization.  Each test must belong
to exactly one test case.  Within a test case, test sections can be used
to organize related tests.  These test sections form a tree of arbitrary
depth.  Test sections allow multiple tests to share setup, teardown, or
data.  However, note that the tests are always run separately from start
to finish.  Even if two tests use the same data, the two tests cannot
interact.

Tags allow you to identify related tests.  One important detail is that each
test can have multiple tags. The tags can span multiple test sections.  Tags
allow complicated groupings of tests. Tags do not facilitate sharing of
setup, teardown, or data.
