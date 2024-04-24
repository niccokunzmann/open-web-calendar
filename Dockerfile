# SPDX-FileCopyrightText: 2024 Nicco Kunzmann and Open Web Calendar Contributors <https://open-web-calendar.quelltext.eu/>
#
# SPDX-License-Identifier: GPL-2.0-only

FROM python:3.11-alpine

# make pip also use piwheels
ADD pip.conf /etc/pip.conf

EXPOSE 80
ENV PORT=80
ENV WORKERS=4

# Create app environment
RUN mkdir /app
WORKDIR /app
ENV PYTHONUNBUFFERED=true

# Install Packages
ADD requirements.txt .
RUN apk add libxslt libxml2 libxslt-dev libxml2-dev gcc libc-dev \
 && echo "cython < 4.0" > constraints.txt \
 && export PIP_CONSTRAINT=constraints.txt \
 && pip install --upgrade --no-cache-dir pip \
 && pip install --upgrade --no-cache-dir -r requirements.txt \
 && apk del libxslt-dev libxml2-dev gcc libc-dev

# Start service
ENTRYPOINT ["/bin/sh", "start-service.sh"]

# Add the app
ADD . .
