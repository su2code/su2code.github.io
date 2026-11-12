# Developer documentation

The developer guides and website tools live in this repository. The generator reads an SU2 checkout to produce configuration, output, error and migration references and copies selected notes from the source tree. It stages the site without changing either checkout.

To build locally, install Python 3.8+, Git, Ruby and Bundler versions specified by the website, Doxygen and Graphviz, and install the locked gems. From the website root, run:

```sh
python3 developer-docs/tools/build_docs.py --su2 /path/to/SU2 --site . --build-dir /path/to/empty-build --baseurl /SU2
```

The build directory must be separate from both source trees. The build runs the Python tests, generates the references and Doxygen, builds Jekyll and checks the result. To run the Python tests alone:

```sh
SU2_SOURCE=/path/to/SU2 python3 -m unittest discover -s developer-docs/tools
```

Edit the guides in `developer-docs/pages`; generated pages are built from SU2 and should not be edited directly. The documentation checks workflow builds a preview with SU2 develop and records the revisions used. External links and numerical convergence are not checked.
