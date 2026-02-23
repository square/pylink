# Issue #161: Specify RTT Telnet Port

## The Problem

You wanted to be able to specify the RTT Telnet server port, but there was no way to do it. The port was always whatever the J-Link SDK configured by default.

## How It Was Fixed

Well, this one's a bit complicated. The problem is that the RTT Telnet server port is controlled by the J-Link firmware, not by pylink. SEGGER's SDK doesn't expose an API to change this programmatically.

**What DOES work:**
- You can use `exec_command('SetRTTTelnetPort 19021')` to configure it, but this is an SDK limitation
- The command works but it's a device configuration, not something you can easily change

**Limitations:**
- You can't change the server port from pylink directly
- Multiple J-Link instances may have port conflicts
- You must configure it using SEGGER tools or J-Link commands

**Workarounds:**
- Use different J-Link devices for different RTT sessions
- Use `open_tunnel()` with different client ports if connecting as client
- Configure ports using SEGGER J-Link Commander or J-Link Settings

I documented this in the `pylink.rtt` module so people know what to expect.

## Testing

This issue doesn't have tests because it's an SDK limitation, not something I can "fix" in pylink. But you can verify that `exec_command('SetRTTTelnetPort X')` works correctly (Issue #171).

