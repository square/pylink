# Copyright 2025 Jeremiah Gillis
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .. import enums
from .. import errors

import ctypes

# Global variable to store the ID code
global_id_code = None


def set_unlock_idcode(self, id_code):
    """Sets the J-Link unlock ``IDCODE`` and enables function redirect. This is
    only supported by certain devices such as Renesas.

    Args:
      self (JLink): the ``JLink`` instance
      id_code (str): ``IDCODE`` to unlock debug access in hexadecimal format

    Returns:
      ``None``

    Raises:
      ValueError: if ``id_code`` is not a hexadecimal string.
      JLinkException: if function is not found.
    """
    try:
        int(id_code, 16)
    except ValueError:
        raise ValueError('id_code must be a hexadecimal string.')

    global global_id_code
    global_id_code = id_code

    self._dll.JLINK_GetpFunc.restype = ctypes.c_void_p
    self.unlock_idcode_cb = enums.JLinkFunctions.UNLOCK_IDCODE_HOOK_PROTOTYPE(unlock_idcode_hook_dialog)
    function_ptr = self._dll.JLINK_GetpFunc(enums.JLinkIndirectFunctionIndex.SET_HOOK_DIALOG_UNLOCK_IDCODE)
    if not function_ptr:
        raise errors.JLinkException('Could not find Set Hook Dialog Unlock IDCODE function.')

    callback_override = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
    function = ctypes.cast(function_ptr, callback_override)
    function(self.unlock_idcode_cb)
    return


def unlock_idcode_hook_dialog(title, msg, flags, id_code, max_num_bytes):
    """Unlocks debug access using J-Link IDCODE hook.

    Args:
      title (str): title of the unlock id code dialog
      msg (str): text of the unlock id code dialog
      flags (int): flags specifying which values can be returned
      id_code (void pointer): buffer pointer to store IDCODE
      max_num_bytes (int): maximum number of bytes that can be written to IDCODE buffer

    Returns:
      ``enums.JLinkFlags.DLG_BUTTON_OK``
    """
    global global_id_code
    code_bytes = bytes.fromhex(global_id_code)
    data = ctypes.cast(id_code, ctypes.POINTER(ctypes.c_byte * max_num_bytes))
    data.contents[:min(len(code_bytes), max_num_bytes)] = code_bytes

    return enums.JLinkFlags.DLG_BUTTON_OK
