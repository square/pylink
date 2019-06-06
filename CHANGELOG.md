# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.2.0]

### Added

- @bojanpotocnik: Implemented context manager to enable automatic debugger
  connection opening when context is entered, and connection closed when
  exited.

### Changed

- @bojanpotocnik: Implemented finalizer method '_finalize()' to tear down
  connection on destructor.

## [0.1.3]

### Changed
- @michalfita: Fixed handling for DLL in 64-bit Python instances: on 64-bit
  Windows platforms running 64-bit Python, the 32-bit DLL was always being
  loaded; now the 64-bit DLL will be loaded instead.

## [0.1.2]

### Changed
- @wallacbe: Removed `sleep` after `connect`; no-op issued to make sure the
  target is ready for debugging.

## [0.1.1]

### Changed
- @ford: `async` decorator renamed to `async_decorator` to support
  new linting rules in Python3.

### Added

- @ford: Added missing `six` requirement to `setup.py` and
  `requirements.txt`.
- @Sauci: Added `open_tunnel()` method to connect to a J-Link over the
  remote server.

## [0.1.0]

### Changed

- @charlesnicholson: flash commands no longer default to powering on the
  target.

## [0.0.10]

### Changed

- @MarekNovakNXP: Fixed casting of `swd_read32` to properly handle reading
  32-bit register when MSB is set.
- @sstallion: Fixed casting of `swd_read8`, and `swd_read16` to properly handle
  reading 32-bit register when MSB is set.

## [0.0.9]

### Changed

- @charlesnicholson: fixed non-deterministic crash on Linux when unloading DLL.

## [0.0.8]

### Changed

- @eldonrivers: added support for 'nxp' name for kinetis/freescale chips

## [0.0.7]

### Added

- @charlesnicholson: Added support for for RTT.
  - `rtt_stop`
  - `rtt_read`
  - `rtt_write`
  - `rtt_get_num_up_buffers`
  - `rtt_get_num_down_buffers`
  - `rtt_control`

## [0.0.6]

### Changed

- Cleaned up documentation.
- Linted code.

## [0.0.5]

### Changed

- Fixed `os.path.isfile` typo.

## [0.0.4]

### Changed

- When loading the SEGGER lib on Linux, `os.walk` is used to descend
  recursively through the directory tree.

## [0.0.3]

### Added

- API Functions
  - `set_trace_source`
  - `set_etb_trace`
  - `set_etm_trace`
- ETM
  - `etm_supported`
  - `etm_register_read`
  - `etm_register_write`
- Simple Trace API
  - `strace_configure`
  - `strace_start`
  - `strace_stop`
  - `strace_read`
  - `strace_code_fetch_event`
  - `strace_data_access_event`
  - `strace_data_load_event`
  - `strace_data_store_event`
  - `strace_clear`
  - `strace_clear_all`
  - `strace_set_buffer_size`
  - Example application for simple trace API under `examples/strace.py`.
- Trace API
  - `trace_start`
  - `trace_stop`
  - `trace_flush`
  - `trace_sample_count`
  - `trace_buffer_size`
  - `trace_set_buffer_size`
  - `trace_min_buffer_size`
  - `trace_max_buffer_size`
  - `trace_set_format`
  - `trace_format`
  - `trace_region_count`
  - `trace_region`
  - `trace_read`

### Changed

- Serial number no longer required command-line argument for command-line tool;
  if not specified, selects the first emulator.
- Fixed bug in Linux library load where 32-bit DLL was loaded on 64-bit
  platform.

## [0.0.2]

### Added

- Support added for writing to flash outside of flashing firmware:
  - `flash_write`
  - `flash_write8`
  - `flash_write16`
  - `flash_write32`
- Added `unlock` method for unlocking a device connected to a J-Link instance.

### Changed

- Fixed logic for determine if J-Link is halted; SDK documentation implies that
  return value for `JLINKARM_IsHalted()` is `<= 1`, but example on Page 144
  suggests otherwise; `.halted()` changed to reflect examples suggestion.
- Fixed logic in `.exec_command()`.  Since the J-Link SDK does not conform to
  the standard of returning zero only in cases of error, `JLINKARM_ExecCommand`
  may succeed, but still return a non-zero value.  Checking the error string is
  the best way to handle this, and the return value should be ignored.
- Fixed logic in handling the return value of `JLINKARM_Connect()`,
  `JLINKARM_Connect()` can return with a positive value which still indicates
  success.

## [0.0.1d]

### Changed

- `open()` with `serial_no=None` and `ip_addr=None` will connect to the first
  USB device. This permits operation without having to define serial numbers for
  workflows using one emulator.


## [0.0.1c]

### Changed

- `reset()` with `halt=False` would previously cause a mass erase of the device
  as it used `JLINKARM_ResetNoHalt()`; now uses `JLINKARM_Reset()` followed by
  a call to `JLINKARM_Go()`, and does not trigger a mass erase if the device is
  secure.


## [0.0.1b]

### Added

- `sync_firmware`

### Changed

- Added a minimum version decorator to wrap functions that require at least
  a certain version of the J-Link software in order to be used.
- Removed 'open_required()' for 'exec_command()', 'disable_dialog_boxes()',
  and 'enable_dialog_boxes()'.
