<?php
$list = "qwertyuiopasdfghjklzxcvbnm1234567890";
$length = 8;
$dirname = substr(str_shuffle($list),1,$length);
$target_dir = "uploads/{$dirname}/";
$target_file = $target_dir . basename($_FILES["fileUpload"]["name"]);
$uploadGood = 1;
$target_file_escaped = htmlspecialchars($target_file);

if ($_FILES["fileUpload"]["size"] > 1000000000) {
        $uploadGood = 0;
}

if ($uploadGood == 0) {
        header('http://files.icurriculum.co/fail.html', true, 200);
}

else {
        mkdir($target_dir);
        move_uploaded_file($_FILES["fileUpload"]["tmp_name"], $target_file);
        print "<head><link rel=\"stylesheet\" type=\"text/css\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css\"><script src=\"https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js\" integrity=\"sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQR$</script><script defer=\"\" src=\"https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js\" integrity=\"sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfk$</script><script src=\"https://code.jquery.com/jquery-3.6.0.min.js\" integrity=\"sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=\" crossorigin=\"anonymous\"></script><meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\"><meta name=\"description\" content=\"File uploader.\"><link rel=\"stylesheet\" type=\"text/css\" href=\"https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/darkly/bootstrap.min.css\"></head><nav class=\"navbar navbar-expand-lg navbar-dark bg-dark\"><a class=\"navbar-brand\" href=\"/index.html\">File Uploader</a></nav><body><div style=\"padding: 80px\"></div><div class=\"d-flex justify-content-center\"><h3>Link Shortened!</h3></div></div><div style=\"padding: 10px\"/><div class=\"d-flex justify-content-center\"><h5>Your file is located at https://your_host_here.com/{$target_file_escaped}.</h5></div></div></div></body>";


}


?>
