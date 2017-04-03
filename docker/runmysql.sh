#!/bin/bash
CONTAINER=mysql
DOCKER_IMAGE=mysql:5.7

DIR="$(dirname "$PWD")"

docker rm -f -v $CONTAINER
cmd="docker run -d --name $CONTAINER \
 MYSQL_ROOT_PASSWORD=password \
 -v $DIR/mysql:/var/lib/mysql \
 -v $DIR/conf/my.cnf:/etc/mysql/my.cnf \
 -p 3306:3306 \
   $DOCKER_IMAGE \
"
# docker run -d -e MYSQL_ROOT_PASSWORD=password -v $PWD/mysql:/var/lib/mysql -v $PWD/conf/my.cnf:/etc/mysql/my.cnf -p 3306:3306 --name mysql mysql:5.7
echo $cmd
eval $cmd
