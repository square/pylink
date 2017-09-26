/******************************************************************************
 * File: main.c
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
#include "etm.h"
#include "swo.h"
#define CPU_SPEED          21004050   // 21 MHz
#define SWO_SPEED          3000000    // 3 MHz
#define PORT_MASK          0x1        // Enable one port.
#define FOREVER            for(;;)

void test_func(void) {
    static volatile int counter = 0;
    counter++;
}

int main(void) {
    int counter = 0;
    const char *string = "You must construct additional pylons.";
    SWO_Init(CPU_SPEED, SWO_SPEED, PORT_MASK);
    ETM_Init();

    FOREVER {
        counter++;
        SWO_Puts(0, string);
        if (counter % 3) {
            test_func();
        }
    }

    return 0;
}
