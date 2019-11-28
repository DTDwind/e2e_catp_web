
if [ $# != 1 ]; then
   echo "Usage: $0 [options] <kaldi-dir>";
   echo "e.g.: $0 ~/kaldi-trunk"
   echo "options: "
   echo "				"
   exit 1;
fi

kaldi_dir=$1


echo "Creating necessary directory ... "
rm -rf src
mkdir src
mkdir -p tmp
mkdir -p wav
chmod 777 tmp
chmod 777 wav

echo "kaldi directory : [ "${kaldi_dir}" ] "
echo "Linking kaldi function to here ..."

echo " [ compute-mfcc-feats ] "
ln -s ${kaldi_dir}/src/featbin/compute-mfcc-feats src/compute-mfcc-feats
echo " [ nnet-forward ] "
ln -s ${kaldi_dir}/src/nnetbin/nnet-forward src/nnet-forward
echo " [ sym2int.pl ] "
ln -s ${kaldi_dir}/egs/wsj/s5/utils/sym2int.pl src/sym2int.pl
echo " [ compile-train-graphs ] "
ln -s ${kaldi_dir}/src/bin/compile-train-graphs src/compile-train-graphs
echo " [ align-compiled-mapped ] "
ln -s ${kaldi_dir}/src/bin/align-compiled-mapped src/align-compiled-mapped
echo " [ add-deltas ] "
ln -s ${kaldi_dir}/src/featbin/add-deltas src/add-deltas
echo " [ compute-kaldi-pitch-feats ] "
ln -s ${kaldi_dir}/src/featbin/compute-kaldi-pitch-feats src/compute-kaldi-pitch-feats
echo " [ compute-fbank-feats ] "
ln -s ${kaldi_dir}/src/featbin/compute-fbank-feats src/compute-fbank-feats
echo " [ paste-feats ] "
ln -s ${kaldi_dir}/src/featbin/paste-feats src/paste-feats
echo " [ process-kaldi-pitch-feats ] "
ln -s ${kaldi_dir}/src/featbin/process-kaldi-pitch-feats src/process-kaldi-pitch-feats


rm utils steps
echo " [ utils ] "
ln -s ${kaldi_dir}/egs/wsj/s5/utils utils
echo " [ steps ] "
ln -s ${kaldi_dir}/egs/wsj/s5/steps steps


echo "Done."