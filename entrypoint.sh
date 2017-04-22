#!/bin/bash
python checkdb.py
python init_data_to_mysql.py train
python -c 'import service; service._movie_poster_retrieve()' &
gunicorn --bind 0.0.0.0:5678 --timeout=20 --workers=1 service:app --access-logfile=/tmp/apilog --error-logfile=/tmp/errorapilog &
/usr/sbin/apache2ctl -D FOREGROUND