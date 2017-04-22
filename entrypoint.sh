#!/bin/bash
python checkdb.py
python init_data_to_mysql.py train
gunicorn --bind 0.0.0.0:5678 --timeout=20 --workers=1 service:app --access-logfile=/tmp/apilog --error-logfile=/tmp/errorapilog &
/usr/sbin/apache2ctl -D FOREGROUND