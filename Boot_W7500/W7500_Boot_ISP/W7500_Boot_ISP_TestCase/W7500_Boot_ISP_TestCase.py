'''
Created on 2014. 8. 5.

@author: kaizen
'''
import unittest
import serial
import time
from xmodem import XMODEM

COM = 'COM4'
BAUD = 115200
comP = COM
baudR = BAUD
RET_SUCCESS     = '0'
RET_IVLD_SIZE   = '1'
RET_IVLD_ADDR   = '2'
RET_IVLD_CMD    = '3'
RET_NO_PRIV     = '4'
RET_IVLD_PARAM  = '5'
RET_READ_LOCK   = '6'
RET_WRITE_LOCK  = '7' 
RET_RESET       = '8'

class W7500_ISP(object):
    def __init__(self, comP, baud, timeoutValue):
        self.ser = serial.Serial(comP, baud, timeout = timeoutValue)

    def serialClose(self):
        self.ser.close()
    def __del__(self):
        self.serialClose()
        
    def negoComP(self):
        while True:
            self.ser.write('U')
            recv = self.ser.read()
            print recv
            if recv == 'U':     break
            time.sleep(1)
            
        print self.ser.readline()
        
    def writeCmd(self,cmd,resp="0",paramLine=1,loopCnt=3,opt=0):
        cmd = cmd + '\r'
        resp = resp + '\r\n'
        
        print "Send Command : %s" % cmd
        self.ser.write(cmd)
        tempData =""
        
        for i in range(loopCnt):
            respData = self.ser.readline()
            if(i == paramLine -1):
                tempData = respData
            
            print "Resp : %s" % respData,
            if(respData == resp):
                break

        print("")
        return tempData
    
    def getc(self,size,timeout=1):
        return self.ser.read(size)
    def putc(self,data,timeout=1):
        return self.ser.write(data)
    
    def Xmodem_init(self):
        self.xmodem = XMODEM(self.getc,self.putc)
    def Xmodem_Send(self,start_addr,size,file_path):
        cmd = "XPRG " + start_addr + " " + size + "\r"
        self.ser.write(cmd)
        stream = open(file_path,'rb')
        print "Start Send Binary using XMODEM"
        self.xmodem.send(stream)
        stream.close()

        print self.ser.readall()
        print "End XMODEM"

