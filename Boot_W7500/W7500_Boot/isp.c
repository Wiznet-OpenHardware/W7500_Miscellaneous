/*
 * isp.c
 *
 *  Created on: Jun 24, 2014
 *      Author: kaizen
 */
#include "isp.h"
#include "flash.h"
#include "xmodem.h"

extern uint32_t LOCKINFO[2];

uint32_t ispNegotiation(uint32_t baud)
{
	uint8_t recv_data, send_data = 'U';
	uint8_t i;
	uint32_t *p;
	
	//Uart2Flush();
	Uart2Init( baud );

	recv_data = Uart2Getc(0);
	Uart2Putc(recv_data);
	if( recv_data == 'U' )
		return RET_SUCCESS;

	
	recv_data = Uart2Getc(0);
	Uart2Putc(recv_data);
	if( recv_data == 'U' )
		return RET_SUCCESS;

	return RET_FAIL;
}

uint32_t run_isp( )
{
	uint8_t *p;
	uint8_t cnt=0;
	uint8_t str[MAX_CMD_SIZE],param[4][12]={0};
	uint32_t flash_num=0;
	uint32_t result=0,idx,cmd;
	int	ret_size;
	TypeDef_Cmd_Param iap;

	Uart2Gets(str, MAX_CMD_SIZE);
	p = cus_strtok(str);
	cmd = *(uint32_t*)p;

	while( p = cus_strtok(0) )
	{
		idx = 0;
		while((idx < 9) & ((param[cnt][idx] = *p++) != 0) ) idx++;
		cnt++;
		if(cnt>4 | idx >= 9)	return RET_ISP_IVLD_PARM;
	}

   switch(cmd)
   {
      case ISP_ERAS:
         switch(*(uint32_t*)param[0])
         { 
            case ISP_DAT0:
				if(LOCKINFO[0] & FLOCKR0_DWL0) return RET_ISP_WRITE_LOCK;
				result = FlashEraseSector(RDN0_BASE_ADDR);
				break;
            case ISP_DAT1:
               if(LOCKINFO[0] & FLOCKR0_DWL1) return RET_ISP_WRITE_LOCK;
			   result = FlashEraseSector(RDN1_BASE_ADDR);
               break;
            case ISP_MASS:
				if(  (LOCKINFO[0] & (FL0_LSH(FLOCKR0_CABWL) | FL0_LSH(FLOCKR0_DWL0) | FL0_LSH(FLOCKR0_DWL1))) 
      			  || (LOCKINFO[1] & 0xFFFFFFFF) )			
      					return RET_ISP_WRITE_LOCK;
			   result = FlashEraseAll(IAP_ERAS_MASS);
			   break;
            case ISP_CHIP:
      			if( (LOCKINFO[0] & FL0_LSH(FLOCKR0_CABWL)) || (LOCKINFO[1] & 0xFFFFFFFF) )
      			   return RET_ISP_WRITE_LOCK;
			   	result = FlashEraseAll(IAP_ERAS_CHIP);
      			break;
      	   case ISP_SECT:
    			if(StringHexToHex(param[1],&iap.f_addr) != RET_SUCCESS)				return RET_ISP_IVLD_ADDR;
				iap.f_addr |= 0x10000000;		// for converting to flash area in boot
				if((iap.f_addr < FLASH_BASE_ADDR) || (iap.f_addr >= FLASH_END_ADDR))return RET_ISP_IVLD_ADDR;
				if( LOCKINFO[1] & (1 << (iap.f_addr >> 12)))						return RET_ISP_WRITE_LOCK;
				result = FlashEraseSector(iap.f_addr);
				break;
	  	   case ISP_BLCK:
				if(StringHexToHex(param[1],&iap.f_addr) != RET_SUCCESS)				return RET_ISP_IVLD_ADDR;
				iap.f_addr |= 0x10000000;		// for converting to flash area in boot
   				if( (iap.f_addr < FLASH_BASE_ADDR) || (iap.f_addr >= FLASH_END_ADDR))return RET_ISP_IVLD_ADDR;
				if( LOCKINFO[1] & (1 << (iap.f_addr >> 12)))						return RET_ISP_WRITE_LOCK;
				result = FlashEraseBlock(iap.f_addr);	
	  			break;
		   default:
				return RET_ISP_IVLD_PARM;
      	      break;
		}
		break;
	 case ISP_PROG:
		switch(*(uint32_t*)param[0])
		{ 
			case ISP_DAT0:
			case ISP_DAT1:
				if		( *(uint32_t*)param[0] == ISP_DAT0)
				{
					iap.f_addr = RDN0_BASE_ADDR;
					if(	LOCKINFO[0] & FL0_LSH(FLOCKR0_DWL0) )		return RET_ISP_WRITE_LOCK;
				}
				else if	( *(uint32_t*)param[0] == ISP_DAT1)
				{
					iap.f_addr = RDN1_BASE_ADDR;
					if( LOCKINFO[0] & FL0_LSH(FLOCKR0_DWL1) )		return RET_ISP_WRITE_LOCK;
				}
				if( StringHexToHex(param[1],&iap.s_addr) != RET_SUCCESS )	return RET_ISP_IVLD_ADDR;
				if(iap.s_addr < SRAM_START || iap.s_addr >= SRAM_END)		return RET_ISP_IVLD_ADDR;
				//flash_num = ( (DATIDX(*(uint32_t*)param[0])) - 0x30ul );
				//if(LOCKINFO[0] & (FL0_LSH(FLOCKR0_DWL0) << flash_num))		return RET_ISP_WRITE_LOCK;
				result = FlashProgramSector(iap.f_addr, (uint8_t*)iap.s_addr, 256 );
				break;
			case ISP_CODE:
				if( (StringHexToHex(param[1],&iap.f_addr) != RET_SUCCESS) ||
	                (StringHexToHex(param[2],&iap.s_addr) != RET_SUCCESS) )			return RET_ISP_IVLD_ADDR;
				iap.f_addr |= 0x10000000;	// for converting to flash area in boot
         		if((iap.f_addr < FLASH_BASE_ADDR) || (iap.f_addr >= FLASH_END_ADDR))return RET_ISP_IVLD_ADDR;
				if((iap.s_addr < SRAM_START) || (iap.s_addr >= SRAM_END))			return RET_ISP_IVLD_ADDR;
	            if( LOCKINFO[0] & (FL0_LSH(FLOCKR0_CABWL)))							return RET_ISP_WRITE_LOCK;
				if( LOCKINFO[1] & (1 << (iap.f_addr >> 12)))						return RET_ISP_WRITE_LOCK;
               	if( StringHexToHex(param[3],&iap.size) != RET_SUCCESS )				return RET_ISP_IVLD_SIZE;
				if( ((iap.f_addr + iap.size) > FLASH_END_ADDR) || 
					(iap.s_addr + iap.size > SRAM_END) )							return RET_ISP_IVLD_SIZE;
				result = FlashProgramSector(iap.f_addr, (uint8_t*)iap.s_addr, iap.size);
				break;
	         default:
	            return RET_ISP_IVLD_PARM;
	            break;
		}
		break;
	case ISP_DOWN:
		if( StringHexToHex(param[0],&iap.s_addr) != RET_SUCCESS )	return RET_ISP_IVLD_ADDR;
   		if( StringHexToHex(param[1],&iap.size) != RET_SUCCESS )		return RET_ISP_IVLD_SIZE;
   		if( (iap.s_addr < SRAM_START) || (iap.s_addr >= SRAM_END) )	return RET_ISP_IVLD_ADDR;
		if( (iap.s_addr + iap.size) > SRAM_END) 					return RET_ISP_IVLD_SIZE;
		result = DownByte((uint8_t*)iap.s_addr, iap.size);
   		break;
	case ISP_DUMP:
		if( StringHexToHex(param[0],&iap.any_addr) != RET_SUCCESS )		return RET_ISP_IVLD_ADDR;
		if( StringHexToHex(param[1],&iap.size) != RET_SUCCESS )			return RET_ISP_IVLD_SIZE;

		result = MemoryDump(iap.any_addr, (uint32_t)iap.size);
		break;
	case ISP_XPRG:
		if( StringHexToHex(param[0],&iap.any_addr) != RET_SUCCESS )		return RET_ISP_IVLD_ADDR;
		if( StringHexToHex(param[1],&iap.size) != RET_SUCCESS )			return RET_ISP_IVLD_SIZE;

		if( (iap.any_addr >= SRAM_START) && ((iap.any_addr + iap.size) <= SRAM_END) )
		{
			if( xmodemReceive((uint8_t*)iap.any_addr, (int)iap.size, XMDM_SRAM) < 0 )
				result = RET_ISP_IVLD_SIZE;
			else														
				result = RET_ISP_S;
		}
		else if( ((iap.any_addr >= 0x00000000) && (iap.any_addr < 0x00040000)) ||
				 ((iap.any_addr >= 0x10000000) && (iap.any_addr < 0x10040000)) )
		{
			iap.any_addr |= 0x10000000;	// for converting to flash area in boot
			if( (iap.any_addr >= FLASH_BASE_ADDR) && ((iap.any_addr+iap.size) <= FLASH_END_ADDR) )
			{
				if( (LOCKINFO[0] & FL0_LSH(FLOCKR0_CABWL)) || LOCKINFO[1] )	return RET_ISP_WRITE_LOCK;
			}
			else if( (iap.any_addr >= RDN0_BASE_ADDR) && ((iap.any_addr+iap.size) <= RDN0_END_ADDR ) )
			{
				if( (LOCKINFO[0] & FL0_LSH(FLOCKR0_DWL0)) )					return RET_ISP_WRITE_LOCK;
			}
			else if( (iap.any_addr >= RDN1_BASE_ADDR) && ((iap.any_addr+iap.size) <= RDN1_END_ADDR) )
			{
				if( (LOCKINFO[0] & FL0_LSH(FLOCKR0_DWL1)) )					return RET_ISP_WRITE_LOCK;
			}
	   		else															return RET_ISP_IVLD_ADDR;

			if( xmodemReceive((uint8_t*)iap.any_addr, (int)iap.size, XMDM_FLSH) < 0)
				result = RET_ISP_IVLD_SIZE;
			else														
				result = RET_ISP_S;
		}
		else																
			return RET_ISP_IVLD_ADDR;

		break;
	case ISP_LOCK:
		if(		*(uint32_t*)param[0] == ISP_READ)	result = FlashLock(IAP_LOCK_READ,0,0);
		else if(*(uint32_t*)param[0] == ISP_PROG)
		{
			if( StringHexToHex(param[1],&iap.flockr0) != RET_SUCCESS )		return RET_ISP_IVLD_PARM;
			if( StringHexToHex(param[2],&iap.flockr1) != RET_SUCCESS )		return RET_ISP_IVLD_PARM;
			result = FlashLock(IAP_LOCK_PROG,iap.flockr0,iap.flockr1);
		}
		else
			return RET_ISP_IVLD_PARM;
		break;
	case ISP_COPY:
		if( (StringHexToHex(param[0],&iap.f_addr) != RET_SUCCESS) ||
			(StringHexToHex(param[1],&iap.s_addr) != RET_SUCCESS) )			return RET_ISP_IVLD_ADDR;
		if( StringHexToHex(param[2],&iap.size) != RET_SUCCESS )				return RET_ISP_IVLD_SIZE;
		
		iap.f_addr |= 0x10000000;	// for converting to flash area in boot
		if( (iap.s_addr < SRAM_START) || ((iap.s_addr + iap.size) > SRAM_END) )	
			return RET_ISP_IVLD_ADDR;

		if( ((iap.f_addr + iap.size) <= FLASH_END_ADDR) ||
			((iap.f_addr >= RDN0_BASE_ADDR) && ((iap.f_addr + iap.size) <= (RDN1_BASE_ADDR+FLASH_SECT_SIZE))) )
		{
			if( isReadLock(iap.f_addr) == RET_LOCK)	return RET_ISP_READ_LOCK;
			result = CopyToRAM((uint8_t*)iap.s_addr, (uint8_t*)iap.f_addr, iap.size);
		}
		else
			return RET_ISP_IVLD_ADDR;

		break;	
	case ISP_EXEC:
		if( StringHexToHex(param[0],&iap.any_addr) != RET_SUCCESS )		return RET_ISP_IVLD_ADDR;
		// for converting to flash area in boot
		if( ((iap.any_addr >= 0x00000000) && (iap.any_addr < 0x00020000)) ||
			((iap.any_addr >= 0x0003FC00) && (iap.any_addr < 0x00040000)) )	iap.any_addr |= 0x10000000;
		
		((void (*)(void))iap.any_addr)();
		break;
	case ISP_REMP:
		switch(*(uint32_t*)param[0])
		{
		case ISP_BOOT:
			HW32_REG(REG_REMAP) = REMAP_BOOT;
			break;
		case ISP_FLSH:
			HW32_REG(REG_REMAP) = REMAP_FLSH;
			break;
		case ISP_SRAM:
			HW32_REG(REG_REMAP) = REMAP_SRAM;
			break;
		default:
			return RET_ISP_IVLD_PARM;
		}
		break;
	case ISP_REST:
		return RET_ISP_RESET;	
		break;
    default:
         return RET_ISP_IVLD_CMD;
		 break;
   }

	return result;
}

