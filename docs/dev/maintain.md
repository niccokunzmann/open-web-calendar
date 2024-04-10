
# Notes for Maintainers

This section clarifies how to maintain the project.

## Update Dependencies

1. Enter your virtual environment. E.g.

        source .tox/py39/bin/activate

2. Install all dependencies:

        pip install --upgrade -r requirements.in -r test-requirements.in pip-tools

3. Fix the dependencies:

        rm *requirements.txt
        pip-compile --output-file=requirements.txt requirements.in
        pip-compile --output-file=test-requirements.txt test-requirements.in

4. Create a branch, commit:

        git branch -d update
        git checkout -b update
        git add *requirements.txt
        git commit -m"Update dependencies"
        git push -u origin update

5. Create a Pull Request and see if the tests run.

## Release a new Version

To release a new version:

1. Edit the `docs/changelog.md` file in the Changelog Section and add the changes.

        git add docs/changelog.md
        git commit -m"log changes"
        git push

2. Create a tag for the version.

        git tag v1.30
        git push origin v1.30

3. Notify issues and pull requests about the release.
