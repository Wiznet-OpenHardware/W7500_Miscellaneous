'''
Created on 2014. 8. 5.

@author: kaizen
'''
import unittest
import serial
import time
from xmodem import XMODEM
import os

COM = 'COM10'
BAUD = 115200
# BAUD = 460800
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
            try:
                self.ser.write(str.encode('U'))
                recv = self.ser.read()
                # print (recv.decode("utf-8"))
                
                if recv.decode("utf-8") == 'U':  
                    print (recv.decode("utf-8") + self.ser.readline().decode("utf-8"))
                    print ('Boot Mode Entered')         

                    self.ser.write('\r'.encode('utf-8'))
                    time.sleep(1)
                    self.ser.read_all()          
                    break
                else :  
                    # print(recv)
                    print('.')
                time.sleep(1)
            except:
                pass
        
    def writeCmd(self,cmd,resp="0",paramLine=1,loopCnt=3,opt=0):
        cmd = cmd + '\r'
        resp = resp + '\r\n'
        
        print ("Send Command : %s" % cmd)
        for i in cmd:
            self.ser.write(i.encode('utf-8'))
            time.sleep(0.01)
        # print(self.ser.write(cmd.encode('utf-8')))
        tempData = ""
        respData = ""
        
        for i in range(loopCnt):
            respData = self.ser.readline()
            respData = respData.decode("utf-8")
            if(i == paramLine -1):
                tempData = respData
            
            print ("Resp : %s" % (respData))
            if(respData == resp):
                print("Success")
                time.sleep(1)
                self.ser.read_all()
                break

        print("")
        return respData
    
    def unlockReadWrite(self):
        resp = self.writeCmd("LOCK PROG 00000000 00000000") 
        return resp

    def eraseFlash(self):
        resp = self.writeCmd("ERAS MASS")
        return resp

    def eraseDataFlash(self, sector):
        if sector is '0':
            resp = self.writeCmd("ERAS DAT0")
        elif sector is '1':
            resp = self.writeCmd("ERAS DAT1")

        return resp
    
    def progDataFlash(self, sector):
        if sector is '0':
            resp = self.writeCmd("PROG DAT0 20000000")
            # resp = self.writeCmd("PROG DAT0")
        elif sector is '1':
            resp = self.writeCmd("PROG DAT1 20000100")
            # resp = self.writeCmd("PROG DAT1")

    def dumpData(self, flag):
        if flag is 'code':
            resp = self.writeCmd("DUMP 10000000 00020000", loopCnt=(1024*32+1))
        elif flag is 'data':
            resp = self.writeCmd("DUMP 1003FE00 00000200", loopCnt=129)
        elif flag is 'sram':
            resp = self.writeCmd("DUMP 20000000 00000200", loopCnt=129)
        return resp

    def downloadDatatoSRAM(self, filename):
        filesize = 0
        sentsize = 0
        with open(filename, 'rb') as f:
            read_data = f.read()
            filesize = len(read_data)
            print('filesize : %s' % str.format('{:08}', filesize))
            # send command
            self.writeCmd("DOWN 20000000 00000004", loopCnt=1)
            time.sleep(1)
            # if option is '0':
            #     tmp_data = read_data[0:256]
            # elif option is '1':
            #     tmp_data = read_data[256:512]

            bytemsg = ""
            for bytedata in range(4):
            # for bytedata in read_data:
                # hexadecimals = hex(bytedata)
                # print('%s, %s, %s' % (bytedata, hexadecimals, ''.join('%02X' % bytedata)))
                bytemsg = bytemsg + str.format('{:02X} ', bytedata)
                print('%s, %s' % (bytedata, bytemsg))

                sentsize = self.ser.write('a')
                print('%s sent' % (sentsize))
                # sentsize += self.ser.write(str.format('{:02X}', bytedata).encode('utf-8'))
                # print('%s, %s, %s, %s' % (bytedata, ord(bytedata), hex(ord(bytedata)), hex(ord(bytedata))[2:]))
            print('sentsize: %s' % sentsize)
            print(bytemsg)
            resp = self.ser.readline()
            resp = resp.decode('utf-8')
            print(resp)
            time.sleep(1)
            self.ser.read_all()
            self.ser.write('\r'.encode('utf-8'))
            self.ser.write('\r'.encode('utf-8'))
            # print('file size: %s' % filesize)
        f.closed

        return resp

        # hexadecimals = hex(size)
        # print(int(hexadecimals[2:]))
        # self.writeCmd("DOWN 20000000 " + str.format('{:08}', int(hexadecimals[2:])))
        # for i in range(size):
        #     self.ser.write('A'.encode('utf-8'))
        # resp = self.ser.readline()
        # resp = resp.decode('utf-8')
        # print(resp)

        # return resp

    def getc(self,size,timeout=1):
        return self.ser.read(size)

    def putc(self,data,timeout=1):
        return self.ser.write(data)

    def Xmodem_init(self):
        self.xmodem = XMODEM(self.getc, self.putc)

    def Xmodem_Send(self, filename, option):
        if option is 'code':
            cmd = "XPRG " + "10000000" + " " + "00020000" + "\r"
        elif option is 'sram':
            cmd = "XPRG " + "20000000" + " " + "00000200" + "\r"
        print(cmd)
        self.ser.write(cmd.encode('utf-8'))
        print ("Start Send Binary using XMODEM")
        stream = open(filename, 'rb')
        print(self.xmodem.send(stream))
        stream.close()

        print (self.ser.readall())
        print ("End XMODEM")

    def downloadDataByXModem(self, filename, option):
        self.Xmodem_init()
        self.Xmodem_Send(filename, option)

      
    def resetSystem(self):
        self.ser.write("REST\r".encode('utf-8')) 
        resp = self.ser.readline()
        print(resp)
        return resp

    def readSerial(self):
        return self.ser.read_all()
        
if __name__ == "__main__":
    # filename = 'WIZ750SRv124_incl_Boot.bin'
    filename = 'data_flash.bin'
    # filename = 'a.txt'

    isp = W7500_ISP(COM, BAUD, 1)
    print ("Set Up")
    print ("Press the reset button")
    isp.negoComP()
    # if isp.unlockReadWrite()[0] is not RET_SUCCESS :
    #     print('UNLOCK FAILED')
    #     exit(0)
    # print("UNLOCK SUCCEEDED")
    # if isp.eraseFlash()[0] is not RET_SUCCESS:
    #     print("ERASE FAILED")
    #     exit(0)
    # print("ERASE SUCCEEDED")

    # isp.downloadDataByXModem(filename, 'data')
    # isp.progDataFlash('0')

    # print('DOWNLOAD SUCCEEDED')

    # isp.resetSystem()

    isp.eraseDataFlash('0')
    isp.eraseDataFlash('1')
    isp.dumpData('data')
    # isp.downloadDatatoSRAM(filename)
    # isp.dumpData('sram')
    # isp.dumpData('data')
    isp.downloadDataByXModem(filename, 'sram')
    isp.dumpData('sram')
    isp.progDataFlash('0')
    isp.progDataFlash('1')
    isp.dumpData('data')

    # while True:
    #     print(isp.readSerial())
    #     time.sleep(1)


