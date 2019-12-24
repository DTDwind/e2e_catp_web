
        var recorder;
		var audio_context;
		var myip;
		var auto_stop = 3000

        var audio = document.querySelector('audio');
		window.onload = function init() {
			
			HZRecorder.get(function (rec) {
                recorder = rec;
				});
			console.log('Requesting Microphone....');
			
		}

	
        function startRecording() {
            $('#reg').text("");
			recorder.start();
			console.log("Recording...");
			setTimeout("stopRecording()",auto_stop)
        }

        function stopRecording() {
            recorder.stop();
            console.log("Stop Recording.");
            console.log("Send the WAV file...");
            uploadAudio(recorder.getBlob());
        }
		
		function uploadAudio( blob ) {
			var reader = new FileReader();
			reader.onload = function(event){
				var fd = {};
				var now = new Date();
				start = new Date().getTime();
				fd["fname"] = (now.getYear()+1900)+""+(now.getMonth()+1)+""+now.getDate()+""+now.getHours()+""+now.getMinutes()+""+now.getSeconds(); //當前時間+亂數名稱(前3~6碼為當前時間(有個位數的可能)、後六碼100000~999999)，共9~12碼
				fd["data"] = event.target.result;
				fd["text1"] = document.getElementById("t1").value;
				$.ajax({
				type: 'POST',
				url: 'receive.php',
				data: fd,
				dataType: 'text',
				success: function(msg){
					// msg = msg.match(/[CDIS]+/g) 忽略I
					string_len = 2
					msg = msg.match(/[CDS]+/g)
					CAPT_result = []
					for(i=0;i<string_len;i++){
						if(msg[i] == "C") CAPT_result[i] = 1
						else CAPT_result[i] = 0
					}
					ans = document.getElementById("t1").value;
					ans_result =""
					for(i=0;i<string_len;i++){
						if(CAPT_result[i])ans_result += "<span color=green>"+ans[i]+"</span>"
						else ans_result += "<span style=color:red;>"+ans[i]+"</span>"
					}
					// $('#reg').text(ans_result);
					$('#reg').append(ans_result)
					end = new Date().getTime();
					console.log("total time : "+(end - start) / 1000 + " sec");
                },
				error: function(xhr, ajaxOptions, thrownError){ 
					console.log("error code : "+xhr.status+", "+thrownError);
                }
				});
		};
		reader.readAsDataURL(blob);
		}
		function setText1() {
            var elem = document.getElementById("t1");
			elem.value = "I like hiking.";
			auto_stop = 3000;
        }