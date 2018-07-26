/*
 * timer.c
 *
 *  Created on: Jun 20, 2014
 *      Author: kaizen
 */

#include "timer.h"
#include "uart.h"


// Init global value
volatile uint32_t g_isTimeout[2] = {0,};

void DUALTIMER0_Handler(void)
{
	if (TIMER0->TimerMIS != 0)
	{
  		TIMER0->TimerIntClr = 0;	// dualtimer_irq_clear
		g_isTimeout[0]++;
	} 
	if (TIMER1->TimerMIS != 0)
	{
  		TIMER1->TimerIntClr = 0;	// dualtimer_irq_clear
		g_isTimeout[1]++;
	}
}


void Dualtimer0_Init(DUALTIMER_SINGLE_TypeDef *TIMERx, DualTimerModeDef mode,
		DualTimerBitDef size, uint32_t cycle, uint32_t prescale, uint32_t interrupt )
{
	uint32_t ctrl_val;

	TIMERx->TimerControl = 0;
	TIMERx->TimerIntClr = 0;	// dualtimer_irq_clear
	TIMERx->TimerLoad = cycle;

	ctrl_val = DUALTIMER_CTRL_PRESCALE(prescale) | DUALTIMER_CTRL_SIZE(size) | DUALTIMER_CTRL_EN;

	if( interrupt )
	{
		ctrl_val = ctrl_val | DUALTIMER_CTRL_INTEN(interrupt);
		NVIC_EnableIRQ(DUALTIMER0_IRQn);
	}

	if(mode == ONESHOT)
	{
		ctrl_val = ctrl_val | DUALTIMER_CTRL_MODE(1) | DUALTIMER_CTRL_ONESHOT(1);
	}

	else
	{
		ctrl_val |= DUALTIMER_CTRL_MODE(mode);
	}

	TIMERx->TimerControl = ctrl_val;
}

void Dualtimer0_Deinit(DUALTIMER_SINGLE_TypeDef *TIMERx)
{
	NVIC_DisableIRQ(DUALTIMER0_IRQn);
 	TIMERx->TimerControl &= ~DUALTIMER_CTRL_EN;
}

void Delay(DelayUnitDef unit, uint32_t nTime)
{
	uint32_t timer_val;

	// Timer init;
	TIMER_CLKEN(0);

	if(unit == DELAY_US)
		timer_val = nTime * 20;
	else
		timer_val = nTime * 20 * 1000;

	Dualtimer0_Init(TIMER0, ONESHOT, TIMER_32BIT, timer_val, PRESCALE_1_1, USE_IRQ);
	
	while( g_isTimeout[0] == 0 );


	Dualtimer0_Deinit(TIMER0);
	TIMER_CLKDIS(0);
}

void timeout_us(uint32_t nTime)
{
	uint32_t timer_val;

	TIMER_CLKEN(1);
	timer_val = nTime * 20;
	Dualtimer0_Init(TIMER1, ONESHOT, TIMER_32BIT, timer_val, PRESCALE_1_1, USE_IRQ);
}

void timeout_ms(uint32_t nTime)
{
	uint32_t timer_val;

	TIMER_CLKEN(1);
	timer_val = nTime * 20 * 1000;
	Dualtimer0_Init(TIMER1, ONESHOT, TIMER_32BIT, timer_val, PRESCALE_1_1, USE_IRQ);
}

uint8_t is_timeout()
{
	if( g_isTimeout[1] > 0 )
	{
		Dualtimer0_Deinit(TIMER1);
		TIMER_CLKDIS(1);
		return RET_SUCCESS;
	}

	return RET_FAIL;
}



///* Start the timer */
//void dualtimer_start(CMSDK_DUALTIMER_SINGLE_TypeDef *CMSDK_DUALTIMERx)
//{
//  CMSDK_DUALTIMERx->TimerControl |= CMSDK_DUALTIMER_CTRL_EN_Msk;
//}

/*
void timeout_us(uint32_t nTime)
{
	uint32_t timer_val;

	timer_val = nTime * 20;

	CMSDK_DUALTIMER_CLKEN(0);
	NVIC_EnableIRQ(DUALTIMER0_IRQn);
	dualtimer_setup(CMSDK_DUALTIMER0, ONESHOOT, TIMER_32BIT, timer_val, PRESCALE_1_1,DUALTIMER0_IRQn);
}

void timeout_ms(uint32_t nTime)
{
	uint32_t timer_val;

	CMSDK_DUALTIMER_CLKEN(0);

	timer_val = nTime * 20 * 1000;
	NVIC_EnableIRQ(DUALTIMER0_IRQn);
	dualtimer_setup(CMSDK_DUALTIMER0, ONESHOOT, TIMER_32BIT, timer_val, PRESCALE_1_1,DUALTIMER0_IRQn);
}

uint32_t isTimeout()
{
	if(g_isTimeout >= 1)
	{
		dualtimer_stop(CMSDK_DUALTIMER0);
		NVIC_EnableIRQ(DUALTIMER0_IRQn);
		return 1;
	}

	return 0;
}

void clearTimeoutVal()
{
	g_isTimeout = 0;
}
*/

/*
void delay_us(uint32_t nTime)
{
	uint32_t timer_val, i;
	// Timer init;
	CMSDK_DUALTIMER_CLKEN(0);

	dualtimer_setup(CMSDK_DUALTIMER0, PERIODIC, TIMER_16BIT, 20, PRESCALE_1_1, NO_IRQ);

	for(i=0; i<nTime; i++)
	{
		while( (CMSDK_DUALTIMER0->TimerValue) > 0 );
	}

	dualtimer_stop(CMSDK_DUALTIMER0);
	CMSDK_DUALTIMER_CLKEN(1);
}

void delay_ms(uint32_t nTime)
{
	uint32_t i;

	for(i=0; i<nTime; i++)
		delay_us(1000);
}
*/
