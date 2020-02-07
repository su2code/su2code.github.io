---
title: Contribute
permalink: /tutorials/contribute/
disable_header: true
written_by: economon
for_version: 6.0.0
revised_by: economon
revision_date: 2018-02-13
revised_version: 6.0.0
---

Do you want to contribute to SU2 with a tutorial? It's easy! Just create a fork of the [SU2 Project Website repository](https://github.com/su2code/su2code.github.io), write your tutorial and open a pull request. 

## Writing content

The tutorials in this section of the site are stored under the `_tutorials` folder. To add your contributions:

**1.** Create a new subfolder in `_tutorials/` as `_tutorials/Your_Folder_Name`, where you will store your subgroup of tutorials. You can also add your conribution to an existing folder if it fits better within the existing structure.

**2.** Add a new Markdown file inside the subfolder, as `_tutorials/Your_Folder_Name/Your_Tutorial.md`. Add the following [front matter](https://jekyllrb.com/docs/frontmatter/) to your file:

```
---
title: Your Tutorial Title
permalink: /docs/Your_Folder_Name/Your_Tutorial/
---

I'm contributing to SU2!
```

**3.** Add the tutorial pagename to the `_data/tutorials.yml` file, in order to list it in the navigation panel:

```
- title: Your Subgroup of Tutorials 
  docs:
  - Your_Tutorial
```

**4.** Create a folder in the root directory of the repo with the name `Your_Tutorial_Name`.

**5.** Add your `config.cfg`, `mesh.su2` and any other auxiliary files to the folder `Your_Tutorial_Name`. Don't forget to provide the relative links in your Markdown file to these auxiliary files, if necessary.

**6.** When you are ready, submit a pull request to the **develop** branch of the [SU2 Project Website repository](https://github.com/su2code/su2code.github.io)... and it's all done! Thanks for your contribution!
