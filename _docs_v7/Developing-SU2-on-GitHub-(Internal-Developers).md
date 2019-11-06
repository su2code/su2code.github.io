---
title: Developing SU2 on GitHub (Internal Developers)
permalink: /docs_v7/Developing-SU2-on-GitHub-(Internal-Developers)/
---

The repository for SU2 is being hosted here on GitHub. As you are likely aware, GitHub is simply an online project hosting service with a very useful web interface and additional tools to aid code development with Git as its backbone. Git is a version control system (VCS) that is similar to SVN, Mercurial, etc., and it helps organize the development of code over time by tracking changes. 

To get started, you need to create a personal user account on GitHub (free) and follow the [basic setup instructions](https://help.github.com/articles/set-up-git). These instructions include how to get Git installed on your local machine. To sync up your local settings with GitHub, change the user.email and user.name variables for your local git configuration with
```
git config --global user.email "your_email@domain.com" 
git config --global user.name "Your Name"
```
Note that the email address should be the one associated with your GitHub account.

SU2 is an open-source repository that can be found as part of the [**su2code** organization on GitHub](https://github.com/su2code). The web interface is useful for viewing the recent commits to the code, changes to the code over time, documentation and tutorials, or for creating and viewing branches, for instance. To contribute to the SU2 organization repositories directly, an administrator for the project must add you as a member of the development team with push and pull privileges. However, we encourage all developers to fork the repository and to submit pull requests with their interesting new features that they would like included in the code. We are constantly reviewing pull requests as a development team.

Most of the day-to-day development of the code will be done on your local machine at the command line using Git. After setting up Git and gaining access to the SU2 repository, create a local copy of the entire repository on your machine by cloning the version that is hosted on GitHub:
```
git clone https://github.com/su2code/SU2.git
```
After cloning, you should have a new SU2/ folder in your current working directory. Move into SU2/ to see the project files and to start working with the code through Git. You can see the most recent changes by typing
```
git log
```

## Typical Workflow with Git

Now that you have a local copy of SU2 from the GitHub repository, you can begin to make changes to the codebase. This section gives an example of the typical workflow for making changes to the code, committing them locally, and then pushing your changes to the remote GitHub repository. 

Please read the "Code Reviews" section of the wiki before making changes to familiarize yourself with the requirements for a good code change.

We follow the popular ["GitFlow"](https://nvie.com/posts/a-successful-git-branching-model/) branching model for scalable development. In the SU2 repository, the master branch represents the latest stable major or minor release (7.0, 6.2.0, etc.), it should only be modified during version releases. Work that is staged for release is put into the develop branch via Pull Requests (to be discussed in a moment) from various "feature" branches where folks do their day-to-day work on the code. At release time, the work that has been merged into the develop branch is pushed to the master branch and tagged as a release.

When a repository is cloned, all of the branches are as well, and so no additional work is necessary to acquire the development branch. However, you must tell git to switch to the development branch, which can be done with the "checkout" command
 ``` 
 git checkout -b develop origin/develop
 ```
 
 
### Opening a Pull Request ###

Now that changes will be on top of the development branch, code changes can be made. This next section describes the steps for creating a pull request. 

1. Create a new branch for making your changes.
    ```
    git checkout -b fix_quadvol
    ```
   Additionally, create a branch with the same name on the SU2 github repository. First, make sure the current SU2 branch is set to develop

   ![Develop Branch](../../docs_files/pr_develop_branch.png)

   then create a new branch with the appropriate name.

   ![Create Branch](../../docs_files/pr_create_branch.png)
  
   Depending on whether your branch name starts with `fix_`, `feature_` or `chore_`, if you open a pull request for that branch, it will automatically get the label `fix`, `feature` or`chore`, respectively. Once it is merged, this label and the title of your PR will be used to generate a change log for the next release.
  
2. Make changes to the existing files (using your favorite text editor or integrated development environment, IDE) or add local files or folders to be tracked and compared against the global repo files.

    ```
    git add file1.cpp file2.cpp
    ```

3. Optionally check that your changes have been registered and/or the files that you want have been added added

    ```
    git status 
    ```

4. Commit the changes to your local repository (not the global repository on GitHub) and create a descriptive message about your change. Commit messages are the easiest tool for examining past code changes, so it is important that they serve as documentation. A good commit message will consist of a short descriptive message on the first line, followed by a longer descriptive message. If the PR addresses any issues, they should be identified in the commit message. A good (fake) commit message is below.

    ```
    git commit -m "Fix computation of the volume for skewed quadrilateral elements." \
    -m "If a 2-D quadrilateral element is sufficiently skewed, the volume approximation is not computed properly. This modifies the volume computation to use the base and height of the quadrilateral instead of the base and hypotenuse. This fixes cases where the volume was incorrectly computed to be less than zero. Fixes issue #10."
    ```


4. Push the code to the remote version of the branch on GitHub

    ```
    git push origin fixquadvol 
    ```

5. This will automatically register on github, and you can use the online API to make a pull request

   ![Submit Request 1](../../docs_files/pr_submit_request_1.png)

   ![Submit Request 2](../../docs_files/pr_submit_request_2.png)

6. Now your code is available for code review!

We encourage developers to submit draft pull requests on GitHub, which has several benefits. This helps keep the community updated as you work on your particular feature, and offers the opportunity for others to collaborate or offer helpful feedback in the process. Duplicate work and wasted effort can be avoided this way. Additionally, draft pull requests will also benefit from continuous integration testing, and you will be alerted to any regression test failures immediately, which can also save development effort.
