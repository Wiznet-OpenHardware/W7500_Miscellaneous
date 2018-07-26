rm ./cnvt/*.bin
rm ./cnvt/*.hex
cp ./emul_boot.bin ./cnvt/boot_origin.bin
python ./cnvt/split_boot.py ./cnvt/boot_origin.bin ./cnvt/emul_boot.bin
rm ./cnvt/boot_origin.bin
cd cnvt
python run_ftp.py 222.98.173.202 kaizen 1234 emul_boot.bin
cd ..
