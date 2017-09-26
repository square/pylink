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
 * Created: November 10th, 2016
 * Modified: November 10th, 2016
 *****************************************************************************/
#include <stdint.h>
#include <stdlib.h>
#define FOREVER for(;;)

static unsigned int s_counter = 0;

static unsigned int increment_counter(void) {
    s_counter++;
    return s_counter;
}

int main(void) {
    FOREVER {
        increment_counter();
    }

    return 0;
}
