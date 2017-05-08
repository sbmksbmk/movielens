<?php
session_start();
include_once("lib/conf.php");
if (preg_match("/^\d+$/", $_GET['movieid']) && preg_match("/^\d+(\.\d{1,2})?/", $_GET['rating']))
{
    if(!isset($_SESSION[$sessionID]))
    {

        if(!isset($_SESSION[$guest_rating]))
        {
            $_SESSION[$guest_rating] = array($_GET['movieid'] => $_GET['rating']);
        }
        else
        {
            $_SESSION[$guest_rating][$_GET['movieid']] = $_GET['rating'];
        }
    }
    else
    {
        include_once("lib/db.php");
        //save rating into db
        $sn = $_SESSION[$sessionID] . str_pad($_GET['movieid'], 5, '0', STR_PAD_LEFT);
        $_SESSION[$done_rate] = 1;
        $time = date('Y-m-d H:i:s');
        $str = "insert into member_rating (sn, member_id, movieid, rating, ratingtime) values " .
               "('" . $sn . "', '" . $_SESSION[$sessionID] . "', " . $_GET['movieid'] . ", " .
               $_GET['rating'] . ", '" . $time . "') " .
               "on duplicate key update rating = " . $_GET['rating'] . ", ratingtime = '" . $time . "'";
        mysql_query($str);
        $str = "update member set done_rate = 1 where userid = '" . $_SESSION[$sessionID] . "'";
        mysql_query($str);
    }
    echo "1";
}
else
{
    echo "0";
}
?>