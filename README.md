# SU2 website

[Official website](https://su2code.github.io/) · [Documentation preview](https://rois1995.github.io/SU2/)

## Editing documentation

User guide, setup and model pages live in `_docs_v7/`; worked examples live in `_tutorials/`; verification and validation comparisons live in `_vandv/`. Navigation is in `_data/`, and `search.json` indexes those three collections. The `docs_v7` URL is retained for compatibility; check the version stated on each page.

Keep each explanation in the appropriate section and link to related pages. See `_docs_v7/Using-the-Documentation.md` for their roles and evidence conventions. The nine setup guides share `_includes/setup-guide-intro.md`; retain draft labels and review marks until the stated review is complete.

Developer pages and generated references are overlaid from the SU2 repository. Edit developer pages in `Docs/website/pages/` there and option descriptions in the source; do not create competing copies here.

## Building and checking

Use Ruby **3.3.12** from `.ruby-version` and Bundler **2.4.22** with the tracked `Gemfile.lock`. The combined build entry point is `Docs/website/tools/build_docs.py` in the SU2 checkout. Its README, `Docs/website/README.md`, gives the local commands and output-directory rules. It builds and checks the same staged site locally and in CI, including red preview highlighting when `--mark-changes` is passed.

`.github/workflows/docs-check.yml` checks pushes to `docs_site`, `docs/user-guides` and `docs/naca0021`, and pull requests targeting `develop`, `docs_site` or `docs/user-guides`. It uses SU2 branch `docs/developer-guides` by default and uploads `docs-preview`. A manual run accepts an exact SU2 SHA through `su2_ref`. It checks internal references, search coverage, documented option names and source descriptions for new options. Historical findings are tracked explicitly in SU2's `check-baseline.json`; new findings fail.

Search behavior is checked separately with Node.js 22: run `node tools/test_search.js` from this repository. CI runs the same check before building the site. No npm packages are needed.

Website-only changes do not publish directly to SU2's Pages site. Publishing is currently restricted to `docs_site` in `rois1995/SU2`. First ensure that branch contains the reviewed SU2 tools, then start **Docs Website** there with the reviewed website commit SHA as `site_ref`. Check both recorded source revisions against the reviewed build before accepting the deployment. The result records both commit SHAs and tool versions in `build-info.json` and check results in `docs-check.json`. This avoids requiring a token with cross-repository write access for website pull requests.

The current preview uses the `rois1995` forks. Website PR branches are `docs/user-guides` and `docs/naca0021`; `docs_site` is the existing published preview branch. Submit upstream changes through pull requests to `develop`. Do not push development branches directly to the official repositories.
