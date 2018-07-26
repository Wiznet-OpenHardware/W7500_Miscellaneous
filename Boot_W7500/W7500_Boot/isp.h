/*
 * isp.h
 *
 *  Created on: Jun 24, 2014
 *      Author: kaizen
 */

#ifndef ISP_H_
#define ISP_H_

#include <stdint.h>
#include "general_function.h"
#include "uart.h"

#define RET_ISP_S				0
#define RET_ISP_IVLD_SIZE		(RET_ISP_S + 1)	
#define RET_ISP_IVLD_ADDR		(RET_ISP_S + 2)
#define RET_ISP_IVLD_CMD		(RET_ISP_S + 3)
#define RET_ISP_NOPRIVILGE		(RET_ISP_S + 4)
#define RET_ISP_IVLD_PARM		(RET_ISP_S + 5)
#define RET_ISP_READ_LOCK		(RET_ISP_S + 6)
#define RET_ISP_WRITE_LOCK		(RET_ISP_S + 7)
#define RET_ISP_RESET			(RET_ISP_S + 8)	

#define ISP_ERAS	0x53415245			//Hex value of ERAS			
#define ISP_DOWN	0x4E574F44			//Hex value of DOWN
#define ISP_PROG	0x474F5250			//Hex value of PROG
#define ISP_DUMP	0x504D5544			//Hex value of DUMP 
#define ISP_COPY	0x59504F43			//Hex value of COPY
#define ISP_EXEC	0x43455845			//Hex value of EXEC
#define ISP_LOCK	0x4B434F4C			//Hex value of LOCK
#define ISP_REMP	0x504D4552			//Hex value of REMP
#define ISP_REST	0x54534552			//Hex value of REST

#define ISP_DAT0	0x30544144			//Hex value of DAT0
#define ISP_DAT1	0x31544144			//Hex value of DAT1
#define DATIDX(X)	((X & 0x005444144) >> 24) 
#define ISP_MASS	0x5353414D			//Hex value of MASS
#define ISP_CODE	0x45444F43			//Hex value of CODE
#define ISP_CHIP	0x50494843			//Hex value of CHIP
#define ISP_SECT	0x54434553			//Hex value of SECT
#define ISP_BLCK	0x4B434C42			//Hex value of BLCK

#define ISP_XPRG	0x47525058			//Hex value of XPRG 
#define ISP_READ	0x44414552			//Hex value of READ
#define ISP_SRAM	0x4D415253			//Hex value of SRAM
#define ISP_FLSH	0x48534C46			//Hex value of FLSH
#define ISP_BOOT	0x544F4F42			//Hex value of BOOT

#define MAX_CMD_SIZE 80
//#define FLSH_CODE_START	0x10000000
//#define FLSH_CODE_END	0x10020000

//#define FLSH_RDN0_START	0x1003FE00
//#define FLSH_RDN0_END	0x1003FF00

//#define FLSH_RDN1_START	0x1003FF00
//#define FLSH_RDN1_END	0x10040000

#define SRAM_START		0x20000000
#define SRAM_END		0x20003800

#define REMAP_FLSH  0x00
#define REMAP_BOOT	0x01
#define REMAP_SRAM	0x02



typedef struct{
	uint32_t cmd_idx;
	uint32_t any_addr;
	uint32_t f_addr;
	uint32_t s_addr;
	uint32_t flockr0;
	uint32_t flockr1;
	uint32_t size;
}TypeDef_Cmd_Param;


uint32_t ispNegotiation	(uint32_t baud);

uint32_t is_readable_buf(uint8_t idx);
uint32_t parse_cmd		( TypeDef_Cmd_Param *param );
void 	 buf_flush		(uint8_t idx);
uint32_t run_isp		();



#endif /* ISP_H_ */

