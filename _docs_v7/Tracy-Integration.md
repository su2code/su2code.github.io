---
title: Integrating Tracy Profiler with SU2
permalink: /docs_v7/Tracy-Integration/
---

---

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Integrating Tracy with SU2](#integrating-tracy-with-su2)
- [Setting Up the Tracy Server](#setting-up-the-tracy-server)
- [Instrumenting SU2 Code](#instrumenting-su2-code)
- [Using Tracy for Profiling](#using-tracy-for-profiling)
- [Conclusion](#conclusion)

---

## Introduction

Tracy is a high-performance, real-time profiler designed for C++ applications, offering nanosecond-resolution timing with minimal overhead. It is an excellent tool for profiling computationally intensive software like SU2, where traditional profilers such as Valgrind may introduce significant slowdowns. This guide provides step-by-step instructions for integrating Tracy with SU2, enabling users to analyze and optimize the performance of their CFD simulations effectively.

## Prerequisites

Before integrating Tracy with SU2, ensure the following software is installed:

- **SU2 Source Code**: Version 8.2.0 or later.
- **Meson Build System**: Version 0.61.1 or later.
- **Git**: For retrieving the Tracy repository.
- **C++ Compiler**: Such as GCC.
- **CMake**: Required for building the Tracy profiler.

For Ubuntu users, install additional dependencies required for the Tracy server with:

```bash
sudo apt install libfreetype6-dev libcapstone-dev libdbus-1-dev \
libxkbcommon-dev libwayland-dev wayland-protocols \
libegl1-mesa-dev libglvnd-dev libgtk-3-dev
```

## Integrating Tracy with SU2

To embed the Tracy client into SU2, you need to modify the Meson build configuration. The client collects profiling data during runtime. Follow these steps:

1. **Create a Wrap File for Tracy:**

   - Navigate to the SU2 source directory: `cd <SU2_SOURCE_DIR>`.
   - Create a file named `subprojects/tracy.wrap` with the following content:

     ```ini
     [wrap-git]
     url = https://github.com/wolfpld/tracy.git
     revision = master
     depth = 1
     ```

2. **Update Meson Options:**

   - Edit `meson_options.txt` (or `meson.options`) in `<SU2_SOURCE_DIR>` to include:

     ```meson
     option('tracy_enable', 
            type: 'boolean', 
            value: false, 
            description: 'Enable Tracy profiling support')
     ```

3. **Modify the Main Meson Build File:**

   - Open `meson.build` in `<SU2_SOURCE_DIR>` and add Tracy as a dependency when enabled:

     ```meson
     if get_option('tracy_enable')
         tracy_dep = dependency('tracy', static: true)
         su2_deps += tracy_dep
         su2_cpp_args += '-DTRACY_ENABLE'
         
         if get_option('buildtype') != 'debugoptimized'
             warning('For optimal Tracy profiling, use --buildtype=debugoptimized')
         endif
     endif
     ```

   - Update the `default_options` at the top of `meson.build`:

     ```meson
     default_options: ['buildtype=release',
                       'warning_level=0',
                       'c_std=c99',
                       'cpp_std=c++11',
                       'tracy_enable=false']
     ```

   - Update the Build Summary to display Tracy status by inserting `get_option('tracy_enable')` into the summary format string (adjust the index accordingly, e.g., `@14@`):

     ```meson
     Tracy Profiler: @14@
     ```

     And update the install instruction line:

     ```meson
     Use './ninja -C @15@ install' to compile and install SU2
     ```

4. **Build SU2 with Tracy:**

   - Ensure Meson is updated:

     ```bash
     pip install --user --upgrade meson
     ```

   - Run the preconfigure script:

     ```bash
     ./preconfigure.py
     ```

   - Configure and build SU2:

     ```bash
     meson build_tracy -Dwith-mpi=disabled -Denable-pywrapper=true -Denable-mlpcpp=true --buildtype=debugoptimized -Dtracy_enable=true --prefix=<SU2_INSTALL_PATH>
     ninja -C build_tracy install
     ```

   - Replace `<SU2_SOURCE_DIR>` with the path to your SU2 source code and `<SU2_INSTALL_PATH>` with your desired installation directory.

This process integrates the Tracy client into SU2, enabling profiling capabilities.

## Setting Up the Tracy Server

The Tracy server is the graphical application that visualizes profiling data collected by the client. To set it up:

1. **Build the Tracy Profiler:**

   - Navigate to the Tracy directory: `cd <SU2_SOURCE_DIR>/subprojects/tracy`.
   - Use CMake to build the profiler:

     ```bash
     cmake -B profiler/build -S profiler -DCMAKE_BUILD_TYPE=Release -DLEGACY=ON
     cmake --build profiler/build --config Release --parallel
     ```

   - The `-DLEGACY=ON` flag enables X11 support, which may be necessary for some systems. Omit this flag if Wayland is preferred and supported.

The Tracy server is now ready to display profiling data.

## Instrumenting SU2 Code

To collect meaningful profiling data, instrument the SU2 source code with Tracy macros. For example, to profile a specific function:

1. **Include the Tracy Header:**

   - Add the following at the top of the source file:

     ```c++
     #include <tracy/Tracy.hpp>
     ```

2. **Add Profiling Macros:**

   - Instrument the function with `ZoneScopedN`:

     ```c++
     void MyFunction() {
         ZoneScopedN("MyFunction");
         // Function implementation
     }
     ```

   - The `ZoneScopedN("name")` macro defines a profiling zone, labeled for identification in the Tracy GUI.

Repeat this process for any functions or code sections you wish to profile.

## Using Tracy for Profiling

With the client integrated, the server built, and the code instrumented, you can profile SU2 simulations:

1. **Launch the Tracy Profiler:**

   - Navigate to the profiler build directory:

     ```bash
     cd <SU2_SOURCE_DIR>/subprojects/tracy/profiler/build
     ```

   - Run the profiler:

     ```bash
     ./tracy-profiler
     ```

   - In the GUI, click "Connect" to wait for a connection from SU2.

2. **Execute the Instrumented SU2 Simulation:**

   - In a separate terminal, navigate to your simulation directory and run:

     ```bash
     <SU2_INSTALL_PATH>/bin/SU2_CFD <your_config_file>.cfg
     ```

   - Replace `<SU2_INSTALL_PATH>` with your installation path and `<your_config_file>` with your configuration file.

As the simulation runs, Tracy will display real-time profiling data, allowing you to analyze performance metrics and identify bottlenecks.

## Conclusion

Integrating Tracy with SU2 equips users with a powerful, low-overhead tool for profiling and optimizing CFD simulations. Its real-time visualization and precise timing capabilities make it ideal for performance analysis. For advanced features, troubleshooting, or additional details, consult the [Tracy documentation](https://github.com/wolfpld/tracy/releases/latest/download/tracy.pdf).