- Added a sample script for automated updates on Windows platforms.


## [0.0.1a]

### Added

- General API Functions (88%):
  - `opened`
  - `connected`
  - `target_connected`
  - `num_connected_emulators`
  - `connected_emulators`
  - `num_supported_devices`
  - `supported_devices`
  - `open`
  - `close`
  - `exec_command`
  - `connect`
  - `error`
  - `clear_error`
  - `compile_date`
  - `version`
  - `hardware_info`
  - `hardware_status`
  - `hardware_version`
  - `firmware_version`
  - `capabilities`
  - `extended_capabilities`
  - `extended_capability`
  - `features`
  - `product_name`
  - `serial_number`
  - `oem`
  - `index`
  - `speed`
  - `set_speed`
  - `set_max_speed`
  - `speed_info`
  - `tif`
  - `supported_tifs`
  - `set_tif`
  - `gpio_properties`
  - `gpio_get`
  - `gpio_set`
  - `comm_supported`
  - `cpu_capability`
  - `power_on`
  - `power_off`
  - `set_reset_strategy`
  - `set_reset_pin_high`
  - `set_reset_pin_low`
  - `set_tck_pin_high`
  - `set_tck_pin_low`
  - `set_tdi_pin_high`
  - `set_tdi_pin_low`
  - `set_tms_pin_high`
  - `set_tms_pin_low`
  - `set_trst_pin_high`
  - `set_trst_pin_low`
  - `erase`
  - `flash`
  - `flash_file`
  - `reset`
  - `reset_tap`
  - `restart`
  - `halt`
  - `halted`
  - `core_id`
  - `core_cpu`
  - `core_name`
  - `ir_len`
  - `scan_len`
  - `scan_chain_len`
  - `device_family`
  - `cpu_speed`
  - `cpu_halt_reasons`
  - `enable_reset_pulls_reset`
  - `disable_reset_pulls_reset`
  - `enable_reset_pulls_trst`
  - `disable_reset_pulls_trst`
  - `enable_reset_inits_registers`
  - `disable_reset_inits_registers`
  - `set_little_endian`
  - `set_big_endian`
  - `set_vector_catch`
  - `step`
  - `enable_soft_breakpoints`
  - `disable_soft_breakpoints`
  - `num_active_breakpoints`
  - `num_available_breakpoints`
  - `breakpoint_info`
  - `breakpoint_find`
  - `breakpoint_set`
  - `software_breakpoint_set`
  - `hardware_breakpoint_set`
  - `breakpoint_clear`
  - `breakpoint_clear_all`
  - `num_active_watchpoints`
  - `num_available_watchpoints`
  - `watchpoint_info`
  - `watchpoint_set`
  - `watchpoint_clear`
  - `watchpoint_clear_all`
- Automation Utilities:
  - `enable_dialog_boxes`
  - `disable_dialog_boxes`
- JTAG API Functions:
  - `jtag_configure`
  - `jtag_create_clock`
  - `jtag_flush`
  - `jtag_send`
- License API:
  - `licenses`
  - `custom_license`
  - `add_license`
  - `erase_licenses`
- Firmware API:
  - `invalidate_firmware`
  - `update_firmware`
  - `firmware_newer`
  - `firmware_outdated`
- Logging Handlers:
  - `log_handler`
  - `detailed_log_handler`
  - `error_handler`
  - `warning_handler`
- Coresight API:
  - `coresight_configure`
  - `coresight_read`
  - `coresight_write`
- SWD API:
  - `swd_read8`
  - `swd_read16`
  - `swd_read32`
  - `swd_write`
  - `swd_write8`
  - `swd_write16`
  - `swd_write32`
  - `swd_sync`
- SWO API:
  - `swo_start`
  - `swo_stop`
  - `swo_enabled`
  - `swo_enable`
  - `swo_disable`
  - `swo_flush`
  - `swo_speed_info`
  - `swo_num_bytes`
  - `swo_set_host_buffer_size`
  - `swo_set_emu_buffer_size`
  - `swo_supported_speeds`
  - `swo_read`
  - `swo_read_stimulus`
- Memory API Functions:
  - `memory_read`
  - `memory_write`
  - `memory_read8`
  - `memory_write8`
  - `memory_read16`
  - `memory_write16`
  - `memory_read32`
  - `memory_write32`
  - `memory_read64`
  - `memory_write64`
  - `num_memory_zones`
  - `memory_zones`
  - `code_memory_read`
- Register API Functions:
  - `register_read`
  - `register_write`
  - `register_read_multiple`
  - `register_write_multiple`
  - `register_list`
  - `register_name`
- ICE Register API Functions:
  - `ice_register_read`
  - `ice_register_write`
- Added PyLink command-line tool:
  - Flash command added.
  - Unlock command added.
  - License command added.
  - Erase command added.
- Added support for accessing the multiple J-Links from the same process.
- Added device lockfiles to prevent multiple accesses to the same J-Link when a
  thread is already accessing that J-Link.
- Example ["Serial Wire Viewer (SWV)"](examples/swv.py) added.
- Example ["Core Information Query (CIQ)"](examples/core.py) added.
- Example ["Target Endianness (TE)"](examples/endian.py) added.
