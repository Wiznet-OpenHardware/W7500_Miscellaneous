#import binascii
import sys

Length = 4096
str = '\xfe\xe7\xfe\xe7'

#f1 = open("./cnvt/boot_origin.bin","r+b")
f1 = open(sys.argv[1],"r+b")
f1.seek(0x00)
#f2 = open("./cnvt/boot.bin","w+b")
f2 = open(sys.argv[2],"w+b")

while Length:
	data = f1.read(1024)
	f2.write(data)
	Length -= 1024

f2.seek(0x00000FFC)
f2.write(str)
f1.seek(0x1FFF1000)

Length = 2048

while Length:
	data = f1.read(1024)
	f2.write(data)
	Length -= 1024

f2.seek(0x00017F8)
f2.write(str)
f1.close()
f2.close()
