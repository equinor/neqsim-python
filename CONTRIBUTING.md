# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change.

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2. Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this
   Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

## Release Process

1. Update the release version in `pyproject.toml` and `conda/meta.yaml`.
2. Update the bundled NeqSim JAR files under `src/neqsim/lib/` for each supported Java runtime.
3. Draft the GitHub release body from `.github/RELEASE_TEMPLATE.md`, keeping the installation and quick-start sections in the release notes.
4. Use GitHub's generated release notes to include categorized pull requests. The categories are configured in `.github/release.yml`.
5. Publish the GitHub release only when ready. A published release triggers the PyPI publishing workflow and the Java stub generation workflow.
