<?php
include_once "lib/conf.php";
if(isset($_POST['options']))
{
    switch ($_POST['options']) {
        case 'reload_movie_info':
        case 'update_poster':
            $url = $apiurl . $_POST['options'];
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_POST, true);
            curl_exec($ch);
            break;
        
        default:
            // do nothing...
            break;
    }
}

?>