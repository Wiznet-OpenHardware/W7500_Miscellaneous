import ftplib
import os
import sys


#s = ftplib.FTP('myserver.com','login','password')
HOST = sys.argv[1]
ID = sys.argv[2]
PASSWD = sys.argv[3]
FILE = sys.argv[4]
	
s = ftplib.FTP(HOST,ID,PASSWD)

f = open(FILE,'rb')
s.storbinary('STOR '+FILE, f)

f.close()
s.quit()
