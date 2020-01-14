wav_name="2019122014112.wav"
model_dictionary="/share/nas165/chengsam/espnet20191017/espnet/egs/E2E_CAPT_web_20191205/L1_T"

. utils/parse_options.sh || exit 1;
# 2019122014112.wav
echo "U0003_DS0001 /share/nas165/chengsam/www/MD_v5_chengsam/wav/$wav_name" > /share/nas165/chengsam/espnet20191017/espnet/egs/E2E_CAPT_web_20191205/L1_T/data/CAPT_WEB_test/wav.scp;
# chmod 777 /share/nas165/chengsam/www/MD_v5_chengsam/wav/$wav_name
# echo "QAQ" > /share/nas165/chengsam/espnet20191017/espnet/egs/E2E_CAPT_web_20191205/L1_T/data/CAPT_WEB_test/text;
cd $model_dictionary;
# sh $model_dictionary/run_CAPT_web_Decoder.sh;
# grep "Eval" exp/train_lsm_pytorch_vggblstmp_e6_subsample1_2_2_1_1_unit320_proj320_d1_unit300_location_aconvc10_aconvf100_mtlalpha0.5_adadelta_sampprob0.0_bs10_mli800_mlo150//decode_CAPT_WEB_test_beam40_emodel.loss.best_p0.0_len0.0-0.0_ctcw0.5_L1/result.txt;
grep "HYP:" exp/train_lsm_pytorch_vggblstmp_e6_subsample1_2_2_1_1_unit320_proj320_d1_unit300_location_aconvc10_aconvf100_mtlalpha0.5_adadelta_sampprob0.0_bs10_mli800_mlo150//decode_CAPT_WEB_test_beam40_emodel.loss.best_p0.0_len0.0-0.0_ctcw0.5_L1/result.txt;