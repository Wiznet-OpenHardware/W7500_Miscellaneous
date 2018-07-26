#include "type.h"
#include "flash.h"
#include "isp.h"

extern uint32_t LOCKINFO[2];

__attribute__ ((section("iap.entry"))) 
int do_iap (uint32_t isp_id, uint32_t dst_addr,uint8_t *src_addr,uint32_t isp_size) 
{
	int result = 0;
	
	if(isp_id == IAP_ERAS_DAT0)
	{		
		result = FlashEraseSector(RDN0_BASE_ADDR);
	}
	else if(isp_id == IAP_ERAS_DAT1)
	{
		result = FlashEraseSector(RDN1_BASE_ADDR);
	}
	else if(isp_id == IAP_ERAS_SECT)
	{
		result = FlashEraseSector(dst_addr);
	}
	else if(isp_id == IAP_ERAS_BLCK)
	{
		result = FlashEraseBlock(dst_addr);
	}
	else if(isp_id == IAP_ERAS_CHIP || isp_id == IAP_ERAS_MASS)
	{
		result = FlashEraseAll(isp_id);
	}
	else if(isp_id == IAP_PROG_CODE)
	{
		result = FlashProgramSector(dst_addr,src_addr, isp_size);
	}
	else
		result = RET_FAIL;
	/*
	switch(isp_id)
	{
		case IAP_ERAS_DAT0:
		case IAP_ERAS_DAT1:
			//result = FlashEraseSector(0x0003FE00 | ((isp_id & 0x01)<<8));
			result = FlashEraseSector(RDN0_BASE_ADDR);
			break;
		case IAP_ERAS_SECT:
			result = FlashEraseSector(dst_addr);
			break;
		case IAP_ERAS_BLCK:
			result = FlashEraseBlock(dst_addr);
			break;
		case IAP_ERAS_CHIP:
			break;
		case IAP_ERAS_MASS:
			result = FlashEraseAll(isp_id);
			break;
		case IAP_PROG_CODE:
			result = FlashProgramSector( dst_addr, (uint8_t*)src_addr, isp_size);
			break;
		default:
			result = RET_ISP_IVLD_CMD;
			break;
	}
	*/
	return result;
}

__attribute__ ((section("isp.EraseSector"))) 
int FlashEraseSector (uint32_t sectorAddr)
{
	int result = 0;
	
	FACCR_SetKey();
	FLASHCTRL->FACCR = FLASHCTRL->FACCR | FACCR_FEN | FACCR_CTRL;

	FLASHCTRL->FADDR = sectorAddr;
	FLASHCTRL->FCTRLR = FCTRLR_SER;
		
	while( (FLASHCTRL->FSTATR & FSTATR_RDY) != FSTATR_RDY );
	result = FLASHCTRL->FSTATR & 0x03;

	FACCR_SetKey();
	FLASHCTRL->FACCR = FLASHCTRL->FACCR & ~( FACCR_FEN | FACCR_CTRL );

	return result;
}

__attribute__ ((section("isp.EraseBlock"))) 
int FlashEraseBlock (uint32_t blockAddr)
{
	int result = 0;
	
	FACCR_SetKey();
	FLASHCTRL->FACCR = FLASHCTRL->FACCR | FACCR_FEN | FACCR_CTRL;

	FLASHCTRL->FADDR = blockAddr;
	FLASHCTRL->FCTRLR = FCTRLR_BER;

	while( (FLASHCTRL->FSTATR & FSTATR_RDY) != FSTATR_RDY );
	result = FLASHCTRL->FSTATR & 0x03;

	FACCR_SetKey();
	FLASHCTRL->FACCR = FLASHCTRL->FACCR & ~( FACCR_FEN | FACCR_CTRL );

	return result;
}

__attribute__ ((section("isp.EraseAll"))) 
int FlashEraseAll(uint8_t id)
{
	int result = 0;
	
	FACCR_SetKey();
	FLASHCTRL->FACCR = FLASHCTRL->FACCR | FACCR_FEN | FACCR_CTRL;

	if (id == IAP_ERAS_CHIP)
		FLASHCTRL->FCTRLR = FCTRLR_CER;
	else if	(id == IAP_ERAS_MASS)
		FLASHCTRL->FCTRLR = FCTRLR_MER;
	else
		return RET_FAIL;

	while( (FLASHCTRL->FSTATR & FSTATR_RDY) != FSTATR_RDY );
	result = FLASHCTRL->FSTATR & 0x03;

	FACCR_SetKey();
	FLASHCTRL->FACCR = FLASHCTRL->FACCR & ~( FACCR_FEN | FACCR_CTRL );

	return result;
}

