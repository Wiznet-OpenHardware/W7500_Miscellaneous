#ifndef UART_H_
#define UART_H_

#include "type.h"
#include "core_cm0.h"


//#define USE_50MHZ


#define UART2_BASE_ADDR			 0x40006000
#define UART2	( (UART2_TypeDef *) UART2_BASE_ADDR )

#ifdef USE_50MHZ
	#define UART2_460800		108		// @50MHz
	#define UART2_230400		217		// @50MHz
	#define UART2_115200		434		// @50MHz
	#define UART2_76800			651		// @50MHz
	#define UART2_57600			868		// @50MHz
	#define UART2_38400			1302	// @50MHz
	#define UART2_19200			2604	// @50MHz
	#define UART2_14400			3472	// @50MHz
	#define UART2_9600			5208	// @50MHz
	#define UART2_2400			20833	// @50MHz
#else
	#define UART2_460800		43		// @20MHz
	#define UART2_230400		86		// @20MHz
	#define UART2_115200		173		// @20MHz
	#define UART2_76800			260		// @20MHz
	#define UART2_57600			347		// @20MHz		
	#define UART2_38400			520		// @20MHz
	#define UART2_19200			1041	// @20MHz
	#define UART2_14400			1388	// @20MHz
	#define UART2_9600			2083	// @20MHz
	#define UART2_2400			8333	// @20MHz
#endif
	
typedef struct
{
  __IO   uint32_t  DATA;          /*!< Offset: 0x000 Data Register    (R/W) */
  __IO   uint32_t  STATE;         /*!< Offset: 0x004 Status Register  (R/W) */
  __IO   uint32_t  CTRL;          /*!< Offset: 0x008 Control Register (R/W) */
  union {
    __I    uint32_t  INTSTATUS;   /*!< Offset: 0x00C Interrupt Status Register (R/ ) */
    __O    uint32_t  INTCLEAR;    /*!< Offset: 0x00C Interrupt Clear Register ( /W) */
    };
  __IO   uint32_t  BAUDDIV;       /*!< Offset: 0x010 Baudrate Divider Register (R/W) */

} UART2_TypeDef;


/*** For Simple UART (UART2 ***/
#define UART2_STATE_RX_BUF_OVERRUN	(0x01ul << 3)		// RX buffer overrun, wirte 1 to clear.
#define UART2_STATE_TX_BUF_OVERRUN	(0x01ul << 2)		// TX buffer overrun, wirte 1 to clear.
#define UART2_STATE_RX_BUF_FULL		(0x01ul << 1)		// RX buffer full, read only.
#define UART2_STATE_TX_BUF_FULL		(0x01ul << 0)		// TX buffer full, read only.

#define UART2_CTRL_HIGH_SPEED_TEST	(0x01ul << 6)		// High-speed test mode for TX only.
#define UART2_CTRL_RX_OVERRUN_EN	(0x01ul << 5)		// RX overrun interrupt enable.
#define UART2_CTRL_TX_OVERRUN_EN	(0x01ul << 4)		// TX overrun interrupt enable.
#define UART2_CTRL_RX_INT_EN		(0x01ul << 3)		// RX interrupt enable.
#define UART2_CTRL_TX_INT_EN		(0x01ul << 2)		// TX interrupt enable.
#define UART2_CTRL_RX_EN			(0x01ul << 1)		// RX enable.
#define UART2_CTRL_TX_EN			(0x01ul << 0)		// TX enable.

#define UART2_INT_RX_OVERRUN		(0x01ul << 3)		// RX overrun interrupt. Wirte 1 to clear
#define UART2_INT_TX_OVERRUN		(0x01ul << 2)		// TX overrun interrupt. Write 1 to clear
#define UART2_INT_RX				(0x01ul << 1)		// RX interrupt. Write 1 to clear
#define UART2_INT_TX				(0x01ul << 0)		// TX interrupt. Write 1 to clear

void	Uart2Init		(uint32_t baud);
uint8_t Uart2Putc		(uint8_t ch);
void 	Uart2Puts		(uint8_t * mytext);
uint8_t Uart2Getc	(uint32_t timeout);
int		Uart2Gets		(uint8_t *str, int size);
//void	Uart2Gets		(uint8_t *str);
void 	Uart2Flush		();



#ifdef USING_UART0_1

#define UART0_BASE_ADDR			 0x4000C000
#define UART1_BASE_ADDR			 0x4000D000

#define UART0	( (UART_TypeDef *)  UART0_BASE_ADDR )
#define UART1	( (UART_TypeDef *)  UART1_BASE_ADDR )

