<?php
session_start();
include_once "lib/db.php";
include_once "lib/conf.php";
?>
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>Movies Recommendation</title>
        <style type="text/css">
            body{
                margin:0px;
                padding:0px;
                background:#fff url("img/background.jpg") center center fixed no-repeat;
                -moz-background-size:cover;
                -webkit-background-size:cover;
                -o-background-size:cover;
                background-size:cover;
            }
        </style>
        <meta name="keywords" content="" />
        <meta name="description" content="" />
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/base/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.11.1/jquery-ui.min.js"></script>
        <script type="text/javascript">
            function findGetParameter(parameterName) {
                var result = null,
                    tmp = [];
                location.search
                .substr(1)
                    .split("&")
                    .forEach(function (item) {
                    tmp = item.split("=");
                    if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
                });
                return result;
            }
            function reload_movie_list()
            {
                var return_max = findGetParameter("return_max");
                if(return_max == null)
                {
                    return_max = 100; 
                }
                $.get("rec_movies.php?return_max=" + return_max, function(data) {
                    //$( ".result" ).html( data );
                    //alert( data );
                    $("#rec_movies").html(data);
                });
            }
            function reload_rated_movie_list()
            {
                $.get("rated_movie_list.php", function(data) {
                    //$( ".result" ).html( data );
                    //alert( data );
                    $("#rated_movies").html(data);
                });
            }
            reload_movie_list();
            reload_rated_movie_list();
            function rating_movie(obj_id, movieid)
            {
                if($(obj_id).val() != "")
                {
                    $url = "rating_movie.php?movieid=" + movieid + "&rating=" + $(obj_id).val();
                    $.get($url, function(){
                        reload_movie_list();
                        reload_rated_movie_list();
                    });
                }
            }
        </script>
    </head>
<?php
if(!isset($_SESSION[$sessionID]))
{
    // without login... show login page
    echo "<a href=login.php>Sign In</a> ";
    echo "<a href=reg.php>Sign Up</a>";
    echo "<p>";
    $_SESSION[$display] = "Guest";
}
else
{
    echo "<a href=logout.php>LOGOUT</a><p>";
}
echo "Hi " . $_SESSION[$display] . "<p>";
?>
<table border=0>
    <tr>
        <td width="60%">This is the movies list you may like<br>
            <div id=rec_movies></div>
        </td>
        <td valign="top">This is your rating movies<br>
            <div id=rated_movies></div>
        </td>
    </tr>
</table>
