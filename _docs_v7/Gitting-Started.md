---
title: GIT-ting Started
permalink: /docs_v7/Gitting-Started/
---

As you now know, GitHub is the center of all development efforts in SU2.  The su2code organization contains the main code repository as well as supporting materials. You can check out all of the development activity, and new developers are encouraged to log feature requests, questions, and bug reports through the GitHub issue tracker. Developers can have their code contributions integrated through GitHub as well.  For more information, keep reading! 

## Branching Model
                
We follow [a popular git branching strategy](http://nvie.com/posts/a-successful-git-branching-model/) in order to leverage decentralized development. This list describes the types of branches on the SU2 repository. You'll want to pick the right one to work with, in order keep the merging process simple.
                
- master -- stable, latest release and fixes
- develop -- current development, generally the branch for you to fork or start a new branch from
- feature_* -- feature specific branches
- fix_* -- branches that fix a particular bug or capability (not new features)
                
## Contributing Code
                
SU2 merges new code contributions through <a href="https://help.github.com/articles/creating-a-pull-request">pull requests</a>.  As a new developer, you'll want to <a href="https://help.github.com/articles/fork-a-repo/">fork</a> SU2 to your personal account.  This creates a clone of the whole SU2 repository, branches and all, inside your github account.  Generally you'll want to **start from the develop branch**, but you can check with the developers if you think it would be more appropriate to work on a feature branch (join the SU2 slack channel or open a GitHub discussion to get in touch).
                
You can push all of your working changes to your forked repository. Once you're happy with these, and want to push them to the origin repository, submit a pull request to the 'develop' branch under the SU2 repo. Make sure to **pull any new changes regularly** from the origin repository before submitting the pull request, so that the changes can be merged more simply. The SU2 developers will review the changes, make comments, ask for some edits, and when everything looks good, your changes will merge into the main development branch!

### General Guidelines
- If you have a very clear plan for the work you are doing, open a **draft pull request** so that the maintainers can start reviewing early.
- If you are working on a large feature (1k+ lines of code (loc), or 200+ loc with changes to 10+ files) ask to be added to the SU2 organization to work from the SU2 repo directly instead of your fork (this makes reviewing easier).
