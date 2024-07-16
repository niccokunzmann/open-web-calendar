---
# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: CC-BY-SA-4.0

comments: true
description: "There are various ways to host the Open Web Calendar yourself and customize the deployment."
---

# Self-Hosting & Deployment

You do not have to host the Open Web Calendar yourself but you are encouraged to.
It is intended to work behind a company firewall, through a proxy and also without access to the Internet.

Several hosting options are already documented.
We are grateful if you can add your favorite one, too.

1. **Choose a hoster.** These are listed below.
2. [**Read about Configuration**](../configure).

## Vercel

You can create a fork of this repository which automatically deploys to [Vercel](https://vercel.com/):

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fniccokunzmann%2Fopen-web-calendar.git)

Alternatively you can create a one off deploy by cloning this repository and running `npx vercel` at the root.

## Heroku

You can deploy the app using [Heroku](https://heroku.com).

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/niccokunzmann/open-web-calendar)

Heroku uses [gunicorn](https://gunicorn.org/)
to run the server, see the [Procfile](https://github.com/niccokunzmann/open-web-calendar/blob/master/Procfile).

## Cloudron

The Open Web Calendar has been integrated into [Cloudron](https://www.cloudron.io/).

- [Cloudron Documentation](https://docs.cloudron.io/apps/openwebcalendar/)
- [Cloudron Repository](https://git.cloudron.io/cloudron/openwebcalendar-app)

## YunoHost

The Open Web Calendar is available as an app for [YunoHost](https://yunohost.org/).

[![Install Open Web Calendar with YunoHost](https://install-app.yunohost.org/install-with-yunohost.svg)](https://install-app.yunohost.org/?app=open-web-calendar)

- [App Description](https://apps.yunohost.org/app/open-web-calendar)
- [Repository](https://github.com/YunoHost-Apps/open-web-calendar_ynh/blob/master/ALL_README.md)

## Docker

If you run your own server, you can choose to run the Open Web Calender with Docker.
Building, running and updating are [documented here](../docker).

## Python Package

You can choose to run the Open Web Calendar installed as a Python package from PyPI.
To do this, have a look at [the documentation](../pypi).

## Update Notifications

If you wish to receive notifications about new updates of the software,
watch the [GitHub repository]({{link.repo}}).

![Repository, Watch, Custom, Releases](/assets/img/subscribe-to-release.png)

## Further Configuration

After you have set up your own server,
you can [configure the behavior](../configure).


[open-web-calendar.hosted.quelltext.eu]: {{link.web}}
[tor.open-web-calendar.hosted.quelltext.eu]: {{link.tor}}
