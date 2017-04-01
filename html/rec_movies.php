<?php
session_start();
include_once "lib/db.php";
include_once "lib/conf.php";
?>
<table border="1">
    <tr>
        <td width="70">Movie ID</td>
        <td>Movie Title</td>
        <td width="50">Movie Rating</td>
    </tr>
<?php
if(isset($_SESSION[$sessionID]) && $_SESSION[$done_rate] == 1)
{
    $url = $apiurl . "rating_rec/" . $_SESSION[$sessionID];
    $ch = curl_init();
    curl_setopt($ch,CURLOPT_URL, $url);
    curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
    $output = json_decode(curl_exec($ch));
}
else
{
    $url = $apiurl . $nonrate_rec;
    $ch = curl_init();
    curl_setopt($ch,CURLOPT_URL, $url);
    curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
    $output = json_decode(curl_exec($ch));
}
foreach($output as $rec)
{
    echo "<tr>";
    echo "<td>" . $rec->{'movieid'} . "</td>";
    echo "<td><a href=\"" . $rec->{'url'} . "\" target=_blank>" . $rec->{'title'} . "</a></td>";
    echo "<td>" . number_format($rec->{'rating'}, 2) . "</td>";
    echo "</tr>";
}
?>
</table>
<?php

?>