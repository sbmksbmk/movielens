<?php
include_once "lib/db.php";
header("Content-Type:text/html; charset=utf-8");
if(isset($_POST['acc']))
{
    $time = date('Y-m-d H:i:s');
    $name = $_POST['acc'];
    $str = "insert into member (userid, password, username, email, sex, birthday, created_time) values " .
           "('" . $_POST['acc'] . "', '" . $_POST['pwd'] . "', '" . mysql_real_escape_string($name) . "', " .
           "'" . $_POST['email'] . "', '" . $_POST['sex'] . "', '" . $_POST['birthday'] . "', " .
           "'" . $time . "')";
    mysql_query($str);
    if(mysql_errno() == 0)
    {
        echo $str;
        //header("location: index.php");
    }
    else
    {
        if(mysql_errno() == 1062)
        {
            echo "<div align=center><font color=red>";
            if(endsWith(mysql_error(), "'PRIMARY'"))
            {
                echo "Account Existed!!";
            }
            else if(endsWith(mysql_error(), "'email_UNIQUE'"))
            {
                echo "eMail Existed!!";
            }
            else
            {
                echo "Something wrong!!";
            }
            echo "</font></div>";
        }
    }
}
function endsWith($haystack, $needle)
{
    $length = strlen($needle);
    if ($length == 0) {
        return true;
    }

    return (substr($haystack, -$length) === $needle);
}
?>
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta name="keywords" content="" />
        <meta name="description" content="" />
        <meta http-equiv="content-type" content="text/html; charset=utf-8" />
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8/themes/base/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.11.1/jquery-ui.min.js"></script>
        <script src="js/md5.min.js"></script>
        <script>
            $(function() {
                $( "#datepicker" ).datepicker({defaultDate: "2000/01/01", dateFormat: "yy/mm/dd", changeYear: true, changeMonth: true, });
            });
        </script>
        <script type="text/javascript">
            function validateEmail(email)
            {
                var re = /^\w+([\.-_]?\w+)*@\w+([\.-]?\w+)*(\.\w+)+$/;
                return re.test(email);
            }
            function checkreg(form)
            {
                if(!validateEmail(form.email.value))
                {
                    alert("eMail form error!");
                    return false;
                }
                if(form.pwd.value != form.vpwd.value)
                {
                    alert("password not the same");
                    return false;
                }
                else
                {
                    form.pwd.value = md5(form.pwd.value);
                    form.vpwd.value = null;
                    return true;
                }
                return false;
            }
        </script>
    </head>
<div align="center">
<form method=POST id="regform" onsubmit="return checkreg(this)">
    <table border=1>
        <tr>
            <td colspan="2" align="center">建立帳號</td>
        </tr>
        <tr>
            <td>帳號</td>
            <td><input type=text name=acc required value="<?php echo $_POST['acc'];?>"></td>
        </tr>
        <tr>
            <td>密碼</td>
            <td><input type=password name=pwd required></td>
        </tr>
        <tr>
            <td>密碼驗證</td>
            <td><input type=password name=vpwd required></td>
        </tr>
        <tr>
            <td>eMail</td>
            <td><input type="email" placeholder="me@example.com" name=email required value="<?php echo $_POST['email'];?>"></td>
        </tr>
        <tr>
            <td>性別</td>
            <td>
                <select name=sex>
                    <option value="f">女</option>
                    <option value="m" <?php if($_POST['sex'] == "m") echo "selected";?>>男</option>
                </select>
            </td>
        </tr>
        <tr>
            <td>生日</td>
            <td><input type=text name=birthday maxlength=15 id="datepicker" required value="<?php echo $_POST['birthday'];?>"></td>
        </tr>
            <td colspan="2" align="center"><input type=submit value="建立"></td>
        </tr>
    </table>
</form>
</div>