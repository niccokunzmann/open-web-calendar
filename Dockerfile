# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

FROM python:3.13-alpine

# make pip also use piwheels
ADD docker/pip.conf /etc/pip.conf

# licenses
ADD LICENSE .
ADD LICENSES .
ADD REUSE.toml .

# server environment variables
EXPOSE 80
ENV PORT=80
ENV WORKERS=4

# Create app environment
RUN mkdir /app
WORKDIR /app
ENV PYTHONUNBUFFERED=true
ADD docker/start-service.sh .

# Install Packages
ADD docker/constraints.txt .
ENV PIP_CONSTRAINT=constraints.txt
ADD requirements.txt .
RUN apk add libxslt libxml2 libxslt-dev libxml2-dev gcc libc-dev \
 && pip install --upgrade --no-cache-dir pip \
 && pip install --upgrade --no-cache-dir -r requirements.txt \
 && apk del libxslt-dev libxml2-dev gcc libc-dev

# Start service
ENTRYPOINT ["/bin/sh", "start-service.sh"]

# Add the app
ADD open_web_calendar open_web_calendar
