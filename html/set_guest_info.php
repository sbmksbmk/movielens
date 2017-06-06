<?php
session_start();
include_once "lib/conf.php";
if(!isset($_SESSION[$sessionID]))
{
    if($_GET['gender'])
    {
        if(strtolower($_GET['gender']) == 'm')
        {
            $_SESSION['gender'] = 5;
        }
        elseif (strtolower($_GET['gender']) == 'f')
        {
            $_SESSION['gender'] = 1;
        }
    }
    if($_GET['age'] && preg_match("/^\d+$/", $_GET['age']))
    {
        $age = min(100, $_GET['age']);
        $_SESSION['age'] = $age / 25.0 + 1;
    }
    else
    {
        unset($_SESSION['age']);
    }
    if(isset($_GET['guest_info']) && $_GET['guest_info'] == 0)
    {
        $_SESSION['guest_info'] = 0;
        unset($_SESSION['age']);
        unset($_SESSION['gender']);
    }
    else
    {
        $_SESSION['guest_info'] = 1;
    }

}
?>