<?php

$source = $_FILES['profile']['tmp_name'];
$dest = "./".basename($_FILES['profile']['name']);
move_uploaded_file($source,$dest);
?>

<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title></title>
    </head>

    <body>
        <img src="<?=$_FILES['image_file']['name']?>" alt="">
    </body>
</html>

<!-- 보류 -->