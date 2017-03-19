<?php
session_start();
include_once "lib/db.php";
$str = "select * from recommendation_for_new_user order by rating desc";
$res = mysql_query($str);
while($data = mysql_fetch_array($res))
{
    echo "Movie ID:" . $data['movieid'] . " Ranking:" . $data['rating'] . "<br>";
}
$url = "http://localhost:5678/";

echo file_get_contents($url);
?>