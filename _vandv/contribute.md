---
title: Contribute
permalink: /vandv/Contribute/
---

Do you want to contribute to SU2 with a V&V case study? It's easy! Just create a fork of the [SU2 Project Website repository](https://github.com/su2code/su2code.github.io), write your case study and open a pull request. 

## Writing content

The case studies in this section of the site are stored under the `_vandv` folder. To add your contributions:

**1.** Add a new Markdown file inside the subfolder, as `_vandv/Your_Case_Name.md`. Add the following [front matter](https://jekyllrb.com/docs/frontmatter/) to your file:

```
---
title: Your Case Study Title
permalink: /docs/Your_Case_Name
---

I'm contributing to SU2!
```

**2.** Create a new subfolder in `_vandv_files/` as `_vand/Your_Case_Name`, where you can store any additional files needed for your case study, such as images of results. Don't forget to provide the relative links in your Markdown file to these auxiliary files, if necessary.

**3.** Add the case study pagename to the `_data/vandv.yml` file, in order to list it in the navigation panel:

```
- title: Your Subgroup of Case Studies 
  vandv:
  - Your_Case Name
```

**4.** When you are ready, submit a pull request to the **develop** branch of the [SU2 Project Website repository](https://github.com/su2code/su2code.github.io)... and it's all done! Thanks for your contribution!
