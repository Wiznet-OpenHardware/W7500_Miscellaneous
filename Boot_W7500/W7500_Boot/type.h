/*
 * type.h
 *
 *  Created on: Jun 13, 2014
 *      Author: kaizen
 */

#ifndef TYPE_H_
#define TYPE_H_

#include <stdint.h>
//typedef unsigned long 	uint32_t;
//typedef unsigned short	uint16_t;
//typedef unsigned char	uint8_t;


#define   __I     volatile const       /*!< Defines 'read only' permissions                 */
#define   __O     volatile             /*!< Defines 'write only' permissions                */
#define   __IO    volatile             /*!< Defines 'read / write' permissions              */


//#define BOOT_TEST
//#define ISP_TEST
//#define UART_TEST



/* DEFINE */
#define HW32_REG(ADDRESS)  (*((volatile uint32_t  *)(ADDRESS)))
#define HW16_REG(ADDRESS)  (*((volatile uint16_t *)(ADDRESS)))
#define HW8_REG(ADDRESS)   (*((volatile uint8_t  *)(ADDRESS)))

#define RET_SUCCESS	0
#define RET_FAIL	1
#define RET_LOCK	2
#define RET_UNLOCK	3

#define W7500_GW_IP		0x46006008
#define W7500_SUB_IP	0x4600600C
#define W7500_SRC_IP	0x46006010


typedef enum IRQn
{
/******  Cortex-M0 Processor Exceptions Numbers ***************************************************/

/* ToDo: use this Cortex interrupt numbers if your device is a CORTEX-M0 device                   */
  NonMaskableInt_IRQn           = -14,      /*!<  2 Cortex-M0 Non Maskable Interrupt              */
  HardFault_IRQn                = -13,      /*!<  3 Cortex-M0 Hard Fault Interrupt                */
  SVCall_IRQn                   = -5,       /*!< 11 Cortex-M0 SV Call Interrupt                   */
  PendSV_IRQn                   = -2,       /*!< 14 Cortex-M0 Pend SV Interrupt                   */
  SysTick_IRQn                  = -1,       /*!< 15 Cortex-M0 System Tick Interrupt               */

  /******  CMSDK Specific Interrupt Numbers *********************************************************/

  // kaizen 20140620
  SSP0_IRQn                    =  0,       /*!< SSP 0 Interrupt                                   */
  SSP1_IRQn                    =  1,       /*!< SSP 1 Interrupt                                   */
  UART0_IRQn                   =  2,       /*!< UART 0 Interrupt                                  */
  UART1_IRQn                   =  3,       /*!< UART 1 Interrupt                                  */
  UART2_IRQn                   =  4,       /*!< UART 2 Interrupt                                  */
  I2C0_IRQn                    =  5,       /*!< I2C 0 Interrupt                                   */
  I2C1_IRQn                    =  6,       /*!< I2C 1 Interrupt                                   */
  PORT0_IRQn                   =  7,       /*!< Port 1 combined Interrupt                         */
  PORT1_IRQn                   =  8,       /*!< Port 2 combined Interrupt                         */
  PORT2_IRQn                   =  9,       /*!< Port 3 combined Interrupt                         */
  PORT3_IRQn                   = 10,       /*!< Port 4 combined Interrupt                         */
  DMA_IRqn                     = 11,       /*!< DMA Interrupt                                     */
  DUALTIMER0_IRQn              = 12,       /*!< Dual Timer0 Interrupt                             */
  DUALTIMER1_IRQn              = 13,       /*!< Dual Timer1 Interrupt                             */
  PWM0_IRQn                    = 14,       /*!< PWM  Interrupt                                    */
  PWM1_IRQn                    = 15,       /*!< PWM1  Interrupt                                   */
  PWM2_IRQn                    = 16,       /*!< PWM2  Interrupt                                   */
  PWM3_IRQn                    = 17,       /*!< PWM3  Interrupt                                   */
  PWM4_IRQn                    = 18,       /*!< PWM4  Interrupt                                   */
  PWM5_IRQn                    = 19,       /*!< PWM5  Interrupt                                   */
  PWM6_IRQn                    = 20,       /*!< PWM6  Interrupt                                   */
  PWM7_IRQn                    = 21,       /*!< PWM7  Interrupt                                   */
  RTC_IRQn                     = 22,       /*!< RTC  Interrupt                                    */
  ADC_IRQn                     = 23,       /*!< ADC  Interrupt                                    */
  WZTOE_IRQn                   = 24,       /*!< WZTOE  Interrupt                                  */

} IRQn_Type;


#endif /* TYPE_H_ */
