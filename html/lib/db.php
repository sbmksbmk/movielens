<?php
$link = mysql_connect("172.17.0.1", "root", "password") or die("Could not connect to server.");
mysql_select_db("movielens");
mysql_query("SET NAMES UTF8;", $link);
$tz = 'Asia/Taipei';
date_default_timezone_set($tz);
?>