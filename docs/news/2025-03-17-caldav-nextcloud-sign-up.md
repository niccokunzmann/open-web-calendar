---
# SPDX-FileCopyrightText: 2025 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
---

# Introducing CalDAV and Signing up to Events with Nextcloud

For years now, the Open Web Calendar has served as a static display for your online calendar.
Due to to the funding we have received from [NLNet][grant], it can be an active part of your website: Sign up to events!

First, we had to solve a few problems.

## No Knowledge Challenge

The Open Web Calendar is designed to shield you from potential trackers, see [the video about its architecture][vid-architecture].
Part of the idea is to get you started fast: No sign-up, no emails, no identification.
This way, the Open Web Calendar does not need to store anything about the calendars that it displays or the people using them.

> We show how to create services that **protect your privacy** and do not treat your data as a business value.

Having no knowledge about its users comes with lots of **benefits**:

- No data breaches
- No passwords stolen
- No database and not much storage required

So whether we have 10 or 100.000 calendars, it still costs roughly the same.
We call this cloud architecture pattern "Function as a Service" (FaaS).

A **challenge** now arises: How can we display calendars publicly if they have sensitive information such as passwords?

## Encrypted URLs

Encrypted source URLs are the answer to securing passwords in public calendars!

When you create a calendar, you have the choice of encrypting your URL.
Then, only the Open Web Calendar can read it, authenticate and display the calendar.
As an add-on, we generate a random password which you can use to decrypt the URL later.

As before, the Open Web Calendar does not store any sensitive information.
Everything is included in the encrypted part of the URL.

**Technically**, we solved this using Python's `cryptography` library and the Fernet encryption.
This comes with a few advantages:

- URLs cannot be tempered with by malicious actors.
- We can create new encryption keys and maintain all calendars.
- We can merge and host several compatible instances of the Open Web Calendar.
- Decryption allows migration from one instance to another.
- Your security depends on audited and well-established encryption libraries.

We want to thank [Radically Open Security] for their security review of the software,
(see [Issue 595](https://github.com/niccokunzmann/open-web-calendar/issues/595), NF-008).

By encrypting URLs, the Open Web Calendar now provides an additional layer of protection for sensitive information.

## CalDAV Calendars

CalDAV is the web standard to manage calendars on web servers.
Users can organize their events and TODOs, share calendars and invite others to collaborate.
For the CalDAV feature, we have chosen [Nextcloud] to test compatibility as it is a widely trusted open-source in-house cloud solution.

Technically, we use the [`caldav` library](https://pypi.org/project/caldav/) as it utilizes `recurring-ical-events`,
one of the components of the Open Web Calendar.
Additionally to this relationship and because of `caldav`'s year-long experience, it instantly boosts the compatibility of the Open Web Calendar with existing CalDAV servers.

Leveraging the speed of open-source development, we get:

- a securely authenticated public display of chosen cloud calendars
- the option of signing up to events

Have a look below and sign up to an event.
If the event is in the future, Nextcloud will also send you an email invitation that you can accept!

<iframe class="open-web-calendar" id="" style="background:url('/assets/img/circular-loader.gif') center center no-repeat; border-radius: 10px;" src="https://open-web-calendar.hosted.quelltext.eu/calendar.html?specification_url=https://open-web-calendar.quelltext.eu/assets/templates/caldav-signup.json&" sandbox="allow-scripts allow-same-origin allow-top-navigation" allowTransparency="true" scrolling="no" frameborder="0" height="600px" width="100%"></iframe>

You can find the resulting calendar in the [Examples Section][templates], too.

## Economic Summary

Using industry-proven, open-source libraries, we build secure solutions fast.
They respect privacy and deliver new use-cases.
Having a stable open-source ecosystem around existing web-standards allows us to create compatible software at scale.
NLNet funded [Python's calendaring ecosystem in 2024][grant] which is built on open web-standards that everyone can use.
With this, critical public infrastructure is secured, yielding economic value for everyone in the EU and world-wide,
achieved on a relatively small budget.

Leveraging an open-source architecture design, the Open Web Calendar builds on compatible software components.
Some of these are:

- `icalendar` with more than 1.5 million downloads / month
- `recurring-ical-events` with more than 357.000 downloads / month
- `caldav` with more than 60.000 downloads / month

Having a vibrant ecosystem around open standards with their implementations at hand thus secures

- economic independence from market-dominating actors
- social independence to organize, meet and collaborate
- data sovereignty, hosted locally, GDPR compliant
- diversity and innovation, empowering small-scale actors
- healthy competition and prevention of cartels
- stability of critical infrastructure

We want to thank NLNet for the opportunity to work for the open web and a democratic society in a technical era.

## Project Summary

As one of the highlights of the [2024 grant by NLNet][grant], the CalDAV implementation added exciting new features:

Now, it is possible to display your private calendars publicly on your website, from any source.
Even if the calendar is usually protected by a password, you can now share it with others.
There exist many CalDAV servers.
Using the Open Web Calendar, they support signing up to events on a public page!

We hope to see this feature used and users to come back with ideas of how to make their calendars even better.

[vid-architecture]: https://www.youtube.com/watch?v=JVosZ6zht5I&list=PLxMGFFiBKgdaIo4j-Cw4SOjE_7ta7TM5q&index=2
[Radically Open Security]: https://radicallyopensecurity.com/
[Nextcloud]: https://nextcloud.com/
[templates]: ../../templates#caldav-sign-up
[grant]: /news/2024-04-10-website
