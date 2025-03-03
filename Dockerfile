# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

FROM python:3.13-alpine

# make pip also use piwheels
COPY docker/pip.conf /etc/pip.conf

# licenses
COPY LICENSE .
COPY LICENSES .
COPY REUSE.toml .

# server environment variables
EXPOSE 80
ENV PORT=80
ENV WORKERS=4

# Create app environment
RUN mkdir /app
WORKDIR /app
ENV PYTHONUNBUFFERED=true
COPY docker/start-service.sh .

# Install Packages
COPY docker/constraints.txt .
ENV PIP_CONSTRAINT=constraints.txt
COPY requirements/base.txt requirements.txt
COPY pyproject.toml .
# see https://stackoverflow.com/a/64352966/1320237
RUN apk add --no-cache cargo gcc libc-dev libffi libffi-dev libxml2 libxml2-dev libxslt \
 && apk add --no-cache libxslt-dev openssl openssl-dev python3-dev rust \
 && pip install --upgrade --no-cache-dir pip \
 && pip install --upgrade --no-cache-dir -r requirements.txt \
 && apk del libxslt-dev libxml2-dev gcc libc-dev python3-dev libffi-dev openssl-dev rust cargo

# Start service
ENTRYPOINT ["/bin/sh", "start-service.sh"]

# Add the app
COPY open_web_calendar open_web_calendar
