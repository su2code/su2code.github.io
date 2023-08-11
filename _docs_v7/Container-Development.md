---
title: Containers for Development
permalink: /docs_v7/Container-Development/
---

---

- [Running a container](#running-a-container)
- [Using the scripts to compile SU2](#using-the-scripts-to-compile-su2)
  - [Accessing source code and binaries](#accessing-source-code-and-binaries)
  - [Compile existing source code](#compile-existing-source-code)
- [Running the Test Cases](#running-the-test-cases)


---



A container is a virtual runtime environment that runs on top of a single operating system (OS) kernel and emulates an operating system rather than the underlying hardware (as compared to a virtual machine). It allows you to locally run the same (or almost the same) environment for development, testing and production use.

We use [Docker](https://www.docker.com/) container during the software development life-cycle for running the regression tests and creating binaries for different operating systems during the release process. The execution of these containers is triggered by events (e.g. by a push to an open pull request) on Github using the [Github Actions](https://github.com/features/actions) feature.

The files for the creation of the containers can found in the [Docker-Builds](https://github.com/su2code/Docker-Builds) repository. Currently we have three different containers:

- **build-su2**: Based on Ubuntu 20.04 (GCC v9.4.0, OpenMPI v4.0.3) it features all necessary packages that are needed to compile SU2. Furthermore a script is provided (set as the [entrypoint](https://docs.docker.com/engine/reference/builder/#entrypoint)) that will checkout and compile a specific branch with provided build options.
- **test-su2**: Based on the latest **build-su2** container. Includes a script that checks out the test cases and the tutorials and runs a specified test script.
- **build-su2-cross**:  Based on the latest **build-su2** container it features an environment to create binaries for Linux, MacOS and Windows. All libraries are linked statically (including a custom build MPICH v3.3.2) with the binaries if a host file is specified in order achieve portability. For more information have a look at the [ReadMe](https://github.com/su2code/Docker-Builds/blob/master/build_cross/README.md).
- **build-su2-tsan**: Based on the same setup as **build-su2**, this container is intended to build SU2 with the thread sanitizer for automatic data race detection. To this end, it features a custom gcc build and provides a preconfigured environment for building with the thread sanitizer.
- **test-su2-tsan**: Like **test-su2** but based on the latest **build-su2-tsan** container instead. Can be used like **test-su2** and is intended for testing for data races.

**Note:** The build containers *do not* include binaries to run SU2, and they are not intended to do so (except for running the regression tests). 

It is assumed that you have added your linux username to the `docker` group, like it is explained [here](https://docs.docker.com/install/linux/linux-postinstall/). Otherwise `sudo` is required to run docker. There also a [rootless version](https://docs.docker.com/engine/security/rootless/) available.

The most recent versions of prebuilt container images can be found in the [GitHub container registry](https://github.com/orgs/su2code/packages). You can click on an image to see its versions and the command for pulling it, e.g., `docker pull ghcr.io/su2code/su2/build-su2:230704-1323`.


In the following we give a small overview on how to use the containers to compile and run the tests. We will only cover basic commands for docker. If you are interested in learning more, check out the [official documentation](https://docs.docker.com/).


## Running a container ##

A container can be started using the `run` command and the name, e.g.

```
docker run su2code/su2/build-su2
```
You should see the following message, which means that everything works as intended:
```
SU2 v7 Docker Compilation Container
SU2 source directory not found. Make sure to ...
```
The containers we provide all feature entrypoint scripts, i.e. a script that is executed when the container is started. If no arguments are given, like in the command above, it just prints an error message. The arguments of the compile and test scripts are discussed [here](#using-the-scripts-to-compile-su2). If the image does not already exist locally, it will be pulled from docker hub. You can specify a tag by adding `:tagname` to the name. If none is specified, it will use `:latest` by default. Let us have a look at the most important arguments for the `docker run` command:

- `-ti` (or `--interactive --tty`): Needed to provide input to the container (stdin) via the terminal.
- `--rm`: Automatically remove the container when it exits (otherwise ressources (disk space) are still occupied)
- `--entrypoint <command>`: Override the entrypoint script with `<command>`.
- `--volume <folder_on_host>:<folder_in_container>` (or `-v`): Bind mount a volume where `<folder_on_host>` is a local folder on the host and `<folder_in_container>` the mount location in the container.
- `--workdir <directory>` (or `-w`): The working directory inside the container.

A typical call where the current directory on the host is mounted and used as working directory would look like this: 
```
docker run -ti --rm -v $PWD:/workdir/  -w /workdir --entrypoint bash su2code/su2/build-su2
```
Here, we also override the entrypoint in order to execute a bash shell. Note, that all changes you make will be lost after you exit the container (except from changes in the working directory). Once in the bash you can simply use an existing or new clone of the repository to compile SU2 [the usual way](/docs_v7/Build-SU2-Linux-MacOS/).


## Using the scripts to compile SU2 ##

The scripts provide an easy way to directly clone and compile a specific branch from the commandline on the host. The arguments to that script have to be provided *after* the name of the container. In order to use the script, make sure that the argument `--entrypoint` is not given to the `docker run` command.

The [compile script](https://github.com/su2code/Docker-Builds/blob/master/build/compileSU2.sh) expects two arguments, the build flags for meson and the branch name. They are given with `-f` and `-b`, respectively. E.g. to compile the master branch with python wrapper enabled:
```
docker run -ti --rm su2code/su2/build-su2 -f "-Denable-pywrapper=true" -b master
```

### Accessing source code and binaries ###

Inside of the container, the script will clone the source code to `/<workdir>/src/SU2_<branch>`, where `<workdir>` is the path specified with the `-w` option to the `run` command and `<branch>` the name of the branch set with the `-b` option of the (entrypoint) script. The binaries will be installed to `/<workdir>/install/bin`. Hence, to access the source code and/or the binaries after compilation it is sufficient to mount the current directory as the working directory using `-v $PWD:/workdir/  -w /workdir`.

### Compile existing source code ###

Instead of checking out a fresh copy of the source code, it is also possible to compile an already existing version of the source code. This can be achieved by mounting the source code directory in the container at `<workdir>/src/SU2`. In that case no branch has to be provided. Additionally, to get access to the binaries, we must mount a directory at `<workdir>/install/`. For example if your source code root of SU2 is on the host machine at `~/Documents/SU2` we would use the following command:

```
docker run -ti --rm -v ~/Documents/SU2:/workdir/src/SU2 \
 -v ~/Documents/SU2/bin:/workdir/install/ -w /workdir \
 su2code/su2/build-su2 -f "-Denable-pywrapper=true"
```

The binaries can then be found at `~/Documents/SU2/bin`.

The meson build directory is called `docker_build`. If this directory exists already in your source root, options provided with the `-f` flag are ignored. Delete that directory in case you want to set new build options.


## Running the Test Cases ##

For running the tests we use the `test-su2` container. It is based on the `build-su2` and it adds a [script](https://github.com/su2code/Docker-Builds/blob/master/test/runTests.sh) to run the regression tests as entrypoint. The options for `docker run` are the same as above. The test script itself requires branch names for the su2code.github.io (Tutorials), SU2 and TestCases repositories which can be given using the `-t`, `-b` and `-c` options. Furthermore the test script that should be executed is specified with `-s`.

The compiled binaries used for the tests must be mounted at `/install/bin`. 

The following command will clone the master branches of all required repositories and run the `parallel_regression.py` script:
```
docker run -ti --rm -v ~/Documents/SU2/bin:/workdir/install/bin \
 -w /workdir su2code/su2/test-su2 -t master -b master -c master -s parallel_regression.py
```

Similar to the compilation script, you can use already existing clones of the repositories by mounting them at `<workdir>/src/Tutorials`, `<workdir>/src/SU2`, `<workdir>/src/TestData` and omitting the `-t`, `-b` or `-c` option, respectively.

The following example will compile SU2 using the `build-su2` container and then use the binaries to run the tests:

```
docker run -ti --rm -v $PWD:/workdir/ -w /workdir \
  su2code/su2/build-su2 -f "-Denable-pywrapper=true" -b develop

docker run -ti --rm -v $PWD/install/bin:/workdir/install/bin -w /workdir \
  -v $PWD/src/SU2_develop:/workdir/src/SU2 \
  su2code/su2/test-su2 -t develop -c develop -s parallel_regression.py
```
