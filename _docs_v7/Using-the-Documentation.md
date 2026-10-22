---
title: Using the Documentation
permalink: /docs_v7/Using-the-Documentation/
---

Choose a page by the question you need to answer. The setup guides, tutorials and verification and validation (V&V) cases complement each other; they serve different purposes.

| Your question | Where to start | What to expect |
| --- | --- | --- |
| How do I install SU2 and run a first case? | [Installation](../Installation/) and [Quick Start](../Quick-Start/) | Installation steps and a first run. |
| Which settings matter for my kind of problem? | **Case Setup Guides** in the menu | Choices, their consequences, convergence checks and common problems; links to worked cases. |
| How do I run a complete example? | [Tutorials]({{ '/tutorials/home/' | relative_url }}) | Meshes, configurations, commands and post-processing for a particular problem. |
| What evidence supports a model or discretization? | [V&V]({{ '/vandv/home/' | relative_url }}) | Comparisons with exact or manufactured solutions, other codes or physical data, within the scope of each case. |
| What does SU2 implement? | [Theory](../Theory/) and **Physical Models** in the menu | Model definitions, assumptions, variants, implementation differences and references. |
| What does an option or output field mean? | [Option Reference](../Option-Reference/) and [Output Fields Reference](../Output-Fields-Reference/) | Facts extracted from the source, with the limits of extraction stated on each reference. |
| Where do I change or extend the implementation? | [Code Structure](../Code-Structure/), **Developer Docs** and **How to Add...** | Source locations, implementation steps and relevant tests; [Code Reference](../Code-Reference/) for class details. |

## Versions and applicability

Check the version information on the page and the SU2 version used by its linked case. The `docs_v7` URL is retained for existing links; it does not mean every page describes SU2 v7. New model and setup pages state the source commit they were checked against, while older tutorials may describe an earlier release. Use the [migration guide](../Guide-to-v8/) and [renamed options](../Renamed-Options/) when moving an older configuration to a newer version.

A setting accepted by the parser may still be unsupported for a particular solver, model combination or adjoint calculation. Read the model's limitations and the conditions attached to an option. Template values and regression configurations are examples; they need not be defaults or suitable settings for your problem.

## Sources and review status

Setup guides use these tags to distinguish evidence from recommendations. A tag on a list or table introduction applies to that whole list or table.

| Tag | Meaning | Limit |
| --- | --- | --- |
| **(code)** | Checked in the SU2 source. | Describes implementation; does not establish numerical accuracy. Defaults are taken from registration or initialization, not inferred from a template example. |
| **(test case)** | Used in a regression configuration. | A regression detects changes in selected results. Its settings and iteration count need not produce a converged engineering solution. |
| **(tutorial)** | Used or explained in a tutorial. | Applies to that example and its stated version and conditions. |
| **(docs)** | Stated in another documentation page. | Follow the link for its scope and evidence. |
| **(advice)** | A practical CFD recommendation. | Requires judgment for the flow, model, mesh and numerical scheme. |
| **(to be reviewed)** | An explicit request for expert review. | Applies to the statement beside it, regardless of its other source tag. |

A **Draft** label means that review remains incomplete. A successful configuration run or website build does not remove that label. Verification asks whether the implementation solves the specified equations correctly; validation asks how well the model represents the physical situation. Neither supports unrestricted claims for other meshes, models or flows.

## How the pages fit together

For example, start with the [external RANS setup guide](../Setup-Guide-RANS-External-Aero/) to understand the choices, use [Turbulence Models](../Turbulence-Models/) and [Wall Treatment](../Wall-Treatment/) to check model assumptions, then follow the linked tutorial to run a case. Use the V&V comparisons relevant to that model and flow when assessing its accuracy.

When contributing, keep worked case instructions in Tutorials and numerical comparisons in V&V. Explain general choices in setup guides, and link to those cases instead of copying their full instructions. Model pages should identify the exact variant, define symbols and units, cite the relevant paper or equation, and distinguish the published model from SU2's implementation. Developer pages should connect implementation steps to the source and an appropriate test.