#define UART_IBRD_460800	  2		// @20MHz
#define UART_FBRD_460800	 46		// @20MHz
#define UART_IBRD_230400	  5		// @20MHz
#define UART_FBRD_230400	 27		// @20MHz
#define UART_IBRD_115200	 10		// @20MHz
#define UART_FBRD_115200	 54		// @20MHz
#define UART_IBRD_76800		 16		// @20MHz
#define UART_FBRD_76800		 18		// @20MHz
#define UART_IBRD_57600		 21		// @20MHz
#define UART_FBRD_57600		 45		// @20MHz
#define UART_IBRD_38400		 32		// @20MHz
#define UART_FBRD_38400		 35		// @20MHz
#define UART_IBRD_19200		 65		// @20MHz
#define UART_FBRD_19200		  7		// @20MHz
#define UART_IBRD_14400		 86		// @20MHz
#define UART_FBRD_14400		 52		// @20MHz
#define UART_IBRD_9600		130		// @20MHz
#define UART_FBRD_9600		 13		// @20MHz
#define UART_IBRD_2400		520		// @20MHz
#define UART_FBRD_2400		 53		// @20MHz


typedef struct
{
  __IO   uint32_t  DATA;          /*!< Offset: 0x000 Data Register    (R/W) */
  union {
  __IO   uint32_t  RSR;           /*!< Offset: 0x004 Receive Status Register (R/W) */
  __IO   uint32_t  ECR;           /*!< Offset: 0x004 Error Clear Register (R/W) */
  };
         uint32_t  RESERVED0[4];
   __I   uint32_t  FR;           /*!< Offset: 0x018 Flag Register (R/ ) */
         uint32_t  RESERVED1;
  __IO   uint32_t  ILPR;         /*!< Offset: 0x020 IrDA Low Power Counter Register (R/W ) */
  __IO   uint32_t  IBRD;         /*!< Offset: 0x024 Integer Baud Rate Register (R/W ) */
  __IO   uint32_t  FBRD;         /*!< Offset: 0x028 Fractional Baud Rate Register (R/W ) */
  __IO   uint32_t  LCRH;         /*!< Offset: 0x02C Line Control Register (R/W ) */
  __IO   uint32_t  CR;           /*!< Offset: 0x030 Control Register (R/W ) */
  __IO   uint32_t  IFLS;         /*!< Offset: 0x034 Interrupt FIFO Level Select Register (R/W ) */
  __IO   uint32_t  IMSC;         /*!< Offset: 0x038 Interrupt Mask Set/Clear Register (R/W ) */
   __I   uint32_t  RIS;          /*!< Offset: 0x03C Raw Interrupt Status Register (R/ ) */
   __I   uint32_t  MIS;          /*!< Offset: 0x040 Masked Interrupt Status Register (R/ ) */
   __O   uint32_t  ICR;          /*!< Offset: 0x044 Interrupt Clear Register ( /W) */
  __IO   uint32_t  DMACR;        /*!< Offset: 0x048 UART DMA Control Register (R/W ) */
} UART_TypeDef;


/*********************** UART0 REGISTERS ****/
#define UART0TCR_Test            (UART0_BASE_ADDR + 0x0080)   // Reserved for Test purpose
#define UART0ITIP_Test           (UART0_BASE_ADDR + 0x0084)   // Reserved for Test purpose
#define UART0ITOP_Test           (UART0_BASE_ADDR + 0x0088)   // Reserved for Test purpose
#define UART0TDR_Test            (UART0_BASE_ADDR + 0x008C)   // Reserved for Test purpose
#define UART0PERIPHID0           (UART0_BASE_ADDR + 0x0FE0)   // UART0 PeriphID0 Register
#define UART0PERIPHID1           (UART0_BASE_ADDR + 0x0FE4)   // UART0 PeriphID1 Register
#define UART0PERIPHID2           (UART0_BASE_ADDR + 0x0FE8)   // UART0 PeriphID2 Register
#define UART0PERIPHID3           (UART0_BASE_ADDR + 0x0FEC)   // UART0 PeriphID3 Register
#define UART0PRIMECELLID0        (UART0_BASE_ADDR + 0x0FF0)   // UART0 CellID0 Register
#define UART0PRIMECELLID1        (UART0_BASE_ADDR + 0x0FF4)   // UART0 CellID1 Register
#define UART0PRIMECELLID2        (UART0_BASE_ADDR + 0x0FF8)   // UART0 CellID2 Register
#define UART0PRIMECELLID3        (UART0_BASE_ADDR + 0x0FFC)   // UART0 CellID3 Register
/********************************************/

