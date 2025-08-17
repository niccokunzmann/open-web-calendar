---
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "This page lists the changes made to the Open Web Calendar in a reader friendly way."
---

# Versions and Changes

This is a history of changes in the stable version of the Open Web Calendar.
These correspond to the [tags]({{link.tags}}).
The latest version might not be released, yet.

<!-- Contributors, if you like to be linked, please put your name down here with a link. -->
[தமிழ்நேரம்]: https://tamilneram.github.io/

## v1.51

- Update dependencies
- Update Dutch translation by Mark Kuiphuis and michte, Finnish by Ricky Tigg, Tamil by [தமிழ்நேரம்], Icelandic by Sveinn í Felli, Ukrainian by Максим Горпиніч, Slovak by Warder, Kabyle by ButterflyOfFire, Chinese (Simplified Han script) by Alioc

## v1.50

- Free up space at the top of the calendar if there are no controls, see [Issue 753](https://github.com/niccokunzmann/open-web-calendar/issues/753)
- Always display the bottom navigation bar, also in small screens, see [Issue 752](https://github.com/niccokunzmann/open-web-calendar/issues/752)
- Update dependencies
- Update translations:
  - Russian by Yurt Page
  - Ukrainian by Максим Горпиніч
  - German by Nicco Kunzmann
  - Finnish by Ricky Tigg and Tomi Pöyskö
  - Tamil by [தமிழ்நேரம்] and Anonymous
  - Greek by Dimitris B, French by Méli and Dream X
  - Slovak by Warder, Icelandic by Sveinn í Felli
  - Portuguese by Manuela Silva and Lourenço Martins
  - Turkish by Busra, Mehmet Sefa Ercan and Serhat
  - Thai by Afdol Kareena
  - Kabyle by ButterflyOfFire
  - Hebrew by Eden Kuperman
  - Polish by Provek
  - Czech by Tomáš Chlubna
- Update DHTMLX Scheduler to 7.2.3
- Add option to disable map links for event locations, see [Issue 717](https://github.com/niccokunzmann/open-web-calendar/issues/717)
- Remove `event_url_name` parameter and translate "OpenStreetMap".
- Stop checking links in documentation because it take too long to build the web page.
- Update Weblate plugins to allow all files to be translated. They were sometimes empty.
- Manually only display languages in the documentation drop-down menu that translate parts of the main page.
- Sort languages in language drop down of documentation.
- Display unknown Kabyle strings as Arabic
- Remove usage of Google Fonts by DHTMLX Scheduler default skin.
- Add a calendar menu:
  - Display the calendar name and description.
  - Allow hiding and showing calendars.
- Add a `calendar.json` endpoint for calendar metadata.


## v1.49

- Allow CalDAV sign-up, see [Issue 679](https://github.com/niccokunzmann/open-web-calendar/issues/679)
- Document CalDAV sign up with an example
- Update Ukrainian translation by Максим Горпиніч, German by Nicco Kunzmann, Czech by Tomáš Chlubna, Indonesian by Fajar Shiddiq
- Correct spelling mistakes in the English translation base
- Add Icelandic translation by Sveinn í Felli
- Correct the style of the Free/Busy example
- Update dependencies
- Open the link to resulting calendar in another tab, see [Issue 683](https://github.com/niccokunzmann/open-web-calendar/issues/683)
- Add options to show attendees and organizer as participants, including status, role and type, see [Issue 680](https://github.com/niccokunzmann/open-web-calendar/issues/680)
- Add Youtube playlist to documentation.
- Add recurrence ID to downloaded events to identify them across calendars, see [Issue 651](https://github.com/niccokunzmann/open-web-calendar/issues/651)
- Remove categories from week and day view, see [Pull Request 704](https://github.com/niccokunzmann/open-web-calendar/pull/704)
- Attempt Azure auto-deploy and add GitHub Actions for this.
- Allow configuring the pop-up behavior, introducing the `plugin_event_details` and `plugin_event_tooltip` specification parameters, see [Issue 447](https://github.com/niccokunzmann/open-web-calendar/issues/447).


## v1.48

- Fix automatic updates of dependencies by Renovate
- Add encryption of URLs, see [Issue 468](https://github.com/niccokunzmann/open-web-calendar/issues/468)

    - Add `cryptography` to encrypt and decrypt URLs with the Fernet cipher
    - Support `fernet://` links with encrypted JSON content
    - Use `bcrypt` to check if the password is correct and the decrypted value can be exposed to the user
    - Add documentation on how to setup encryption with the `OWC_ENCRYPTION_KEYS` environment variable
    - Add `/encrypt` and `/decrypt` JSON endpoints
    - Fix Docker build as linux/i386 requires build dependencies

- Remove stack traces from production output as they might contain sensitive data
- Update Italian translation by albanobattistella, Ukranian by Максим Горпиніч, German by Nicco Kunzmann, Spanish by Camilo M
- Add support for CalDAV URLs, see [Issue 189](https://github.com/niccokunzmann/open-web-calendar/issues/189)

    - Allow choosing from calendars
    - Allow entering a CalDAV URL with username and password
    - Add `caldav` dependency

- Allow recording of APIs requests in development mode to use in tests
- Allow editing of URLs with more comfort

    - Edit encrypted URLs if the right password is given
    - Add username and password field
    - Leave public urls unencrypted
    - Encrypt sensitive URLs with credentials by default

- New UI for editing the calendar

    - Separate page for each of the features
    - Overview at the bottom of the page
    - Resizing of calendar
    - Wide screen shows calendar on the side
    - Long screen shows calendar on the bottom
    - Translate the project name in the title of the page
    - Remove box shadow for default skin, see [Issue 449](https://github.com/niccokunzmann/open-web-calendar/issues/449)
    - Add delete and edit buttons for URLs
    - Add a few new translation strings

## v1.47

- Add option to download events in ICS format, see [Issue 206](https://github.com/niccokunzmann/open-web-calendar/issues/206)
- Remove `pytz` as dependency, replace it by `zoneinfo`
- Update dependencies
- Update Ukrainian translation by Максим Горпиніч, Hungarian by Vág Csaba, Finnish by Ricky Tigg, German by Nicco Kunzmann
- Describe how to use the Squid proxy to protect from SSRF attacks.
- Create `tox -e dev` to run the Open Web Calendar in development mode.

## v1.46

- Fix escaping [JavaScript](https://github.com/niccokunzmann/open-web-calendar/issues/631) and [CSS](https://github.com/niccokunzmann/open-web-calendar/issues/396)
- Allow installation with fixed depdencies using `pip install open-web-calendar[production]`
- Update dependencies
- Use `pip-compile-multi` and `hatch-requirements-txt` for dependencies, see [Issue 481](https://github.com/niccokunzmann/open-web-calendar/issues/481).
- Update Ukrainian translation by Максим Горпиніч, Tamil by Nicco Kunzmann and [தமிழ்நேரம்], Croatian by Milo Ivir, Dutch by Pander
- Add use `python-mergecal` to merge calendars, see [Issue 466](https://github.com/niccokunzmann/open-web-calendar/issues/466).
- Include `VTIMEZONE` component in merged calendars
- Speed up the Docker build

## v1.45

- Fix several XSS vulnerabilities, see [Issue 563](https://github.com/niccokunzmann/open-web-calendar/issues/563).
- Improve German translation by Nicco Kunzmann, Croatian by Milo Ivir
- Correct links in documentation
- Add Tamil translation by [தமிழ்நேரம்]
- Speed up web tests
- Update dependencies
- Use more indirect links in the documentation

## v1.44

- Fix bug introduced by v1.43: The calendar now changes the language again. (parameter `language`), see [Issue 599](https://github.com/niccokunzmann/open-web-calendar/issues/599).
- Improve Ukrainian translation by Максим Горпиніч, German by Nicco Kunzmann
- Update dependencies
- Document how to create a docker network to mitigate SSRF attacks.

## v1.43

- Update dependencies
- Improve Belarusian translation by Yauhen, Ukrainian by Максим Горпиніч, Esperanto by phlostically
- Update Security Policy
- Add a way to choose the map, see [Issue 23](https://github.com/niccokunzmann/open-web-calendar/issues/23)
- [Update DHTMLX Scheduler] to v7.2.1
- Introduce, test and document the `OWC_SPECIFICATION` environment variable.

[Update DHTMLX Scheduler]: https://docs.dhtmlx.com/scheduler/what_s_new.html

## v1.42

- Improve gunicorn, PyPI and service documentation
- Update dependencies
- Allow debugging UI tests with screenshots
- Update Italian translation by albanobattistella, German by Nicco Kunzmann, Korean by Paimon (JeaHoon Cha), Ukrainian by Максим Горпиніч, Spanish by gallegonovato
- Fix UI test failures due to race condition when clicking a link
- Improve load times for static files
- [Update DHTMLX Scheduler] to v7.1.3

## v1.41

- Update dependencies
- Use renovate to auto-update dependencies
- Update Spanish by gallegonovato
- Improve funding documentation
- fix: use flask-allowed-hosts because flask-allowedhosts was deleted

## v1.40

- Support `webcal://` links
- Provide docker releases with proper tag release information
- Add choice: Choose the language of the viewer
- [Update DHTMLX Scheduler] to v7.1.1
- Update examples to work with DHTMLX Scheduler v7.1.1
- Add script to automatically [Update DHTMLX Scheduler]
- Update dependencies
- Deprecate Python 3.8
- Add Chinese (Traditional Han script) and Korean
- Update Hebrew by Ori, Chinese (Traditional Han script) by 張可揚, Spanish by gallegonovato, German by Nicco Kunzmann, Slovak by Milan Šalka and Nicco Kunzmann, Croatian by Milo Ivir and Welsh by Siaron James
- Fix links to new location in the `open_web_calendar` subdirectory
- Set `__all__` variable for package export

## v1.39

- Add version to footer
- Allow specifying the version of the software through the `version` parameter
- Fix: show broken calendars again
- Fix: Remove CSS attack from broken calendar sources

## v1.38

- Create [PyPI package](https://pypi.org/project/open-web-calendar/) and deployment
- Update dependencies

## v1.37

- Update dependencies
- Improve German translation by Nicco Kunzmann and Mathieu Graf, Indonesian by Krisna A. Prayoga, Croatian by Milo Ivir, Turkish by Oğuz Ersen, Polish by Eryk Michalak, Spanish by gallegonovato
- Add calendar example that has multiple source calendars with different styling
- Fix translation mistakes in Thai and Italian
- Fix styling for calendar colors in Week and Day view
- Improve documented exapmple of choosing time zones
- Add link to Mastodon in documentation
- Use Ruff as code styler

## v1.36

- Make event title a link to the event if it has a URL set, see [Issue 388](https://github.com/niccokunzmann/open-web-calendar/issues/388)
- Improve Code Quality
- Improve Thai translation by nissara pengpol, Ukrainian by mondstern and Italian by albanobattistella
- Update dependencies

## v1.35

- Add link to Privacy Policy.
- Update dependencies
- Improve Spanish by gallegonovato, German by Nicco Kunzmann, Sinhala by Dilitha Ransara, Norwegian Bokmål by Allan Nordhøy
- Improve documentation, translate documentation to German and Spanish
- Build documentation with Python 3.11
- Update documentation languages automatically
- Allow translating the documentation with Weblate

## v1.34

- Ensures every HTML document has a lang attribute (html) [Issue 347](https://github.com/niccokunzmann/open-web-calendar/issues/347)
- Allow hosters to close the Host Header Injection vulnerability, see [PR 366](https://github.com/niccokunzmann/open-web-calendar/pull/366)
- Improve documentation and Docker build
- Add Esperanto by phlostically
- Improve Slovak, Russian, Portuguese, Indonesian by phlostically
- Update requirements

## v1.33

- Update dependencies
- Add alternate link to "text/calendar" content to ease subscribing for other calendars, see [Issue 308](https://github.com/niccokunzmann/open-web-calendar/issues/308)
- Use calendar feeds from alternate links to "text/calendar" content, see [Issue 309](https://github.com/niccokunzmann/open-web-calendar/issues/309)
- Use HTML description from various sources, see [Issue 300](https://github.com/niccokunzmann/open-web-calendar/issues/300)
- Allow JavaScript customization of the calendar, see [Issue 71](https://github.com/niccokunzmann/open-web-calendar/issues/71)
- Improve Portuguese by qeepoo
- Increase Python version for Docker to 3.11

## v1.32

- Update Italian translation by albanobattistella
- Open links in event descriptions in new tab or as configured, see [Issue 287](https://github.com/niccokunzmann/open-web-calendar/issues/287)
- Add giscus to discuss the documentation

## v1.31

- Move documentation to [open-web-calendar.quelltext.eu](https://open-web-calendar.quelltext.eu)
- Update dependencies
- Generate GitHub Releases to notify watchers
- Update Russian translation by Nicco Kunzmann, Turkish by Oğuz Ersen, Spanish by gallegonovato and German by Nicco Kunzmann

## v1.30

- Improve Italian translation by albanobattistella and Russian translation by Ivan V
- Update dependencies
- Remove CSS attacks from event sources through HTML injection, see [Issue 165](https://github.com/niccokunzmann/open-web-calendar/issues/165)
- Add CSS classes for events, see [Issue 305](https://github.com/niccokunzmann/open-web-calendar/issues/305)
- Add a way to give calendars a different color, see [Issue 141](https://github.com/niccokunzmann/open-web-calendar/issues/141) and [Issue 52](https://github.com/niccokunzmann/open-web-calendar/issues/52)
- Document CSS classes, see [Issue 202](https://github.com/niccokunzmann/open-web-calendar/issues/202)
- Add checkboxes for the event status, see [PR 306](https://github.com/niccokunzmann/open-web-calendar/pull/306)

## v1.29

- Improve Indonesian translation by Reza Almanda, Croatian by Milo Ivir,
    German by Nicco Kunzmann, Spanish by gallegonovato, Turkish by Oğuz Ersen
- Update dependencies and documentation
- Work week now skips Saturday and Sunday in Day View, see [Issue 258](https://github.com/niccokunzmann/open-web-calendar/issues/258)

## v1.28

- Update dependencies
- Allow editing calendar copies, see [Issue 180](https://github.com/niccokunzmann/open-web-calendar/issues/180)
- Improve Finnish translation by Tomi Pöyskö and Croatian by Milo Ivir
- Improve visibility on small screens, see [PR 284](https://github.com/niccokunzmann/open-web-calendar/pull/284)
- Fix: show event title in mobile agenda view, see [Issue 277](https://github.com/niccokunzmann/open-web-calendar/issues/277)
- Fix Chrome driver timeout in CI tests, see [PR 279](https://github.com/niccokunzmann/open-web-calendar/pull/279)

## v1.27

- Browser tests run with Firefox and Chrome, see [PR 272](https://github.com/niccokunzmann/open-web-calendar/pull/272)
- Add responsive layout, see [PR 273](https://github.com/niccokunzmann/open-web-calendar/pull/273)
    - Remove tooltip on touch devices as it overlaps with the quick info
    - Expose `compact_layout_width` parameter so you can change when to compact the layout, default is 600px width

## v1.26

- Use HTML color chooser for custom CSS
- Add a red bar at the current time in the week view and the day view, see [PR 265](https://github.com/niccokunzmann/open-web-calendar/pull/265).
- Expose the `hour_format` parameter and add choices for the 12h format, see [PR 266](https://github.com/niccokunzmann/open-web-calendar/pull/266).
- Update Turkish by oersen, Spanish by gallegonovato and German
- Update dependencies
- Update GitHub Actions with Dependabot

## v1.25

- Update dependencies
- Implement work week view, see [Issue 258](https://github.com/niccokunzmann/open-web-calendar/issues/258)
- Update translations

## v1.24

- Test and support Python 3.12
- Fix rendering error for unknown/malformed time zones (use DHTMLX's timeshift)
- Improve Indonesian translation by Reza Almanda

## v1.23

- Add documentation and dependencies to use a Tor proxy to prevent SSRF attacks.
- Remove temporary cache directory vulnerability [GitHub](https://github.com/niccokunzmann/open-web-calendar/security/code-scanning/2) [CWE-377](https://cwe.mitre.org/data/definitions/377.html)

## v1.22

- Update dependencies

## v1.21

- Update Chinese translation by dingc
- Update French translation by Thomas Moerschell
- Fix Content-Type header for .js files, see [Issue 241](https://github.com/niccokunzmann/open-web-calendar/issues/241)
- Add logo [Issue 205](https://github.com/niccokunzmann/open-web-calendar/issues/205)

## v1.20

- Turkish translation by Oğuz Ersen
- Spanish translation by gallegonovato
- Indonesian translation by Reza Almanda
- Update dependencies
- Correct links

## v1.19

- Update dependencies

## v1.18

- Update dependencies
- Update Finnish by Teemu
- Update Slovak by Milan Šalka
- Update Polish by Piotr Strebski
- Update Japanese by onokatio

## v1.17

- Add User-Agent header, see [Issue #225](https://github.com/niccokunzmann/open-web-calendar/issues/225).
- Close security vulnerability, [Pull Request #223](https://github.com/niccokunzmann/open-web-calendar/pull/223)
- Update German, Welsh, Croatian

## v1.16

- Add a dropdown to choose another time zone to view the calendar in the about screen, see [Issue #213](https://github.com/niccokunzmann/open-web-calendar/issues/213).

## v1.15

- Update dependencies

## v1.14

- Improve Indonesian translation by Reza Almanda
- Improve Spanish translation by zyloj
- Improve Polish translation by Eryk Michalak
- Update dependencies
- Do not test Python 3.7 any more
- Test Python 3.11

## v1.13

- Improve French translation
- Update dependencies

## v1.12

- Add Croatian UI by Milo Ivir

## v1.11

- Add German UI
- Improve calendar in Polish
- Add Welsh calendar

## v1.10

- Add translations for nb_NO.
- Translate the user interface.
- Use weblate to translate files.

## v1.9

- Speed up loading with start and stop date range. [Pull Request #177](https://github.com/niccokunzmann/open-web-calendar/pull/177).

## v1.8

- Add start of day, end of day and time step (hour be default) in [Pull Request #158](https://github.com/niccokunzmann/open-web-calendar/pull/158) thanks to [@TheoLeCalvar](https://github.com/TheoLeCalvar).

## v1.7

- Add timezone functionality. See [Issue #171](https://github.com/niccokunzmann/open-web-calendar/issues/171).

## v1.6

- Add choice of Sunday or Monday for the start of the week [Issue 39](https://github.com/niccokunzmann/open-web-calendar/issues/39) - backed by [donation]!

## v1.5

- add link to [Contributing Section](../contributing) in about page
- make event clickable even if there is a tool tip window
- [@MrKoga](https://github.com/MrKoga) [donated][github-sponsors] to the project! Thanks!

## v1.4

- add event categories when you click an event, see [PR 159](https://github.com/niccokunzmann/open-web-calendar/pull/159).

## v1.3

- update translation mistake
- fix encoding problem for languages other than en/de
- add ability to remove all controls
- test with GitHub actions
- test user interface

## v1.2

- Use Gunicorn in Docker image
- change deployment to https://open-web-calendar.hosted.quelltext.eu/

## v1.1

- Add Coatian Language by Tomislav Gomerčić

## v1.0

- Create the changelog.
- Add support for colors from ICS calendars, see [Issue #52](https://github.com/niccokunzmann/open-web-calendar/issues/52) and [Pull Request 88](https://github.com/niccokunzmann/open-web-calendar/pull/88).
