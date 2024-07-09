<!--
SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>

SPDX-License-Identifier: CC-BY-SA-4.0
-->

Localization
============

The scheduler can be localized.
Reading:

- [scheduler localization]
- [issue 21]

Extraction
----------

We can extract the current translations from the [scheduler localization].

```
var s="";
for (var tr of document.getElementsByTagName("tr")) {
  var td = tr.getElementsByTagName("td");
  var f = td[1].innerText.replace(/^\s+|\s+$/g, "");
  var m = f.match(/locale_(.+)\.js/);
  if (!m) continue;
  s += ('  ["' + td[0].innerText.replace(/^\s+|\s+$/g, "") + '", "' + f + '", "' + m[1] + '"],\n');
}
console.log(s);
```

Then, edit it a little and put it into [languages.json]
This is the base for the localization.

From the [example](https://docs.dhtmlx.com/scheduler/samples/01_initialization_loading/07_locale_usage.html),
we can see that we can download the files.
https://docs.dhtmlx.com/scheduler/codebase/locale/locale_es.js

```
cd static/js/dhtmlx/locale/
for locale in `grep -Eo 'locale_.+\.js' languages.json `; do
    wget https://docs.dhtmlx.com/scheduler/codebase/locale/$locale
done
```

Contributing
------------

If you like to create new translations in other languages because
your language is not incuded, we should send them to
[support@dhtmlx.com](mailto:support@dhtmlx.com), too, as mentioned
in the [scheduler localization].

Licensing
---------

The license in these files prohibits them for use somewhere else, thus also
for this project.
However, the translation of a few words fall way below the threshold or
creativity to claim copy right for.
Thus these files are used either way.


[scheduler localization]: https://docs.dhtmlx.com/scheduler/localization.html
[issue 21]: https://github.com/niccokunzmann/open-web-calendar/issues/21
[languages.json]: languages.json

