/******************************************************************************
 * File: main.c
 *
 * Copyright (c) 2019 Square, Inc.
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
 * Created: March 12th, 2019
 * Modified: March 12th, 2019
 *****************************************************************************/

#include <SEGGER_RTT.h>

#include <string.h>

#define FOREVER  for(;;)


int main(void) {
    char up_buf[2][1024] = {{0}};
    char down_buf[2][1024] = {{0}};
    char input;

    SEGGER_RTT_Init();

    // Up Buffer 0 is configured at compile-time; can only change name.
    SEGGER_RTT_SetNameUpBuffer(0, "PuTTY");
    SEGGER_RTT_ConfigUpBuffer(1, "RUMBA", up_buf[0], sizeof(up_buf[0]), 0x0);
    SEGGER_RTT_ConfigUpBuffer(2, "ZOC", up_buf[1], sizeof(up_buf[1]), 0x0);

    // Down Buffer 0 is configured at compile-time; can only change name.
    SEGGER_RTT_SetNameDownBuffer(0, "iTerm2");
    SEGGER_RTT_ConfigDownBuffer(1, "ZTerm", down_buf[0], sizeof(down_buf[0]), 0x0);
    SEGGER_RTT_ConfigDownBuffer(2, "xterm", down_buf[1], sizeof(down_buf[1]), 0x0);

    FOREVER {
        input = (char)0;
        while (!input) {
            SEGGER_RTT_Read(0, &input, 1);
        }
        SEGGER_RTT_PutChar(0, input);
    }

    return 0;
}
