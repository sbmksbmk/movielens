<?php
session_start();

if(isset($_POST['uid']))
{
    $_SESSION['userid'] = $_POST['uid'];

    header("location: index.php");
}
?>
<form method=post>
    <table border=0>
        <tr>
            <td>ID</td>
            <td><input type=text name=uid></td>
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