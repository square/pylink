# Copyright 2017 Square, Inc.
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

import pylink.structs as structs

import ctypes
import unittest


class TestStructs(unittest.TestCase):
    """Unit test for the ``structs`` submodule."""

    def setUp(self):
        """Called before each test.

        Performs setup.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns:
          ``None``
        """
        pass

    def tearDown(self):
        """Called after each test.

        Performs teardown.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns:
          ``None``
        """
        pass

    def test_jlink_connect_info(self):
        """Tests the ``JLinkConnectInfo`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns
          ``None``
        """
        info = structs.JLinkConnectInfo()
        info.SerialNumber = 3042517899
        info.acProduct = str.encode('J-Link Plus')
        info.Connection = 1

        info_string = 'J-Link Plus <Serial No. %s, Conn. USB>' % (info.SerialNumber)
        self.assertEqual(info_string, str(info))
        self.assertEqual('JLinkConnectInfo(%s)' % info_string, repr(info))

        info.Connection = 0
        info_string = 'J-Link Plus <Serial No. %s, Conn. IP>' % (info.SerialNumber)
        self.assertEqual(info_string, str(info))
        self.assertEqual('JLinkConnectInfo(%s)' % info_string, repr(info))

    def test_jlink_flash_area(self):
        """Tests the ``JLinkFlashArea`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns
          ``None``
        """
        flash_area = structs.JLinkFlashArea()
        flash_area.Addr = int(0xDEADBEEF)
        flash_area.Size = 1337

        flash_area_string = 'Address = 0xdeadbeef, Size = 1337'
        self.assertEqual(flash_area_string, str(flash_area))
        self.assertEqual('JLinkFlashArea(%s)' % flash_area_string, repr(flash_area))

    def test_jlink_ram_area(self):
        """Tests the ``JLinkRAMArea`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns
          ``None``
        """
        ram_area = structs.JLinkRAMArea()
        ram_area.Addr = int(0xDEADBEEF)
        ram_area.Size = 1337

        ram_area_string = 'Address = 0xdeadbeef, Size = 1337'
        self.assertEqual(ram_area_string, str(ram_area))
        self.assertEqual('JLinkRAMArea(%s)' % ram_area_string, repr(ram_area))

    def test_jlink_device_info(self):
        """Tests the ``JLinkDeviceInfo`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns
          ``None``
        """
        info = structs.JLinkDeviceInfo()
        self.assertEqual(info.SizeofStruct, ctypes.sizeof(info))

        name = b'A Feast For Crows'
        info.sName = ctypes.cast(name, ctypes.POINTER(ctypes.c_char))
        self.assertEqual(name.decode(), info.name)

        manufacturer = b'G.R.R. Martin'
        info.sManu = ctypes.cast(manufacturer, ctypes.POINTER(ctypes.c_char))
        self.assertEqual(manufacturer.decode(), info.manufacturer)

        info_string = 'A Feast For Crows <Core Id. 0, Manu. G.R.R. Martin>'
        self.assertEqual(info_string, str(info))
        self.assertEqual('JLinkDeviceInfo(%s)' % info_string, repr(info))

    def test_jlink_hardware_status(self):
        """Tests the ``JLinkHardwareStatus`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns
          ``None``
        """
        voltage = 100
        status = structs.JLinkHardwareStatus()
        status.VTarget = voltage
        self.assertEqual(voltage, status.voltage)
        self.assertEqual('JLinkHardwareStatus(VTarget=100mV)', str(status))
        self.assertEqual('JLinkHardwareStatus(VTarget=100mV)', repr(status))

    def test_jlink_gpio_descriptor(self):
        """Tests the ``JLinkGPIODescriptor`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns
          ``None``
        """
        name = 'Samuel L. Jackson'
        gpio = structs.JLinkGPIODescriptor()
        gpio.acName = name.encode()

        self.assertEqual(name, str(gpio))
        self.assertEqual('JLinkGPIODescriptor(%s)' % name, repr(gpio))

    def test_jlink_memory_zone(self):
        """Tests the ``JLinkMemoryZone`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns:
          ``None``
        """
        name = b'Futurama'
        desc = b'A show about future stuff'
        addr = 0xdeadbeef

        memory_zone = structs.JLinkMemoryZone()
        memory_zone.sName = ctypes.cast(name, ctypes.c_char_p)
        memory_zone.sDesc = ctypes.cast(desc, ctypes.c_char_p)
        memory_zone.VirtAddr = addr

        memory_zone_string = '%s <Desc. %s, VirtAddr. 0x%x>' % (name, desc, addr)
        self.assertEqual(name, memory_zone.name)
        self.assertEqual(memory_zone_string, str(memory_zone))
        self.assertEqual('JLinkMemoryZone(%s)' % memory_zone_string, repr(memory_zone))

    def test_jlink_speed_info(self):
        """Tests the ``JLinkSpeedInfo`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns:
          ``None``
        """
        info = structs.JLinkSpeedInfo()

        self.assertEqual(ctypes.sizeof(info), info.SizeOfStruct)

        info_string = 'JLinkSpeedInfo(Freq=0Hz)'
        self.assertEqual(info_string, str(info))
        self.assertEqual(info_string, repr(info))

    def test_jlink_swo_start_info(self):
        """Tests the ``JLinkSWOStartInfo`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns:
          ``None``
        """
        start_info = structs.JLinkSWOStartInfo()
        self.assertEqual(ctypes.sizeof(start_info), start_info.SizeofStruct)
        self.assertEqual(0, start_info.Interface)

        info_string = 'JLinkSWOStartInfo(Speed=0Hz)'
        self.assertEqual(info_string, repr(start_info))
        self.assertEqual(info_string, str(start_info))

    def test_jlink_swo_speed_info(self):
        """Tests the ``JLinkSWOSpeedInfo`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns:
          ``None``
        """
        speed_info = structs.JLinkSWOSpeedInfo()
        self.assertEqual(ctypes.sizeof(speed_info), speed_info.SizeofStruct)
        self.assertEqual(0, speed_info.Interface)

        speed_string = 'JLinkSWOSpeedInfo(Interface=UART, Freq=0Hz)'
        self.assertEqual(speed_string, repr(speed_info))
        self.assertEqual(speed_string, str(speed_info))

    def test_jlink_moe_info(self):
        """Tests the ``JLinkMOEInfo`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns:
          ``None``
        """
        moe_info = structs.JLinkMOEInfo()

        # DBGRQ
        moe_info.HaltReason = 0
        self.assertTrue(moe_info.dbgrq())
        self.assertFalse(moe_info.code_breakpoint())
        self.assertFalse(moe_info.data_breakpoint())
        self.assertFalse(moe_info.vector_catch())
        self.assertEqual('JLinkMOEInfo(DBGRQ)', repr(moe_info))
        self.assertEqual('DBGRQ', str(moe_info))

        # Code Breakpoint
        moe_info.HaltReason = 1
        self.assertFalse(moe_info.dbgrq())
        self.assertTrue(moe_info.code_breakpoint())
        self.assertFalse(moe_info.data_breakpoint())
        self.assertFalse(moe_info.vector_catch())
        self.assertEqual('JLinkMOEInfo(Code Breakpoint)', repr(moe_info))
        self.assertEqual('Code Breakpoint', str(moe_info))

        # Data Breakpoint
        moe_info.HaltReason = 2
        self.assertFalse(moe_info.dbgrq())
        self.assertFalse(moe_info.code_breakpoint())
        self.assertTrue(moe_info.data_breakpoint())
        self.assertFalse(moe_info.vector_catch())
        self.assertEqual('JLinkMOEInfo(Data Breakpoint)', repr(moe_info))
        self.assertEqual('Data Breakpoint', str(moe_info))

        # Vector Catch
        moe_info.HaltReason = 3
        self.assertFalse(moe_info.dbgrq())
        self.assertFalse(moe_info.code_breakpoint())
        self.assertFalse(moe_info.data_breakpoint())
        self.assertTrue(moe_info.vector_catch())
        self.assertEqual('JLinkMOEInfo(Vector Catch)', repr(moe_info))
        self.assertEqual('Vector Catch', str(moe_info))

    def test_jlink_breakpoint_info(self):
        """Tests the ``JLinkBreakpointInfo`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns:
          ``None``
        """
        bp = structs.JLinkBreakpointInfo()
        self.assertEqual(ctypes.sizeof(bp), bp.SizeOfStruct)
        self.assertFalse(bp.software_breakpoint())
        self.assertFalse(bp.hardware_breakpoint())
        self.assertFalse(bp.pending())

        rep = 'JLinkBreakpointInfo(Handle 0, Address 0)'
        self.assertEqual(rep, str(bp))
        self.assertEqual(rep, repr(bp))

    def test_jlink_data_event(self):
        """Tests the ``JLinkDataEvent`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns:
          ``None``
        """
        event = structs.JLinkDataEvent()
        self.assertEqual(1 << 0, event.Type)
        self.assertEqual(ctypes.sizeof(event), event.SizeOfStruct)

        rep = 'JLinkDataEvent(Type 1, Address 0)'
        self.assertEqual(rep, repr(event))
        self.assertEqual(rep, str(event))

    def test_jlink_watchpoint_info(self):
        """Tests the ``JLinkWatchpointInfo`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns:
          ``None``
        """
        wp = structs.JLinkWatchpointInfo()
        self.assertEqual(ctypes.sizeof(wp), wp.SizeOfStruct)

        rep = 'JLinkWatchpointInfo(Handle 0, Address 0)'
        self.assertEqual(rep, repr(wp))
        self.assertEqual(rep, str(wp))

    def test_jlink_strace_event_info(self):
        """Tests the ``JLinkStraceEventInfo`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns:
          ``None``
        """
        event_info = structs.JLinkStraceEventInfo()
        self.assertEqual(ctypes.sizeof(event_info), event_info.SizeOfStruct)

        rep = 'JLinkStraceEventInfo(Type=0, Op=0)'
        self.assertEqual(rep, str(event_info))
        self.assertEqual(rep, repr(event_info))

    def test_jlink_trace_data(self):
        """Tests the ``JLinkTraceData`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns:
          ``None``
        """
        data = structs.JLinkTraceData()
        rep = 'JLinkTraceData(0)'
        self.assertEqual(rep, str(data))
        self.assertEqual(rep, repr(data))

        pipe_methods = [
            data.instruction,
            data.data_instruction,
            data.non_instruction,
            data.wait,
            data.branch,
            data.data_branch,
            data.trigger,
            data.trace_disabled
        ]

        for i in range(len(pipe_methods)):
            data.PipeStat = i
            for (j, method) in enumerate(pipe_methods):
                if i == j:
                    self.assertTrue(method())
                else:
                    self.assertFalse(method())

        return None

    def test_jlink_trace_region(self):
        """Tests the ``JLinkTraceRegion`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns:
          ``None``
        """
        region = structs.JLinkTraceRegion()
        self.assertEqual(ctypes.sizeof(region), region.SizeOfStruct)

        rep = 'JLinkTraceRegion(Index=0)'
        self.assertEqual(rep, str(region))
        self.assertEqual(rep, repr(region))

    def test_jlink_rtt_terminal_start(self):
        """Tests the ``JLinkRTTerminalStart`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns:
          ``None``
        """
        start = structs.JLinkRTTerminalStart()
        rep = 'JLinkRTTerminalStart(ConfigAddress=0x0)'
        self.assertEqual(rep, repr(start))

        start.ConfigBlockAddress = 0xDEADBEEF
        rep = 'JLinkRTTerminalStart(ConfigAddress=0xDEADBEEF)'
        self.assertEqual(rep, str(start))

    def test_jlink_rtt_terminal_buf_desc(self):
        """Tests the ``JLinkRTTerminalBufDesc`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns:
          ``None``
        """
        desc = structs.JLinkRTTerminalBufDesc()
        desc.BufferIndex = 7
        desc.SizeOfBuffer = 1337
        desc.Flags = 0
        desc.acName = str.encode('The Winds of Winter')

        desc.Direction = 0
        self.assertTrue(desc.up)
        self.assertFalse(desc.down)

        desc.Direction = 1
        self.assertTrue(desc.down)
        self.assertFalse(desc.up)

        self.assertEqual('The Winds of Winter', desc.name)
        self.assertEqual('JLinkRTTerminalBufDesc(Index=7, Name=The Winds of Winter)', repr(desc))
        self.assertEqual('The Winds of Winter <Index=7, Direction=down, Size=1337>', str(desc))

        desc.Direction = 0
        self.assertEqual('The Winds of Winter <Index=7, Direction=up, Size=1337>', str(desc))

    def test_jlink_rtt_terminal_stat(self):
        """Tests the ``JLinkRTTerminalStatus`` structure.

        Args:
          self (TestStructs): the ``TestStructs`` instance

        Returns:
          ``None``
        """
        stat = structs.JLinkRTTerminalStatus()
        stat.NumUpBuffers = 3
        stat.NumDownBuffers = 3
        stat.IsRunning = 1

        self.assertEqual('JLinkRTTerminalStatus(NumUpBuffers=3, NumDownBuffers=3)', repr(stat))
        self.assertEqual('Status <NumUpBuffers=3, NumDownBuffers=3, Running=1>', str(stat))


if __name__ == '__main__':
    unittest.main()
