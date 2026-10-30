---
title: Contribute
permalink: /docs_v7/contribute/
---

Documentation contributions include correcting explanations, checking examples, improving source comments and reviewing draft guidance. Start with [Using the Documentation](../Using-the-Documentation/) for the role of each section and [Documentation Improvements and Status](../Documentation-Status/) for completed work, remaining gaps and priorities.

## Choose the owning repository

| Content | Where to edit |
| --- | --- |
| User guide, model explanations and setup guides | `_docs_v7/` in the website repository. |
| Complete worked examples | `_tutorials/` in the website repository. |
| Verification and validation comparisons | `_vandv/` in the website repository. |
| Developer pages and the documentation status record | `Docs/website/pages/` in the SU2 source repository. The build overlays these pages onto the website. |
| Option descriptions | The registration comments in `Common/src/CConfig.cpp`, with consistent examples in `config_template.cfg`. |
| Generated references and checks | Their tools in `Docs/website/tools/`; do not edit generated website copies. |

The current overhaul is maintained on the `docs_site` branches of [rois1995/SU2](https://github.com/rois1995/SU2/tree/docs_site) and [rois1995/su2code.github.io](https://github.com/rois1995/su2code.github.io/tree/docs_site). The fork preview does not imply official adoption. Proposals for the official repositories need a separate review through their contribution process.

## Write and connect the page

Use a focused explanation and link to related material instead of duplicating it. State the applicable version, assumptions and evidence; retain draft labels where review is incomplete.

A user-guide page needs front matter such as:

```markdown
---
title: Your Documentation Page
permalink: /docs_v7/Your-Documentation/
---
```

Add its file stem to the relevant section of `_data/docs_v7.yml`. Tutorials and V&V use their corresponding collections and navigation files. Developer pages in `Docs/website/pages/` are added to the built menu by the generator. Put website images in `docs_files/`; developer-page assets can use `Docs/website/pages/img/`. Keep relative links valid under the preview's `/SU2` base path.

For theoretical claims, identify the model variant and cite the relevant paper or equation. For implementation claims, identify the source and checked version. A short regression run is evidence of that check, not proof of convergence or physical validation.

## Check and record the change

Use the shared build described in [Docs/website/README.md](https://github.com/rois1995/SU2/blob/docs_site/Docs/website/README.md). It runs the regression checks, generates references, builds the site and checks internal links, configuration facts and search coverage. Both repositories' pull-request workflows also build checked previews.

When a batch is completed, update the relevant status/backlog row and dated history in [Documentation Improvements and Status](../Documentation-Status/#keeping-this-page-current), with links to its changes and the checks actually performed. Remove a historical baseline entry only when its finding is resolved. Do not mark scientific guidance as reviewed or validated based only on a successful website build.

For website-only changes, publish the reviewed website commit through the SU2 **Docs Website** workflow. The build manifest records both source revisions; the status page explains the current publishing and review limits.
