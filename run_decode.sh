wav_name="QAQ"

. utils/parse_options.sh || exit 1;
# echo {{$wav_name}};
# 20191219164236.wav
echo "U0003_DS0001 /share/nas165/chengsam/www/MD_v5_chengsam/wav/$wav_name" > /share/nas165/chengsam/espnet20191017/espnet/egs/E2E_CAPT_web_20191205/L1_T/data/CAPT_WEB_test/wav.scp;
/share/nas165/chengsam/espnet20191017/espnet/egs/E2E_CAPT_web_20191205/L1_T/run_CAPT_web_Decoder.sh
# echo "TATTT"