/*********************** UART1 REGISTERS ****/
#define UART1TCR_Test            (UART1_BASE_ADDR + 0x0080)    // Reserved for Test purpose
#define UART1ITIP_Test           (UART1_BASE_ADDR + 0x0084)    // Reserved for Test purpose
#define UART1ITOP_Test           (UART1_BASE_ADDR + 0x0088)    // Reserved for Test purpose
#define UART1TDR_Test            (UART1_BASE_ADDR + 0x008C)    // Reserved for Test purpose
#define UART1PERIPHID0           (UART1_BASE_ADDR + 0x0FE0)    // UART1 PeriphID0 Register
#define UART1PERIPHID1           (UART1_BASE_ADDR + 0x0FE4)    // UART1 PeriphID1 Register
#define UART1PERIPHID2           (UART1_BASE_ADDR + 0x0FE8)    // UART1 PeriphID2 Register
#define UART1PERIPHID3           (UART1_BASE_ADDR + 0x0FEC)    // UART1 PeriphID3 Register
#define UART1PRIMECELLID0        (UART1_BASE_ADDR + 0x0FF0)    // UART1 CellID0 Register
#define UART1PRIMECELLID1        (UART1_BASE_ADDR + 0x0FF4)    // UART1 CellID1 Register
#define UART1PRIMECELLID2        (UART1_BASE_ADDR + 0x0FF8)    // UART1 CellID2 Register
#define UART1PRIMECELLID3        (UART1_BASE_ADDR + 0x0FFC)    // UART1 CellID3 Register
/********************************************/


#define UART_CTRL_RXEN			(0x01ul << 9)
#define UART_CTRL_TXEN			(0x01ul << 8)
#define UART_CTRL_EN			(0x01ul << 0)

#define UART_LCRH_SPS			(0x01ul << 7)		// Stick parity select
#define UART_LCRH_WLEN(n)		((n & 0x03) << 5)	// Word length ( 11:8bit, 10:7bit, 01:6bit, 00:5bit )
#define UART_LCRH_FEN			(0x01ul << 4)		// Enable FIFOs
#define UART_LCRH_STP2			(0x01ul << 3)		// Two stop bits select
#define UART_LCRH_EPS			(0x01ul << 2)		// Even parity select
#define UART_LCRH_PEN			(0x01ul << 1)		// Parity Enable
#define UART_LCRH_BRK			(0x01ul << 0)		// Send break

#define UART_IMSC_OEIM			(0x01ul << 10)		// Overrun error interrupt mask
#define UART_IMSC_BEIM			(0x01ul <<  9)		// Break error interrupt mask
#define UART_IMSC_PEIM			(0x01ul <<  8)		// Parity error interrupt mask
#define UART_IMSC_FEIM			(0x01ul <<  7)		// Framing error interrupt mask
#define UART_IMSC_RTIM			(0x01ul <<  6)		// Receive timeout interrupt mask
#define UART_IMSC_TXIM			(0x01ul <<  5)		// Transmit interrupt mask
#define UART_IMSC_RXIM			(0x01ul <<  4)		// Receive interrupt mask
#define UART_IMSC_DSRMIM		(0x01ul <<  3)		// nUARTDSR modem interrupt mask
#define UART_IMSC_DCDMIM		(0x01ul <<  2)		// nUARTDCD modem interrupt mask
#define UART_IMSC_CTSMIM		(0x01ul <<  1)		// nUARTCTS modem interrupt mask
#define UART_IMSC_RIMIM			(0x01ul <<  0)		// nUARTRI modem interrupt mask

#define UART_FR_RI				(0x01ul << 8)		// Ring indicator
#define UART_FR_TXFE			(0x01ul << 7)		// Transmit FIFO empty
#define UART_FR_RXFF			(0x01ul << 6)		// Receive FIFO full
#define UART_FR_TXFF			(0x01ul << 5)		// Transmit FIFO full
#define UART_FR_RXFE			(0x01ul << 4)		// Receive FIFO empty
#define UART_FR_BUSY			(0x01ul << 3)		// UART is busy transmitting data
#define UART_FR_DCD				(0x01ul << 2)		// Data carrier detect
#define UART_FR_DSR				(0x01ul << 1)		// Data set ready
#define UART_FR_CTS				(0x01ul << 0)		// Clear to send


uint32_t	UartInit			(UART_TypeDef *UARTx, uint32_t divider);
uint8_t		UartxPutc			(UART_TypeDef *UARTx, uint8_t ch);
void		UartxPuts			(UART_TypeDef *UARTx, uint8_t *str);
uint8_t		UartxGetc			(UART_TypeDef *UARTx);
uint8_t		UartxGetc_nonblk	(UART_TypeDef *UARTx);
void 		UartGets			(UART_TypeDef *UARTx, uint8_t *str);

#endif //  USING_UART0_1
 
#endif /* UART_H_ */
