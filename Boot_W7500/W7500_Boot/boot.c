/*
 *-----------------------------------------------------------------------------
 * The confidential and proprietary information contained in this file may
 * only be used by a person authorised under and to the extent permitted
 * by a subsisting licensing agreement from ARM Limited.
 *
 *            (C) COPYRIGHT 2010-2013 ARM Limited.
 *                ALL RIGHTS RESERVED
 *
 * This entire notice must be reproduced on all copies of this file
 * and copies of this file may only be made by a person if such person is
 * permitted to do so under the terms of a subsisting license agreement
 * from ARM Limited.
 *
 *      SVN Information
 *
 *      Checked In          : $Date: 2013-03-27 23:58:01 +0000 (Wed, 27 Mar 2013) $
 *
 *      Revision            : $Revision: 242484 $
 *
 *      Release Information : Cortex-M System Design Kit-r1p0-00rel0
 *-----------------------------------------------------------------------------
 */

#ifdef CORTEX_M0
#include "core_cm0.h"
#endif

#include "boot.h"
#include "flash.h"
#include "uart.h"
#include "isp.h"
#include "xmodem.h"

const char BOOT_VER[4] __attribute__((section(".boot_ver"))) = "1.2\0";
#define DIV_MAX_CNT 10	
uint32_t DIV_LIST[DIV_MAX_CNT] = { UART2_460800,UART2_230400,UART2_115200,UART2_76800, UART2_57600,UART2_38400,UART2_19200,UART2_14400,UART2_9600,UART2_2400};
uint32_t LOCKINFO[2];


int main (void)
{
	uint32_t boot_mode = 0;
	uint8_t  idx = 0, i;
	uint32_t result;
	uint32_t conf_reg;
	uint32_t temp_lock_info;

	// Wait for FLASH READY
	for(i=0;i<25;i++)
	{
		asm("nop");
	}

	// Get Trim Information
	{
		uint32_t temp_trim_bgt, temp_trim_osc;
		temp_trim_bgt = HW32_REG(NVR2_TRIM_BGT);
		temp_trim_osc = HW32_REG(NVR2_TRIM_OSC);

		if( (temp_trim_bgt & 0xFFFF0000)  == IS_VALID_TRIM )
			HW32_REG(W7500_TRIM_BGT) = temp_trim_bgt;

		if( (temp_trim_osc & 0xFFFF0000)  == IS_VALID_TRIM )
			HW32_REG(W7500_TRIM_OSC) = temp_trim_osc;

		asm("nop");	asm("nop");
		asm("nop");	asm("nop");
	}

#ifdef FPGA_TEST
#else
	// Get ConfInfo From NVR2
	for(i=0;i<8;i++)	
	{
		conf_reg = HW32_REG( NVR2_CONF(i) );

		FACCR_SetKey();
		FLASHCTRL->FACCR = FLASHCTRL->FACCR | FACCR_FEN | FACCR_CTRL;
		FLASHCTRL->FADDR = NVR2_CONF(i);
		FLASHCTRL->FDATAR = conf_reg;
		FLASHCTRL->FCTRLR = FCTRLR_CWR;
		while( FLASHCTRL->FSTATR != FSTATR_RDY);

		FACCR_SetKey();
		FLASHCTRL->FACCR = FLASHCTRL->FACCR & ~(FACCR_FEN|FACCR_CTRL);
	}
#endif
	// Get BadSectInfo From NVR2
	{
		FLASHCTRL->BSADDR[0] = HW32_REG( NVR2_BAD_SECT0 );
		FLASHCTRL->BSADDR[1] = HW32_REG( NVR2_BAD_SECT1 );
	}

	{
	LOCKINFO[0] = ~( ((IS_FLASH_UNLOCK(NVR1->CRL  )) << FLOCKR0_CRL)   |
                     ((IS_FLASH_UNLOCK(NVR1->CABWL)) << FLOCKR0_CABWL) |
                     ((IS_FLASH_UNLOCK(NVR1->DRL0 )) << FLOCKR0_DRL0)  |
                     ((IS_FLASH_UNLOCK(NVR1->DRL1 )) << FLOCKR0_DRL1)  |
                     ((IS_FLASH_UNLOCK(NVR1->DWL0 )) << FLOCKR0_DWL0)  |
                     ((IS_FLASH_UNLOCK(NVR1->DWL1 )) << FLOCKR0_DWL1)  |  
					 (0x3FFFFFF0) );
                              
	temp_lock_info = NVR1->CBWL ^ NVR1->ICBWL;
   	if( temp_lock_info != 0xFFFFFFFF )
   		LOCKINFO[1] = NVR1->CBWL | ~temp_lock_info;
	else
		LOCKINFO[1] = NVR1->CBWL;
	}

    boot_mode =  (HW32_REG(REG_BOOT) & 0x00000003);
    switch(boot_mode)
    {
    case BOOT_APP_MODE:
		HW32_REG(REG_REMAP) = REMAP_FLSH;		// Remap to FLASH
    	break;

	case BOOT_ISP_MODE:		// ISP Mode
		idx = 0;
		while(1)
		{
			result = ispNegotiation( DIV_LIST[idx] );
			if( result == RET_SUCCESS )
				break;

			idx++;
			if( idx == DIV_MAX_CNT )
				idx = 0;
		}
		
		Uart2Puts((uint8_t*)BOOT_VER);
		Uart2Puts("\r\n");
		while(1)
		{
			result = run_isp();
			Uart2Putc( 0x30 + result);
			Uart2Puts("\r\n");

			if(result == RET_ISP_RESET)		break;
		}
		break;
   
	case BOOT_PP_MODE:		// PP Mode
		FACCR_SetKey();
		FLASHCTRL->FACCR = FLASHCTRL->FACCR | FACCR_PPEN;
		
		HW16_REG(0x42000010UL) = HW16_REG(0x42000010UL) | 0x8000;
	   	break;
    }

	FLASHCTRL->FLOCKR0 = LOCKINFO[0];
	FLASHCTRL->FLOCKR1 = LOCKINFO[1];

	if(boot_mode != BOOT_PP_MODE)
	{
		NVIC_SystemReset();
	}
	while(1)
	{
		HW16_REG(0x42000004UL) = HW16_REG(0x42000004UL) | 0x8000;
		HW16_REG(0x42000004UL) = HW16_REG(0x42000004UL) & 0x7FFF;
	}

}

