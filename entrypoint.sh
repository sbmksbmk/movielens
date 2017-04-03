#!/bin/bash
python checkdb.py
gunicorn --bind 0.0.0.0:5678 --timeout=20 --workers=1 service:app &
/usr/sbin/apache2ctl -D FOREGROUND