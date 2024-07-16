---
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "A guide on how to migrate calendars from one instance to another."
---

# Move Your Calendars to Another Server

The Open Web Calendar does not need a database and does not save data about your calendars.
Thus it is easy to change the location of the calendar host to another server.

You might migrate out of these reasons:

- You use the hosted version but you have set up your own server.
- You would like to use the Open Web Calendar behind a firewall or as a local service.
- You made modifications to the Open Web Calendar that are not yet in this repository.

Moving the calendar requires you to edit the URL that is used.
This is an example URL that you would use to display or link to the calendar:

**https://open-web-calendar.hosted.quelltext.eu**/calendar.html?language=de&url=https%3A%2F%2Fexample.co.uk%2Fcalendar.ics

You only need to replace the **bold** part of the calendar with the new server location.
If your server runs with a [local development setup](../../dev) at `http://localhost:8000`, 
you would migrate your calendar by editing the URL, leaving everything behind the first `/` as it is:

**http://localhost:8000**/calendar.html?language=de&url=https%3A%2F%2Fexample.co.uk%2Fcalendar.ics

That is all! Migration done!

## Versions and Compatibility

Different versions have different features.
Generally **upgrading** the Open Web Calendar version improves the calendar functionality,
leaving most features as is.

**Downgrading** - moving to an earlier version of the Open Web Calendar - should generally work
without total loss as new configuration parameters are ignored. However, some functionalities might get lost.

Have a look at the [Changelog](../../changelog) for new features added and if you can downgrade
without loss.

## Migration with Altered Default Parameters

The Open Web Calendar allows modification of all calendar parameters, as stated in the [Configuration Section](../configure).
In order to migrate from or to a server that has modified the `default_specification.yml` file,
you will need to retrieve the specification of the calendar.

1. Click on the question mark at the bottom.
2. Click on "Download Calendar Specification".
3. Save and upload this specification.
4. Create a calendar link replacing `...` with the URL to the hosted specification: `http://localhost:8000/calendar.html?specification_url=...`

The migrated calendar should look excatly the same as the calendar you had before.