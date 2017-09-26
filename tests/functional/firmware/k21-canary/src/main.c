/******************************************************************************
 * File: main.c
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
 * Created: September 28th, 2016
 * Modified: September 28th, 2016
 *****************************************************************************/
#include <stdint.h>
#include <stdlib.h>
#define BUFFER_SIZE   (40)
#define OVERFLOW_SIZE (BUFFER_SIZE + 8)
#if UINT32_MAX == UINTPTR_MAX
#define STACK_CHK_GUARD 0xe2dee396
#else
#define STACK_CHK_GUARD 0x595e9fbd94fda766
#endif

uintptr_t __stack_chk_guard = STACK_CHK_GUARD;

__attribute__((noreturn)) void __stack_chk_fail(void) {
    asm("BKPT");
    abort();
}

int function_that_overflows(void) {
    volatile unsigned int data[BUFFER_SIZE];
    volatile unsigned int i = 0;
    for (i = 0; i < OVERFLOW_SIZE; i++) {
        data[i] = i;
    }
    return data[i - 1];
}

int main(void) {
    function_that_overflows();

    while (1);

    return 0;
}
