<?php
session_start();
include_once "lib/db.php";
include_once "lib/conf.php";

if(isset($_GET['return_max']))
{
    $return_max = $_GET['return_max'];
}
else
{
    $return_max = 100;
}
?>
<table border="1">
    <tr>
        <td width="30">ID</td>
        <td colspan="2">Movie Title</td>
        <td width="70">Your Rating</td>
        <td width="50">Movie Rating</td>
    </tr>
<?php
if(isset($_SESSION[$sessionID]) && $_SESSION[$done_rate] == 1)
{
    // recommendation for members who had rating before
    $url = $apiurl . "rating_rec/" . $_SESSION[$sessionID] .
           "?return_max=" . $return_max . "&age=" . $_SESSION['age'] .
           "&gender=" . $_SESSION['gender'];
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $output = json_decode(curl_exec($ch));
}
elseif(isset($_SESSION[$guest_rating]))
{
    // recommendation for GUEST
    $rating = $_SESSION[$guest_rating];
    if(isset($_SESSION['age']))
    {
        $rating['age'] = $_SESSION['age'];
    }
    if(isset($_SESSION['gender']))
    {
        $rating['gender'] = $_SESSION['gender'];
    }
    $url = $apiurl . "rating_rec_guest" . "?return_max=" . $return_max;
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $rating);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $output = json_decode(curl_exec($ch));
}
else
{
    // recommendation for each one who never rating before
    $url = $apiurl . $nonrate_rec . "?return_max=" . $return_max;
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $output = json_decode(curl_exec($ch));
}
foreach($output as $rec)
{
    $movieid = $rec->{'movieid'};
    $obj_name = "my_rate_" . $movieid;
    echo "<tr>";
    echo "<td>" . $movieid . "</td>";
    echo "<td style=\"border-right-style:hidden;\"><img src=\"" . $rec->{'poster'} . "\" width=150></td>";
    echo "<td valign=top style=\"border-left-style:hidden;\"><a href=\"" . $rec->{'url'} . "\" target=_blank>" .
         "<font size=5>" . $rec->{'title'} . "</font></a><p><b>Genres:</b> " . $rec->{'movie_type'} . "<p>" .
         "<b>Description:</b> " . $rec->{'description'} . "</td>";
    echo "<td><select id=\"" . $obj_name . "\">";
    echo get_option(number_format($rec->{'rating'}, 2));
    echo "<select><br>";
    echo "<button onclick=\"rating_movie('#" . $obj_name . "', " . $movieid . ")\">Rating It</button></td>"; 
    echo "<td>" . number_format($rec->{'rating'}, 2) . "</td>";
    echo "</tr>";
}
?>
</table>
<?php
function get_option($rating)
{
    $rec_score = round($rating * 2) / 2;
    $option = "<option value=5.0 selected>5.0</option>";
    for($i = 4.5 ; $i >= 1.0 ; $i = $i - 0.5)
    {
        $option .= "<option value=" . sprintf("%.1f", $i);
        if($i == $rec_score)
        {
            $option .= " selected ";
        }
        $option .= ">" . sprintf("%.1f", $i) . "</option>";
    }
    return $option;
}
?>