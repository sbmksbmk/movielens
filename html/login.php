<?php
session_start();
include_once "lib/db.php";
include_once "lib/conf.php";
if(isset($_SESSION[$sessionID]))
{
    header("location: index.php");
}

if(isset($_POST['uid']))
{
    $str = "select * from member where userid = \"" . $_POST['uid'] . "\"";
    $res = mysql_query($str);
    if(mysql_num_rows($res) == 1)
    {
        $data = mysql_fetch_array($res);
        if($data['password'] == $_POST['pwd'])
        {
            $_SESSION[$sessionID] = $_POST['uid'];
            $_SESSION[$done_rate] = $data[$done_rate];
            $_SESSION[$display] = $_POST['uid'];
            unset($_SESSION[$guest_rating]);
            header("location: index.php");
        }
        else
        {
            echo "Login Failed!<br>";
        }
        
    }
    else
    {
        echo "Login Failed!<br>";
    }
}
?>
<script src="js/md5.min.js"></script>
<script type="text/javascript">
function checkreg(form)
{
    form.pwd.value = md5(form.pwd.value);
}
</script>
<form method=post id="loginform" onsubmit="checkreg(this)">
    <table border=0>
        <tr>
            <td>ID</td>
            <td><input type=text name=uid <?php echo $_POST['uid'];?>></td>
        </tr>
        <tr>
            <td>Password</td>
            <td><input type=password name=pwd></td>
        </tr>
        <tr>
            <td colspan="2">
                <input type=submit value="Login">
            </td>
        </tr>
    </table>
</form>

