/* File: bootloader.s
 * Purpose: bootstrap the firmware
 * Date Modified: 13 September 2016
 *
 * Modified from the original `startup_ARMCM4.S` file.
 * Original Version: V2.0
 * Date Created: 16 August 2013
 *
/* Copyright (c) 2011 - 2013 ARM LIMITED

   All rights reserved.
   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are met:
   - Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
   - Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.
   - Neither the name of ARM nor the names of its contributors may be used
     to endorse or promote products derived from this software without
     specific prior written permission.
   *
   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
   ARE DISCLAIMED. IN NO EVENT SHALL COPYRIGHT HOLDERS AND CONTRIBUTORS BE
   LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
   CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
   SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
   INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
   CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
   ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
   POSSIBILITY OF SUCH DAMAGE.
   ---------------------------------------------------------------------------*/
	.syntax	unified
	.arch	armv7e-m

	WDOG_BASE_ADDR	= 0x40052000
	WDOG_STCTRLH	= 0x00
	WDOG_UNLOCK	= 0x0E

        .section .stack
        .align  3
        .equ    Stack_Size, 1024
        .globl  __StackTop
        .globl  __StackLimit
__StackLimit:
        .space  Stack_Size
        .size   __StackLimit, . - __StackLimit
__StackTop:
        .size   __StackTop, . - __StackTop

#if 0
        .section .heap
        .align  3
        .equ    Heap_Size, 1024
        .globl  __HeapBase
        .globl  __HeapLimit
__HeapBase:
        .space  Heap_Size
        .size   __HeapBase, . - __HeapBase
__HeapLimit:
        .size   __HeapLimit, . - __HeapLimit
#endif

	.section .isr_vector
	.align	2
	.globl	__isr_vector
__isr_vector:
	.long	__StackTop            /* Top of Stack */
	.long	Reset_Handler         /* Reset Handler */
	.long	NMI_Handler           /* NMI Handler */
	.long	HardFault_Handler     /* Hard Fault Handler */
	.long	MemManage_Handler     /* MPU Fault Handler */
	.long	BusFault_Handler      /* Bus Fault Handler */
	.long	UsageFault_Handler    /* Usage Fault Handler */
	.long	0                     /* Reserved */
	.long	0                     /* Reserved */
	.long	0                     /* Reserved */
	.long	0                     /* Reserved */
	.long	SVC_Handler           /* SVCall Handler */
	.long	DebugMon_Handler      /* Debug Monitor Handler */
	.long	0                     /* Reserved */
	.long	PendSV_Handler        /* PendSV Handler */
	.long	SysTick_Handler       /* SysTick Handler */

	/* External interrupts */
	.long	Default_Handler

	.size	__isr_vector, . - __isr_vector

	.section .fcf
	.byte	0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF	/* Backdoor Comparison Key */
	.byte   0xFF, 0xFF, 0xFF, 0xFF				/* FPROT[3..0] */
	.byte	0xFE						/* FSEC */
	.byte	0x07						/* FOPT */
	.byte	0xFF						/* FEPROT */
	.byte	0xFF						/* FDPROT */

	.text
	.thumb
	.thumb_func
	.align	2
	.globl	Reset_Handler
	.type	Reset_Handler, %function
Reset_Handler:
	/* Unlock WDOG */
	ldr	r0, =WDOG_BASE_ADDR
	ldr	r1, =0xC520
	strh	r1, [r0, WDOG_UNLOCK]
	ldr	r1, =0xD928
	strh	r1, [r0, WDOG_UNLOCK]

	/* Disable WDOG */
	ldrh	r1, [r0, WDOG_STCTRLH]
	bic	r1, #1
	strh	r1, [r0, WDOG_STCTRLH]

/*     Loop to copy data from read only memory to RAM. The ranges
 *      of copy from/to are specified by following symbols evaluated in
 *      linker script.
 *      __etext: End of code section, i.e., begin of data sections to copy from.
 *      __data_start__/__data_end__: RAM address range that data should be
 *      copied to. Both must be aligned to 4 bytes boundary.  */

        ldr     r1, =__etext
        ldr     r2, =__data_start__
        ldr     r3, =__data_end__

/* Here are two copies of loop implemenations. First one favors code size
 * and the second one favors performance. Default uses the first one.
 * Change to "#if 0" to use the second one */
.flash_to_ram_loop:
        cmp     r2, r3
        ittt    lt
        ldrlt   r0, [r1], #4
        strlt   r0, [r2], #4
        blt     .flash_to_ram_loop

/* Clear .bss segment */
        mov     r0, #0
        ldr     r1, =__bss_start__
        ldr     r2, =__bss_end__
.clear_bss_loop:
        cmp     r1, r2
        itt     lt
        strlt   r0, [r1], #4
        blt     .clear_bss_loop

/* Call libc init routines */
        bl      __libc_init_array

/* Call main */
        bl      main
        bl      abort
.exit_loop:
        b       .exit_loop

	.pool
	.size	Reset_Handler, . - Reset_Handler

	.align	1
	.thumb_func
	.weak	Default_Handler
	.type	Default_Handler, %function
Default_Handler:
	b	.
	.size	Default_Handler, . - Default_Handler

/*    Macro to define default handlers. Default handler
 *    will be weak symbol and just dead loops. They can be
 *    overwritten by other handlers */
	.macro	def_irq_handler	handler_name
	.weak	\handler_name
	.set	\handler_name, Default_Handler
	.endm

	def_irq_handler	NMI_Handler
	def_irq_handler	HardFault_Handler
	def_irq_handler	MemManage_Handler
	def_irq_handler	BusFault_Handler
	def_irq_handler	UsageFault_Handler
	def_irq_handler	SVC_Handler
	def_irq_handler	DebugMon_Handler
	def_irq_handler	PendSV_Handler
	def_irq_handler	SysTick_Handler
	def_irq_handler	DEF_IRQHandler

        .end
