rm ./cnvt/*.bin
rm ./cnvt/*.hex
cp ./boot.bin ./cnvt/boot_origin.bin
python ./cnvt/split_boot.py ./cnvt/boot_origin.bin ./cnvt/boot.bin
rm ./cnvt/boot_origin.bin
python2.7 ./cnvt/bin2ascii_hex.py ./cnvt/boot.bin ./cnvt/boot.hex
python2.7 ./cnvt/ascii_hex2ascii_bin.py ./cnvt/boot.hex ./cnvt/cvt_boot.bin
cp ./cnvt/cvt_boot.bin ../../../single_w7500tb/code/
cp ./cnvt/cvt_boot.bin ../../../dual_w7500tb/code/
cp ./cnvt/cvt_boot.bin ../../../postsim_w7500tb/code/
cp ./cnvt/boot.hex ../../../single_w7500tb/code/
cp ./cnvt/boot.hex ../../../dual_w7500tb/code/
cp ./cnvt/boot.hex ../../../postsim_w7500tb/code/
