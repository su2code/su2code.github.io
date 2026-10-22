# SU2 website

[Official website](https://su2code.github.io/) · [Documentation preview](https://rois1995.github.io/SU2/)

## Editing documentation

User guide, setup and model pages live in `_docs_v7/`; worked examples live in `_tutorials/`; verification and validation comparisons live in `_vandv/`. Navigation is in `_data/`, and `search.json` indexes those three collections. The `docs_v7` URL is retained for compatibility; check the version stated on each page.

Keep each explanation in the appropriate section and link to related pages. See `_docs_v7/Using-the-Documentation.md` for their roles and evidence conventions. The nine setup guides share `_includes/setup-guide-intro.md`; retain draft labels and review marks until the stated review is complete.

Developer pages and generated references are overlaid from the SU2 repository. Edit developer pages in `Docs/website/pages/` there and option descriptions in the source; do not create competing copies here.

## Building and checking

Use Ruby **3.3.12** from `.ruby-version` and Bundler **2.4.22** with the tracked `Gemfile.lock`. The combined build entry point is `Docs/website/tools/build_docs.py` in the SU2 checkout. Its README, `Docs/website/README.md`, gives the local commands and output-directory rules. It builds and checks the same staged site locally and in CI, including red preview highlighting when `--mark-changes` is passed.

`.github/workflows/docs-check.yml` checks `docs_site` pushes and pull requests against SU2 `docs_site` and uploads `docs-preview`. A manual run accepts an exact SU2 SHA. It checks internal references, search coverage, documented option names and source descriptions for new options. Historical findings are tracked explicitly in SU2's `check-baseline.json`; new findings fail.

Website-only changes do not publish directly to SU2's Pages site. After their checks pass, start **Docs Website** in `rois1995/SU2`, with the website commit SHA as `site_ref`. The result records both commit SHAs and tool versions in `build-info.json` and check results in `docs-check.json`. This avoids requiring a token with cross-repository write access for website pull requests.

Push development changes only to `rois1995/su2code.github.io`, branch `docs_site`; official-repository pushes are disabled.
