#!/bin/sh

gunicorn -w "$WORKERS" -b "0.0.0.0:$PORT" app:app
