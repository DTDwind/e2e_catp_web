<?php
// 為超時做準備。
// https://www.itread01.com/p/964655.html

$model_dir="";
$wav_dir="wav";
$tmp_dir="tmp";
// $tau="-3";
// $reject_rate="0.1";

$sample_frequency=16000;
$make_mfcc="src/compute-mfcc-feats --use-energy=false --verbose=2 --config=conf/mfcc.conf";
$make_fbank="src/compute-fbank-feats --use-energy=false --verbose=2 --config=conf/fbank.conf";
$make_pitch="src/compute-kaldi-pitch-feats --sample-frequency=$sample_frequency --verbose=2 --config=conf/pitch.conf";
$paste_feats="src/paste-feats ";
$process_kaldi_pitch_feats="src/process-kaldi-pitch-feats ";
$sym2int="src/sym2int.pl --map-oov `cat $lang_dir/oov.int` -f 2- $words_txt";
$AddDeltas="src/add-deltas ";

// GOP
// $CheckWordExist="python py_code/CheckWordExist.py $words_txt";
// $graphfile="$graph_dir";
// $PhoneLevelGOP="python py_code/PhoneLevelGOP_v3.py $tau $reject_rate $phones_txt $transitions";
// $Word2Phone="python py_code/Word2Phone.py $lexicon ";

$mtime = explode(" ", microtime()); //寫檔
$startTime = $mtime[1] + $mtime[0];

// pull the raw binary data from the POST array
$data = substr($_POST['data'], strpos($_POST['data'], ",") + 1);
// decode it
$decodedData = base64_decode($data);

$random_code=$_POST['fname'];
$filename = $wav_dir."/".$_POST['fname'].".wav";

$fp1 = fopen($filename, 'wb');
fwrite($fp1, $decodedData);
fclose($fp1);

$fp2 = fopen($wav_dir."/".$random_code."_ANSlist.txt", 'wb');//將最原始的答案存到硬碟中(未來發展用)
fwrite($fp2, $_POST['text1']."\n");
fwrite($fp2, "############\n");



//$symbol = [" ",",",".","?","!","(",")" ,"N'T" ,"'S" ,"'M"];
//$rp_sym = ["#","#","#","#","#","#","#" ,"#NOT","#IS","#AM"];
$symbol = [" ",",",".","?","!","(",")","’"];
$rp_sym = ["#","#","#","#","#","#","#","'"];

//var_dump($symbol);
for($i = 0; $i < sizeof($symbol);$i++)
{
	$_POST['text1'] = str_replace($symbol[$i],$rp_sym[$i],$_POST['text1']);
}
$WordsOption=$_POST['text1'];
$WordsOption = str_replace("'","#",$WordsOption);

$_POST['text1'] = "#".$_POST['text1']."#";//前後都加上#，減少邊界造成的麻煩
//目前只處理到連續符號20個，超過20個連續符號則會造成錯誤
$symbol = ["###################","##################","#################","################","###############",
	"##############","#############","############","###########","##########",
	"##########","#########","########","#######","######","#####","####" ,"###" ,"##" ,"#"];
$rp_sym = [" "];
for($i = 0; $i < sizeof($symbol);$i++)
{
	$_POST['text1'] = str_replace($symbol[$i],$rp_sym[0],$_POST['text1']);//將符號#正規化成一個space
}

$text_array = $_POST['text1'];//將最原始的答案先暫存起來

$_POST['text1'] = strtoupper($_POST['text1']);



$ret;
$text_reg = " ";//暫存辨識出來的答案



// if (file_exists("$graph_dir/$WordsOption"))//Graph已經存在了，只需指向該Graph，不須再mkgraph。
// {
// 	$graphfile="$graph_dir/$WordsOption";
// 	//$dnndecode="$kaldi_dir/src/bin/latgen-faster-mapped-parallel --num-threads=1 --min-active=200 --max-active=7000 --max-mem=50000000 --beam=18 --lattice-beam=10 --acoustic-scale=0.10 --allow-partial=false --word-symbol-table=$graphdir/words.txt $model $graphfile";
// 	$ret[0] = "No Create Graph.";
// }
// if(0)1;
// else//不存在該Graph，需要建立一個新的，但在建立之前要先確定沒有任何單字有拚錯(或太特別不存在於字典)。
// {
// 	exec($CheckWordExist." \"".$_POST['text1']."\" ", $ret,$ret_code);
// 	//var_dump($ret);
// 	if ($ret[0] == "No Error.")
// 	{
// 		$tmp_text = tempnam("$tmp_dir", $random_code."_text_");
// 		file_put_contents("$tmp_text","key ".$_POST['text1']."\n");
// 		$tmp_tra = tempnam("$tmp_dir", $random_code."_tra_");
// 		passthru("$sym2int $tmp_text > $tmp_tra ");
// 		$graph_name = $graph_dir."/".$WordsOption;
// 		passthru("$CompileTrainGraphs ark:$tmp_tra ark:$graph_name ");
// 		$graphfile="$graph_dir/$WordsOption";
// 	}
// 	else if($ret[0] == "Error Words!")
// 	{
// 		echo $ret[0]."\n";
// 		fwrite($fp2, $ret[0]."\n");
// 	}
	
// }
$wavscp = tempnam("$tmp_dir", $random_code."_wavscp_");
//file_put_contents("$wavscp","key sox --norm -t wav $filename -r 16k -t wav -|\n");
file_put_contents("$wavscp","key $filename\n");
$fb40 = tempnam("$tmp_dir", $random_code."_fb40_");
passthru("$make_fbank scp:$wavscp ark:$fb40");
$pitch = tempnam("$tmp_dir", $random_code."_pitch_");
passthru("$make_pitch scp:$wavscp ark:- | $process_kaldi_pitch_feats ark:- ark:$pitch");
//add CMVN


// 丟到NN的輸出
// $nnposterior = tempnam("$tmp_dir", $random_code."_nnposterior_");
// passthru("$paste_feats ark:$fb40 ark:$pitch ark:- | $AddDeltas ark:- ark:- | $dnnforward ark:- ark,t:$nnposterior ");



//時間資訊
// $ali = tempnam("$tmp_dir", $random_code."_ali_");


// passthru("$AlignCompiledMapped ark:$graphfile ark,t:$nnposterior ark,t:$ali ");
// exec("$PhoneLevelGOP $ali $nnposterior ", $pronun,$pronun_code);
// //var_dump($_POST['text1']);
// //var_dump($pronun);
// exec("$Word2Phone \"".$text_array."\" \"$pronun[0]\" ", $word_level_pronun,$pronun_code);
// //var_dump($word_level_pronun);
// foreach($word_level_pronun as $p)
// {
// 	echo "$p\n";
// 	fwrite($fp2, "$p\n");
// }


$mtime = explode(" ", microtime()); 
$endTime = $mtime[1] + $mtime[0]; 
$totalTime = ($endTime - $startTime); 
//echo "辨識所需時間".$totalTime." seconds\n";

?>