__attribute__ ((section("isp.ProgramPage"))) 
int FlashProgramSector ( uint32_t dst_addr, uint8_t *buf, uint32_t size)
{
	int result;
	uint32_t fdata;
	int i;
	uint32_t bak_faccr_sz;

	bak_faccr_sz = FLASHCTRL->FACCR & 0x000000C0; 
	
	FACCR_SetKey();
	FLASHCTRL->FACCR = ((FLASHCTRL->FACCR & 0xFFFFFF03) | FACCR_FEN | FACCR_CTRL | FACCR_SET_SZ(1) );
	FLASHCTRL->FADDR = dst_addr;
	for(i=0; (dst_addr & 0x03) && (i<(4-(dst_addr & 0x03))) && (i < size); i++)
	{
		FLASHCTRL->FDATAR = buf[i];
		FLASHCTRL->FCTRLR = FCTRLR_WRI;
		while( (FLASHCTRL->FSTATR & FSTATR_RDY) != FSTATR_RDY);
		result = FLASHCTRL->FSTATR & 0x03;
		if( result != 0 )	goto PROG_END;
	}
	size -= i;
	
	FACCR_SetKey();
	FLASHCTRL->FACCR = ((FLASHCTRL->FACCR & 0xFFFFFF03) | FACCR_SET_SZ(3) );
	FLASHCTRL->FADDR = dst_addr + i;
	
	for(;(int)size >= 4 ; i+=4, size-=4)
	{
		FLASHCTRL->FDATAR = (buf[i+3] << 24) + (buf[i+2] << 16) +(buf[i+1] << 8) + buf[i];
		FLASHCTRL->FCTRLR = FCTRLR_WRI;
		while( (FLASHCTRL->FSTATR & FSTATR_RDY) != FSTATR_RDY);
		result = FLASHCTRL->FSTATR & 0x03;
		if( result != 0 )	goto PROG_END;
	}


	FACCR_SetKey();
	FLASHCTRL->FACCR = ((FLASHCTRL->FACCR & 0xFFFFFF03) | FACCR_FEN | FACCR_CTRL | FACCR_SET_SZ(1) );
	FLASHCTRL->FADDR = dst_addr +i;

	for(;(int)size > 0 ; i++, size--)
	{
		FLASHCTRL->FDATAR = buf[i];
		FLASHCTRL->FCTRLR = FCTRLR_WRI;
		while( (FLASHCTRL->FSTATR & FSTATR_RDY) != FSTATR_RDY);
		result = FLASHCTRL->FSTATR & 0x03;
		if( result != 0 )	goto PROG_END;
	}
	
PROG_END:
	FACCR_SetKey();
	FLASHCTRL->FACCR = ((FLASHCTRL->FACCR & 0xFFFFFF03) & ~( FACCR_FEN | FACCR_CTRL)) | bak_faccr_sz;

	return result;			
}
	
__attribute__ ((section("isp.DownByte"))) 
int DownByte( uint8_t *s_addr, uint32_t size)
{
	uint8_t recv=0;
	uint32_t recv_cnt=0;

	while(1)
	{
		if(recv_cnt >=size)	break;
		*s_addr++ = Uart2Getc(0); 
		recv_cnt++;
	}

	return RET_SUCCESS;
}


__attribute__ ((section("isp.MemoryDump"))) 
int MemoryDump (uint32_t dst_addr, uint32_t isp_size)	// isp_size = 1word
{
	uint8_t value[9];
	uint32_t word_cnt = 0,isLock=0;
	uint32_t temp_addr;
	
	dst_addr &= ~(0x03ul);					// Mask for 32bit address ( 0x0, 0x4, 0x8, 0xC )
	
	while(1)
	{
		if( word_cnt >= isp_size )	break;

		Bin2HexStr(value,dst_addr);		// print address
		Uart2Puts(value);
		Uart2Putc(':');

		if(dst_addr <= 0x00040000)
			temp_addr = dst_addr | 0x10000000;
		else
			temp_addr = dst_addr;
		
		if( isReadLock(temp_addr) == RET_LOCK )
			Bin2HexStr(value,0x00000000); 
		else
			Bin2HexStr(value, HW32_REG(temp_addr));

		Uart2Puts(value);
		Uart2Puts("\r\n");
		word_cnt += 4;
		dst_addr += 4;
	}

	return RET_SUCCESS;
}

