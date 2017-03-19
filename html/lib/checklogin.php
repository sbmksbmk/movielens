<?php
session_start();
if(!isset($_SESSION["userid"]))
{
    print_r($_SESSION);
    header("location: ../login.php");
}
?>