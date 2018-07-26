#ifndef FLASH_H_
#define FLASH_H_


typedef struct
{
	__IO uint32_t FACCR;			/*!< Offset: 0x000 Flash Access Control Register  (R/W) */
	__IO uint32_t FADDR;			/*!< Offset: 0x004 Flash Address Register         (R/W) */
	__IO uint32_t FDATAR;			/*!< Offset: 0x008 Flash Data Register            (R/W) */
	__IO uint32_t FCTRLR;			/*!< Offset: 0x00C Flash Control Register         (R/W) */
	 __I uint32_t FSTATR;			/*!< Offset: 0x010 Flash Status Register          (R/ ) */
	__IO uint32_t FLOCKR0;			/*!< Offset: 0x014 Flash Lock Register            (R/W) */
	__IO uint32_t FLOCKR1;			/*!< Offset: 0x018 Flash Lock Register            (R/W) */
		 uint32_t RESERVD0[5];		
	__IO uint32_t FKEYR0;			/*!< Offset: 0x030 Flash Access Control Key0      (R/W) */
	__IO uint32_t FKEYR1;			/*!< Offset: 0x034 Flash Access Cotnrol Key1      (R/W) */
	__IO uint32_t BSADDR[2];		/*!< Offset: 0x038 Flash Bad Sector from NVR2     (R/W) */
}FLASH_CTRL_TypeDef;


#pragma pack(push, 2)
typedef struct
{
	__IO uint16_t CRL;				/*!< Offset: 0x000 Code Read Lock                        (R/W) */
	__IO uint16_t CABWL;			/*!< Offset: 0x002 Code All Block Write Lock             (R/W) */
	__IO uint16_t DRL0;				/*!< Offset: 0x004 Data Read Lock_0                      (R/W) */
	__IO uint16_t DRL1;				/*!< Offset: 0x006 Data Read Lock_1                      (R/W) */
	__IO uint16_t DWL0;				/*!< Offset: 0x008 Data Write Lock_0                     (R/W) */
	__IO uint16_t DWL1;				/*!< Offset: 0x00A Data Write Lock_1                     (R/W) */
	__IO uint32_t CBWL;				/*!< Offset: 0x00C Code Block Write Lock                 (R/W) */
	__IO uint32_t ICBWL;			/*!< Offset: 0x010 Code Block Write Lock Complement      (R/W) */
}NVR1_TypeDef;
#pragma pack(pop)


//typedef struct
//{
//	 __I uint32_t CONF[8];			/*!< Offset: 0x00 Configration Information   (R/ ) */
//	 __I uint32_t TRIM_BGT;			/*!< Offset: 0xB8 Trim BGT                   (R/ ) */
//	 __I uint32_t TRIM_OSC;			/*!< Offset: 0xBC Trim OSC                   (R/ ) */
//	 __I uint32_t BAD_SECT[2];		/*!< Offset: 0xF8 BAD Sector Information     (R/ ) */
//}NVR2_TypeDef;


#define FLASH_BASE_ADDR 0x10000000
#define FLASH_END_ADDR	0x10020000
#define FLASH_BLCK_SIZE	0x1000
#define FLASH_SECT_SIZE	0x100

#define NVR1_BASE_ADDR		0x1003FC00
#define NVR2_BASE_ADDR		0x1003FD00

#define RDN0_BASE_ADDR		0x1003FE00
#define RDN0_END_ADDR		0x1003FF00

#define RDN1_BASE_ADDR		0x1003FF00
#define RDN1_END_ADDR		0x10040000

#define FLASHCTRL_BASE_ADDR 0x41005000

#define SYSMEM_BASE 		0x40010000
#define REG_REMAP			(SYSMEM_BASE + 0xF000)


#define W7500_TRIM_BGT		0x41001210 //  5bit
#define W7500_TRIM_OSC		0x41001004 // 10bit

#define FLASH_UNLOCK		0x8A75
#define IS_FLASH_UNLOCK(X)	((0x8A75 == X))
#define IS_VALID_TRIM		0xAA550000
#define VALID_KEYR0			0x52537175
#define VALID_KEYR1			0xA91875FC

#define NVR1		((NVR1_TypeDef *) NVR1_BASE_ADDR )
//#define NVR2		((NVR2_TypeDef *) NVR2_BASE_ADDR )
#define FLASHCTRL	((FLASH_CTRL_TypeDef *) FLASHCTRL_BASE_ADDR )

