/*
 * general_function.c
 *
 *  Created on: Jun 24, 2014
 *      Author: kaizen
 */
#include "general_function.h"


uint8_t *cus_strtok(uint8_t *src)
{
	static uint8_t * next = 0;
	uint8_t        * start;

	if(src)	next = src;

	start = next;

	while(*next)
	{
		if(*next == '\r' || *next == '\n' || *next == '\t' || *next == ' ')
		{
			if(next == start)
			{
				start++;
			}
			else
			{
				//*next++ = '\0';
				*next++ = 0;
				return start;
			}
		}
		next++;
	}
	if(start == next) return 0;
	return start;
}


/*
uint8_t *cus_strtok(uint8_t *src, uint8_t sep)
{
	static uint8_t *next = '\0';

	if(!src && !next)	return '\0';
	if(src)	next = src;

	uint8_t *start = next;

	while(*next){
		if(*next == sep){
			if(next == start){
				start++;
				continue;
			}
			*next = '\0';
			next++;
			return start;
		}
		next++;
	}
	next = '\0';
	return start;
}
*/

/*
uint8_t *cus_strcpy(uint8_t *dst, const uint8_t *src)
{
	uint8_t *cp = dst;
	while(*cp++ = *src++);
	return dst;
}
*/

/*
uint8_t *cus_strncpy(uint8_t *dst, const uint8_t*src, uint32_t size)
{
	uint8_t *start = dst;

	while(size && (*dst++ = *src++)) size--;
	if(size) while(--size) *dst++ = '\0';

	return start;
}
*/

/*
uint32_t cus_strlen(const uint8_t *str)
{
	uint32_t len=0, i=0;

	while(str[i++] != '\0')
		len++;

	return len;
}
*/

/*
int cus_strcmp(const uint8_t *str1, const uint8_t *str2)
{
	while( *str1 == *str2 && *str1 != '\0' && *str2 != '\0' )
	{
		str1++;
		str2++;
	}
	if(*str1 < *str2)
		return -1;
	else if(*str1 > *str2)
		return 1;
	else
		return 0;
}
*/
/*
int cus_strcmp(const uint32_t *str1, const uint32_t *str2)	// compare 4byte
{
	while( *str1 == *str2 && *str1 != '\0' && *str2 != '\0' )
	{
		str1++;
		str2++;
	}
	if(*str1 < *str2)
		return -1;
	else if(*str1 > *str2)
		return 1;
	else
		return 0;
}
*/

/*
int cus_atoi(uint8_t *str)
{
	uint32_t i=0, num=0;

	for(; str[i] != 0x00; i++)
	{
		if( str[i] < '0' || str[i] > '9' )	return -1;

		num = num * 10;
		num = num + (str[i] - '0');
	}

	return num;
}
*/

int isHex( uint8_t ch )
{
	if( (ch >= '0' && ch <= '9') || (ch >= 'A' && ch <= 'F') ||
	   (ch >= 'a' && ch <= 'f') )
		return RET_SUCCESS;

	return RET_FAIL;
}

uint8_t HexChToHex( uint8_t ch)
{
	uint8_t ret_val = 0x00;

	if(ch >= '0' && ch <= '9')
		ret_val = 0x00 + (uint8_t)( ch - '0' );
	else if( ch >= 'A' && ch <= 'F' )
		ret_val = 0x00 + (uint8_t)( ch - 'A' + 10 );
	else if( ch >= 'a' && ch <= 'f' )
		ret_val = 0x00 + (uint8_t)( ch - 'a' + 10 );

	ret_val = ret_val & 0x0F;

	return ret_val;
}

/*
int isAddress(uint8_t *str)
{
	if(cus_strlen(str) > 8) return RET_FAIL;
	while(*str != '\0')
	{
		if( isHex(*str) != RET_SUCCESS )
			return RET_FAIL;

		str++;
	}

	return RET_SUCCESS;
}

uint32_t StringHexToHex(uint8_t *str, uint32_t *hex)
{
	uint32_t val=0;
	uint32_t temp_val=0;

	while(*str != '\0')
	{
		val = val << 4;
		temp_val = HexChToHex(*str);
		val +=  temp_val;
		str++;
	}

	return val;
}
*/

uint32_t StringHexToHex(uint8_t *str, uint32_t *hex)
{
	uint32_t val=0, len=0;
	uint32_t temp_val=0;

	//while(str[len] != '\0')
	while(str[len] != 0 )
	{
		if( isHex(str[len]) != RET_SUCCESS )	return RET_FAIL;

		val = val << 4;
		temp_val = HexChToHex(str[len]);
		val |= temp_val;
		len++;
	}
	
	if( len != 8 )	return RET_FAIL;
	*hex = val;

	return RET_SUCCESS;
}


void Bin2HexStr(uint8_t *pHex, uint32_t Bin)
{
	uint8_t i;
	uint8_t Byte;
	uint8_t Shift=32;

	//Shift = 32;
	for(i=0;i<8;i++)
	{
		Shift -= 4;			// shift nibble
		Byte = Bin >> Shift;
		Byte &= 0x0F;		// get nibble

		if(Byte >= 0x0A && Byte <= 0x0F)
		{
			*pHex++ = 'A' + Byte - 0x0A;
		}
		else
		{
			*pHex++ = '0' + Byte;
		}
	}
	*pHex = '\0'; // null
}

/*
void cus_memcpy(uint8_t *dst, uint8_t *src, uint32_t n)
{
	uint32_t i;

	for(i=0;i<n;i++)
		dst[i] = src[i];
}
*/
/*
void cus_memset(uint8_t *dst, uint8_t dt, uint32_t n)
{
	uint32_t i;

	for(i=0;i<n;i++)
		dst[i] = dt;
}
*/
