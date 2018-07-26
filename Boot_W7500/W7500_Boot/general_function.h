/*
 * general_function.h
 *
 *  Created on: Jun 24, 2014
 *      Author: kaizen
 */

#ifndef GENERAL_FUNCTION_H_
#define GENERAL_FUNCTION_H_

#include "type.h"

//uint8_t *	cus_strtok		(uint8_t *src, uint8_t sep);
uint8_t *	cus_strtok		(uint8_t *src);
//uint8_t *	cus_strcpy		(uint8_t *dst, const uint8_t *src);
//uint8_t *	cus_strncpy		(uint8_t *dst, const uint8_t *src, uint32_t size);
//uint32_t	cus_strlen		(const uint8_t *str);
//int 		cus_strcmp		(const uint8_t *str1, const uint8_t *str2);
//int		cus_strcmp		(const uint32_t *str1, const uint32_t *str2);	// compare 4byte
//int 		cus_atoi		(uint8_t *str);


int 		isHex			( uint8_t ch );
//int			isAddress		( uint8_t *str );
uint8_t		HexChToHex		( uint8_t ch );
uint32_t	StringHexToHex	( uint8_t *str, uint32_t *hex );


void Bin2HexStr		(uint8_t *pHex, uint32_t Bin);
/*
void cus_memcpy		(uint8_t *dst, uint8_t *src, uint32_t n);
void cus_memset		(uint8_t *dst, uint8_t dt, uint32_t n);
*/

#endif /* GENERAL_FUNCTION_H_ */
