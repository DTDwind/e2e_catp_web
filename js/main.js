var audio_context;
var recorder;
var btn_flag = 0;
function __log(e, data) {
	// log.innerHTML += "\n" + e + " " + (data || '');
}
window.onload = function init() {
    try {
      // webkit shim
      window.AudioContext = window.AudioContext || window.webkitAudioContext;
      navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;
      window.URL = window.URL || window.webkitURL;
      
      audio_context = new AudioContext;
      __log('Audio context set up.');
      console.log('navigator.getUserMedia ' + (navigator.getUserMedia ? 'available.' : 'not present!'));
    } catch (e) {
      alert('No web audio support in this browser!');
	}

	navigator.mediaDevices.getUserMedia({audio: true}).then(function(stream) {
		startUserMedia(stream)
	})

};
function click_btn() {
	if(btn_flag%2==0){
		btn_flag++
		$('#reg').text("");
		$("#Recording_control_btn").val("結束");
		// recorder.start();
		startRecording()
		console.log("Recording...");
	}
	else{
		// stopRecording();
		stopRecording();
		$("#Recording_control_btn").val("開始");
		btn_flag++
	}
	// setTimeout("stopRecording()",60000) //60秒自動結束
}
function startUserMedia(stream) {
    var input = audio_context.createMediaStreamSource(stream);
    __log('Media stream created.');
    // Uncomment if you want the audio to feedback directly
    //input.connect(audio_context.destination);
    //__log('Input connected to audio context destination.');
    
    recorder = new Recorder(input,cfg={numChannels:1,sampleBits:16,sampleRate:16000,});
    __log('Recorder initialised.');
  }
function startRecording() {
	recorder && recorder.record();
	// button.disabled = true;
	// button.nextElementSibling.disabled = false;
	__log('Recording...');
}
function stopRecording() {
	recorder && recorder.stop();
	// button.disabled = true;
	// button.previousElementSibling.disabled = false;
	__log('Stopped recording.');

	// create WAV download link using audio data blob
	// createDownloadLink();
	recorder && recorder.exportWAV(upload_to_server)
	recorder.clear();
}

function upload_to_server(blob){
	var fd = {};
	var now = new Date();
	start = new Date().getTime();
	
	var reader = new FileReader();
	reader.onload = function(e) {
		fd["fname"] = (now.getYear()+1900)+""+(now.getMonth()+1)+""+now.getDate()+""+now.getHours()+""+now.getMinutes()+""+now.getSeconds(); //當前時間+亂數名稱(前3~6碼為當前時間(有個位數的可能)、後六碼100000~999999)，共9~12碼
		fd["data"] = e.target.result;
		fd["text1"] = document.getElementById("t1").value;
		$('#reg').text("辨識中...");
		$.ajax({
			type: 'POST',
			url: 'receive.php',
			data: fd,
			dataType: 'text',
			success: function(msg){
				// msg = msg.match(/[CDIS]+/g) 忽略I
				string_len = 2
				// msg = msg.match(/[CDS]+/g)
				// CAPT_result = []
				// for(i=0;i<string_len;i++){
				// 	if(msg[i] == "C") CAPT_result[i] = 1
				// 	else CAPT_result[i] = 0
				// }
				ans = document.getElementById("t1").value;
				ans_result =""
				ans_result = msg
				// for(i=0;i<string_len;i++){
				// 	if(CAPT_result[i])ans_result += "<span color=green>"+ans[i]+"</span>"
				// 	else ans_result += "<span style=color:red;>"+ans[i]+"</span>"
				// }

				$('#reg').text(ans_result);
				// $('#reg').append(ans_result)
				end = new Date().getTime();
				console.log("total time : "+(end - start) / 1000 + " sec");
			},
			error: function(xhr, ajaxOptions, thrownError){ 
				console.log("error code : "+xhr.status+", "+thrownError);
			}
		});
	}
	reader.readAsDataURL(blob);
}
// function createDownloadLink() {
// 		recorder && recorder.exportWAV(function(blob) {
// 		var url = URL.createObjectURL(blob);
// 		var li = document.createElement('li');
// 		var au = document.createElement('audio');
// 		var hf = document.createElement('a');
		
// 		au.controls = true;
// 		au.src = url;
// 		hf.href = url;
// 		hf.download = new Date().toISOString() + '.wav';
// 		hf.innerHTML = hf.download;
// 		li.appendChild(au);
// 		li.appendChild(hf);
// 		recordingslist.appendChild(li);
// 	});
// }