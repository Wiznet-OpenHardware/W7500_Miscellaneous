#-----------------------------------------------------------------------------
# The confidential and proprietary information contained in this file may
# only be used by a person authorised under and to the extent permitted
# by a subsisting licensing agreement from ARM Limited.
#
#            (C) COPYRIGHT 2010-2013 ARM Limited.
#                ALL RIGHTS RESERVED
#
# This entire notice must be reproduced on all copies of this file
# and copies of this file may only be made by a person if such person is
# permitted to do so under the terms of a subsisting license agreement
# from ARM Limited.
#
#      SVN Information
#
#      Checked In          : $Date: 2013-04-03 15:01:25 +0100 (Wed, 03 Apr 2013) $
#
#      Revision            : $Revision: 242777 $
#
#      Release Information : Cortex-M System Design Kit-r1p0-00rel0
#-----------------------------------------------------------------------------
#
# Cortex-M System Design Kit software compilation make file
#
#-----------------------------------------------------------------------------
#
#  Configurations
#
# Choose the core instantiated, can be
#  - CORTEX_M0
#  - CORTEX_M0PLUS
#CPU_PRODUCT = CORTEX_M0PLUS
CPU_PRODUCT = CORTEX_M0
TOOL_CHAIN	= gcc
CPU_TYPE	= -mcpu=cortex-m0

GNU_CC      = arm-none-eabi-gcc
GNU_OBJDUMP = arm-none-eabi-objdump
GNU_OBJCOPY = arm-none-eabi-objcopy

#GNU_CC_FLAGS = -g -O3 -mthumb $(CPU_TYPE)
GNU_CC_FLAGS = -O1 -mthumb $(CPU_TYPE) -nostdlib 

STARTUP_DIR_F	= ./script
STARTUP_FILE	= startup_CMSDK_CM0

TESTNAME		= boot

SOFTWARE_DIR = ../../../software
#LINKER_SCRIPT_PATH = $(SOFTWARE_DIR)/common/scripts
#LINKER_SCRIPT = $(LINKER_SCRIPT_PATH)/cmsdk_cm0.ld

LINKER_SCRIPT_PATH = ./script
LINKER_SCRIPT = $(LINKER_SCRIPT_PATH)/cmsdk_cm0.ld

INCLUDE_DIR  = /usr/local/bin/gcc-arm-none-eabi-4_7-2013q3/lib/gcc/arm-none-eabi/4.7.4/include

CMSIS_DIR    = $(SOFTWARE_DIR)/cmsis
CORE_DIR     = $(CMSIS_DIR)/CMSIS/Include
DEVICE_DIR   = $(CMSIS_DIR)/Device/ARM/CMSDK_CM0

USER_DEFINE    = -DCORTEX_M0



# ---------------------------------------------------------------------------------------
all: all_$(TOOL_CHAIN)

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# gcc : 
all_gcc:
	$(GNU_CC) $(GNU_CC_FLAGS)\
		$(STARTUP_DIR_F)/$(STARTUP_FILE).s \
		$(TESTNAME).c \
		flash.c uart.c general_function.c isp.c xmodem.c \
		-I ./Include \
		-L $(LINKER_SCRIPT_PATH) \
		$(USER_DEFINE) -T $(LINKER_SCRIPT) -o $(TESTNAME).o \
		-Wl,-Map $(TESTNAME).map \

    # Generate disassembly code
	$(GNU_OBJDUMP) -S $(TESTNAME).o > $(TESTNAME).lst
    # Generate binary file
	$(GNU_OBJCOPY) -S $(TESTNAME).o -O binary $(TESTNAME).bin
    # Generate hex file
	$(GNU_OBJCOPY) -S $(TESTNAME).o -O verilog $(TESTNAME).hex

	./mkcnvt.sh
	rm $(TESTNAME).bin
	rm $(TESTNAME).hex


#-I $(CORE_DIR) -I $(DEVICE_DIR)/Include

#-I $(INCLUDE_DIR) \
#-I $(CORE_DIR) -I $(DEVICE_DIR)/Include \

#flash.c uart.c general_function.c isp.c xmodem.c \


emul_flash:
	
	$(GNU_CC) $(GNU_CC_FLAGS)\
		$(STARTUP_DIR_F)/$(STARTUP_FILE).s \
		$(TESTNAME).c \
		e_flash.c uart.c general_function.c isp.c xmodem.c \
		-I ./Include \
		-L $(LINKER_SCRIPT_PATH) \
		$(USER_DEFINE) -DFPGA_TEST -T $(LINKER_SCRIPT) -o emul_boot.o \
		-Wl,-Map emul_boot.map \

    # Generate disassembly code
	$(GNU_OBJDUMP) -S emul_boot.o > emul_boot.lst
    # Generate binary file
	$(GNU_OBJCOPY) -S emul_boot.o -O binary emul_boot.bin
    # Generate hex file
	$(GNU_OBJCOPY) -S emul_boot.o -O verilog emul_boot.hex

	./emul_mkcnvt.sh
	rm emul_boot.bin
	rm emul_boot.hex





# ---------------------------------------------------------------------------------------
# Clean
clean :
	@rm -rf *.o
	@if [ -e $(TESTNAME).hex ] ; then \
		rm -rf $(TESTNAME).hex ; \
	fi
	@if [ -e $(TESTNAME).lst ] ; then \
		rm -rf $(TESTNAME).lst ; \
	fi
	@if [ -e $(TESTNAME).ELF ] ; then \
		rm -rf $(TESTNAME).ELF ; \
	fi
	@if [ -e $(TESTNAME).bin ] ; then \
	rm -rf $(TESTNAME).bin ; \
	fi
	@rm -rf *.crf
	@rm -rf *.plg
	@rm -rf *.tra
	@rm -rf *.htm
	@rm -rf *.dep
	@rm -rf *.d
	@rm -rf *.lnp
	@rm -rf *.bak
	@rm -rf *.lst
	@rm -rf *.axf
	@rm -rf *.sct
	@rm -rf *.__i
	@rm -rf *._ia

