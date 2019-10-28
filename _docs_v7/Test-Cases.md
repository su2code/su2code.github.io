---
title: Test Cases
permalink: /docs_v7/Test-Cases/
---

If you would like to experiment with some available cases, be sure to check out the suite of test cases that are available to you, as described below.

**Note:** While many of the cases are used for regression testing, the test case suite is provided **without any guarantees on performance or expected results**. Tutorials (which are more thoroughly checked for convergence and results) can be found [here](/tutorials/home/).

The test cases have been structured to separate the config files (found in the SU2 repo in SU2/TestCases/), which need to remain under version control, from the mesh/solution data (remain in a separate TestCases repo). The idea is that developers will update their config files along with their code changes in the SU2 repo so that pull requests can be automatically checked with Travis CI. The meshes and solution data, which change much less frequently and are larger files, remain in the TestCases repo.

The two repositories contain the same directory structure for the test cases, with complementary (**not overlapping**) file sets. The responsibility is on the developer to add files to both repositories in matching directory locations when adding new test cases. This makes it very easy for one to recombine the full set of files or for Travis CI to do this automatically. To run the regression tests locally, one might do the following, assuming paths are set correctly such that SU2_CFD is available:
```
$ git clone https://github.com/su2code/SU2.git
$ git clone https://github.com/su2code/TestCases.git
$ cd SU2/
$ ./configure
$ make install
$ cp -R ../TestCases/* ./TestCases/
$ cd ./TestCases/
$ python serial_regression.py
```

Note that there are a number of test cases included in the suite that are not covered within the regressions. After completing the copy step in the process above, one will have all of the necessary config and mesh files within the appropriate locations for running the test cases individually instead of through the regression script. If you would like to view the separate test cases repository with the mesh/solution data, you can find it within a dedicated repo on [GitHub](https://github.com/su2code/TestCases).
