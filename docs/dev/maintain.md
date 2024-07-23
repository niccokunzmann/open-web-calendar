---
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

description: "Code and guide to maintain the Open Web Calendar project."
---

# Notes for Maintainers

This section clarifies how to maintain the project.

## Update Dependencies

1. Enter your virtual environment. E.g.

    ```sh
    source .tox/py311/bin/activate
    ```

2. Install all dependencies:

    ```sh
    pip install --upgrade -r requirements.in -r test-requirements.in -r docs-requirements.in pip-tools
    ```

3. Fix the dependencies:

    ```sh
    rm *requirements.txt
    pip-compile --output-file=requirements.txt requirements.in
    pip-compile --output-file=test-requirements.txt test-requirements.in
    pip-compile --output-file=docs-requirements.txt docs-requirements.in
    ```

4. Create a branch, commit:

    ```sh
    git branch -d update
    git checkout -b update
    git add *requirements.txt
    git commit -m"Update dependencies"
    git push -u origin update
    ```

5. Create a Pull Request and see if the tests run.

## Update DHTMLX Scheduler

DHTMLX Scheduler can be updated from its [GitHub repository](https://github.com/DHTMLX/scheduler).
There is a script which updates the scheduler.
Still their changelog needs to be considered.

```shell
./scripts/update-scheduler.sh
```

If you update the scheduler, also add this to the changelog.

## Release a new Version

To release a new version:

1. Edit the `docs/changelog.md` file in the Changelog Section and add the changes.

    ```sh
    git checkout master
    git pull
    git add docs/changelog.md
    git commit -m"log changes"
    git push
    ```

2. Create a tag for the version.

    ```sh
    git tag v1.30
    git push origin v1.30
    ```

## Package

The Open Web Calendar is a package on PyPI.
You can build the package locally.

```shell
python3 -m pip install --upgrade build wheel twine
python3 -m build
```

New versions are automatically uploaded.
This process follows [the official tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

## Translate Documentation Files

We might add more Markdown documentation files to the [Weblate translation]({{link.weblate}}).
The aim of this section is to have a consistent outcome.

1. Create a component **From existing component**, the `index.html`.

    - Use the page title as **title** like `Documentation - 00 - Getting Started`
    - Use file name as **slug** like `documentation-index`

2. Choose the right File settings:

    - File format: `gettext PO file` - **bi**lingual
    - Repository browser: `https://github.com/niccokunzmann/open-web-calendar/blob/{{branch}}/docs/<file>?plain=1#L{{line}}` - replace `<file>`
    - File mask: `translations/*/LC_MESSAGES/<file>.md.po` - replace `<file>`
    - Monolingual base language file: empty
    - Edit base file: **not** checked
    - Intermediate language file: empty
    - Adding new translation: `Create new language file`
    - Template for new translations: `translations/en/LC_MESSAGES/<file>.md.po` - replace `<file>`
    - Translation license: `Create Commons Attribution Share Alike 4.0 International`
    - Language code style: `Default based on the file format`
    - Language filter:

        ```
        ^(?!(en)$)[^.]+$
        ```

        excludes `en`

    - Source language: `English`
    - Manage strings: **not** checked

3. **Save**
4. In the **Settings** 🠚 **Translation**:

    - **Un**check **Suggestion voting**
    - Set **Automatically accept suggestions** to `0`
    - Check **Allow translation propagation**
    - **Un**check **Manage strings**
    - Add **Translation flags**:

        ```
        md-text,safe-html,xml-text
        ```

    - choose **Enforced checks**:

        - Markdown links
        - Markdown references
        - Markdown syntax
        - Unsafe HTML
        - XML markup
        - XML syntax

    - **Save**

5. Upload a **screenshot** of the page

    - Restrict width and height to 2000px:

        ```sh
        convert 'Screenshot.png' -resize x2000 'Getting-started.png'
        ```

    - Click on the empty **Search** button
    - Add all strings to it

6. Go to the **Manage** 🠚 **Add-ons** and add:

    - Add missing languages (enabled in project, will activate after 24h)
    - Cleanup translation files (enabled in project)
    - Contributors in comment (enabled in project)

    These component Add-Ons are installed project-wide.

7. Clear any component alerts.
8. Skip through all the strings. If some strings are not for translation,
    add the flag `read-only`.
