# Tools Directory

This directory contains utility scripts and tools for pylink development, testing, and verification that are not tied to specific GitHub issues.

## Contents

### Installation Verification

- **[verify_installation.py](verify_installation.py)**: Script to verify pylink installation and check if the modified version from the sandbox is being used. Verifies that custom modifications (such as improved `rtt_start()` method) are present in the installed version.

## Usage

Run utility scripts from the `sandbox/pylink` directory:

```bash
cd sandbox/pylink
python3 issues/tools/verify_installation.py
```

Or make them executable and run directly:

```bash
chmod +x issues/tools/verify_installation.py
./issues/tools/verify_installation.py
```

## Requirements

- pylink-square installed (editable install recommended for development)
- Python 3.x

## Notes

- These tools are for general development and verification purposes
- Issue-specific tools are located in their respective issue directories
- Test scripts are located in `issues/tests/`

