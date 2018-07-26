#include "xmodem.h"
#include "general_function.h"
#include "flash.h"


unsigned short crc16_ccitt(const void *buf, int len)
{
	int i;
    	unsigned short crc = 0;

	for (i=0;i<len;i++)
	{
		crc  = (unsigned char)(crc >> 8) | (crc << 8);
		crc ^= ((unsigned char *)buf)[i];
		crc ^= (unsigned char)(crc & 0xff) >> 4;
		crc ^= (crc << 8) << 4;
		crc ^= ((crc & 0xff) << 4) << 1;
	}
	
	return crc;	
}

/*
void _outbyte(char ch)
{
	Uart2Putc(ch);
}
*/

/*
int _inbyte(int timeout) // msec timeout
{
	return (Uart2Getc(timeout));
}
*/


int check(unsigned char *buf, int sz)
{
	unsigned short crc = crc16_ccitt(buf, sz);
	unsigned short tcrc = (buf[sz]<<8)+buf[sz+1];

	if (crc == tcrc)
		return 1;
	return 0;
}


void flushinput(void)
{
	Uart2Flush();
}

/*
  128 byte data, crc16 only
*/
int xmodemReceive(unsigned char *dest, int destsz, int opt)
{
	unsigned char xbuff[134]; /* SOH(1) + BlockNO(1) + ~BlockNO(1) +  DATA(128) + CRC16(2) + numl(1) */
	unsigned char *p;
	int bufsz;
	char trychar = 'C';
	unsigned char packetno = 1;
	int i, c, len = 0;
	int retrans = MAXRETRANS;
	
	for(;;) 
	{
		while(1)
		{
			if (trychar) Uart2Putc(trychar);//_outbyte(trychar);
			//if ((c = _inbyte((DLY_1S)<<1)) >= 0) 
			if ((c = Uart2Getc((DLY_1S)<<1)) >= 0) 
			{
				switch (c) 
				{
				case SOH:
					bufsz = 128;
					goto start_recv;
				case EOT:
					flushinput();
					Uart2Putc(ACK);
					//_outbyte(ACK);
					return len; /* normal end */
				case CAN:
					//if ((c = _inbyte(DLY_1S)) == CAN) 
					if ((c = Uart2Getc(DLY_1S)) == CAN) 
					{
						flushinput();
						Uart2Putc(ACK);
						//_outbyte(ACK);
						return -1; /* canceled by remote */
					}
					break;
				default:
					break;
				}
			}
		}
		flushinput();

		Uart2Putc(CAN);
		Uart2Putc(CAN);
		Uart2Putc(CAN);
//		_outbyte(CAN);
//		_outbyte(CAN);
//		_outbyte(CAN);
		return -2; /* sync error */ 
		
	start_recv:
		trychar = 0;
		p = xbuff;
		*p++ = c;
		for (i = 0;  i < (bufsz+4); ++i) 
		{
			//if ((c = _inbyte(DLY_1S)) < 0) goto reject;
			if ((c = Uart2Getc(DLY_1S)) < 0) goto reject;
			*p++ = c;
		}

		if (xbuff[1] == (unsigned char)(~xbuff[2]) && 
			(xbuff[1] == packetno || xbuff[1] == (unsigned char)packetno-1) &&
			check(&xbuff[3], bufsz)) 
		{
			if (xbuff[1] == packetno)	
			{
				int count = destsz - len;
				if (count > bufsz) count = bufsz;
				if (count > 0) 
				{
          			//cus_memcpy (&dest[len], &xbuff[3], count);
					//do_iap(IAP_PROG_CODE,(uint32_t)&dest[len], count, (uint32_t)&xbuff[3]);
					if(opt == XMDM_FLSH)
						FlashProgramSector((uint32_t)&dest[len],(uint8_t*)&xbuff[3], count);
					else
					{
						for(i=0;i<count;i++)
							dest[len+i] = xbuff[3+i];		
					}
	
					len += count;
				}
				++packetno;
				retrans = MAXRETRANS+1;
			}
			if (--retrans <= 0) 
			{
				flushinput();
				Uart2Putc(CAN);
				Uart2Putc(CAN);
				Uart2Putc(CAN);
				//_outbyte(CAN);
				//_outbyte(CAN);
				//_outbyte(CAN);
				return -3; /* too many retry error */
			}
			//_outbyte(ACK);
			Uart2Putc(ACK);
			continue;
		}
	reject:
		flushinput();
		
		Uart2Putc(NAK);
		//_outbyte(NAK);
	}
}



