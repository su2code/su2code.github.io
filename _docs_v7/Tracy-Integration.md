---
title: Integrating Tracy Profiler with SU2
permalink: /docs_v7/Tracy-Integration/
---

- [Introduction](#introduction)
- [Compiling SU2 with Tracy](#compiling-su2-with-tracy)
- [Instrumenting SU2 Code](#instrumenting-su2-code)
- [Running the Profiler and Visualizing Data](#running-the-profiler-and-visualizing-data)
- [Conclusion](#conclusion)

---

## Introduction

Tracy is a high-performance, real-time profiler designed for C++ applications, offering nanosecond-resolution timing with minimal overhead. It is an excellent tool for profiling computationally intensive software like SU2, where traditional profilers such as Valgrind may introduce significant slowdowns. This guide provides step-by-step instructions for integrating Tracy with SU2, enabling users to analyze and optimize the performance of their CFD simulations effectively.

## Compiling SU2 with Tracy

To compile SU2 with Tracy support, follow these steps:

1. **Install Required Tools:**
   - Tracy requires Meson version >=1.3.0, which is newer than the version provided by SU2. Install it manually:
     ```bash
     pip install --user --upgrade meson
     ```
   - Install Ninja manually, as it is required for the build process:
     ```bash
     sudo apt install ninja-build
     ```

2. **Run the Preconfigure Script:**
   - Since the provided `meson.py` script is not used, run the preconfigure script to set up the build environment:
     ```bash
     ./preconfigure.py
     ```

3. **Configure and Build SU2:**
   - Configure the build with Tracy enabled using Meson:
     ```bash
     meson setup build_tracy -Dwith-mpi=disabled -Denable-mlpcpp=true --buildtype=debugoptimized -Dtracy_enable=true --prefix=<SU2_INSTALL_PATH>
     ```
   - Build and install SU2:
     ```bash
     ninja -C build_tracy install
     ```
   - Replace `<SU2_INSTALL_PATH>` with your desired installation directory.

This embeds the Tracy client into SU2 for profiling.

## Instrumenting SU2 Code

To profile a function in SU2, add Tracy macros to the source code. Here’s an example:

1. **Include the Tracy Header:**
   - Add this at the top of the source file:
     ```c++
     #include <tracy/Tracy.hpp>
     ```

2. **Instrument the Function:**
   - Use `ZoneScopedN` to mark the function for profiling:
     ```c++
     void MyFunction() {
         ZoneScopedN("MyFunction");
         // Function implementation
     }
     ```
   - The `"MyFunction"` label identifies this section in the Tracy GUI.

## Running the Profiler and Visualizing Data

After compiling and instrumenting SU2, profile and visualize the data as follows:

1. **Build the Tracy Server:**
   - Navigate to the Tracy directory: `cd <SU2_SOURCE_DIR>/subprojects/tracy`.
   - Build the profiler using CMake:
     ```bash
     cmake -B profiler/build -S profiler -DCMAKE_BUILD_TYPE=Release
     cmake --build profiler/build --config Release --parallel
     ```

2. **Launch the Tracy Profiler:**
   - Run the profiler:
     ```bash
     ./profiler/build/tracy-profiler
     ```
   - Click "Connect" in the GUI to wait for SU2.

3. **Run the SU2 Simulation:**
   - In a separate terminal, execute your simulation:
     ```bash
     <SU2_INSTALL_PATH>/bin/SU2_CFD <your_config_file>.cfg
     ```
   - Replace `<SU2_INSTALL_PATH>` and `<your_config_file>` with your installation path and configuration file.

The Tracy GUI will display real-time profiling data during the simulation.

## Conclusion

Integrating Tracy with SU2 equips users with a powerful, low-overhead tool for profiling and optimizing CFD simulations. Its real-time visualization and precise timing capabilities make it ideal for performance analysis. For advanced features, troubleshooting, or additional details, consult the [Tracy documentation](https://github.com/wolfpld/tracy/releases/latest/download/tracy.pdf).
