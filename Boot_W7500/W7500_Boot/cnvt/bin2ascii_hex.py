import struct
import binascii
import sys


if __name__ == "__main__":

	#f1 = open("boot.bin","rb")
	#f2 = open("cvnt_boot.txt","wb")
	f1 = open(sys.argv[1],"rb")
	f2 = open(sys.argv[2],"wb")
	
	intsize = struct.calcsize('I')
	while 1:
		data = f1.read(intsize)
		if data == '':
			break
		contents = struct.unpack('<I',data)[0]
		num = "%08X" % contents
		f2.write(num)
		f2.write('\n')
	
	f1.close()
	f2.close()
	
