---
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "Translate the Open Web Calender"
---

# Translate

You can help us by [translating the project]({{link.weblate}}) to your language.

- [Translate on Weblate]({{link.weblate}})

Here, you can see the current translation status:

[![Translation status](https://hosted.weblate.org/widgets/open-web-calendar/-/multi-auto.svg)]({{link.weblate}})

## Request a new language

Adding a new language to the project is restricted to the maintainers
on Weblate. To get yours added:

1. Open the [Weblate project]({{link.weblate}}), pick any component, and
   use Weblate's button to suggest or start a new translation in your
   language. The request reaches the maintainers.
2. If you do not see the option, open an issue on the
   [tracker]({{link.issues}}) and mention the language you want.

Once a maintainer adds the language, please translate the `language` and
`language-en` strings first. They control how the language appears in the
calendar's language dropdown (see [Calendar language strings](#calendar-language-strings)
below for details).

## Translator Guide

Translations are contributed by volunteers and [logged](../../changelog).
After 48 hours they are usually live at the [hosted instance]({{link.web}}).

1. The most important file is probably the **calendar file**.
2. The **About Page** and **Common Translations** is also very important as users see it when they click the `?` at the bottom right.
3. If you would like to have the **Configuration Page** available for people in your language.
4. You are very welcome to also translate the documentation:

    1. The **Documentation - Getting Started** motivates usage.
    2. The **Documentation - Examples** showcase how to use the calendar.

Generally, feel free to translate the title and translate the sense of the content more than the literal words.
I am not a native speaker, so my English is a bit clunky and your translation could be better!

## Calendar language strings

Two strings in the calendar component control how a language appears in the
language dropdown:

- `language`: the native name, for example `Deutsch` or `Español`.
- `language-en`: the English name, for example `German` or `Spanish`,
  used as a fallback when `language` is not set.

If neither is set, the language does not appear in the dropdown at all.
Translate both early on so the dropdown shows the native name with the
English fallback in place.

## Get featured on the front page

For your language to appear in the language list on the front page, you need
at least **50%** of the strings translated across the **Configuration Page**
(`index`) and the **Common Translations** (`common`).

## Reporting issues

If you find a typo in the source English, open an issue on the
[tracker]({{link.issues}}).
For Weblate itself (component errors, file format issues, missing strings),
use Weblate's report mechanism inside the component view.

If you are adding a new documentation component, see the
[maintainer notes](maintain.md#translate-documentation-files) for the
Weblate setup steps.

Have **fun** translating and thank you so much! If you have any questions, get in contact with me, @niccokunzmann.

Feel free to add a section for your language below:

### German (de)

We use "Du" and "Dein", not "Sie" or "Ihr".
