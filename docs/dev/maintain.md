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

## Release a new Version

To release a new version:

1. Edit the `docs/changelog.md` file in the Changelog Section and add the changes.

    ```sh
    git add docs/changelog.md
    git commit -m"log changes"
    ```

2. Create a tag for the version.

    ```sh
    git tag v1.30
    git push origin v1.30
    ```

## Translate Documentation Files

We might add more Markdown documentation files to the [Weblate translation]({{link.weblate}}).
The aim of this section is to have a consistent outcome.

1. Create a component **From existing component**, the `index.html`.

    - Use the page title as **title** like `Documentation - Getting Started`
    - Use file name as **slug** like `documentation-index`

2. Choose the right `gettext PO file (monolingual)`.
3. Set the **Repository browser** to the right URL, replace `index.md`: `https://github.com/niccokunzmann/open-web-calendar/blob/{{branch}}/docs/index.md?plain=1#L{{line}}`
4. For **Translation license** choose `Create Commons Attribution Share Alike 4.0 International`.
5. Save.

6. Add **Flags**, example link: https://hosted.weblate.org/settings/open-web-calendar/documentation-index/#translation

    - add `md-text,safe-html` as **Translation flags**
    - choose **Enforced checks**:

        - Markdown links
        - Markdown references
        - Markdown syntax
        - Unsafe HTML

7. Upload a **screenshot** of the page

    - Restrict width and height to 2000px

        ```sh
        convert 'Screenshot.png' -resize x2000 'Getting-started.png'
        ```

    - Click on the empty **Search** button
    - Add all strings to it

8. Clear any component alerts.

These component Add-Ons are automatically installed: ([Page](https://hosted.weblate.org/addons/open-web-calendar/))

- Cleanup translation files
- Contributors in comment
- Add missing languages
