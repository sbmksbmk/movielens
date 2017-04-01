#!/bin/bash
docker run -d -p 8080:80 -v $PWD/html/:/var/www/html -v $PWD/apache2.conf:/etc/apache2/apache2.conf --name myservice myservice:no