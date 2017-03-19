FROM eboraas/apache-php

RUN apt-get update
RUN apt-get install -y python2.7 python-pip gunicorn

COPY . /usr/src/app
RUN pip install -r /usr/src/app/requirements.txt

WORKDIR "/usr/src/app"
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
