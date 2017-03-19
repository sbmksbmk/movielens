docker run -d -e MYSQL_ROOT_PASSWORD=password -v ~/intowow/forintowow/mysql:/var/lib/mysql -v ~/intowow/forintowow/conf/my.cnf:/etc/mysql/my.cnf -p 3306:3306 --name mysql mysql:5.7
