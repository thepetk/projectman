# projectman

This action automates the process of creating & managing github projects for your issues and/or PRs. It is a python project working with `python 3.11`.

In order to be configurable, projectman uses the `.projectman.json` file to fetch user preferences inside each repo.


## Usage

The initial release of this project is still WIP.

<!-- TODO: Add usage information for projectman.json -->

<!-- TODO: Add usage information for workflow yaml -->


<!-- 
# Scenarios

TODO: Add use case scenarios like:

- [Configure Simple Project](#configure-simple-project)
-->

## License

The scripts and documentation in this project are released under the [Apache 2.0](LICENSE)

## Release process

A projectman release is created each time a PR having updates on code is merged. You can create a new release [here](https://github.com/thepetk/projectman/releases/new).

- A _tag_ should be created with the version of the release as name. `projectman` follows the `v{major}.{minor}.{bugfix}` format (e.g `v0.1.0`)
- The _title_ of the release has to be the equal to the new tag created for the release.
- The _description_ of the release is optional. You may add a description if there were outstanding updates in the project, not mentioned in the issues or PRs of this release.

## Feedback & Questions

If you discover a bug or you want to request a new feature, create an issue and we will take a look as soon as possible.