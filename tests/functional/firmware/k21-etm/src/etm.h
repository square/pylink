/******************************************************************************
 * File: etm.h
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
#ifndef __ETM_H__
#define __ETM_H__

#define ETM_Init etm_init

/**
 * etm_init:
 *  Performs initialization sequence for Embedded Trace Macrocell (ETM).
 *
 *  This is a blocking call.
 */
void etm_init(void);

#endif /* __ETM_H__ */