#define NVR2_CONF(n)		(NVR2_BASE_ADDR + (n*4))
#define NVR2_TRIM_BGT		(NVR2_BASE_ADDR + 0xB8)
#define NVR2_TRIM_OSC		(NVR2_BASE_ADDR + 0xBC)
#define NVR2_BAD_SECT0		(NVR2_BASE_ADDR + 0xF8)
#define NVR2_BAD_SECT1		(NVR2_BASE_ADDR + 0xFC)


// FACCR bit
#define FACCR_LOCK			(1 << 31)
#define FACCR_PPEN			(1 << 30)
#define FACCR_CTRL			(1 << 17)
#define FACCR_FEN			(1 << 16)
#define FACCR_SET_SZ(n)		((n & 0x03) << 2)
#define FACCR_SET_RC(n)		((n & 0x03) << 0)

// FCTRLR Flag bit
#define FCTRLR_FRST			(1 << 31)		// Reset
#define FCTRLR_MER			(1 << 30)		// Code & Data Erase
#define FCTRLR_CER			(1 << 29)		// Code Erase
#define FCTRLR_BER			(1 << 28)		// Code Block Erase
#define FCTRLR_SER			(1 << 27)		// Sector Erase
#define FCTRLR_CWR			(1 << 16)		//
#define FCTRLR_WRI			(1 <<  7)		// Write ( Auto Increase )
#define FCTRLR_WR			(1 <<  6)		// Write ( Non Increase )
#define FCTRLR_RDI			(1 <<  1)		// Read ( Auto Increase )
#define FCTRLR_RD			(1 <<  0)		// Read ( Non Increase )

// FLOCKR0
#define FLOCKR0_CRL			31		// Code Read Lock
#define FLOCKR0_CABWL		30		// Code all block write lock
#define FLOCKR0_DRL1		3		// Data 1 Read Lock
#define FLOCKR0_DRL0		2		// Data 0 Read Lock
#define FLOCKR0_DWL1		1		// Data 1 Write Lock
#define FLOCKR0_DWL0		0		// Data 0 Write Lock

#define FL0_LSH(X) 			(1<<X)

// FSTATR Flag bit
#define FSTATR_RDY			(1 << 31)
#define FSTATR_NOPRI		(1 <<  2)
#define FSTATR_INVADDR		(1 <<  1)
#define FSTATR_INVSIZE		(1 <<  0)


#define IAP_ERAS			0x010
#define IAP_ERAS_DAT0		(IAP_ERAS + 0)
#define IAP_ERAS_DAT1		(IAP_ERAS + 1)
#define IAP_ERAS_SECT		(IAP_ERAS + 2)				
#define IAP_ERAS_BLCK		(IAP_ERAS + 3)	
#define IAP_ERAS_CHIP		(IAP_ERAS + 4)	
#define IAP_ERAS_MASS		(IAP_ERAS + 5)	

#define IAP_PROG			0x020
#define IAP_PROG_DAT0		(IAP_PROG + 0)	
#define IAP_PROG_DAT1		(IAP_PROG + 1)	
#define IAP_PROG_CODE		(IAP_PROG + 2)	


#define IAP_DOWN			0x040
#define IAP_DUMP			0x080

#define IAP_XPRG			0x0C0

#define IAP_LOCK			0x100
#define IAP_LOCK_READ		(IAP_LOCK + 0)	
#define IAP_LOCK_PROG		(IAP_LOCK + 1)	

#define IAP_REST			0x200

#define IAP_COPY			0x400
#define IAP_EXEC			0x800

#define IAP_REMP			0xC00
#define IAP_REMP_BOOT		(IAP_REMP + 0)
#define IAP_REMP_FLSH		(IAP_REMP + 1)
#define IAP_REMP_SRAM		(IAP_REMP + 2)


#define FACCR_SetKey()					\
{										\
	FLASHCTRL->FKEYR0 = VALID_KEYR0;	\
	FLASHCTRL->FKEYR1 = VALID_KEYR1;	\
}										\



// Function
int do_iap				(uint32_t isp_id, uint32_t dst_addr, uint8_t *src_addr, uint32_t isp_size);
int FlashEraseSector	(uint32_t sectorAddr);
int FlashEraseBlock		(uint32_t blockAddr);
int FlashEraseAll		(uint8_t id);
int FlashProgramSector	(uint32_t dst_addr, uint8_t *buf, uint32_t size);
int DownByte			(uint8_t *s_addr, uint32_t size);
int MemoryDump 			(uint32_t dst_addr, uint32_t isp_size);
int CopyToRAM			( uint8_t *dst_addr, uint8_t *src_addr, uint32_t size);
int FlashLock			(uint32_t id, uint32_t FlockR0, uint32_t FlockR1);

uint32_t isReadLock		(uint32_t addr);

#endif /* FLASH_H_ */

