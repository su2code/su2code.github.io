---
title: Running Regression Tests
permalink: /docs_v7/Running-Regression-Tests/
---

The regression tests can be run on your local machine by using the Python scripts available in the SU2/TestCases/ directory and the mesh files from the su2code/TestCases repository. See the [Test Cases](/docs_v7/Test-Cases/) page for more information on working with the TestCases repo.

When you are ready to combine your modifications into the develop branch, creating a pull request will automatically run these same regression tests on the Travis CI system. Your pull request must pass these tests in order to be merged into the develop branch. In the pull request, you will be able to see the state of the tests, and by clicking on links find the details of the test results. 

If you are working with a forked version of the repository, you can use the following directions to run these same regression tests within your repository rather than within the su2code/ repository. This is preferable if you are not ready to submit your code to the develop branch and just want to run the tests, or if you want to create your own regression tests.
 
1. Modify the travis.yml file in the develop branch to update the ***email address*** and ***repository url***. At this point you can also modify which branch will have the tests run. Commit the change to your fork/develop.
2. Sign up for Travis CI and allow access to your account. 
3. Activate the repository within Travis CI.
4. Modify the "README" file in the SU2/ directory such that the url points to the results for your fork rather than su2code/SU2.
5. Commit the result into your fork/develop.
6. View the results: when you open up your fork/develop on github the readme file should display. There will be a colored link going to the travis CI build which state whether the test is building, passing, or failing. This link will lead to the details of the tests. Pull requests between your fork/develop and any branches you have created on your fork will also run regression tests. 

If the tests do not run at first, double check that the repository is activated within Travis CI, and if so push a commit with some small change to the travis.yml file to your repository. If it still doesn't work, double check your urls and refer to Travis CI help menu. 
