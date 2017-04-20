#!/usr/bin/env bash

export PYTHONPATH=/var/www/backend:${PYTHONPATH}

uwsgi --http-socket 0.0.0.0:5000 --master --workers 1 --module service.auth.app:app --vacuum --die-on-term
