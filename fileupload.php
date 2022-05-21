<?php
use Aws\S3\S3Client;
require 'vendor/autoload.php';
$key = $_ENV['s3_key'];
$secret = $_ENV['s3_secret'];

$raw_credentials = array(
    'credentials' => [
        'key' => $key,
        'secret' => 
    ],
    'endpoint' => 'https://s3.wasabisys.com', 
    'region' => 'us-east-1', 
    'version' => 'latest',
    'use_path_style_endpoint' => true
);

$list = "qwertyuiopasdfghjklzxcvbnm1234567890";
$length = 8;
$ext = pathinfo($_FILES["file"]["name"], PATHINFO_EXTENSION);

$filename = substr(str_shuffle($list),1,$length);
$filename = "{filename}{ext}";
$filepath = "../privuploads/{filename}";

$bucket = $_ENV['s3_bucket'];

// create connection to s3
$s3 = S3Client::factory($raw_credentials);

move_uploaded_file($_FILES["fileUpload"]["tmp_name"], $filepath);

try {
    // upload file
    $result = $s3->putObject([
        'Bucket' => $bucket,
        'Key' => $key,
        'SourceFile' => $filepath]);
    unlink($filepath);
} catch (S3Exception $e) {
    unlink($filepath);
    echo $e->getMessage() . PHP_EOL;
}


print "<head><link rel=\"stylesheet\" type=\"text/css\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css\"><script src=\"https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js\" integrity=\"sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQR$</script><script defer=\"\" src=\"https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js\" integrity=\"sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfk$</script><script src=\"https://code.jquery.com/jquery-3.6.0.min.js\" integrity=\"sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=\" crossorigin=\"anonymous\"></script><meta name=\"viewport\" content=\"width=device-width, initial-scale=1, shrink-to-fit=no\"><meta name=\"description\" content=\"File uploader.\"><link rel=\"stylesheet\" type=\"text/css\" href=\"https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/darkly/bootstrap.min.css\"></head><nav class=\"navbar navbar-expand-lg navbar-dark bg-dark\"><a class=\"navbar-brand\" href=\"/index.html\">File Uploader</a></nav><body><div style=\"padding: 80px\"></div><div class=\"d-flex justify-content-center\"><h3>Link Shortened!</h3></div></div><div style=\"padding: 10px\"/><div class=\"d-flex justify-content-center\"><h5>Your file is located at https://uploads.trihard.space/{$filename}.</h5></div></div></div></body>";


}


?>