class Isp_Test(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print "Set Up"
        print "Press the reset button"
        self.isp = W7500_ISP(comP, baudR, 1)
        self.isp.negoComP()
        self.isp.writeCmd("","3")
        resp = self.isp.writeCmd("LOCK PROG 00000000 00000000")
    @classmethod
    def tearDownClass(self):
        print "Tear Down"
        self.isp.serialClose()

    def test1_EraseCmd(self):
        print "*******************************************************"
        print "ERAS Command Test"
        print "*******************************************************"
        resp = self.isp.writeCmd("ERAS DAT0")
        self.assertEqual(resp[0],RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 0003FEFC 00000004","0",1)
        self.assertEqual(resp,"0003FEFC:FFFFFFFF\r\n")
          
        resp = self.isp.writeCmd("ERAS DAT1")
        self.assertEqual(resp[0],RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 0003FFFC 00000004","0",1)
        self.assertEqual(resp,"0003FFFC:FFFFFFFF\r\n")
          
        resp = self.isp.writeCmd("ERAS SECT 00000000")
        self.assertEqual(resp[0],RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 000000FC 00000004","0",1)
        self.assertEqual(resp,"000000FC:FFFFFFFF\r\n")
  
        resp = self.isp.writeCmd("ERAS CHIP")
        self.assertEqual(resp[0],RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 00000000 00000004","0",1)
        self.assertEqual(resp,"00000000:FFFFFFFF\r\n")
        resp = self.isp.writeCmd("DUMP 0001FFFC 00000004","0",1)
        self.assertEqual(resp,"0001FFFC:FFFFFFFF\r\n")
  
        resp = self.isp.writeCmd("ERAS MASS")
        self.assertEqual(resp[0],RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 0001FFFC 00000004","0",1)
        self.assertEqual(resp,"0001FFFC:FFFFFFFF\r\n")
        resp = self.isp.writeCmd("DUMP 0003FEFC 00000004","0",1)
        self.assertEqual(resp,"0003FEFC:FFFFFFFF\r\n")
        resp = self.isp.writeCmd("DUMP 0003FFFC 00000004","0",1)
        self.assertEqual(resp,"0003FFFC:FFFFFFFF\r\n")
          
    def test2_DownCmd(self):
        print "*******************************************************"
        print "Down Command Test"
        print "*******************************************************"
        self.isp.writeCmd("DOWN 20000000 00003000",RET_SUCCESS,1,0)  #12KB
        data_value = 'A'
        for i in range(12*1024): 
            self.isp.ser.write(data_value)
        resp = self.isp.ser.readline()
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 20000000 00000004","0",1)
        self.assertEqual(resp,"20000000:41414141\r\n")
        resp = self.isp.writeCmd("DUMP 20002FFC 00000004","0",1)
        self.assertEqual(resp,"20002FFC:41414141\r\n")
          
        self.isp.writeCmd("DOWN 20000000 00000100","0",1,0) #256Byte
        data_value = 'B'
        for i in range(256):
            self.isp.ser.write(data_value)
        resp = self.isp.ser.readline()
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 200000FC 00000004","0",1)
        self.assertEqual(resp,"200000FC:42424242\r\n")
          
        self.isp.writeCmd("DOWN 20000100 00000100","0",1,0) #256Byte
        data_value = 'C'
        for i in range(256):
            self.isp.ser.write(data_value)
        resp = self.isp.ser.readline()
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 200001FC 00000004","0",1)
        self.assertEqual(resp,"200001FC:43434343\r\n")
  
  
        self.isp.writeCmd("DOWN 20000200 00002800","0",1,0) #10KByte
        data_value = 'D'
        for i in range(10240):
            self.isp.ser.write(data_value)
        resp = self.isp.ser.readline()
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 200020FC 00000004","0",1)
        self.assertEqual(resp,"200020FC:44444444\r\n")
          
    def test3_ProgCmd(self):
        print "*******************************************************"
        print "PROG Command Test"
        print "*******************************************************"
        resp = self.isp.writeCmd("ERAS MASS")
        self.assertEqual(resp[0],RET_SUCCESS)
           
        resp = self.isp.writeCmd("PROG DAT0 20000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 0003FE00 00000004","0",1)
        self.assertEqual(resp,"0003FE00:42424242\r\n")
        resp = self.isp.writeCmd("DUMP 0003FEFC 00000004","0",1)
        self.assertEqual(resp,"0003FEFC:42424242\r\n")
           
        resp = self.isp.writeCmd("PROG DAT1 20000100")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 0003FF00 00000004","0",1)
        self.assertEqual(resp,"0003FF00:43434343\r\n")
        resp = self.isp.writeCmd("DUMP 0003FFFC 00000004","0",1)
        self.assertEqual(resp,"0003FFFC:43434343\r\n")
   
        resp = self.isp.writeCmd("PROG CODE 00010000 20000200 00002800")    #10KByte
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 00010000 00000004","0",1)
        self.assertEqual(resp,"00010000:44444444\r\n")
        resp = self.isp.writeCmd("DUMP 000127FC 00000004","0",1)
        self.assertEqual(resp,"000127FC:44444444\r\n")

        
    def test4_CopyCmd(self):
        print "*******************************************************"
        print "COPY Command Test"
        print "*******************************************************"
        resp = self.isp.writeCmd("COPY 00010000 20000000 00002800")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 20000000 00000004","0",1)
        self.assertEqual(resp,"20000000:44444444\r\n")
        resp = self.isp.writeCmd("DUMP 200027FC 00000004","0",1)
        self.assertEqual(resp,"200027FC:44444444\r\n")
           
    def test5_LockCmd(self):
        print "*******************************************************"
        print "LOCK Command Test"
        print "*******************************************************"
        resp = self.isp.writeCmd("LOCK PROG 00000000 00000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("REST", RET_RESET)
        self.assertEqual(resp[0], RET_RESET)
        self.isp.negoComP()
        self.isp.writeCmd("","3")
   
        resp = self.isp.writeCmd("LOCK READ")
        self.assertEqual(resp, '00000000 00000000\r\n')
           
        resp = self.isp.writeCmd("LOCK PROG FFFFFFFF FFFFFFFF")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("REST", RET_RESET)
        self.assertEqual(resp[0], RET_RESET)
        self.isp.negoComP()
        self.isp.writeCmd("","3")
   
        resp = self.isp.writeCmd("LOCK READ")
        self.assertEqual(resp, 'C000000F FFFFFFFF\r\n')
           
        print "*******************************************************"
        print "Read Lock Test"
        print "*******************************************************"
        resp = self.isp.writeCmd("LOCK PROG 80000000 00000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 00000000 00000004","0",1)
        self.assertEqual(resp, "00000000:00000000\r\n")
        resp = self.isp.writeCmd("DUMP 0001FFFC 00000004","0",1)
        self.assertEqual(resp, "0001FFFC:00000000\r\n")
           
        print "*******************************************************"
        print "Code All Block Write Lock Test"
        print "*******************************************************"
        resp = self.isp.writeCmd("LOCK PROG 40000000 00000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("LOCK READ")
        self.assertEqual(resp, "40000000 00000000\r\n")
        resp = self.isp.writeCmd("PROG CODE 00000000 20000000 00000100",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 0001FFFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
           
           
        print "*******************************************************"
        print "Data 1/0 Read Lock Test"
        print "*******************************************************"
        resp = self.isp.writeCmd("LOCK PROG 00000008 00000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 0003FF00 00000004","0",1)
        self.assertEqual(resp, "0003FF00:00000000\r\n")
        resp = self.isp.writeCmd("DUMP 0003FFFC 00000004","0",1)
        self.assertEqual(resp, "0003FFFC:00000000\r\n")
   
        resp = self.isp.writeCmd("LOCK PROG 00000004 00000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 0003FE00 00000004","0",1)
        self.assertEqual(resp, "0003FE00:00000000\r\n")
        resp = self.isp.writeCmd("DUMP 0003FEFC 00000004","0",1)
        self.assertEqual(resp, "0003FEFC:00000000\r\n")
   
        print "*******************************************************"
        print "Data 1/0 Write Lock Test"
        print "*******************************************************"
        resp = self.isp.writeCmd("LOCK PROG 00000002 00000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG DAT1",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
           
        resp = self.isp.writeCmd("LOCK PROG 00000001 00000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG DAT0",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
   
        print "*******************************************************"
        print "Code Block Wirte Test"
        print "*******************************************************"
        resp = self.isp.writeCmd("LOCK PROG 00000000 00000001")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00000000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00000FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
           
        resp = self.isp.writeCmd("LOCK PROG 00000000 00000002")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00001000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00001FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00000004")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00002000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00002FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00000008")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00003000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00003FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00000010")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00004000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00004FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00000020")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00005000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00005FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00000040")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00006000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00006FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00000080")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00007000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00007FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00000100")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00008000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00008FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00000200")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00009000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00009FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
   
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00000200")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00009000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00009FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00000400")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 0000A000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 0000AFFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00000800")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 0000B000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 0000BFFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00001000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 0000C000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 0000CFFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00002000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 0000D000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 0000DFFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00004000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 0000E000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 0000EFFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00008000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 0000F000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 0000FFFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00010000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00010000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00010FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00020000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00011000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00011FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00040000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00012000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00012FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00080000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00013000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00013FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00100000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00014000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00014FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00200000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00015000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00015FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00400000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00016000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00016FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 00800000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00017000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00017FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 01000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00018000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00018FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 02000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00019000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 00019FFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 04000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 0001A000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 0001AFFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 08000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 0001B000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 0001BFFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 10000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 0001C000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 0001CFFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 20000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 0001D000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 0001DFFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 40000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 0001E000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 0001EFFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
   
        resp = self.isp.writeCmd("LOCK PROG 00000000 80000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 0001F000 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
        resp = self.isp.writeCmd("PROG CODE 0001FFFC 20000000 00000004",RET_WRITE_LOCK)
        self.assertEqual(resp[0], RET_WRITE_LOCK)
           
        resp = self.isp.writeCmd("LOCK PROG 00000000 00000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("PROG CODE 00000000 20000000 00000100")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 00000000 00000004","0",1)
        self.assertEqual(resp,"00000000:44444444\r\n")
        resp = self.isp.writeCmd("LOCK PROG 80000000 00000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 00000000 00000004","0",1)
        self.assertEqual(resp,"00000000:00000000\r\n")
        resp = self.isp.writeCmd("LOCK PROG 00000000 00000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 00000000 00000004","0",1)
        self.assertEqual(resp,"00000000:FFFFFFFF\r\n")
  
    def test6_BadCase(self):
        print "*******************************************************"
        print "Command Error Test"
        print "*******************************************************"
        resp = self.isp.writeCmd("ERAE DAT3",RET_IVLD_CMD)
        self.assertEqual(resp[0],RET_IVLD_CMD)
        resp = self.isp.writeCmd("DOQW DAT3",RET_IVLD_CMD)
        self.assertEqual(resp[0],RET_IVLD_CMD)
        resp = self.isp.writeCmd("PORG DAT3",RET_IVLD_CMD)
        self.assertEqual(resp[0],RET_IVLD_CMD)
        resp = self.isp.writeCmd("PORG DAT3",RET_IVLD_CMD)
        self.assertEqual(resp[0],RET_IVLD_CMD)
        resp = self.isp.writeCmd("DMUP DAT3",RET_IVLD_CMD)
        self.assertEqual(resp[0],RET_IVLD_CMD)
        resp = self.isp.writeCmd("XGPR DAT3",RET_IVLD_CMD)
        self.assertEqual(resp[0],RET_IVLD_CMD)
        resp = self.isp.writeCmd("OCPY DAT3",RET_IVLD_CMD)
        self.assertEqual(resp[0],RET_IVLD_CMD)
        resp = self.isp.writeCmd("LCOK DAT3",RET_IVLD_CMD)
        self.assertEqual(resp[0],RET_IVLD_CMD)
        resp = self.isp.writeCmd("RMPE DAT3",RET_IVLD_CMD)
        self.assertEqual(resp[0],RET_IVLD_CMD)
          
        print "*******************************************************"
        print "Size & Address Error Test"
        print "*******************************************************"
        resp = self.isp.writeCmd("DOWN 20000000 10000000",RET_IVLD_SIZE)
        self.assertEqual(resp[0],RET_IVLD_SIZE)
        resp = self.isp.writeCmd("DOWN 20000000 1234567",RET_IVLD_SIZE)
        self.assertEqual(resp[0],RET_IVLD_SIZE)
        resp = self.isp.writeCmd("DOWN 20000000 00003801",RET_IVLD_SIZE)
        self.assertEqual(resp[0],RET_IVLD_SIZE)
        resp = self.isp.writeCmd("DOWN 20003800 00000001",RET_IVLD_ADDR)
        self.assertEqual(resp[0],RET_IVLD_ADDR)
        resp = self.isp.writeCmd("DOWN 1FFFFFFF 00000001",RET_IVLD_ADDR)
        self.assertEqual(resp[0],RET_IVLD_ADDR)
  
        resp = self.isp.writeCmd("PROG CODE 00000000 20000000 1234567",RET_IVLD_SIZE)
        self.assertEqual(resp[0],RET_IVLD_SIZE)
        resp = self.isp.writeCmd("PROG CODE 00000000 20000000 00003801",RET_IVLD_SIZE)
        self.assertEqual(resp[0],RET_IVLD_SIZE)
        resp = self.isp.writeCmd("PROG CODE 00020000 20000000 00000001",RET_IVLD_ADDR)
        self.assertEqual(resp[0],RET_IVLD_ADDR)
        resp = self.isp.writeCmd("PROG CODE 00000000 20003800 00000001",RET_IVLD_ADDR)
        self.assertEqual(resp[0],RET_IVLD_ADDR)
  
        resp = self.isp.writeCmd("COPY 00000000 20000000 00020001",RET_IVLD_ADDR)
        self.assertEqual(resp[0],RET_IVLD_ADDR)
        resp = self.isp.writeCmd("COPY 0003FE00 20000000 00000201",RET_IVLD_ADDR)
        self.assertEqual(resp[0],RET_IVLD_ADDR)
        resp = self.isp.writeCmd("COPY 0003FF00 20000000 00000101",RET_IVLD_ADDR)
        self.assertEqual(resp[0],RET_IVLD_ADDR)
        resp = self.isp.writeCmd("COPY 00000000 20000000 00003801",RET_IVLD_ADDR)
        self.assertEqual(resp[0],RET_IVLD_ADDR)
  
        resp = self.isp.writeCmd("XPRG 20000000 00003801",RET_IVLD_ADDR)
        self.assertEqual(resp[0],RET_IVLD_ADDR)
  
        resp = self.isp.writeCmd("XPRG 00000000 00020001",RET_IVLD_ADDR)
        self.assertEqual(resp[0],RET_IVLD_ADDR)
        resp = self.isp.writeCmd("XPRG 0003FE00 00000101",RET_IVLD_ADDR)
        self.assertEqual(resp[0],RET_IVLD_ADDR)
        resp = self.isp.writeCmd("XPRG 0003FF00 00000101",RET_IVLD_ADDR)
        self.assertEqual(resp[0],RET_IVLD_ADDR)
      
        resp = self.isp.writeCmd("LOCK PROG 40000000 00000000",RET_SUCCESS)
        self.assertEqual(resp[0],RET_SUCCESS)
        resp = self.isp.writeCmd("XPRG 00000000 00000100",RET_WRITE_LOCK)
        self.assertEqual(resp[0],RET_WRITE_LOCK)
  
        resp = self.isp.writeCmd("LOCK PROG 00000000 FFFFFFFF",RET_SUCCESS)
        self.assertEqual(resp[0],RET_SUCCESS)
        resp = self.isp.writeCmd("XPRG 00000000 00000100",RET_WRITE_LOCK)
        self.assertEqual(resp[0],RET_WRITE_LOCK)
  
        resp = self.isp.writeCmd("LOCK PROG 00000003 00000000",RET_SUCCESS)
        self.assertEqual(resp[0],RET_SUCCESS)
        resp = self.isp.writeCmd("XPRG 0003FE00 00000100",RET_WRITE_LOCK)
        self.assertEqual(resp[0],RET_WRITE_LOCK)
        resp = self.isp.writeCmd("XPRG 0003FF00 00000100",RET_WRITE_LOCK)
        self.assertEqual(resp[0],RET_WRITE_LOCK)
 
     
#     def test7_XPRG_Flsh_Cmd(self):
#         resp = self.isp.writeCmd("LOCK PROG 00000000 00000000")
#         self.assertEqual(resp[0], RET_SUCCESS)
#         resp = self.isp.writeCmd("ERAS CHIP")
#         self.assertEqual(resp[0], RET_SUCCESS)
#         self.isp.Xmodem_init()
#         self.isp.Xmodem_Send("00000000", "00010000", "app_flash.bin")
#         resp = self.isp.writeCmd("REMP FLSH")
#         self.assertEqual(resp[0],RET_SUCCESS)
#         self.isp.writeCmd("REST",RET_RESET)
#         print "*******************************************************"
#         print "Press Reboot Button"
#         print "*******************************************************"
#         self.isp.negoComP()
#         self.isp.writeCmd("")
#         print self.isp.ser.readall()
#  
#         self.isp.Xmodem_init()
#         self.isp.Xmodem_Send("20000000", "00003000", "app_sram.bin")
#         self.isp.writeCmd("REMP SRAM")
#         self.isp.writeCmd("REST",RET_RESET)
#         print "*******************************************************"
#         print "Press Reboot Button"
#         print "*******************************************************"
#         self.isp.negoComP()
#         self.isp.writeCmd("")
#         print self.isp.ser.readall()
#         resp = self.isp.writeCmd("DUMP 20000000 00000004")
        
    def test8_ProgSector(self):
        resp = self.isp.writeCmd("LOCK PROG 00000000 00000000")
        self.assertEqual(resp[0], RET_SUCCESS)

        resp = self.isp.writeCmd("ERAS CHIP")
        self.assertEqual(resp[0], RET_SUCCESS)
        
        resp = self.isp.writeCmd("LOCK PROG 00000000 00000000")
        self.assertEqual(resp[0], RET_SUCCESS)
        
        self.isp.writeCmd("DOWN 20000000 00003000",RET_SUCCESS,1,0)  #12KB
        data_value = 'A'
        for i in range(12*1024): 
            self.isp.ser.write(data_value)
        resp = self.isp.ser.readline()
        self.assertEqual(resp[0], RET_SUCCESS)
        
        resp = self.isp.writeCmd("PROG CODE 00000000 20000000 00003000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 00002FFC 00000004","0",1)
        self.assertEqual(resp, "00002FFC:41414141\r\n")

        resp = self.isp.writeCmd("PROG CODE 00003000 20000000 00003000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 00005FFC 00000004","0",1)
        self.assertEqual(resp, "00005FFC:41414141\r\n")

        resp = self.isp.writeCmd("PROG CODE 00006000 20000000 00003000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 00008FFC 00000004","0",1)
        self.assertEqual(resp, "00008FFC:41414141\r\n")

        resp = self.isp.writeCmd("PROG CODE 00009000 20000000 00003000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 0000BFFC 00000004","0",1)
        self.assertEqual(resp, "0000BFFC:41414141\r\n")

        resp = self.isp.writeCmd("PROG CODE 0000C000 20000000 00003000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 0000EFFC 00000004","0",1)
        self.assertEqual(resp, "0000EFFC:41414141\r\n")

        resp = self.isp.writeCmd("PROG CODE 0000F000 20000000 00001000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 0000FFFC 00000004","0",1)
        self.assertEqual(resp, "0000FFFC:41414141\r\n")

        resp = self.isp.writeCmd("PROG CODE 00010000 20000000 00003000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 00012FFC 00000004","0",1)
        self.assertEqual(resp, "00012FFC:41414141\r\n")

        resp = self.isp.writeCmd("PROG CODE 00013000 20000000 00003000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 00015FFC 00000004","0",1)
        self.assertEqual(resp, "00015FFC:41414141\r\n")

        resp = self.isp.writeCmd("PROG CODE 00016000 20000000 00003000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 00018FFC 00000004","0",1)
        self.assertEqual(resp, "00018FFC:41414141\r\n")

        resp = self.isp.writeCmd("PROG CODE 00019000 20000000 00003000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 0001BFFC 00000004","0",1)
        self.assertEqual(resp, "0001BFFC:41414141\r\n")

        resp = self.isp.writeCmd("PROG CODE 0001C000 20000000 00003000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 0001EFFC 00000004","0",1)
        self.assertEqual(resp, "0001EFFC:41414141\r\n")
        
        resp = self.isp.writeCmd("PROG CODE 0001F000 20000000 00001000")
        self.assertEqual(resp[0], RET_SUCCESS)
        resp = self.isp.writeCmd("DUMP 0001FFFC 00000004","0",1)
        self.assertEqual(resp, "0001FFFC:41414141\r\n")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
