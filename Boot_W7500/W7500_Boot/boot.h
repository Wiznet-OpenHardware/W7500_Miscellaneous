#ifndef BOOT_H_
#define BOOT_H_

#include "type.h"

/* DEFINE */
#define SYSREG_BASE 0x41002000
#define REG_BOOT	(SYSREG_BASE + 0x0100)
#define REG_TEST	(SYSREG_BASE + 0x0104)
#define REG_SMODE	(SYSREG_BASE + 0x0108)

#define BOOT_APP_MODE	0x00
#define BOOT_ISP_MODE	0x01
#define BOOT_PP_MODE	0x03


/* FUNCTION */
void StartApp();

#endif /* BOOT_H_ */
