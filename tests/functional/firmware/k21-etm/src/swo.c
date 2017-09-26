/******************************************************************************
 * File: swo.c
 *
 * Copyright (c) 2016 Square, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Author: Ford Peprah <ford@squareup.com>
 *
 * Created: September 14th, 2016
 * Modified: September 14th, 2016
 *****************************************************************************/
#include "swo.h"

/**
 * Debug Exception and Monitor Control Register (DEMCR)
 *
 * This is a read/write register used for vector catching and debug monitor
 * control.
 */
#define DEMCR  (*((volatile unsigned *)0xE000EDFC))
#define TRCENA (1 << 24)

/**
 * Selected Pin Protocol Register (TPIU_SPPR)
 *
 * This is a read/write register that is reset with a value of `0x1`, which
 * indicates manchester encoding.  This is a trace point unit register which is
 * used to select which protocol to use for trace output.
 */
#define TPIU_SPPR  (*((volatile unsigned *)0xE00400F0))
#define MANCHESTER 0x00000001
#define NRZ        0x00000002

/**
 * Asynchronous Clock Prescaler Register (ACPR)
 *
 * This is a read/write register that is reset with a value of `0`.  It is used
 * to set a prescaler in order to scale the baud rate of the asynchronous
 * output.
 */
#define TPIU_ACPR (*((volatile unsigned *)0xE0040010))

/**
 * Data Watchpoint and Trace Control Register (DWT_CTRL)
 *
 * This is a read/write register that has various reset values.  This register
 * is used to provide information about the data watchpoint.
 */
#define DWT_CTRL (*((volatile unsigned *)0xE0001000))

/**
 * Trace Port Interface Unit Formatter and Flush Control Register (TPIU_FFCR)
 *
 * This is a read/write register that is reset with a value of `0x102`.  This
 * register is used to trigger events, enable and configure formatting, and
 * generate flush events.
 */
#define TPIU_FFCR (*((volatile unsigned *)0xE0040304))

#define ITM_Port8(n)  (*((volatile unsigned char  *)(ITM_BASEADDR + 4 * n)))
#define ITM_Port16(n) (*((volatile unsigned short *)(ITM_BASEADDR + 4 * n)))
#define ITM_Port32(n) (*((volatile unsigned int   *)(ITM_BASEADDR + 4 * n)))

void swo_init(unsigned int cpu_speed, unsigned int swo_speed, unsigned int port_mask) {
    // Bit [24] Read/write TRCENA.  Must be set to `1` to enable use of the
    // trace and debug blocks: Data Watchpoint and Trace (DWT), Instrumentation
    // Trace Macrocell (ITM), Embedded Trace Macrocell (ETM), and Trace Port
    // Interface Unit (TPIU).
    DEMCR |= TRCENA;

    // A privileged write of `0xC5ACCE55` enables more write access to Control
    // Register `0xE00::0xFFC`. An invalid write removes write access.
    ITM_LAR = 0xC5ACCE55;

    // Bits [1:0] read/write select the protocol to use.  `0` and `3` are
    // reserved, while `01` is SWO using Manchester encoding, and `10` is SWO
    // using NRZ encoding.
    TPIU_SPPR = NRZ;

    // Prescaler value is computed as the quotient between the cpu speed and
    // the SWO speed.  We subtract one, as the prescaler is ultimately computed
    // by adding `1` to the value written to the ACPR.
    unsigned int prescaler = (cpu_speed / swo_speed) - 1;
    TPIU_ACPR = prescaler;

    // Bits [3:0] specify which stimulus ports can be accessed and describe the
    // ranges from `31-24`, `23-16`, `15-8`, and `7-0` respectively.  By
    // default, we want to allow access to all.  Note that this is different
    // from actually enabling writing to them.
    ITM_TPR = 0x00000000;

    // DWT Control Register.  We enable the exception trace and exception
    // overhead.
    DWT_CTRL |= 0x400003FE;

    // Bit [0] enables ITM.  Bits[4:2] enable SWV behaviour, DWT stimulus, and
    // sync packets for TPIU respectively.  Bit `16` sets the ATB ID for the
    // Coresight System (we set this to `1`).
    ITM_TCR = 0x0001001F;

    // Bit [9] indicates that a trigger should be fired on a trigger event.
    // This will allow tracing of trigger events.  The rest of the events are
    // disabled.
    TPIU_FFCR = 0x00000100;

    // We set the user specified port mask to enable tracing on the specified
    // ITM stimulus ports.  One bit per stimulus port.
    ITM_TER = port_mask;
}

int swo_putchar(stimulus_port_t port, char ch) {
    // Check that tracing is enabled on the debug monitor.
    if ((DEMCR & TRCENA) == 0) {
        return 0;
    }

    // Check that ITM is enabled.
    if ((ITM_TCR & 1) == 0) {
        return 0;
    }

    // Check that tracing is enabled for the given port.
    if ((ITM_TER & (1 << port)) == 0) {
        return 0;
    }

    while (ITM_Port8(port) == 0);

    ITM_Port8(port) = (int)ch;

    return ch;
}

void swo_puts(stimulus_port_t port, const char *string) {
    while (*string) {
        swo_putchar(port, *string++);
    }
}

#ifdef OVERRIDE_PRINTF

int putchar(int ch) {
    return swo_putchar(STIMULUS_PORT_0, ch);
}

int fputc(int ch, FILE *f) {
    if (f) {
        return swo_putchar(f->port, ch);
    }
    return swo_putchar(STIMULUS_PORT_0, ch);
}

#endif
