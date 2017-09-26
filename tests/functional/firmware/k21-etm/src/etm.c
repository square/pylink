/******************************************************************************
 * File: etm.c
 *
 * Copyright (c) 2017 Square, Inc.
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
 * Created: March 22nd, 2017
 * Modified: March 22nd, 2017
 *****************************************************************************/

#define ETM_LAR   (*((volatile unsigned *)0xE0041FB0))
#define ETM_CR    (*((volatile unsigned *)0xE0041000))
#define ETF_FCR   (*((volatile unsigned *)0xE0043000u))
#define MCM_ETBCC (*((volatile unsigned *)0xE0080014u))
#define SIM_SOPT2 (*((volatile unsigned *)0x40048004u))
#define SIM_SCGC5 (*((volatile unsigned *)0x40048004u))

#define ETM_LAR_UNLOCK          0xC5ACCE55
#define ETF_ETM_ENABLE          0x1u
#define ETMCR_POWER_DOWN_MASK   0x1u
#define MCM_ETBCC_ETDIS_MASK    0x10u

#define SIM_SOPT2_TRACECLKSEL_MASK               0x1000u

#define PORT_PCR_REG(base,index)                 (base[index])
#define PORTE_BASE_PTR                           ((volatile unsigned *)0x4004D000u)
#define PORTE_PCR0                               PORT_PCR_REG(PORTE_BASE_PTR,0)
#define PORTE_PCR1                               PORT_PCR_REG(PORTE_BASE_PTR,1)
#define PORTE_PCR2                               PORT_PCR_REG(PORTE_BASE_PTR,2)
#define PORTE_PCR3                               PORT_PCR_REG(PORTE_BASE_PTR,3)
#define PORTE_PCR4                               PORT_PCR_REG(PORTE_BASE_PTR,4)

#define PORT_PCR_DSE_ENABLE       (1<<6)  /* Port Configuration Register, Drive Strength Enable (DSE) bit */
#define PORT_PCR_MUX_ALTERNATE_5  (5<<8) /* Port Configuration Register, Alternate 5 function (mux as trace pin) */
#define PORT_PCR_CONFIG_FOR_TRACE (PORT_PCR_DSE_ENABLE|PORT_PCR_MUX_ALTERNATE_5) /* for trace, mux it with function 5 and high drive strength */
#define PORTE_CLOCK_GATE          (1<<13)

void etm_configure_gpio(void) {
    /* check and enable clocking of PORTE */
    SIM_SCGC5 |= PORTE_CLOCK_GATE;
    SIM_SOPT2 |= SIM_SOPT2_TRACECLKSEL_MASK; /* Debug trace clock select = Core/system clock */
    /* Trace data (PTE1-4) and clock pin (PTE0), high drive strength */
    PORTE_PCR0 = PORT_PCR_CONFIG_FOR_TRACE; /* PTE0, PORTE_PCR0 at 0x4004D000, trace clock pin, high drive strength */
    PORTE_PCR1 = PORT_PCR_CONFIG_FOR_TRACE; /* PTE1, PORTE_PCR1 at 0x4004D004, trace data pin, high drive strength */
    PORTE_PCR2 = PORT_PCR_CONFIG_FOR_TRACE; /* PTE2, PORTE_PCR3 at 0x4004D008, trace data pin, high drive strength */
    PORTE_PCR3 = PORT_PCR_CONFIG_FOR_TRACE; /* PTE3, PORTE_PCR3 at 0x4004D00C, trace data pin, high drive strength */
    PORTE_PCR4 = PORT_PCR_CONFIG_FOR_TRACE; /* PTE4, PORTE_PCR4 at 0x4004D010, trace data pin, high drive strength */
}

void etm_configure_registers(void) {
    // A privileged write of `0xC5ACCE55` enables write access to the ETM
    // Control Register.
    ETM_LAR = ETM_LAR_UNLOCK;

    // The Power Down bit in the ETM control register must be cleared in order
    // to enable ETM.
    ETM_CR &= ~(ETMCR_POWER_DOWN_MASK);

    /* Set up Embedded Trace FIFO to enable the ETM path. */
    ETF_FCR |= ETF_ETM_ENABLE;

    // Enable the signal path from ETM to TPIU
    // MCM is Kinetis-specific, not ARM.
    MCM_ETBCC &= (~MCM_ETBCC_ETDIS_MASK);
}

void etm_init(void) {
    etm_configure_gpio();
    etm_configure_registers();
}
