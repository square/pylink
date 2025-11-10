# Test Scripts Directory

This directory contains test scripts for pylink functionality that are not tied to specific GitHub issues. These scripts are used for general testing, debugging, and verification of pylink features.

## Contents

### RTT Testing Scripts

- **[test_rtt_connection.py](test_rtt_connection.py)**: Comprehensive RTT connection test script with debug mode. Connects to nRF54L15 via J-Link and displays RTT logs in real-time. Includes graceful shutdown handling and detailed connection status reporting.

- **[test_rtt_diagnostic.py](test_rtt_diagnostic.py)**: Diagnostic script for troubleshooting RTT connection issues. Provides detailed information about RTT buffer detection, search ranges, and connection state.

- **[test_rtt_simple.py](test_rtt_simple.py)**: Simple RTT test for quick verification. Minimal script that tests basic RTT functionality (connect, start RTT, read buffers).

- **[test_rtt_specific_addr.py](test_rtt_specific_addr.py)**: Test script for RTT connection using a specific control block address. Useful for testing when auto-detection fails or when verifying a known RTT address.

## Usage

All test scripts are executable Python scripts. Run them from the `sandbox/pylink` directory:

```bash
cd sandbox/pylink
python3 issues/tests/test_rtt_connection.py
python3 issues/tests/test_rtt_simple.py
python3 issues/tests/test_rtt_diagnostic.py
python3 issues/tests/test_rtt_specific_addr.py
```

Or make them executable and run directly:

```bash
chmod +x issues/tests/test_*.py
./issues/tests/test_rtt_connection.py
```

## Requirements

- pylink-square installed (editable install recommended)
- J-Link probe connected
- Target device (e.g., nRF54L15) connected and powered
- Firmware with RTT enabled flashed to device

## Notes

- These tests are for general RTT functionality verification
- Issue-specific tests are located in their respective issue directories (e.g., `issues/151/test_issue_151.py`)
- Unit tests are located in the `tests/` directory at the project root

