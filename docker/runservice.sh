#!/bin/bash
CONTAINER=recommendation-service
TAG=$(git rev-parse --short HEAD)
DOCKER_IMAGE=$CONTAINER:$TAG

DIR="$(dirname "$PWD")"

docker rm -f -v $CONTAINER
cmd="docker run -d --name $CONTAINER \
 -v $DIR/html/:/var/www/html \
 -v $DIR/conf/apache2.conf:/etc/apache2/apache2.conf \
 -p 8080:80 \
   $DOCKER_IMAGE \
"
# docker run -d -p 8080:80 -v $PWD/html/:/var/www/html -v $PWD/conf/apache2.conf:/etc/apache2/apache2.conf --name myservice myservice:no
echo $cmd
eval $cmd
