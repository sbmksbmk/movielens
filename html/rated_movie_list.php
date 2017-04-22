<?php
session_start();
include_once "lib/db.php";
include_once "lib/conf.php";
?>
<table border="1" width="100%">
    <tr>
        <td width="30">ID</td>
        <td>Movie Title</td>
        <td width="70">Your Rating</td>
    </tr>
<?php
$output = array();
if(isset($_SESSION[$sessionID]))
{
    $str = "select r.movieid as movieid, r.rating as rating, m.url as url, m.title as title " .
           "from member_rating as r, movie as m where r.member_id = '" . $_SESSION[$sessionID] . "' " .
           "and r.movieid = m.movieid order by r.ratingtime desc";
    $res = mysql_query($str);
    while($data = mysql_fetch_array(($res)))
    {
        array_push($output, array("movieid" => $data['movieid'],
                                  "rating" => $data['rating'],
                                  "url" => $data['url'],
                                  "title" => $data['title']));
    }
}
elseif(isset($_SESSION[$guest_rating]))
{
    $movielist = "";
    foreach($_SESSION[$guest_rating] as $key => $valuse)
    {
        $movielist .= $key . ",";
    }
    if($movielist != "")
    {
        // remove the end ","
        $movielist = substr($movielist, 0, -1);
    }
    $str = "select movieid, url, title from movie where movieid in (" . $movielist . ")";
    $res = mysql_query($str);
    while($data = mysql_fetch_array($res))
    {
        array_push($output, array("movieid" => $data['movieid'],
                                  "rating" => $_SESSION[$guest_rating][$data['movieid']],
                                  "url" => $data['url'],
                                  "title" => $data['title']));
    }
}
foreach($output as $rec)
{
    $movieid = $rec['movieid'];
    $obj_name = "my_rate_" . $movieid;
    echo "<tr>";
    echo "<td>" . $movieid . "</td>";
    echo "<td><a href=\"" . $rec['url'] . "\" target=_blank>" . $rec['title'] . "</a></td>";
    echo "<td><select id=\"" . $obj_name . "\">";
    for($i = 5.0 ; $i >= 1.0 ; $i = $i - 0.5)
    {
        echo "<option value=" . sprintf("%.1f", $i);
        if((float)$i == (float)$rec['rating'])
        {
            echo " selected ";
        }
        echo ">" . sprintf("%.1f", $i) . "</option>";
    }
    echo "<select><br>";
    //echo "<td><input type=text id=\"" . $obj_name . "\" size=5 value=" . $rec['rating'] . ">" .
    echo "<button onclick=\"rating_movie('#" . $obj_name . "', " . $movieid . ")\">Re-rating</button></td>";
    echo "</tr>";
}
?>
</table>
<?php

?>