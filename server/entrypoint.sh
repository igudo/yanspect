#!/bin/sh

cd /app
pip install --no-cache-dir -r requirements.txt
exec "$@"