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
     meson setup build -Dwith-mpi=disabled --buildtype=debugoptimized -Denable_tracy=true --prefix=<SU2_INSTALL_PATH>
     ```
   - Build and install SU2:
     ```bash
     ninja -C build install
     ```
   - Replace `<SU2_INSTALL_PATH>` with your desired installation directory.

This embeds the Tracy client into SU2 for profiling.

## Instrumenting SU2 Code

To profile a function in SU2, you must use the project's centralized wrapper macros. This approach ensures that profiling can be cleanly enabled or disabled at compile time without modifying the core logic.

1.  **Include the SU2 Tracy Wrapper Header:**
    -   Add an include directive for `tracy_structure.hpp` at the top of your C++ source file. The relative path will depend on the file's location. For example, for a file in `SU2_CFD/src/fluid/`:
        ```cpp
        #include "../../../Common/include/tracy_structure.hpp"
        ```
    -   **Important:** Do not include `<tracy/Tracy.hpp>` directly. The wrapper header manages the actual Tracy library.

2.  **Instrument the Function with SU2 Macros:**
    -   Use `SU2_ZONE_SCOPED_N("MyLabel")` to mark a function or scope with a custom name. This is the recommended macro for clarity.
        ```cpp
        void MyFunction() {
            SU2_ZONE_SCOPED_N("MyFunction");
            // Function implementation
        }
        ```
    -   The label you provide (e.g., `"MyFunction"`) is what will appear in the Tracy profiler's timeline.
    -   Alternatively, for a quick annotation, you can use `SU2_ZONE_SCOPED;`. This macro automatically uses the compiler-provided function name for the label.
        ```cpp
        void MyFunction() {
            SU2_ZONE_SCOPED;
            // Function implementation
        }
        ```

## Running the Profiler and Visualizing Data

After compiling and instrumenting SU2, profile and visualize the data as follows:

1. **Build the Tracy Server:**

Install additional dependencies required for the Tracy server.
```bash
sudo apt install libfreetype6-dev libcapstone-dev libdbus-1-dev \
libxkbcommon-dev libwayland-dev wayland-protocols \
libegl1-mesa-dev libglvnd-dev libgtk-3-dev
```
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