__attribute__ ((section("isp.CopyToRAM"))) 
int CopyToRAM( uint8_t *dst_addr, uint8_t *src_addr, uint32_t size)
{
	while(size)
	{
		*dst_addr = *src_addr;
		src_addr++;
		dst_addr++;
		size --;
	}
	
	return RET_SUCCESS;
}

__attribute__ ((section("isp.FlashLock"))) 
int FlashLock(uint32_t id, uint32_t FlockR0, uint32_t FlockR1)
{
	uint8_t  val[9];
	NVR1_TypeDef temp_NVR1 = {0xFF,};

	if( id == IAP_LOCK_READ )
	{
		Bin2HexStr(val,LOCKINFO[0]);
		Uart2Puts(val);
		Uart2Puts(" ");
		Bin2HexStr(val,LOCKINFO[1]);
		Uart2Puts(val);
		Uart2Puts("\r\n");
	}
	else if( id == IAP_LOCK_PROG )
	{

		if ( !( FlockR0 & FL0_LSH(FLOCKR0_CRL) )   )
		{
			if( LOCKINFO[0] & FL0_LSH(FLOCKR0_CRL))
			{
				if( FlashEraseAll(IAP_ERAS_CHIP) != 0 )		
					return RET_FAIL;	
			}
			temp_NVR1.CRL   = FLASH_UNLOCK;
		}
		if ( !( FlockR0 & FL0_LSH(FLOCKR0_CABWL))  )	temp_NVR1.CABWL = FLASH_UNLOCK;
		if ( !( FlockR0 & FL0_LSH(FLOCKR0_DRL1) )  )
		{
			if( LOCKINFO[0] & FL0_LSH(FLOCKR0_DRL1) )
			{
				if( FlashEraseSector(RDN1_BASE_ADDR) != 0 )	
					return RET_FAIL;
			}
			temp_NVR1.DRL1  = FLASH_UNLOCK;
		}
		if ( !( FlockR0 & FL0_LSH(FLOCKR0_DRL0) )  )
		{
			if( LOCKINFO[0] & FL0_LSH(FLOCKR0_DRL0) )
			{
				if( FlashEraseSector(RDN0_BASE_ADDR) != 0 )	
					return RET_FAIL;
			}
			temp_NVR1.DRL0  = FLASH_UNLOCK;
		}
		if ( !( FlockR0 & FL0_LSH(FLOCKR0_DWL1) )  )	temp_NVR1.DWL1  = FLASH_UNLOCK;
		if ( !( FlockR0 & FL0_LSH(FLOCKR0_DWL0) )  )	temp_NVR1.DWL0  = FLASH_UNLOCK;

		temp_NVR1.CBWL = FlockR1;
		temp_NVR1.ICBWL= ~FlockR1;

		LOCKINFO[0] = FlockR0;
		LOCKINFO[1] = FlockR1;
		
		FlashEraseSector(NVR1_BASE_ADDR);
		FlashProgramSector ( NVR1_BASE_ADDR, (uint8_t*)&temp_NVR1,sizeof(temp_NVR1));
	}
	else
		return RET_FAIL;

	return RET_SUCCESS;
}

__attribute__ ((section("isp.isReadLock"))) 
uint32_t isReadLock(uint32_t addr)
{
	if( addr < 0x00040000) 
	{
		addr |= 0x10000000;
	}

	if( addr < FLASH_END_ADDR )
	{
		if( LOCKINFO[0] & FL0_LSH(FLOCKR0_CRL) )			return RET_LOCK ;
	}
	else if( addr >= RDN0_BASE_ADDR && addr < RDN1_BASE_ADDR )
	{
		if( LOCKINFO[0] & FL0_LSH(FLOCKR0_DRL0) )			return RET_LOCK;
	}
	else if( addr < (RDN1_BASE_ADDR + FLASH_SECT_SIZE) )
	{
		if( LOCKINFO[0] & FL0_LSH(FLOCKR0_DRL1) )			return RET_LOCK;
	}
	else if( (addr >= 0x1FFF1000) && (addr < 0x1FFF1800) )	return RET_LOCK;
	return RET_UNLOCK;
}

