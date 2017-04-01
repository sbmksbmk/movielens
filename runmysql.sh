#!/bin/bash
docker run -d -e MYSQL_ROOT_PASSWORD=password -v $PWD/mysql:/var/lib/mysql -v $PWD/conf/my.cnf:/etc/mysql/my.cnf -p 3306:3306 --name mysql mysql:5.7
