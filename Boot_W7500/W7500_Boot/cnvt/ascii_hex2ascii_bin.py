import sys
import binascii

def byte_to_binary(n):
	return ''.join(str((n & (1 << i)) and 1) for i in reversed(range(8)))


def hex_to_binary(h):
	return ''.join(byte_to_binary(ord(b)) for b in binascii.unhexlify(h))
				   
if __name__ == "__main__":
	f1 = open(sys.argv[1],"r")
	f2 = open(sys.argv[2],"w")
	cvt_line = ''

	for line in f1:
		cvt_line = line[:8]
		f2.write(hex_to_binary(cvt_line))
		f2.write("\r\n")

	f1.close
	f2.close

