<?php
session_start();
include_once "conf.php";
if(!isset($_SESSION[$sessionID]))
{
    header("location: ../login.php");
}
?>