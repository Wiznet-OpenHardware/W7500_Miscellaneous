/*
 * timer.h
 *
 *  Created on: Jun 20, 2014
 *      Author: kaizen
 */

#ifndef TIMER_H_
#define TIMER_H_

#include "type.h"

#define PRESCALE_1_1   0
#define PRESCALE_1_16  1
#define PRESCALE_1_256 2
#define NO_IRQ         0
#define USE_IRQ        1

#define DUALTIMER0_BASE   ( 0x40001000UL)
#define DUALTIMER1_BASE   ( 0x40002000UL)

#define TIMER0          ((DUALTIMER_SINGLE_TypeDef  *)  DUALTIMER0_BASE )
#define TIMER1          ((DUALTIMER_SINGLE_TypeDef  *) (DUALTIMER0_BASE + 0x20UL))
#define TIMER2          ((DUALTIMER_SINGLE_TypeDef  *)  DUALTIMER1_BASE )
#define TIMER3          ((DUALTIMER_SINGLE_TypeDef  *) (DUALTIMER1_BASE + 0x20UL))

//Clock enable
#define TIMER0_CLKEN    (*(uint32_t *) (DUALTIMER0_BASE | 0x80) )
#define TIMER1_CLKEN    (*(uint32_t *) (DUALTIMER0_BASE | 0xA0) )
#define TIMER2_CLKEN    (*(uint32_t *) (DUALTIMER1_BASE | 0x80) )
#define TIMER3_CLKEN    (*(uint32_t *) (DUALTIMER1_BASE | 0xA0) )

typedef struct
{
  __IO uint32_t TimerLoad;    // <h> Timer Load </h>
  __I  uint32_t TimerValue;   // <h> Timer Counter Current Value <r></h>
  __IO uint32_t TimerControl; // <h> Timer Control
                              //   <o.7> TimerEn: Timer Enable
                              //   <o.6> TimerMode: Timer Mode
                              //     <0=> Freerunning-mode
                              //     <1=> Periodic mode
                              //   <o.5> IntEnable: Interrupt Enable
                              //   <o.2..3> TimerPre: Timer Prescale
                              //     <0=> / 1
                              //     <1=> / 16
                              //     <2=> / 256
                              //     <3=> Undefined!
                              //   <o.1> TimerSize: Timer Size
                              //     <0=> 16-bit counter
                              //     <1=> 32-bit counter
                              //   <o.0> OneShot: One-shoot mode
                              //     <0=> Wrapping mode
                              //     <1=> One-shot mode
                              // </h>
  __O  uint32_t TimerIntClr;  // <h> Timer Interrupt Clear <w></h>
  __I  uint32_t TimerRIS;     // <h> Timer Raw Interrupt Status <r></h>
  __I  uint32_t TimerMIS;     // <h> Timer Masked Interrupt Status <r></h>
  __IO uint32_t TimerBGLoad;  // <h> Background Load Register </h>
} DUALTIMER_SINGLE_TypeDef;

typedef enum DualTimerMode{
	FREE_RUNNING	= 0,
	PERIODIC		= 1,
	ONESHOT			= 2
}DualTimerModeDef;

typedef enum DualTimerBit{
	TIMER_16BIT = 0,
	TIMER_32BIT = 1
}DualTimerBitDef;

typedef enum DelayUnit{
	DELAY_US = 0,
	DELAY_MS = 1,
}DelayUnitDef;

/*
#define DUALTIMER_CTRL_EN			(0x1ul << 7)
#define DUALTIMER_CTRL_MODE			(0x1ul << 6) 	 //  (0: Freerunning, 1: Periodic);
#define DUALTIMER_CTRL_INTEN		(0x1ul << 5)	
#define DUALTIMER_CTRL_PRESCALE		(0x3ul << 2)
#define DUALTIMER_CTRL_SIZE			(0x1ul << 1)	 // (0: 16bit counter, 1: 32bit counter);
#define DUALTIMER_CTRL_ONESHOT		(0x1ul << 0)	 // (0: Wrapping mode, 1: One-shot mode);
*/

#define DUALTIMER_CTRL_EN			(0x1ul << 7)
#define DUALTIMER_CTRL_MODE(n)		((n & 0x1) << 6)	// (0: Freerunning, 1: Periodic)
#define DUALTIMER_CTRL_INTEN(n)		((n & 0x1) << 5)	
#define DUALTIMER_CTRL_PRESCALE(n)	((n & 0x3) << 2)
#define DUALTIMER_CTRL_SIZE(n)		((n & 0x1) << 1) // (0: 16bit counter, 1: 32bit counter);
#define DUALTIMER_CTRL_ONESHOT(n)	((n & 0x1) << 0) // (0: Wrapping mode, 1: One-shot mode);



#define TIMER_CLKEN(n)	(TIMER##n##_CLKEN = 1)
#define TIMER_CLKDIS(n)	(TIMER##n##_CLKEN = 0)




/******* Value ********/


/****** Function *******/
void Dualtimer0_Init(DUALTIMER_SINGLE_TypeDef *DUALTIMERx, DualTimerModeDef mode,		
		DualTimerBitDef size, uint32_t cycle, uint32_t prescale, uint32_t interrupt );
void Dualtimer0_Deinit();
void Delay(DelayUnitDef unit, uint32_t time);

uint32_t IsTimeout	();
void ClearTimeoutValue	();
/************************/


#endif /* TIMER_H_ */
