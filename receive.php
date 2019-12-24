<?php
// 為超時做準備。
// https://www.itread01.com/p/964655.html

$model_dir="";
$wav_dir="wav";
$tmp_dir="tmp";

$wav_file_name = $_POST['fname'];
$answer_text = $_POST['text1'];

$mtime = explode(" ", microtime()); //寫檔
$startTime = $mtime[1] + $mtime[0];

// pull the raw binary data from the POST array
$data = substr($_POST['data'], strpos($_POST['data'], ",") + 1);
// decode it
$decodedData = base64_decode($data);

$file_path = $wav_dir."/".$wav_file_name.".wav";

$fp1 = fopen($file_path, 'wb');
fwrite($fp1, $decodedData);
fclose($fp1);

$fp2 = fopen($wav_dir."/".$wav_file_name."_ANSlist.txt", 'wb');//將最原始的答案存到硬碟中(未來發展用)
fwrite($fp2, $answer_text."\n");

// $a= passthru("./run_decode.sh --wav_name ".$wav_file_name.".wav");
$a = exec("./run_decode.sh --wav_name ".$wav_file_name.".wav");
echo "QQ".$a;
// passthru("./test.sh");

$mtime = explode(" ", microtime()); 
$endTime = $mtime[1] + $mtime[0];
$totalTime = ($endTime - $startTime); 
//echo "辨識所需時間".$totalTime." seconds\n";

?>
