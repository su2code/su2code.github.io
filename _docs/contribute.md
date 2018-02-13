---
title: Contribute
permalink: /docs/contribute/
---

Do you want to contribute to the SU2 documentation? It's easy! Just create a fork of the [SU2 Project Website repository](https://github.com/su2code/su2code.github.io), write your documentation, and open a pull request. 

## Writing content

The documentation in this site is stored under the `_docs` folder. To add your contributions:

**1.** Add a new Markdown file inside the subfolder, as `_docs/Your_Documentation.md`. Add the following [front matter](https://jekyllrb.com/docs/frontmatter/) to your file:

```
---
title: Your Documentation Page
permalink: /docs/Your_Documentation/
---

I'm contributing to SU2! Don't forget the trailing '/' on the permalink!
```

**2.** Add the documentation pagename to the `_data/docs.yml` file, in order to list it in the navigation panel (create a new subgroup if necessary):

```
- title: Your Subgroup of Documentation 
  docs:
  - Your_Documentation
```

**3.** If you have supporting images or other auxiliary files, please add them to the folder `docs_files` in the root directory of the repository. Don't forget to add the correct relative links to these files in your docs, if necessary.

**4.** When you are ready, submit a pull request to the **develop** branch of the [repository](https://github.com/su2code/su2code.github.io)... and it's all done! Thanks for your contribution!
