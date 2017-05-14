#!/usr/bin/env bash
export PYTHONPATH=/var/www/brainminer:${PYTHONPATH}
uwsgi --http-socket 0.0.0.0:5000 --master --workers 4 --module brainminer.app:app --vacuum --die-on-term
