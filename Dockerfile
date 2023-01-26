FROM python:3.9-alpine

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
RUN pip install --upgrade --no-cache-dir -r requirements.txt

# Start service
ENTRYPOINT ["/bin/sh", "start-service.sh"]

# Add the app
ADD . .
