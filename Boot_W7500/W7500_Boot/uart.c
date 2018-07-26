/*
 * uart.c
 *
 *  Created on: Jun 20, 2014
 *      Author: kaizen
 */
#include "uart.h"

void Uart2Init(uint32_t baud)
 {
	UART2->BAUDDIV = baud;
	UART2->CTRL	=  UART2_CTRL_RX_EN | UART2_CTRL_TX_EN;

	 return;
 }

uint8_t Uart2Getc(uint32_t timeout)
{
	uint32_t loop_cnt=0;

	while( (UART2->STATE & UART2_STATE_RX_BUF_FULL) == 0)
	{
		if( timeout == 0)	continue;
		if( loop_cnt++ >= timeout )	return 0;
	}

	return (UART2->DATA);
}

int Uart2Gets(uint8_t *str, int size)
{
	uint8_t recv_data;

	while(size)
	{
		recv_data = Uart2Getc(0);

		if(recv_data != '\n')	(*str) = recv_data;
		if(*str == '\r')		break;

		str++;
		size--;
	}
	*str = 0;

	return size;
}

uint8_t Uart2Putc	(uint8_t ch)
 {
	while((UART2->STATE & UART2_STATE_TX_BUF_FULL));
	UART2->DATA = ch;
	return (ch);
 }

// Uart string output
 void 	Uart2Puts	(uint8_t * mytext)
 {
	 unsigned char CurrChar;
	 do {
		 CurrChar = *mytext;
		 if (CurrChar != (char) 0x0) {
			 Uart2Putc(CurrChar);  // Normal data
		 }
		 *mytext++;
	 } while (CurrChar != 0);
	 return;
 }
 

void Uart2Flush()
{
	while(UART2->STATE & UART2_STATE_TX_BUF_FULL)
	{
		UART2->DATA;
	}
}

