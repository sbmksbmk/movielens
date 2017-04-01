FROM mydocker

COPY . /usr/src/app
RUN pip install -r /usr/src/app/requirements.txt

WORKDIR "/usr/src/app"
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
