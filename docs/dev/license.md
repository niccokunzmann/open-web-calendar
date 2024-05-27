---
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

description: "Development information about licensing."
---

# License Information

This project specifies the licenses of its files according to the
[REUSE](https://reuse.software/) tool.

Run a check:

```sh
tox -e reuse
```

If you added files and now the CI tests fail,
annotate them accordingly.


We use `CC-BY-SA-4.0` for:

- documentation
- `.ics` calendar files
- images

```sh
reuse annotate --year 2024 --copyright="Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>" --license="CC-BY-SA-4.0" <FILES>
```

We use `GPL-2.0-only` for:

- source code
- translations of the source code
- build information
- HTML files

```sh
reuse annotate --year 2024 --copyright="Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>" --license="GPL-2.0-only" <FILES>
```

Hints:

- Add `--force-dot-license` for files that should not be touched.
- Add information to the `.reuse/dep5` file for folders under a certain license.
