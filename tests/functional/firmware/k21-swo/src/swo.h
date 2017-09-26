/******************************************************************************
 * File: swo.h
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
#ifndef __SWO_H__
#define __SWO_H__

#define SWO_Init    swo_init
#define SWO_Putchar swo_putchar
#define SWO_Puts    swo_puts

/**
 * ITM Stimulus Ports
 *
 * There are 32 stimulus ports (indexed `0 - 31`).  Each port has its own
 * address which is calculated by multiplying the index by `4` and adding it to
 * the ITM base address.
 *
 * Reading from any of these ports will return the FIFO status in the last bit.
 * If the FIFO status is `0`, it is full, while `1` is not full.
 */
#define ITM_BASEADDR 0xE0000000

/**
 * ITM Registers
 *
 * ITM Trace Enable Register (ITM_TER), ITM Trace Privilege Register (ITM_TPR),
 * ITM Trace Control Register (ITM_TCR), ITM Lock Access Register (ITM_LAR),
 * and the ITM Lock Status Register (ITM_LSR).
 */
#define ITM_TER  (*((volatile unsigned *)0xE0000E00))
#define ITM_TPR  (*((volatile unsigned *)0xE0000E40))
#define ITM_TCR  (*((volatile unsigned *)0xE0000E80))
#define ITM_LAR  (*((volatile unsigned *)0xE0000FB0))
#define ITM_LSR  (*((volatile unsigned *)0xE0000FB4))

/**
 * Stimulus Port Indices
 */
typedef enum stimulus_port_t {
    STIMULUS_PORT_0 = 0,
    STIMULUS_PORT_1,
    STIMULUS_PORT_2,
    STIMULUS_PORT_3,
    STIMULUS_PORT_4,
    STIMULUS_PORT_5,
    STIMULUS_PORT_6,
    STIMULUS_PORT_7,
    STIMULUS_PORT_8,
    STIMULUS_PORT_9,
    STIMULUS_PORT_10,
    STIMULUS_PORT_11,
    STIMULUS_PORT_12,
    STIMULUS_PORT_13,
    STIMULUS_PORT_14,
    STIMULUS_PORT_15,
    STIMULUS_PORT_16,
    STIMULUS_PORT_17,
    STIMULUS_PORT_18,
    STIMULUS_PORT_19,
    STIMULUS_PORT_20,
    STIMULUS_PORT_21,
    STIMULUS_PORT_22,
    STIMULUS_PORT_23,
    STIMULUS_PORT_24,
    STIMULUS_PORT_25,
    STIMULUS_PORT_26,
    STIMULUS_PORT_27,
    STIMULUS_PORT_28,
    STIMULUS_PORT_29,
    STIMULUS_PORT_30,
    STIMULUS_PORT_31,
    NUM_STIMULUS_PORTS
} stimulus_port_t;

#ifdef OVERRIDE_PRINTF

struct __FILE {
   stimulus_port_t port;
};

typedef struct __FILE FILE;

#endif

/**
 * swo_init:
 *   Performs necessary setup in order to send data over SWO using the ITM.
 *
 *   This is a blocking call.
 */
void swo_init(unsigned int cpu_speed, unsigned int swo_speed, unsigned int port_mask);

/**
 * swo_putchar:
 *   Puts a character to the given stimulus port.
 *
 *   Returns the character written on success, otherwise `0`.
 *
 *   This is a blocking call.
 */
int swo_putchar(stimulus_port_t port, char ch);

/**
 * swo_puts:
 *   Puts a string to the given stimulus port one character at a time.
 *
 *   This is a blocking call.
 */
void swo_puts(stimulus_port_t port, const char *string);

#endif /* __SWO_H__ */
