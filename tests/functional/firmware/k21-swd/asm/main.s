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
        sys_write = 0x05
        sys_exit  = 0x0

        .text
        .thumb
        .thumb_func
        .align        2
        .global       main
        .type         main, %function
main:
        mov     r0, #sys_write
        ldr     r1, =array
        mov     r2, r1

        mov     r3, #0
        str     r3, [r2]

        ldr     r3, =msg
        add     r2, r2, #4
        str     r3, [r2]

        mov     r3, #37
        add     r2, r2, #4
        str     r3, [r2]

        bkpt    sys_write

        mov     r0, #0
        bkpt    sys_exit

        .data
        .balign 4
array:
        .skip 12

msg:
        .asciz "You must construct additional pylons."
        .end
